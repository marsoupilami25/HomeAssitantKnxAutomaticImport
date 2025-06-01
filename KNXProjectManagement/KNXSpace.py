from __future__ import annotations  # Enables forward references in type hints

from unidecode import unidecode

from xknxproject.models import Space

from ClassFromTypedDict import ClassFromTypedDict

class KNXSpace(ClassFromTypedDict):
    _class_ref = Space

    # for information, instance attributes
    # spaces : dict[str, KNXSpace]
    # functions : list[str]

    def __init__(self, data: dict):
        self._name = ""
        super().__init__(data)

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return self.name.lower()