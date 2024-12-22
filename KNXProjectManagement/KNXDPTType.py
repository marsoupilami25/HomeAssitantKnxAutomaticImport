from xknxproject.models import DPTType

from ClassFromTypedDict import ClassFromTypedDict


class KNXDPTType(ClassFromTypedDict):

    _class_ref = DPTType

    @classmethod
    def constructor_from_ints(cls,main: int, sub: int):
        """

        :param main:
        :type main:
        :param sub:
        :type sub:
        :return:
        :rtype:
        """
        dpt: DPTType = { "main" : main,
                         "sub" : sub}
        instance = cls(dpt)
        return instance