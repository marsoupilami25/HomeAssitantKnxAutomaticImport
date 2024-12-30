import logging
from typing import TypedDict

from KNXProjectManagement.KNXDPTType import KNXDPTType
from KNXProjectManagement.KNXFunction import KNXFunction
from KNXProjectManagement.KNXGroupAddress import KNXGroupAddress
from KNXProjectManagement.KNXProjectManager import KNXProjectManager
from Utils.Serializable import Serializable

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
    dpts: list[KNXDPTType]
    keywords: list[str]

class HAKNXDevice(Serializable):
    """
    This class is a super class for HA KNX device.
    An HA KNX object will create an entry in the yaml KNX configuration file for Home Assistant.
    List of devices and possible parameters are available here:  https://www.home-assistant.io/integrations/knx/
    :attr keyname: key name to use for the device in the yaml file
    :attr keywords: list of keywords to identify a HA KNX device. The name of the function shall contain one of the keyword to create the associated device
    :attr parameters: list of expected parameters
    """
    keyname: str
    keywords: list[str]
    parameters: list[KNXDeviceParameter]

    name: str
    _extra: dict

    @classmethod
    def get_device_type_name(cls):
        return cls.keyname

    def __init__(self):
        self.name = ""
        self._extra = {}

    def set_from_function(self, function: KNXFunction, knx_project_manager: KNXProjectManager):
        """
        Constructor of the class based on a function.
        :param function: function to create
        :type function: KNXFunction
        :param knx_project_manager: KNX Project Manager containing the list of GAs
        :type knx_project_manager: KNXProjectManager
        :return: instance of the class
        :rtype: subclass of HAKNXDevice
        """
        self.name = function.name #the name of the device is the name of the KNX function
        gas = function.group_addresses #get group addresses from the function
        for param in self.parameters: #go through all expected parameters in the class
            logging.info(f"Search for parameter {param["name"]}")
            param_found = False
            param_value = None
            for ga_ref in gas.keys(): #go through all group address name
                ga : KNXGroupAddress = knx_project_manager.get_knx_group_address(ga_ref) # get the detail group address
                name = ga.flat_name # get the flat name of the GA
                keyword_found = False
                for key in param["keywords"]: #search it in the keywords list
                    if key in name:
                        keyword_found = True
                        break
                if keyword_found: #if keyword found
                    logging.info(f"Parameter {param["name"]} found in GA '{ga.name}'")
                    #check DPT Type
                    if not param["dpts"]:
                        param_found = True
                        param_value = ga.address
                        break  # stop group address search
                    elif ga.dpt in param["dpts"]:
                        param_found = True
                        param_value = ga.address
                        break  # stop group address search
                    else:
                        logging.warning(f"Incompatible DPT type for parameter {param["name"]} found in GA '{ga.name}'. Have {ga.dpt} but expect {param["dpts"]}")
                        break  # stop group address search
            if param_found: #if parameter has not been found
                setattr(self, param["name"], param_value)  # set the attribute
            else:
                if param["required"]:
                    logging.warning(f"Parameter {param["name"]} not found in function {function.name}")
                    return None
                else:
                    logging.info(f"Parameter {param["name"]} not found in function {function.name}")
                    if not hasattr(self, param["name"]):
                        setattr(self, param["name"], None)

    def set_from_dict(self, params: dict):
        self.from_dict(params)

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
