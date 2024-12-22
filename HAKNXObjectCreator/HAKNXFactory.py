from HAKNXObjectCreator.light import light
from KNXProjectManagement.KNXFunction import KNXFunction
from KNXProjectManagement.KNXProjectManager import KNXProjectManager


class HAKNXFactory:

    _ha_knx_objects_list = [light]

    @classmethod
    def search_associated_class(cls, function: KNXFunction, knx_project_manager: KNXProjectManager):
        for cl in cls._ha_knx_objects_list:
            if cl.is_this_type(function):
                return cl.constructor_with_function(function, knx_project_manager)
        return None