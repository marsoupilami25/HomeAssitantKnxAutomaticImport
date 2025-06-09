from ClassFromTypedDict import ClassFromTypedDict
from xknxproject.models import Flags


class KNXFlags(ClassFromTypedDict):
    _class_ref = Flags

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs to be import otherwise the conversion does not work
    # read: bool
    # write: bool
    # communication: bool
    # transmit: bool
    # update: bool
    # read_on_init: bool


