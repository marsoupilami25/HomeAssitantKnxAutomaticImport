from unidecode import unidecode
from xknxproject.models import GroupAddress

class KNXGroupAddress:
    _group_address: GroupAddress

    def __init__(self, ga: GroupAddress):
        self._group_address = ga

    @property
    def name(self):
        return unidecode(self._group_address["name"])

    @property
    def flat_name(self):
        return self.name.lower()

    @property
    def address(self):
        return self._group_address["address"]

    @property
    def dpt(self):
        return self._group_address["dpt"]
