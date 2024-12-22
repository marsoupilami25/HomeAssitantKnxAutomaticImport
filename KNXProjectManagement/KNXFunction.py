from unidecode import unidecode
from xknxproject.models import Function

from KNXProjectManagement.KNXGroupAddressRef import KNXGroupAddressRef
from Utils.ClassFromTypedDict import ClassFromTypedDict


class KNXFunction(ClassFromTypedDict):
    _class_ref = Function

    _name : str
    group_addresses: dict[str, KNXGroupAddressRef]

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return self.name.lower()
