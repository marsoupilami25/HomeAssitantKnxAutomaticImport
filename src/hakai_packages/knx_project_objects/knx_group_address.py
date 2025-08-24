from classfromtypeddict import ClassFromTypedDict
from unidecode import unidecode
from xknxproject.models import GroupAddress

from hakai_packages.knx_utils import knx_flat_string
from .knx_dpt_type import KNXDPTType

class KNXGroupAddress(ClassFromTypedDict):
    _class_ref = GroupAddress

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs
    #   to be import otherwise the conversion does not work
    # address : str
    # dpt : KNXDPTType
    # communication_object_ids: list[str]

    def __init__(self, data: dict):
        self._name = ""
        self.address : str = ""
        self.dpt : KNXDPTType | None = None #None only for init
        self.communication_object_ids : list[str] = []
        super().__init__(data)

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return knx_flat_string(self.name)
