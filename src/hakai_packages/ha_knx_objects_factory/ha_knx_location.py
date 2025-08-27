import logging
from io import StringIO

from ruamel.yaml import YAML, CommentedMap

from hakai_packages.ha_knx_objects_common import HAKNXDevice
from hakai_packages.knx_project_objects import KNXFunction
from hakai_packages.knx_project_objects import KNXSpace
from hakai_packages.knx_utils import (Serializable, serializable_to_yaml,
                                      knx_transformed_string, knx_flat_string)
from hakai_packages.hakai_conf import HAKAIConfiguration
from .ha_knx_factory import HAKNXFactory

yaml = YAML()
yaml.default_style = None  # no quotes for scalar
yaml.default_flow_style = False  # no JSON format for collections (lists, dictionaries)
yaml.default_tag = None


class HAKNXLocation(Serializable):

    def __init__(self):
        super().__init__()
        self._name = ""
        self._objects = {}
        self._ha_mode = False
        self._touched = False

    @classmethod
    def constructor_from_knx_space(cls, location: KNXSpace):
        instance = cls()
        instance.import_knx_space(location)
        return instance

    @classmethod
    def constructor_from_file(cls, file: str, name: str):
        instance = cls()
        instance.name = name
        instance.import_from_file(file)
        return instance

    def is_touched(self) -> bool:
        return self._touched

    def touched(self):
        self._touched = True

    def import_knx_space(self, location: KNXSpace):
        knx_project_manager = HAKAIConfiguration.get_instance().project
        self._name = location.name
        logging.info("Update location %s", self._name)
        for element in location.functions:
            function: KNXFunction = knx_project_manager.get_knx_function(element)
            #search if function already converted in device in _objects
            flat_list = [item for sublist in self._objects.values() for item in sublist]
            existing_devices: list[HAKNXDevice] = list(
                filter(lambda obj,
                       f = function: obj.get_converted_name(f.transformed_name) == obj.name,
                       flat_list))
            if len(existing_devices) == 0:
                ha_knx_object_type = HAKNXFactory.search_associated_class_from_function(function)
                if ha_knx_object_type is None:
                    logging.warning("No class found for function %s",
                                    function.name)
                else:
                    logging.info("New object of type %s", ha_knx_object_type.__name__)
                    ha_knx_object: HAKNXDevice = ha_knx_object_type()
                    ha_knx_object.parent = self.transformed_name
                    if ha_knx_object.set_from_function(function):
                        ha_knx_object.touched()
                        class_type = ha_knx_object.get_device_type_name()
                        if class_type in self._objects:
                            self._objects[class_type].append(ha_knx_object)
                        else:
                            self._objects[class_type] = [ha_knx_object]
            elif len(existing_devices) == 1:
                logging.info("Existing object of type %s",
                             existing_devices[0].__class__.__name__)
                existing_devices[0].parent = self.transformed_name
                existing_devices[0].set_from_function(function)
                existing_devices[0].touched()
            else:
                raise ValueError(f"Several existing functions with name {function.name} "
                                 f"in location {self._name}")

    def import_from_file(self, file: str):
        with open(file, 'r', encoding="utf-8") as yaml_file:
            logging.info("Read file %s", file)
            imported_dict = yaml.load(yaml_file)
            if not imported_dict:
                logging.info("No data found in file %s", yaml_file)
                return
            self.from_dict(imported_dict)
            for device_list in self._objects.values():
                for element in device_list:
                    element.parent = self.transformed_name

    def check(self):
        if HAKAIConfiguration.get_instance().not_remove_device:
            return
        for device_list in self._objects.values():
            list_to_remove: list[HAKNXDevice] = []
            for element in device_list:
                if not element.is_touched():
                    list_to_remove.append(element)
            for element in list_to_remove:
                logging.info("Device %s does not exist anymore in the location %s."
                             " Device is removed.", element.name, self.transformed_name)
                device_list.remove(element)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def flat_name(self):
        return knx_flat_string(self.name)

    @property
    def transformed_name(self):
        return knx_transformed_string(self.name)

    def is_empty(self):
        return len(self._objects) == 0

    def from_dict(self, dict_obj: CommentedMap):
        # detect if it is a ha yaml file and remove useless values
        comment_pre = dict_obj.ca.comment
        if comment_pre:
            self._comments['HAKNXLocation'] = comment_pre
        key_list = list(dict_obj.keys())
        key='knx'
        if (len(key_list) == 1) and (key_list[0] == key):
            self._ha_mode=True
            final_dict = dict_obj[key]
            comment_pre = dict_obj.ca.items.get(key)
            if comment_pre:
                self._comments[key] = comment_pre
        else:
            self._ha_mode=False
            final_dict = dict_obj
        for key in final_dict.keys():
            comment_pre = final_dict.ca.items.get(key)
            if comment_pre:
                self._comments[key] = comment_pre
            ha_knx_object_type = HAKNXFactory.search_associated_class_from_key_name(key)
            objects_to_import = final_dict[key]
            list_of_objects = []
            for element in objects_to_import:
                ha_knx_object = ha_knx_object_type()
                if ha_knx_object is None:
                    logging.warning("No class found for key %s", key)
                else:
                    ha_knx_object.from_dict(element)
                    list_of_objects.append(ha_knx_object)
            self._objects[key] = list_of_objects

    def dump(self):
        ha_mode = HAKAIConfiguration.get_instance().hamode
        if not ha_mode is None:
            self._ha_mode = ha_mode
        stream = StringIO()
        yaml.dump(self, stream)
        return stream.getvalue()

    def to_yaml(self, representer):
        commented_map = CommentedMap(self._objects)
        for obj in self._objects:
            if obj in self._comments:
                commented_map.ca.items[obj] = self._comments[obj]
        if self._ha_mode:
            commented_map = CommentedMap( { 'knx' : commented_map} )
            knx_key = 'knx'
            if knx_key in self._comments:
                commented_map.ca.items[knx_key] = self._comments[knx_key]
        key='HAKNXLocation'
        if key in self._comments:
            commented_map.ca.comment = self._comments[key]
        output_node = representer.represent_mapping('tag:yaml.org,2002:map', commented_map)
        return output_node

yaml=YAML()
yaml.register_class(HAKNXLocation)
yaml.representer.add_representer(HAKNXLocation, serializable_to_yaml)
