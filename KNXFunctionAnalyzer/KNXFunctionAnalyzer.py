import logging

from KNXFunctionAnalyzer.KNXSpacesRepository import KNXSpacesRepository
from KNXProjectManagement.KNXProjectManager import KNXProjectManager
from KNXProjectManagement.KNXSpace import KNXSpace

separator: str ="_"

class KNXFunctionAnalyzer:

    # for information, instance attributes
    # _knx_project: KNXProjectManager
    # _spaces_repository: KNXSpacesRepository

    def __init__(self, knx_project: KNXProjectManager):
        self._knx_project = knx_project
        self._spaces_repository = KNXSpacesRepository()

    def star_analysis(self):
        self.__recursive_function_searcher(1, self._knx_project.info.name, self._knx_project.locations)

    def __recursive_function_searcher(self, level : int, name: str, spaces: dict[str, KNXSpace]):
        nb_elem = len(spaces)
        logging.info(f"{nb_elem} level location has been found at level {level} in {name}")
        space: KNXSpace
        for space in spaces.values():
            new_name = name + separator + space.name
            new_level=level+1
            logging.info(f"Starting analysis at level {new_level} of {new_name}")
            self._spaces_repository.add_space(new_name,space)
            self.__recursive_function_searcher(new_level, new_name, space.spaces)

    @property
    def locations(self):
        return self._spaces_repository

    def __iter__(self):
        return self._spaces_repository.__iter__()

    def __next__(self):
        return self._spaces_repository.__next__()
