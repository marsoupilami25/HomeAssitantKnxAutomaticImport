from unidecode import unidecode
from xknxproject.models import GroupAddress, DPTType

from KNXProjectManagement.KNXDPTType import KNXDPTType
from Utils.FromDict import FromDict


class KNXGroupAddress(FromDict):
    _class_ref = GroupAddress

    _name : str

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, string: str):
        self._name = unidecode(string)

    @property
    def flat_name(self):
        return self._name.lower()
