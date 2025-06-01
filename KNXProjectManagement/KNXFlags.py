from ClassFromTypedDict import ClassFromTypedDict
from xknxproject.models import Flags


class KNXFlags(ClassFromTypedDict):
    _class_ref = Flags

    # for information, instance attributes
    # read: bool
    # write: bool
    # communication: bool
    # transmit: bool
    # update: bool
    # read_on_init: bool


