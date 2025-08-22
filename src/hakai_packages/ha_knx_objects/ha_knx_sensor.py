from hakai_packages.ha_knx_objects_common import HAKNXDevice, KNXDeviceParameterType
from hakai_packages.ha_knx_objects_common import HAKNXValueType
from hakai_packages.knx_project_objects import KNXDPTType
from hakai_packages.knx_utils import Quoted

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
