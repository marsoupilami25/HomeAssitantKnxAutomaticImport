from HAKNXObjectCreator.HAKNXLight import HAKNXLight
from HAKNXObjectCreator.HAKNXSensor import HAKNXSensor
from HAKNXObjectCreator.HAKNXSwitch import HAKNXSwitch
from KNXProjectManagement.KNXFunction import KNXFunction


class HAKNXFactory:

    _ha_knx_objects_list = [HAKNXLight, HAKNXSwitch, HAKNXSensor]

    @classmethod
    def search_associated_class_from_function(cls, function: KNXFunction) -> type | None :
        for cl in cls._ha_knx_objects_list:
            if cl.is_this_type_from_function(function):
                return cl
        return None

    @classmethod
    def search_associated_class_from_key_name(cls, key_name: str) -> type | None :
        for cl in cls._ha_knx_objects_list:
            if cl.is_this_type_from_key_name(key_name):
                return cl
