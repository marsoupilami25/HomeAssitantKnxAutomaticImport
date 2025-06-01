from unidecode import unidecode
from xknxproject.models import ProjectInfo

from ClassFromTypedDict import ClassFromTypedDict


class KNXProjectInfo(ClassFromTypedDict):
    _class_ref = ProjectInfo

    # for information, instance attributes
    # _name : str

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return self.name.lower()