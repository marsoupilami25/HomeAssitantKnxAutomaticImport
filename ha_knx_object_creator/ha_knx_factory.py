from ruamel.yaml import YAML

from ha_knx_object_creator.ha_knx_cover import HAKNXCover
from ha_knx_object_creator.ha_knx_date import HAKNXDate
from ha_knx_object_creator.ha_knx_date_time import HAKNXDateTime
from ha_knx_object_creator.ha_knx_expose import HAKNXExpose
from ha_knx_object_creator.ha_knx_light import HAKNXLight
from ha_knx_object_creator.ha_knx_sensor import HAKNXSensor
from ha_knx_object_creator.ha_knx_switch import HAKNXSwitch
from ha_knx_object_creator.ha_knx_time import HAKNXTime
from knx_project_management.knx_function import KNXFunction
from utils.serializable import serializable_to_yaml


class HAKNXFactory:

    ha_knx_objects_list = [HAKNXLight,
                           HAKNXSwitch,
                           HAKNXSensor,
                           HAKNXDateTime,
                           HAKNXDate,
                           HAKNXTime,
                           HAKNXCover,
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
        return None

yaml=YAML()
for loc_cls in HAKNXFactory.ha_knx_objects_list:
    yaml.register_class(loc_cls)
    yaml.representer.add_representer(loc_cls, serializable_to_yaml)
