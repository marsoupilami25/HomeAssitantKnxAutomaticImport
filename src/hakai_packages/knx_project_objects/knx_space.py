from __future__ import annotations  # Enables forward references in type hints

from xknxproject.models import Space

from classfromtypeddict import ClassFromTypedDict
from hakai_packages.knx_utils import KNXNamedClass


class KNXSpace(ClassFromTypedDict, KNXNamedClass):
    _class_ref = Space

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs
    #   to be import otherwise the conversion does not work
    # spaces : dict[str, KNXSpace]
    # functions : list[str]

    def __init__(self, data: dict):
        self.spaces : dict[str, KNXSpace] = {}
        self.functions : list[str] = []
        KNXNamedClass.__init__(self)
        ClassFromTypedDict.__init__(self,data)
