from ClassFromTypedDict import ClassFromTypedDict
from unidecode import unidecode
from xknxproject.models import GroupAddress

from KNXProjectManagement.KNXDPTType import KNXDPTType


class KNXGroupAddress(ClassFromTypedDict):
    _class_ref = GroupAddress

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs to be import otherwise the conversion does not work
    # address : str
    # dpt : KNXDPTType
    # communication_object_ids: list[str]

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
