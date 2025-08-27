import logging
import os
import sys

from hakai_packages.ha_knx_objects_factory import HAKNXLocation
from hakai_packages.hakai_conf import HAKAIConfiguration
from hakai_packages.knx_utils import knx_transformed_string
from .knx_spaces_repository import KNXSpacesRepository


class HAKNXLocationsRepository:

    # for information, instance attributes
    #_locations_list: list[HAKNXLocation]

    def __init__(self):
        self._locations_list = []

    def import_from_knx_spaces_repository(self,
                                          knx_spaces_repository: KNXSpacesRepository):
        for name, element in knx_spaces_repository:
            # warning: after an import from path, the name of the location is the transformed
            searched_name = knx_transformed_string(name)
            existing_locations: list[HAKNXLocation] =\
                list(filter(lambda obj, n = searched_name: n == obj.name,
                            self._locations_list))
            # force the name to a complete structured name
            # to avoid duplication and limit confusion
            element.name = name
            if len(existing_locations) == 0:
                location = HAKNXLocation.constructor_from_knx_space(element)
                # force the name to a complete structured name
                # to avoid duplication and limit confusion
                # location.name = name
                if not location.is_empty():
                    location.touched()
                    self.add_location(location)
            elif len(existing_locations) == 1:
                existing_locations[0].import_knx_space(element)
                # force the name to a complete structured name
                # to avoid duplication and limit confusion
                # existing_locations[0].name = name
                existing_locations[0].check()
                existing_locations[0].touched()
            else:
                raise ValueError(f"Several existing locations with name {name}")

    def import_from_path(self, import_path):
        for file in os.listdir(import_path):
            if file.endswith(".yaml"):
                file_name = os.path.splitext(file)[0]
                file_path = os.path.join(import_path, file)
                location = HAKNXLocation.constructor_from_file(file_path, file_name)
                if not location.is_empty():
                    self.add_location(location)

    def add_location(self, location: HAKNXLocation):
        self._locations_list.append(location)

    def remove_location(self, location: HAKNXLocation):
        try:
            self._locations_list.remove(location)
        except ValueError:
            logging.critical("Exception: %s is not a location present"
                             " in the locations repository", location.name())
            sys.exit(1)

    def check(self):
        if HAKAIConfiguration.get_instance().not_remove_location:
            return
        list_to_remove : list[HAKNXLocation] = []
        for element in self._locations_list:
            if not element.is_touched():
                list_to_remove.append(element)
        for element in list_to_remove:
            logging.info("%s does not exist anymore in the project."
                         " File will not be generated.", element.name)
            self.remove_location(element)

    @property
    def list(self):
        return self._locations_list

    def __iter__(self):
        return self._locations_list.__iter__()

    def __next__(self):
        return self._locations_list.__iter__().__next__()

    def dump(self,
             output_path,
             create_output_path: bool = False):
        overwrite = HAKAIConfiguration.get_instance().overwrite
        if not os.path.exists(output_path):
            if create_output_path:
                os.makedirs(output_path, exist_ok=True)
            else:
                raise FileNotFoundError(f"Output path '{output_path}' does not exist.")
        if not os.path.isdir(output_path):
            raise NotADirectoryError(f"Output path '{output_path}' is not a directory.")
        for element in self._locations_list:
            file_path = os.path.join(output_path, f"{element.transformed_name}.yaml")
            if os.path.exists(file_path) and not overwrite:
                raise PermissionError(f"File '{file_path}' already exists. "
                                      f"Overwrite not authorized.")
            with open(file_path, "w", encoding="utf-8") as file:
                initial_dump = element.dump()
                file.write(initial_dump)
