import logging
import os
import sys

from classfromtypeddict import ClassFromTypedDict

from xknxproject import XKNXProj
from xknxproject.models import KNXProject

from knx_project_management.knx_com_object import KNXComObject
from knx_project_management.knx_function import KNXFunction
from knx_project_management.knx_group_address import KNXGroupAddress
from knx_project_management.knx_project_info import KNXProjectInfo
from knx_project_management.knx_space import KNXSpace

class KNXProjectManager(ClassFromTypedDict):
    _class_ref = KNXProject

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs
    #   to be import otherwise the conversion does not work
    # info: KNXProjectInfo
    # functions: dict[str, KNXFunction]
    # group_addresses: dict[str, KNXGroupAddress]
    # locations: dict[str, KNXSpace]
    # communication_objects: dict[str, KNXComObject]

    def __init__(self, data: dict):
        self.info: KNXProjectInfo | None = None #None only for init
        self.functions : dict[str, KNXFunction] = {}
        self.group_addresses : dict[str, KNXGroupAddress] = {}
        self.locations: dict[str, KNXSpace] = {}
        self.communication_objects: dict[str, KNXComObject] = {}
        super().__init__(data)

    @classmethod
    def init(cls, file: str):
        if os.path.exists(file) and os.path.isfile(file):
            knx_project: XKNXProj
            try:
                knx_project = XKNXProj(
                    path=file,
                )
            except Exception as e: # pylint: disable=broad-except
                logging.critical("Exception during file opening: %s", e)
                sys.exit(1)
            try:
                xknx_project = knx_project.parse()
            except Exception as e: # pylint: disable=broad-except
                logging.critical("Exception during file opening: %s", e)
                sys.exit(1)
        else:
            logging.critical("%s does not exist", file)
            sys.exit(1)
        return cls(dict(xknx_project))

    def print_knx_project_properties(self):
        name = self.info.name
        logging.info("Project %s opened", name)
        for attr, value in self.info.__dict__.items():
            if not attr.startswith('_'):  # Exclude special methods
                logging.info("%s = %s", attr, value)

    def get_knx_function(self, name: str) -> KNXFunction | None:
        if name in self.functions:
            function = self.functions.get(name)
            logging.info("Function '%s' found", function.name)
            return function
        logging.warning("Function %s not found", name)
        return None

    def get_knx_group_address(self, ref: str) -> KNXGroupAddress | None:
        if ref in self.group_addresses:
            ga = self.group_addresses[ref]
            return ga
        logging.error("Group Address ref %s not found", ref)
        return None

    def get_com_object(self, ref: str) -> KNXComObject | None:
        if ref in self.communication_objects:
            co = self.communication_objects[ref]
            return co
        logging.error("Communication Object ref %s not found", ref)
        return None
