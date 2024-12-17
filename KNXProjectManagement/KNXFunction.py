from unidecode import unidecode
from xknxproject.models import Function

class KNXFunction:
    _knx_function: Function

    def __init__(self, function:Function):
        self._knx_function = function

    @property
    def name(self) -> str:
        return unidecode(self._knx_function["name"])

    @property
    def flat_name(self) -> str:
        return self.name.lower()

    def group_addresses(self):
        return self._knx_function["group_addresses"]