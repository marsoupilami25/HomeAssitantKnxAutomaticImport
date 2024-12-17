from xknxproject.models import DPTType

from Utils.FromDict import FromDict


class KNXDPTType(FromDict):

    _class_ref = DPTType

    @classmethod
    def constructor_from_ints(cls,main: int, sub: int):
        dpt: DPTType = { "main" : main,
                         "sub" : sub}
        instance = cls(dpt)
        return instance