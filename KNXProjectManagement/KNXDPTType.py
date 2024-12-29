from xknxproject.models import DPTType

from ClassFromTypedDict import ClassFromTypedDict


class KNXDPTType(ClassFromTypedDict):

    _class_ref = DPTType

    main: int
    sub: int

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

    def __eq__(self, other):
        if not isinstance(other, KNXDPTType):
            return False
        return (self.main == other.main) and (self.sub == other.sub)

    def __str__(self):
        return f"DPT {self.main}.{self.sub:03}"

    def __repr__(self):
        return self.__str__()