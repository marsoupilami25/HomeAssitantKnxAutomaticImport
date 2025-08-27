from unidecode import unidecode
from xknxproject.models import Function

from classfromtypeddict import ClassFromTypedDict
from hakai_packages.knx_utils import knx_flat_string, knx_transformed_string, Quoted
from hakai_packages.hakai_conf import HAKAIConfiguration
from .knx_group_address_ref import KNXGroupAddressRef

class KNXFunction(ClassFromTypedDict):
    _class_ref = Function

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs
    #   to be import otherwise the conversion does not work
    # group_addresses: dict[str, KNXGroupAddressRef]

    def __init__(self, data: dict):
        self._name = ""
        self.group_addresses : dict[str, KNXGroupAddressRef] | None = None #None only for init
        super().__init__(data)

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return knx_flat_string(self.name)

    def transformed_name(self, keywords: list[str]) -> str:
        result_name = Quoted(knx_transformed_string(self.name))
        if HAKAIConfiguration.get_instance().remove_keyword:
            new_name = result_name
            for kw in keywords:
                # apply transformation to the keyword
                tkw = knx_transformed_string(kw)
                # remove all occurrences
                new_name = new_name.replace(tkw, "")
            new_name = new_name.strip()
            if new_name != '':
                result_name = Quoted(new_name)
        return result_name
