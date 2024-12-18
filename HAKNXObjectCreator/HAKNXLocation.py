import logging

import yaml

from HAKNXObjectCreator.HAKNXObject import HAKNXObject
from KNXProjectManagement.KNXSpace import KNXSpace
from Utils.Serializable import Serializable


class HAKNXLocation(Serializable):

    _name: str
    _objects: dict[str, list[HAKNXObject]]

    def __init__(self, location: KNXSpace):
        self._name = location.name
        self._objects = {}
        logging.info(f"Create location {self._name}")
        for element in location.functions:
            # function: KNXFunction = knx_project_manager.functions.get_knx_function(element)
            # knx_object = HAKNXFactory.search_associated_class(function)
            knx_object = None
            if knx_object is None:
                logging.warning(f"No class found for function {function.name}")
            else:
                class_type = knx_object.__class__.__name__
                if class_type in self._objects:
                    self._objects[class_type].append(knx_object)
                else:
                    self._objects[class_type] = [knx_object]

    def is_empty(self):
        return len(self._objects) == 0

    def to_dict(self):
        return Serializable.convert_to_dict(self._objects)

    def dump(self):
        dico = self.to_dict()
        return yaml.dump(dico, sort_keys=False, default_style=None)