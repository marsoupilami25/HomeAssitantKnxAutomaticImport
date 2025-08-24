from __future__ import annotations  # Enables forward references in type hints

from unidecode import unidecode

from xknxproject.models import Space

from classfromtypeddict import ClassFromTypedDict
from hakai_packages.hakai_conf import HAKAIConfiguration
from hakai_packages.knx_utils import knx_flat_string


class KNXSpace(ClassFromTypedDict):
    _class_ref = Space

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs
    #   to be import otherwise the conversion does not work
    # spaces : dict[str, KNXSpace]
    # functions : list[str]

    def __init__(self, data: dict):
        self._name = ""
        self.spaces : dict[str, KNXSpace] = {}
        self.functions : list[str] = []
        super().__init__(data)

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return knx_flat_string(self.name)

    @property
    def transformed_name(self):
        new_char = HAKAIConfiguration.get_instance().replace_spaces
        if new_char == ' ':
            return self.flat_name
        if new_char == '/':
            return self.flat_name.replace(' ','')
        return self.flat_name.replace(' ',new_char)
