import logging

from xknxproject.models import GroupAddress

from KNXProjectManagement.KNXGroupAddress import KNXGroupAddress

class KNXGroupAddressList:
    _knx_group_address_list: dict[str, GroupAddress]

    def __init__(self, ga_list: dict[str, GroupAddress]):
        self._knx_group_address_list = ga_list

    def get_knx_group_address(self, ref: str) -> KNXGroupAddress:
        if ref in self._knx_group_address_list:
            ga: GroupAddress = self._knx_group_address_list[ref]
            knx_ga: KNXGroupAddress = KNXGroupAddress(ga)
            return knx_ga
        else:
            logging.error(f"Group Address ref {ref} not found")
            return None