from unidecode import unidecode
from xknxproject.models import Function

from Utils.ClassFromTypedDict import ClassFromTypedDict


class KNXFunction(ClassFromTypedDict):
    _class_ref = Function

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
