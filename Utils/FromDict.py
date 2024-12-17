import importlib
from typing import get_type_hints, get_origin, get_args, _TypedDictMeta

from pydantic.typing import is_union
from typing import TypedDict


class FromDict:

    _class_ref: TypedDict
    _typeddict_class_association = {}

    @classmethod
    def set_typeddict_class_association(cls, association: dict):
        cls._typeddict_class_association=association

    # Dynamic creation of the class
    def __init__(self, data: dict):
        hints = get_type_hints(self._class_ref)  # Gather TypedDict annotations

        # Check there is no unexpected fields
        extra_fields = [field for field in data.keys() if field not in hints.keys()]
        if extra_fields:
            raise TypeError(f"Unexpected fields: {', '.join(extra_fields)}")

        # Check there is missing no field
        missing_fields = [field for field in hints.keys() if field not in data.keys()]
        if missing_fields:
            raise TypeError(f"Missing required fields: {', '.join(missing_fields)}")

        # gather attributes
        for field, field_type in hints.items():
            self.__analyze_data(data[field], type(data[field]), field, field_type)

    def __analyze_data(self, data, data_type, field, field_type):
        origin_type = get_origin(field_type)
        if origin_type is None:
            if not self.__check_data(data, data_type, field, field_type):
                raise TypeError(f"Field '{field}' must be of type {field_type}, got {data_type}")
        elif is_union(origin_type):
            types = get_args(field_type)
            type_found = False
            for type_elem in types:
                check_result = self.__check_data(data, data_type, field, type_elem)
                type_found = type_found or check_result
                if type_found:
                    break
            if not type_found:
                raise TypeError(f"Field '{field}' must be of one of the type {field_type}, got {data_type}")
        elif issubclass(origin_type, list):
            # in the case of list, the case of list of TypedDict or more complex type containing TypedDict is not managed
            # at this current time, the xknx project does not contain such case
            setattr(self, field, data)
        elif issubclass(origin_type, dict):
            raise TypeError("dict case not managed")
        else:
            raise TypeError(f"Unexpected case for data '{data[field]}' must be of type {data_type}")

    def __check_data(self, data, data_type, field, field_type) -> bool:
        if issubclass(type(field_type), _TypedDictMeta):
            if data_type is dict:
                new_data = self.__convert_dict_to_class(field_type, data)
                setattr(self, field, new_data)
                return True
            else:
                return False
        else:
            if data_type == field_type:
                setattr(self, field, data)
                return True
            else:
                return False

    def __convert_dict_to_class(self, field_type, data):
        field_type_name = field_type.__name__
        if field_type_name in self._typeddict_class_association:
            module_name, class_name = self._typeddict_class_association[field_type_name].rsplit(".", 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            new_data = cls(data)
            return new_data
        else:
            return data