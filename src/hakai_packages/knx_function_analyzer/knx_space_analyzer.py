import logging

from .knx_spaces_repository import KNXSpacesRepository
from hakai_packages.knx_project_objects import KNXSpace
from hakai_packages.hakai_conf import HAKAIConfiguration

class KNXSpaceAnalyzer:

    # for information, instance attributes
    # _spaces_repository: KNXSpacesRepository

    def __init__(self):
        self._spaces_repository = KNXSpacesRepository()
        self.__star_analysis()

    def __star_analysis(self):
        root_name : str
        if HAKAIConfiguration.get_instance().suppress_project_name:
            root_name = ""
        else:
            root_name = HAKAIConfiguration.get_instance().project.info.name
        self.__recursive_space_searcher(1,
                                        root_name,
                                        HAKAIConfiguration.get_instance().project.locations)

    def __recursive_space_searcher(self,
                                   level : int,
                                   name: str,
                                   spaces: dict[str, KNXSpace]):
        nb_elem = len(spaces)
        logging.info("%s location(s) has been found at level %s in %s",
                     nb_elem, level, name)
        space: KNXSpace
        separator = HAKAIConfiguration.get_instance().location_separator
        for space in spaces.values():
            new_name : str
            if name == "":
                new_name = space.name
            else:
                new_name = name + separator + space.name
            new_level=level+1
            logging.info("Starting analysis at level %s of %s",
                         new_level, new_name)
            self._spaces_repository.add_space(new_name,space)
            self.__recursive_space_searcher(new_level, new_name, space.spaces)

    @property
    def repository(self):
        return self._spaces_repository

    def __iter__(self):
        return self._spaces_repository.__iter__()

    def __next__(self):
        return self._spaces_repository.__next__()
