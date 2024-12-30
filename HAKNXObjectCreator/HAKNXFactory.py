from HAKNXObjectCreator.HAKNXLight import HAKNXLight
from KNXProjectManagement.KNXFunction import KNXFunction
from KNXProjectManagement.KNXProjectManager import KNXProjectManager


class HAKNXFactory:

    _ha_knx_objects_list = [HAKNXLight]

    @classmethod
    def search_associated_class_from_function(cls, function: KNXFunction, knx_project_manager: KNXProjectManager):
        for cl in cls._ha_knx_objects_list:
            if cl.is_this_type_from_function(function):
                return cl.constructor_with_function(function, knx_project_manager)
        return None

    @classmethod
    def search_associated_class_from_key_name(cls, key_name: str, params: dict):
        for cl in cls._ha_knx_objects_list:
            if cl.is_this_type_from_key_name(key_name):
                return cl.constructor_with_dict(params)
