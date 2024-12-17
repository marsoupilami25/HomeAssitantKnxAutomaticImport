import logging

from xknxproject.models import Function

from KNXProjectManagement.KNXFunction import KNXFunction


class KNXFunctionsList:
    _knx_functions_list: dict[str, Function]

    def __init__(self, functions_list: dict[str, Function]):
        self._knx_functions_list = functions_list

    def get_knx_function(self, name: str) -> KNXFunction:
        if name in self._knx_functions_list:
            function = KNXFunction(self._knx_functions_list.get(name))
            logging.info(f"Function '{function.name}' found")
            return function
        else:
            logging.warning(f"Function {name} not found")
            return None