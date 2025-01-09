import inspect

from ruamel.yaml import YAML, yaml_object
from ruamel.yaml.scalarstring import DoubleQuotedScalarString


class Quoted(str):
    pass

yaml = YAML()

@yaml_object(yaml)
class Serializable:

    @classmethod
    def to_yaml(cls, representer, node):
        DQ = DoubleQuotedScalarString
        state = node.__dict__.copy()
        for key, value in node.__dict__.items():
            # Skip private attributes (names starting with "_")
            if key.startswith('_'):
                state.pop(key)
            # Skip attributes with value of None
            if value is None:
                state.pop(key)
            if isinstance(value,str):
                state[key] = DoubleQuotedScalarString(value)
        output_node = representer.represent_mapping('tag:yaml.org,2002:map', state)
        return output_node

    def from_dict(self, dict_obj: dict):
        type_list = {}
        for base in inspect.getmro(type(self)):
            new_list = inspect.get_annotations(base)
            type_list.update(new_list)
        for key, value in dict_obj.items():
            if key in type_list.keys():
                attr_type = type_list[key]
                value_type = type(value)
                if issubclass(attr_type, Serializable):
                    obj = attr_type()
                    obj.from_dict(value)
                    setattr(self, key, obj)
                else:
                    setattr(self, key, value)
            else:
                setattr(self, key, value)

