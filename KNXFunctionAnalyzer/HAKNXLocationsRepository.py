import yaml
from yaml import Dumper

from HAKNXObjectCreator.HAKNXLocation import HAKNXLocation
from KNXFunctionAnalyzer.KNXSpacesRepository import KNXSpacesRepository
from KNXProjectManagement.KNXProjectManager import KNXProjectManager
from Utils.Serializable import Quoted



class HAKNXLocationsRepository:
    _locations_list: list[HAKNXLocation]

    # Custom dumper to add quotes only for string values in yaml
    @staticmethod
    def __custom_representer(dumper: Dumper, value):
        if isinstance(value, str):
            return dumper.represent_scalar('tag:yaml.org,2002:str', value, style='"')
        return dumper.represent_data(value)

    def __init__(self, knx_spaces_repository: KNXSpacesRepository, knx_project_manager: KNXProjectManager):
        self._locations_list = []
        # Add the custom representer to the PyYAML instance
        yaml.add_representer(Quoted, self.__custom_representer)
        for name, element in knx_spaces_repository:
            location = HAKNXLocation(element, knx_project_manager)
            location._name = name
            if not location.is_empty():
                self.add_location(location)

    def add_location(self, location: HAKNXLocation):
        self._locations_list.append(location)

    @property
    def list(self):
        return self._locations_list

    def __iter__(self):
        return self._locations_list.__iter__()

    def __next__(self):
        return self._locations_list.__iter__().__next__()

    def dump(self):
        for element in self._locations_list:
            print(element.dump())

