import logging
import os

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

    def __init__(self):
        self._locations_list = []
        # Add the custom representer to the PyYAML instance
        yaml.add_representer(Quoted, self.__custom_representer)

    def import_from_knx_spaces_repository(self, knx_spaces_repository: KNXSpacesRepository, knx_project_manager: KNXProjectManager):
        for name, element in knx_spaces_repository:
            existing_locations: list[HAKNXLocation] = list(filter(lambda obj: name == obj.get_name(), self._locations_list))
            if len(existing_locations) == 0:
                location = HAKNXLocation.constructor_from_knx_space(element, knx_project_manager)
                #force the name to a complete structured name to avoid duplication and limit confusion
                location.set_name(name)
                if not location.is_empty():
                    self.add_location(location)
            elif len(existing_locations) == 1:
                existing_locations[0].import_knx_space(element, knx_project_manager)
                #force the name to a complete structured name to avoid duplication and limit confusion
                existing_locations[0].set_name(name)
            else:
                raise ValueError(f"Several existing locations with name {name}")

    def import_from_path(self, import_path):
        for file in os.listdir(import_path):
            if file.endswith(".yaml"):
                file_name = os.path.splitext(file)[0]
                file_path = os.path.join(import_path, file)
                location = HAKNXLocation.constructor_from_file(file_path)
                location._name = file_name
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

    def dump(self, output_path, create_output_path: bool = False, overwrite: bool = False):
        if not os.path.exists(output_path):
            if create_output_path:
                os.makedirs(output_path, exist_ok=True)
            else:
                raise FileNotFoundError(f"Output path '{output_path}' does not exist.")
        if not os.path.isdir(output_path):
            raise NotADirectoryError(f"Output path '{output_path}' is not a directory.")
        for element in self._locations_list:
            file_path = os.path.join(output_path, f"{element.get_name()}.yaml")
            if os.path.exists(file_path) and not overwrite:
                raise PermissionError(f"File '{file_path}' already exists.")
            else:
                with open(file_path, "w") as file:
                    file.write(element.dump())

