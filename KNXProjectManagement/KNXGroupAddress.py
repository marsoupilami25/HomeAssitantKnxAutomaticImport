from ClassFromTypedDict import ClassFromTypedDict
from unidecode import unidecode
from xknxproject.models import GroupAddress

from KNXProjectManagement.KNXDPTType import KNXDPTType


class KNXGroupAddress(ClassFromTypedDict):
    _class_ref = GroupAddress

    _name : str
    address : str
    dpt : KNXDPTType
    communication_object_ids: list[str]

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return self.name.lower()
