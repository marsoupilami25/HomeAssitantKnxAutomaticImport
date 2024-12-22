import logging
import os
import sys
from typing import NewType

from xknxproject import XKNXProj
from xknxproject.models import KNXProject

from KNXProjectManagement.KNXFunction import KNXFunction
from KNXProjectManagement.KNXGroupAddress import KNXGroupAddress
from KNXProjectManagement.KNXProjectInfo import KNXProjectInfo
from KNXProjectManagement.KNXSpace import KNXSpace
from Utils.ClassFromTypedDict import ClassFromTypedDict

class KNXProjectManager(ClassFromTypedDict):
    _class_ref = KNXProject
    info: KNXProjectInfo
    functions: dict[str, KNXFunction]
    group_addresses: dict[str, KNXGroupAddress]
    locations: dict[str, KNXSpace]

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
                print(f"{attr} = {value}")

    def get_knx_function(self, name: str) -> KNXFunction:
        if name in self.functions:
            function = self.functions.get(name)
            logging.info(f"Function '{function.name}' found")
            return function
        else:
            logging.warning(f"Function {name} not found")
            return None

    def get_knx_group_address(self, ref: str) -> KNXGroupAddress:
        if ref in self.group_addresses.keys():
            ga = self.group_addresses[ref]
            return ga
        else:
            logging.error(f"Group Address ref {ref} not found")
            return None