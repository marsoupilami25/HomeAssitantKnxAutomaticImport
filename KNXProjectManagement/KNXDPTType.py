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
        # two DPT are equal if they have the same main and sub or if thay have the same main but one of the sub is 0
        # when sub is 0, it covers all possible value of the sub
        return (self.main == other.main) and ((self.sub == other.sub) or (self.sub == 0) or (other.sub == 0))

    def __str__(self):
        if self.sub == 0:
            return f"DPT {self.main}"
        else:
            return f"DPT {self.main}.{self.sub:03}"

    def __repr__(self):
        return self.__str__()