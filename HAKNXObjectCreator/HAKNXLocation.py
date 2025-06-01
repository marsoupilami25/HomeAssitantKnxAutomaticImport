import logging
from io import StringIO
from typing import cast

# import yaml

from ruamel.yaml import YAML, yaml_object, CommentedMap, CommentedSeq

from HAKNXObjectCreator.HAKNXFactory import HAKNXFactory
from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice
from KNXProjectManagement.KNXFunction import KNXFunction
from KNXProjectManagement.KNXProjectManager import KNXProjectManager
from KNXProjectManagement.KNXSpace import KNXSpace
from Utils.Serializable import Serializable, serializable_to_yaml

yaml = YAML()
yaml.default_style = None  # Pas de guillemets autour des scalaires
yaml.default_flow_style = False  # Pas de format JSON pour les collections (listes, dictionnaires)
yaml.default_tag = None


class HAKNXLocation(Serializable):

    _name: str # private attribute not to be serialized
    _objects: dict[str, list[HAKNXDevice]]

    def __init__(self):
        super().__init__()
        self._name = ""
        self._objects = {}
        self._ha_mode = False

    @classmethod
    def constructor_from_knx_space(cls, location: KNXSpace, knx_project_manager: KNXProjectManager):
        instance = cls()
        instance.import_knx_space(location, knx_project_manager)
        return instance

    @classmethod
    def constructor_from_file(cls, file: str):
        instance = cls()
        instance.import_from_file(file)
        return instance

    def import_knx_space(self, location: KNXSpace, knx_project_manager: KNXProjectManager):
        self._name = location.name
        logging.info(f"Update location {self._name}")
        for element in location.functions:
            function: KNXFunction = knx_project_manager.get_knx_function(element)
            #search if function already converted in device in _objects
            flat_list = [item for sublist in self._objects.values() for item in sublist]
            existing_devices: list[HAKNXDevice] = list(filter(lambda obj: function.name == obj.name, flat_list))
            if len(existing_devices) == 0:
                ha_knx_object_type = HAKNXFactory.search_associated_class_from_function(function)
                if ha_knx_object_type is None:
                    logging.warning(f"No class found for function {function.name}")
                else:
                    ha_knx_object: HAKNXDevice = ha_knx_object_type()
                    if ha_knx_object.set_from_function(function, knx_project_manager):
                        class_type = ha_knx_object.get_device_type_name()
                        if class_type in self._objects:
                            self._objects[class_type].append(ha_knx_object)
                        else:
                            self._objects[class_type] = [ha_knx_object]
            elif len(existing_devices) == 1:
                existing_devices[0].set_from_function(function, knx_project_manager)
            else:
                raise ValueError(f"Several existing functions with name {function.name} in location {self._name}")

    def import_from_file(self, file: str):
        with (open(file, 'r') as yaml_file):
            logging.info(f"Read file {file}")
            imported_dict = yaml.load(yaml_file)
            if not imported_dict:
                logging.info(f"No data found in file {yaml_file}")
                return
            self.from_dict(imported_dict)

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

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
                    logging.warning(f"No class found for key {key}")
                else:
                    ha_knx_object.from_dict(element)
                    list_of_objects.append(ha_knx_object)
            self._objects[key] = list_of_objects

    def dump(self, ha_mode : bool | None = None):
        if not ha_mode is None:
            self._ha_mode = ha_mode
        stream = StringIO()
        yaml.dump(self, stream)
        return stream.getvalue()

    def to_yaml(self, representer):
        commented_map = CommentedMap(self._objects)
        for key in self._objects.keys():
            if key in self._comments.keys():
                commented_map.ca.items[key] = self._comments[key]
        if self._ha_mode:
            commented_map = CommentedMap( { 'knx' : commented_map} )
            knx_key = 'knx'
            if knx_key in self._comments.keys():
                commented_map.ca.items[knx_key] = self._comments[knx_key]
        key='HAKNXLocation'
        if key in self._comments.keys():
            commented_map.ca.comment = self._comments[key]
        output_node = representer.represent_mapping('tag:yaml.org,2002:map', commented_map)
        return output_node

yaml=YAML()
yaml.register_class(HAKNXLocation)
yaml.representer.add_representer(HAKNXLocation, serializable_to_yaml)