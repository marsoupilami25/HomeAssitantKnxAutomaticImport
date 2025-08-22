from unidecode import unidecode
from xknxproject.models import Function

from classfromtypeddict import ClassFromTypedDict
from .knx_group_address_ref import KNXGroupAddressRef

class KNXFunction(ClassFromTypedDict):
    _class_ref = Function

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs
    #   to be import otherwise the conversion does not work
    # group_addresses: dict[str, KNXGroupAddressRef]

    def __init__(self, data: dict):
        self._name = ""
        self.group_addresses : dict[str, KNXGroupAddressRef] | None = None #None only for init
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
