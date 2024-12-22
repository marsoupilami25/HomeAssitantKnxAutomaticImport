import logging

from KNXProjectManagement.KNXFunction import KNXFunction
from KNXProjectManagement.KNXGroupAddress import KNXGroupAddress
from KNXProjectManagement.KNXProjectManager import KNXProjectManager
from Utils.Serializable import Serializable


class HAKNXObject(Serializable):
    keywords: list[str]
    parameters: dict

    name: str
    _extra: dict

    @classmethod
    def constructor_with_init(cls, name: str, **kwargs):
        instance = cls()
        instance.name = name
        instance._extra = kwargs
        return instance

    @classmethod
    def constructor_with_function(cls, function: KNXFunction, knx_project_manager: KNXProjectManager):
        instance = cls()
        instance.name = function.name
        instance._extra = {}
        gas = function.group_addresses
        param_found = False
        for param in cls.parameters.keys():
            logging.info(f"Search for parameter {param}")
            keyword_found = False
            for ga_ref in gas.keys():
                ga : KNXGroupAddress = knx_project_manager.get_knx_group_address(ga_ref)
                name = ga.flat_name
                for key in cls.parameters.get(param):
                    if key in name:
                        keyword_found = True
                        break
                if keyword_found:
                    logging.info(f"Parameter {param} found in GA '{ga.name}'")
                    setattr(instance, param, ga.address)
                    param_found = True
                    break
            if param_found is False:
                logging.warning(f"Parameter {param} not found in function {function.name}")
                setattr(instance, param, "")
        return instance

    @classmethod
    def is_this_type(cls, function: KNXFunction):
        name = function.flat_name
        keyword_found = False
        for key in cls.keywords:
            if key in name:
                keyword_found = True
        return keyword_found
