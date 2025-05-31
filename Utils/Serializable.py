import inspect
from typing import cast

from ruamel.yaml import YAML, yaml_object, CommentedMap
from ruamel.yaml.scalarstring import DoubleQuotedScalarString


class Quoted(str):
    pass

yaml = YAML()

class Serializable:

    def __init__(self):
        self._comments = {}

    def pre_convert(self):
        commented_map = CommentedMap(self.__dict__.copy())
        for key, value in self.__dict__.items():
            # Skip private attributes (names starting with "_")
            if key.startswith('_'):
                commented_map.pop(key)
            else:
                # Skip attributes with value of None
                if value is None:
                    commented_map.pop(key)
                else:
                    if isinstance(value, Quoted):
                        commented_map[key] = DoubleQuotedScalarString(value)
                    if key in self._comments.keys():
                        commented_map.ca.items[key] = self._comments[key]
        return commented_map

    def from_dict(self, dict_obj: CommentedMap):
        type_list = {}
        for base in inspect.getmro(type(self)):
            new_list = inspect.get_annotations(base)
            type_list.update(new_list)
        for key, value in dict_obj.items():
            if key in type_list.keys():
                attr_type = type_list[key]
                if issubclass(attr_type, Serializable):
                    obj = attr_type()
                    obj.from_dict(value)
                    setattr(self, key, obj)
                else:
                    try:
                        final_value = attr_type(value)
                    except:
                        final_value = value
                    setattr(self, key, value)
            else:
                setattr(self, key, value)
            comment_pre = dict_obj.ca.items.get(key)
            if comment_pre:
                self._comments[key] = comment_pre

    def to_yaml(self, representer):
        commented_map = self.pre_convert()
        output_node = representer.represent_mapping('tag:yaml.org,2002:map', commented_map)
        return output_node

def serializable_to_yaml(representer, obj: Serializable):
    return obj.to_yaml(representer)