import inspect
from typing import cast

from ruamel.yaml import YAML, yaml_object, CommentedMap
from ruamel.yaml.scalarstring import DoubleQuotedScalarString


class Quoted(str):
    pass

yaml = YAML()

@yaml_object(yaml)
class Serializable:

    _comments = {}

    @classmethod
    def pre_convert(cls, obj):
        commented_node = CommentedMap(obj.__dict__.copy())
        for key, value in obj.__dict__.items():
            # Skip private attributes (names starting with "_")
            if key.startswith('_'):
                commented_node.pop(key)
            else:
                # Skip attributes with value of None
                if value is None:
                    commented_node.pop(key)
                else:
                    if isinstance(value, Quoted):
                        commented_node[key] = DoubleQuotedScalarString(value)
                    if key in cls._comments[commented_node['name']]:
                        commented_node.ca.items[key] = cls._comments[commented_node['name']][key]
        return commented_node

    @classmethod
    def to_yaml(cls, representer, node):
        state = cls.pre_convert(node)
        output_node = representer.represent_mapping('tag:yaml.org,2002:map', state)
        return output_node

    def from_dict(self, dict_obj: CommentedMap):
        self.__class__._comments[dict_obj['name']] = {}
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
                self._comments[dict_obj['name']][key] = comment_pre

