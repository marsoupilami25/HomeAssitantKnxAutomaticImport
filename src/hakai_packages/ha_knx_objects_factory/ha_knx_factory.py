from ruamel.yaml import YAML

from hakai_packages.ha_knx_objects import HAKNXCover
from hakai_packages.ha_knx_objects import HAKNXDate
from hakai_packages.ha_knx_objects import HAKNXDateTime
from hakai_packages.ha_knx_objects import HAKNXExpose
from hakai_packages.ha_knx_objects import HAKNXLight
from hakai_packages.ha_knx_objects import HAKNXSensor
from hakai_packages.ha_knx_objects import HAKNXSwitch
from hakai_packages.ha_knx_objects import HAKNXTime
from hakai_packages.knx_project_objects import KNXFunction
from hakai_packages.knx_utils import serializable_to_yaml


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
