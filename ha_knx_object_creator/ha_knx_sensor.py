from ha_knx_object_creator.ha_knx_device import HAKNXDevice, KNXDeviceParameterType
from ha_knx_object_creator.ha_knx_value_type import HAKNXValueType
from knx_project_management.knx_dpt_type import KNXDPTType
from utils.serializable import Quoted

# pylint: disable=R0801

class HAKNXSensor(HAKNXDevice):
    keyname = 'sensor'
    keywords = ['sensor', 'senseur', 'capteur']
    parameters = [
        {
            'name': 'state_address',
            'required': True,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(5,None),
                KNXDPTType.constructor_from_ints(6,None),
                KNXDPTType.constructor_from_ints(7,None),
                KNXDPTType.constructor_from_ints(8,None),
                KNXDPTType.constructor_from_ints(9,None),
                KNXDPTType.constructor_from_ints(12,None),
                KNXDPTType.constructor_from_ints(13,None),
                KNXDPTType.constructor_from_ints(14,None),
                KNXDPTType.constructor_from_ints(16,None),
                KNXDPTType.constructor_from_ints(17,None),
                KNXDPTType.constructor_from_ints(29,None)
                ],
                'keywords': []
            },
            'param_class': Quoted
        },
        {
            'name': 'type',
            'required': True,
            'type': KNXDeviceParameterType.VT,
            'configuration': {
                'param_for_state_address': 'state_address'
            },
            'param_class': HAKNXValueType
        }
    ]
