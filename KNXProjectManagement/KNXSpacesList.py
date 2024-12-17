from xknxproject.models import Space

from KNXProjectManagement.KNXSpace import KNXSpace


class KNXSpacesList:
    _knx_spaces_list: list[KNXSpace]

    def __init__(self, spaces_list: list[KNXSpace]):
        self._knx_spaces_list = spaces_list

    @classmethod
    def constructor(cls, spaces_list: dict[str, Space]):
        knx_spaces_list = [KNXSpace(value) for value in spaces_list.values()]
        return cls(knx_spaces_list)

    @property
    def spaces(self) -> list[KNXSpace]:
        return self._knx_spaces_list