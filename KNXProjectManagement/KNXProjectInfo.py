from unidecode import unidecode
from xknxproject.models import ProjectInfo

from ClassFromTypedDict import ClassFromTypedDict


class KNXProjectInfo(ClassFromTypedDict):
    _class_ref = ProjectInfo

    # for information, instance attributes
    # _name : str

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