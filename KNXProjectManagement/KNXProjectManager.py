import logging
import os
import sys
from xknxproject import XKNXProj
from xknxproject.models import KNXProject

from KNXProjectManagement.KNXFunctionsList import KNXFunctionsList
from KNXProjectManagement.KNXGroupAddressList import KNXGroupAddressList
from KNXProjectManagement.KNXSpacesList import KNXSpacesList

class KNXProjectManager:
    _project: KNXProject
    _functions_list: KNXFunctionsList
    _spaces_list: KNXSpacesList
    _ga_list: KNXGroupAddressList

    def init(self, file: str):
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
                self._project = knx_project.parse()
            except Exception as e:
                logging.critical(f"Exception parsing the file: {e}")
                sys.exit(1)
        else:
            logging.critical(f"{file} does not exist")
            sys.exit(1)
        self._functions_list = KNXFunctionsList(self._project["functions"])
        self._spaces_list = KNXSpacesList.constructor(self._project["locations"])
        self._ga_list = KNXGroupAddressList(self._project["group_addresses"])

    @property
    def project(self) -> KNXProject:
        return self._project

    def print_knx_project_properties(self):
        name = self._project["info"]["name"]
        logging.info(f"Project {name} opened")
        for key, value in self._project["info"].items():
            print(f"{key}: {value}")
        return

    @property
    def name(self) -> str:
        return self._project["info"]["name"]

    @property
    def functions(self) -> KNXFunctionsList:
        return self._functions_list

    @property
    def spaces(self) -> KNXSpacesList:
        return self._spaces_list

    @property
    def group_addresses(self) -> KNXGroupAddressList:
        return self._ga_list

knx_project_manager = KNXProjectManager()