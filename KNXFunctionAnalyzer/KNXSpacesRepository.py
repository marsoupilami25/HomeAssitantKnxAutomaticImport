from KNXProjectManagement.KNXSpace import KNXSpace


class KNXSpacesRepository:
    _spaces_dict: dict[str, KNXSpace]

    def __init__(self):
        self._spaces_dict = {}

    def add_space(self, name: str, space: KNXSpace):
        self._spaces_dict[name] = space

    @property
    def list(self):
        return self._spaces_dict

    def __iter__(self):
        return self._spaces_dict.items().__iter__()

    def __next__(self):
        return self._spaces_dict.items().__iter__().__next__()