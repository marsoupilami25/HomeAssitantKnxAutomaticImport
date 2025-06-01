import logging
import os
import sys

from xknxproject import XKNXProj
from xknxproject.models import KNXProject

from KNXProjectManagement.KNXComObject import KNXComObject
from KNXProjectManagement.KNXFunction import KNXFunction
from KNXProjectManagement.KNXGroupAddress import KNXGroupAddress
from KNXProjectManagement.KNXProjectInfo import KNXProjectInfo
from KNXProjectManagement.KNXSpace import KNXSpace
from ClassFromTypedDict import ClassFromTypedDict

class KNXProjectManager(ClassFromTypedDict):
    _class_ref = KNXProject

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs to be import otherwise the conversion does not work
    # info: KNXProjectInfo
    # functions: dict[str, KNXFunction]
    # group_addresses: dict[str, KNXGroupAddress]
    # locations: dict[str, KNXSpace]
    # communication_objects: dict[str, KNXComObject]

    @classmethod
    def init(cls, file: str):
        if os.path.exists(file) and os.path.isfile(file):
            knx_project: XKNXProj
            try:
                knx_project = XKNXProj(
                    path=file,
                )
            except Exception as e:
                logging.critical(f"Exception during file opening: {e}")
                sys.exit(1)
            try:
                xknx_project = knx_project.parse()
            except Exception as e:
                logging.critical(f"Exception parsing the file: {e}")
                sys.exit(1)
        else:
            logging.critical(f"{file} does not exist")
            sys.exit(1)
        return cls(xknx_project)

    def print_knx_project_properties(self):
        name = self.info.name
        logging.info(f"Project {name} opened")
        for attr, value in self.info.__dict__.items():
            if not attr.startswith('_'):  # Exclude special methods
                logging.info(f"{attr} = {value}")

    def get_knx_function(self, name: str) -> KNXFunction | None:
        if name in self.functions:
            function = self.functions.get(name)
            logging.info(f"Function '{function.name}' found")
            return function
        else:
            logging.warning(f"Function {name} not found")
            return None

    def get_knx_group_address(self, ref: str) -> KNXGroupAddress | None:
        if ref in self.group_addresses.keys():
            ga = self.group_addresses[ref]
            return ga
        else:
            logging.error(f"Group Address ref {ref} not found")
            return None

    def get_com_object(self, ref: str) -> KNXComObject | None:
        if ref in self.communication_objects.keys():
            co = self.communication_objects[ref]
            return co
        else:
            logging.error(f"Communication Object ref {ref} not found")
            return None

