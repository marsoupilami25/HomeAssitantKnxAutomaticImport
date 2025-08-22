from knx_project_objects import KNXSpace


class KNXSpacesRepository:

    # for information, instance attributes
    # _spaces_dict: dict[str, KNXSpace]

    def __init__(self):
        self._spaces_dict = {}

    def add_space(self, name: str, space: KNXSpace):
        #name for yaml in HA has several constraints:
        #   . no space
        #   . lower case
        self._spaces_dict[name.lower().replace(" ","")] = space

    @property
    def list(self):
        return self._spaces_dict

    def __iter__(self):
        return self._spaces_dict.items().__iter__()

    def __next__(self):
        return self._spaces_dict.items().__iter__().__next__()
