import logging

from KNXFunctionAnalyzer.KNXSpacesRepository import KNXSpacesRepository, knx_spaces_repository
from KNXProjectManagement.KNXSpacesList import KNXSpacesList
from KNXProjectManagement.KNXProjectManager import KNXProjectManager, knx_project_manager


class KNXFunctionAnalyzer:
    _knx_project: KNXProjectManager
    _spaces_repository: KNXSpacesRepository

    def __init__(self, knx_project: KNXProjectManager):
        self._knx_project = knx_project
        self._spaces_repository = knx_spaces_repository

    def star_analysis(self):
        self.__recursive_function_searcher(1, self._knx_project.name, self._knx_project.spaces)

    def __recursive_function_searcher(self, level : int, name: str, spaces: KNXSpacesList):
        nb_elem = len(spaces.spaces)
        logging.info(f"{nb_elem} level location has been found at level {level} in {name}")
        for space in spaces.spaces:
            newname = name + '.' + space.name
            newlevel=level+1
            logging.info(f"\nStarting analysis at level {newlevel} of {newname}")
            if newname != 0:
                self._spaces_repository.add_space(space)
            self.__recursive_function_searcher(newlevel, newname, KNXSpacesList(space.spaces))

    @property
    def locations(self):
        return self._spaces_repository

    def __iter__(self):
        return self._spaces_repository.__iter__()

    def __next__(self):
        return self._spaces_repository.__next__()

knx_function_analyzer = KNXFunctionAnalyzer(knx_project_manager)