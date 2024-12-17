from typing_extensions import overload

class quoted(str):
    pass

class Serializable:

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            to_add = True
            # Skip private attributes (names starting with "_")
            if key.startswith('_'):
                to_add = False
            # Skip attributes with value of None
            if value is None:
                to_add = False
            if to_add:
                result[key] = Serializable.convert_to_dict(value)
        return result

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(**dict_obj)

    @staticmethod
    def convert_to_dict(obj: object):
        if isinstance(obj, Serializable):
            # Recursively call to_dict() for nested Serializable objects
            return obj.to_dict()
        elif isinstance(obj, list):
            # Handle lists: apply recursion for elements that are Serializable
            result = []
            for item in obj:
                result.append(Serializable.convert_to_dict(item))
            return result
        elif isinstance(obj, dict):
            # Handle dictionaries: apply recursion for values that are Serializable
            result = {}
            for k, v in obj.items():
                result[k] = Serializable.convert_to_dict(v)
            return result
        elif isinstance(obj, str):
            return quoted(obj)
        else:
            # For simple types, just add the value
            return obj
