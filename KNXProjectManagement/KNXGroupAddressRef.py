from unidecode import unidecode
from xknxproject.models import GroupAddressRef

from ClassFromTypedDict import ClassFromTypedDict


class KNXGroupAddressRef(ClassFromTypedDict):
    _class_ref = GroupAddressRef

    # for information, instance attributes
    # _name : str
    # address : str

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return self.name.lower()
