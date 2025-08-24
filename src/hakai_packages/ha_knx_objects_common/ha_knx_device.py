import logging
from enum import Enum
from typing import TypedDict, NamedTuple, Optional, Type
from ruamel.yaml import YAML

from hakai_packages.knx_project_objects import KNXDPTType
from hakai_packages.knx_project_objects import KNXFunction
from hakai_packages.knx_project_objects import KNXGroupAddress
from hakai_packages.knx_project import KNXProjectManager
from hakai_packages.knx_utils import Serializable, Quoted
from .ha_knx_value_type import HAKNXValueType

yaml = YAML()

class KNXDeviceParameterType(Enum):
    GA = 1  # Group Address parameter type
    RTR = 2 # Response to Read Parameter type
    VT = 3 # value type parameter type

    def __str__(self):
        return self.name

class KNXDeviceParameterGA(TypedDict):
    dpts: list[KNXDPTType]
    keywords: list[str]

class KNXDeviceParameterRtR(TypedDict):
    param_for_address: str
    param_for_state_address: str | None

class KNXDeviceParameterVT(TypedDict):
    param_for_state_address: str

class KNXDeviceParameter(TypedDict):
    """
    Configuration of one KNX device parameter
    :attr name: name of the parameter
    :attr required: indicate if the parameter is mandatory or optional
    :attr dpts: type of authorized dpt. Should be empty if no constraints
    :attr keywords: list of keywords to identify the group address attached to the parameter
    """
    name : str
    required: bool
    type: KNXDeviceParameterType
    configuration: KNXDeviceParameterGA | KNXDeviceParameterRtR | KNXDeviceParameterVT
    param_class: Type

