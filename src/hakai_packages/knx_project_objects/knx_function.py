from xknxproject.models import Function

from classfromtypeddict import ClassFromTypedDict
from hakai_packages.knx_utils import KNXNamedClass
from .knx_group_address_ref import KNXGroupAddressRef

class KNXFunction(ClassFromTypedDict, KNXNamedClass):
    _class_ref = Function

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs
    #   to be import otherwise the conversion does not work
    # group_addresses: dict[str, KNXGroupAddressRef]

    def __init__(self, data: dict):
        self.group_addresses : dict[str, KNXGroupAddressRef] | None = None #None only for init
        KNXNamedClass.__init__(self)
        ClassFromTypedDict.__init__(self,data)
