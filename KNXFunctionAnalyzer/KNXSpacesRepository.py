from KNXProjectManagement.KNXSpace import KNXSpace


class KNXSpacesRepository:
    _spaces_list: list[KNXSpace]

    def __init__(self):
        self._spaces_list = []

    def add_space(self, space: KNXSpace):
        self._spaces_list.append(space)

    @property
    def list(self):
        return self._spaces_list

    def __iter__(self):
        return self._spaces_list.__iter__()

    def __next__(self):
        return self._spaces_list.__iter__().__next__()

knx_spaces_repository = KNXSpacesRepository()