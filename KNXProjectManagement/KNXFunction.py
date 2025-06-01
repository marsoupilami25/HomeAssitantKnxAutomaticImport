from unidecode import unidecode
from xknxproject.models import Function

from KNXProjectManagement.KNXGroupAddressRef import KNXGroupAddressRef
from ClassFromTypedDict import ClassFromTypedDict


class KNXFunction(ClassFromTypedDict):
    _class_ref = Function

    # for information, instance attributes
    # group_addresses: dict[str, KNXGroupAddressRef]

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
