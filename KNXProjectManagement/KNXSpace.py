from __future__ import annotations  # Enables forward references in type hints

from typing import NewType

from unidecode import unidecode

from xknxproject.models import Space

from Utils.ClassFromTypedDict import ClassFromTypedDict

class KNXSpace(ClassFromTypedDict):
    _class_ref = Space

    _name : str

    spaces : dict[str, KNXSpace]
    functions : list[str]

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return self.name.lower()