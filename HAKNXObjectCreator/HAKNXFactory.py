from ruamel.yaml import YAML

from HAKNXObjectCreator.HAKNXDate import HAKNXDate
from HAKNXObjectCreator.HAKNXDateTime import HAKNXDateTime
from HAKNXObjectCreator.HAKNXExpose import HAKNXExpose
from HAKNXObjectCreator.HAKNXLight import HAKNXLight
from HAKNXObjectCreator.HAKNXSensor import HAKNXSensor
from HAKNXObjectCreator.HAKNXSwitch import HAKNXSwitch
from HAKNXObjectCreator.HAKNXTime import HAKNXTime
from KNXProjectManagement.KNXFunction import KNXFunction

class HAKNXFactory:

    ha_knx_objects_list = [HAKNXLight,
                           HAKNXSwitch,
                           HAKNXSensor,
                           HAKNXDateTime,
                           HAKNXDate,
                           HAKNXTime,
                           HAKNXExpose
                           ]

    @classmethod
    def search_associated_class_from_function(cls, function: KNXFunction) -> type | None :
        for cl in cls.ha_knx_objects_list:
            if cl.is_this_type_from_function(function):
                return cl
        return None

    @classmethod
    def search_associated_class_from_key_name(cls, key_name: str) -> type | None :
        for cl in cls.ha_knx_objects_list:
            if cl.is_this_type_from_key_name(key_name):
                return cl

yaml=YAML()
for cls in HAKNXFactory.ha_knx_objects_list:
    yaml.register_class(cls)