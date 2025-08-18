from ha_knx_object_creator.ha_knx_device import HAKNXDevice, KNXDeviceParameterType
from knx_project_management.knx_dpt_type import KNXDPTType
from utils.serializable import Quoted

# pylint: disable=R0801

class HAKNXSwitch(HAKNXDevice):
    keyname = 'switch'
    keywords = ['switch', 'commutateur', 'prise', 'interrupteur', 'socket']
    parameters = [
        {
            'name': 'address',
            'required': True,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(1,None)
                ],
                'keywords': ['on', 'off', 'switch', 'commutation']
            },
            'param_class': Quoted
        },
        {
            'name': 'state_address',
            'required': False,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(1,None)
                ],
                'keywords': ['etat', 'state', 'statut']
            },
            'param_class': Quoted
        },
        {
            'name': 'respond_to_read',
            'required': False,
            'type': KNXDeviceParameterType.RTR,
            'configuration': {
                'param_for_address': 'address',
                'param_for_state_address': 'state_address'
            },
            'param_class': bool
        }
    ]
