import logging

import yaml

from HAKNXObjectCreator.HAKNXFactory import HAKNXFactory
from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice
from KNXProjectManagement.KNXFunction import KNXFunction
from KNXProjectManagement.KNXProjectManager import KNXProjectManager
from KNXProjectManagement.KNXSpace import KNXSpace
from Utils.Serializable import Serializable


class HAKNXLocation(Serializable):

    _name: str # private attribute not to be serialized
    _objects: dict[str, list[HAKNXDevice]]

    def __init__(self):
        self._name = ""
        self._objects = {}

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
                    ha_knx_object.set_from_function(function, knx_project_manager)
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
        with open(file, 'r') as yaml_file:
            logging.info(f"Read file {file}")
            imported_dict: dict = yaml.safe_load(yaml_file)
            for key in imported_dict.keys():
                objects_to_import = imported_dict[key]
                list_of_objects = []
                for element in objects_to_import:
                    ha_knx_object_type = HAKNXFactory.search_associated_class_from_key_name(key)
                    ha_knx_object = ha_knx_object_type()
                    if ha_knx_object is None:
                        logging.warning(f"No class found for key {key}")
                    else:
                        ha_knx_object.set_from_dict(element)
                        list_of_objects.append(ha_knx_object)
                self._objects[key] = list_of_objects

    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

    def is_empty(self):
        return len(self._objects) == 0

    def to_dict(self):
        return Serializable.convert_to_dict(self._objects)

    def dump(self):
        dico = self.to_dict()
        return yaml.dump(dico, sort_keys=False, default_style=None)