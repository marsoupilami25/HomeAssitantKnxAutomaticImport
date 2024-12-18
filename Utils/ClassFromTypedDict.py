import importlib
from typing import get_type_hints, get_origin, get_args, _TypedDictMeta, Optional, NamedTuple

from click.testing import Result
from pydantic.typing import is_union
from typing import TypedDict


class ClassFromTypedDict:

    _class_ref: TypedDict
    _typeddict_class_association = {}

    class _Result(NamedTuple):
        found: bool
        data: Optional[object]

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
            new_data = self.__analyze_data(data[field], type(data[field]), field_type, field)
            if new_data is not None:
                setattr(self, field, new_data)

    def __analyze_data(self, data, data_type, expected_data_type, field) -> object:
        origin_type = get_origin(expected_data_type)
        if origin_type is None:
            result : ClassFromTypedDict._Result = self.__check_data(data, data_type, expected_data_type)
            if result.found:
                return result.data
            else:
                raise TypeError(f"Analyzing field '{field}', unexpected type {data_type}, waiting {expected_data_type}")
        elif is_union(origin_type):
            types = get_args(expected_data_type)
            for type_elem in types:
                result : ClassFromTypedDict._Result = self.__check_data(data, data_type, type_elem)
                if result.found:
                    return result.data
            raise TypeError(f"Analyzing field '{field}', unexpected type {data_type}, waiting {expected_data_type} in ")
        elif issubclass(origin_type, list):
            # in the case of list, the case of list of TypedDict or more complex type containing TypedDict is not managed
            # at this current time, the xknx project does not contain such case
            return data
        elif issubclass(origin_type, dict):
            field_key_type, field_value_type = get_args(expected_data_type)
            new_data = {}
            for key, value in data.items():
                new_key = self.__analyze_data(key, type(key), field_key_type, field)
                new_value = self.__analyze_data(value, type(value), field_value_type, field)
                new_data[new_key] = new_value
            return new_data
        else:
            raise TypeError(f"Unexpected case analyzing field '{field}")

    def __check_data(self, data, data_type, field_type) -> _Result:
        if issubclass(type(field_type), _TypedDictMeta):
            if data_type is dict:
                new_data = self.__convert_dict_to_class(field_type, data)
                return self._Result(found=True, data=new_data)
            else:
                return self._Result(found=False, data=None)
        else:
            if data_type == field_type:
                return self._Result(found=True, data=data)
            else:
                return self._Result(found=False, data=None)

    def __convert_dict_to_class(self, field_type, data) -> object:
        field_type_name = field_type.__name__
        if field_type_name in self._typeddict_class_association:
            module_name, class_name = self._typeddict_class_association[field_type_name].rsplit(".", 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            new_data = cls(data)
            return new_data
        else:
            return data