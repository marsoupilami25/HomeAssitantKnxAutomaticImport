from unidecode import unidecode

from hakai_packages.knx_utils import knx_transformed_string, knx_flat_string


class KNXNamedClass():

    def __init__(self):
        self._name = ""

    @property
    def name(self):
        return unidecode(self._name)

    @name.setter
    def name(self, string: str):
        self._name = string

    @property
    def flat_name(self):
        return knx_flat_string(self.name)

    @property
    def transformed_name(self):
        return knx_transformed_string(self.name)
