from unidecode import unidecode
from xknxproject.models import ProjectInfo

from Utils.FromDict import FromDict


class KNXProjectInfo(FromDict):
    _class_ref = ProjectInfo

    _name : str

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return self._name.lower()