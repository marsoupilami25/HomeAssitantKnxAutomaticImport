import logging
import os
import sys
from xknxproject import XKNXProj
from xknxproject.models import KNXProject

from KNXProjectManagement.KNXFunctionsList import KNXFunctionsList
from KNXProjectManagement.KNXGroupAddressList import KNXGroupAddressList
from KNXProjectManagement.KNXProjectInfo import KNXProjectInfo
from KNXProjectManagement.KNXSpacesList import KNXSpacesList
from Utils.ClassFromTypedDict import ClassFromTypedDict


class KNXProjectManager(ClassFromTypedDict):
    _class_ref = KNXProject

    info: KNXProjectInfo
    _functions_list: KNXFunctionsList
    _ga_list: KNXGroupAddressList

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