class HAKNXDevice(Serializable):
    """
    This class is a super class for HA KNX device.
    An HA KNX object will create an entry in the yaml KNX configuration file for Home Assistant.
    List of devices and possible parameters are available here:
                                                https://www.home-assistant.io/integrations/knx/
    :attr keyname: key name to use for the device in the yaml file
    :attr keywords: list of keywords to identify a HA KNX device.
        The name of the function shall contain one of the keyword to create the associated device
    :attr parameters: list of expected parameters
    """
    keyname: str
    keywords: list[str]
    parameters: list[KNXDeviceParameter]

    class _Result(NamedTuple):
        """
        internal class to return a result able to make difference between None and nothing found
        """
        found: bool
        data: Optional[object]

    @classmethod
    def get_device_type_name(cls):
        return cls.keyname

    def __init__(self):
        super().__init__()
        self.name = Quoted("")
        self._extra = {}

    @staticmethod
    def _get_param_for_ga(param_name:str,
                          config: KNXDeviceParameterGA,
                          function: KNXFunction,
                          knx_project_manager: KNXProjectManager) -> _Result:
        param_found = False
        param_value = None
        gas = function.group_addresses #get group addresses from the function
        # no keyword case
        if not config["keywords"]:
            if len(gas) > 1:
                logging.warning("No keyword but many GAs for parameter %s. "
                                "Only one GA is expected.", param_name)
            else:
                ga_ref = list(gas)[0]
                # get the detail group address
                ga: KNXGroupAddress = knx_project_manager.get_knx_group_address(ga_ref)
                logging.info("Parameter %s found in GA '%s'",
                             param_name, ga.name)
                if (not config["dpts"]) or (ga.dpt in config["dpts"]):
                    param_found = True
                    param_value = ga.address
                else:
                    logging.warning(
                        "Incompatible DPT type for parameter %s "
                        "found in GA '%s'. Have %s "
                        "but expect %s", 
                        param_name, ga.name, ga.dpt, config["dpts"])
            return HAKNXDevice._Result(param_found, param_value)
        # keyword case
        for ga_ref in gas.keys():  # go through all group address name
            # get the detail group address
            ga: KNXGroupAddress = knx_project_manager.get_knx_group_address(ga_ref)
            name = ga.flat_name  # get the flat name of the GA
            keyword_found = False
            for key in config["keywords"]:  # search it in the keywords list
                if key in name:
                    keyword_found = True
                    break
            if keyword_found:  # if keyword found
                logging.info("Parameter %s found in GA '%s'",
                             param_name, ga.name)
                # check DPT Type
                if (not config["dpts"]) or (ga.dpt in config["dpts"]):
                    param_found = True
                    param_value = ga.address
                    break  # stop group address search
                logging.warning(
                    "Incompatible DPT type for parameter %s "
                    "found in GA '%s'. Have %s "
                    "but expect %s",
                    param_name, ga.name, ga.dpt, config["dpts"])
                break  # stop group address search
        return HAKNXDevice._Result(param_found, param_value)

    def _get_param_for_rtr(self,
                           param_name:str,
                           config: KNXDeviceParameterRtR,
                           function: KNXFunction, # pylint: disable=unused-argument
                           knx_project_manager: KNXProjectManager) -> _Result:
        param_found = False
        param_value = None
        address_found = False
        address_rtr = None # true if one device answer to a Group value Read request
        state_address_found = False
        # search for address parameter
        if ((hasattr(self,config["param_for_address"]))
                and (getattr(self, config["param_for_address"]) is not None)):
            address_found = True
            address_rtr = False
            ga_ref = getattr(self, config["param_for_address"])
            # get the detail group address
            ga: KNXGroupAddress = knx_project_manager.get_knx_group_address(ga_ref)
            logging.info("Address found %s", ga.name)
            for com_obj in ga.communication_object_ids:
                co = knx_project_manager.get_com_object(com_obj)
                if co.is_readable():
                    logging.info("RtR identified")
                    address_rtr = True
        else:
            logging.warning("No address parameter '%s' "
                            "found for parameter '%s'", 
                            config["param_for_address"], param_name)
        if config["param_for_state_address"] is not None:
            if ((hasattr(self,config["param_for_state_address"]))
                    and (getattr(self, config["param_for_state_address"]) is not None)):
                state_address_found = True
                logging.info("State address found")
        if address_found:
            param_found = True
            param_value = True
            if (address_found and address_rtr) or state_address_found:
                param_value = False
            logging.info("Param for RtR is found and is %s", param_value)
        else:
            logging.info("Param for RtR is not found")
        return HAKNXDevice._Result(param_found, param_value)

    def _get_param_for_vt(self,
                          param_name:str, # pylint: disable=unused-argument
                          config: KNXDeviceParameterVT,
                          function: KNXFunction, # pylint: disable=unused-argument
                          knx_project_manager: KNXProjectManager) -> _Result:
        param_found = False
        param_value = None
        if ((hasattr(self,config["param_for_state_address"]))
                and (getattr(self, config["param_for_state_address"]) is not None)):
            param_found = True
            ga_ref = getattr(self,config["param_for_state_address"])
            # get the detail group address
            ga: KNXGroupAddress = knx_project_manager.get_knx_group_address(ga_ref)
            param_value = HAKNXValueType()
            param_value.dpt = ga.dpt
            logging.info("VT of type %s found", param_value)
        return HAKNXDevice._Result(param_found, param_value)

    def set_from_function(self,
                          function: KNXFunction,
                          knx_project_manager: KNXProjectManager) -> bool:
        """
        Constructor of the class based on a function.
        :param function: function to create
        :type function: KNXFunction
        :param knx_project_manager: KNX Project Manager containing the list of GAs
        :type knx_project_manager: KNXProjectManager
        :return: instance of the class
        :rtype: subclass of HAKNXDevice
        """
        self.name = Quoted(function.name) #the name of the device is the name of the KNX function
        for param in self.parameters: #go through all expected parameters in the class
            logging.info("Search for parameter %s of type %s",
                         param["name"], param["type"])
            result: HAKNXDevice._Result = HAKNXDevice._Result(False, None)
            if param["type"] == KNXDeviceParameterType.GA:
                result = self._get_param_for_ga(param["name"],
                                                param["configuration"],
                                                function,
                                                knx_project_manager)
            elif param["type"] == KNXDeviceParameterType.RTR:
                result = self._get_param_for_rtr(param["name"],
                                                 param["configuration"],
                                                 function,
                                                 knx_project_manager)
            elif param["type"] == KNXDeviceParameterType.VT:
                result = self._get_param_for_vt(param["name"],
                                                param["configuration"],
                                                function,
                                                knx_project_manager)
            else:
                raise ValueError(f"Unexpected Parameter Type {param["type"]}")
            param_found = result.found
            param_value = result.data
            if param_found: #if parameter has not been found
                attr_type = param['param_class']
                try:
                    final_value=attr_type(param_value)
                except (TypeError, ValueError, AttributeError):
                    final_value=param_value
                setattr(self, param["name"], final_value)  # set the attribute
            else:
                if param["required"]:
                    logging.warning("Parameter %s "
                                    "not found in function %s", 
                                    param["name"], function.name)
                    return False
                logging.info("Parameter %s "
                             "not found in function %s",
                             param["name"], function.name)
        return True

    @classmethod
    def is_this_type_from_function(cls, function: KNXFunction):
        name = function.flat_name
        keyword_found = False
        for key in cls.keywords:
            if key in name:
                keyword_found = True
        return keyword_found

    @classmethod
    def is_this_type_from_key_name(cls, key_name : str):
        return key_name == cls.keyname
