from unidecode import unidecode

from xknxproject.models import Space

class KNXSpace:
    _space: Space

    def __init__(self, space: Space):
        self._space = space

    @property
    def space(self) -> Space:
        return self._space

    @property
    def name(self) -> str:
        return unidecode(self._space["name"])

    @property
    def flat_name(self) -> str:
        return self.name.lower()


    @property
    def functions(self) -> list[str]:
        return self._space["functions"]

    @property
    def spaces(self):
        knx_spaces_list = [KNXSpace(value) for value in self._space["spaces"].values()]
        return knx_spaces_list
