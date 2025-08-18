from ha_knx_object_creator.ha_knx_device import HAKNXDevice, KNXDeviceParameterType
from knx_project_management.knx_dpt_type import KNXDPTType
from utils.serializable import Quoted

# pylint: disable=R0801

class HAKNXLight(HAKNXDevice):
    keyname = 'light'
    keywords = ['light', 'lumiere']
    parameters = [
        {
            'name': 'address',
            'required': True,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(1,1)
                ],
                'keywords': ['on', 'off', 'switch']
            },
            'param_class': Quoted
        },
        {
            'name': 'state_address',
            'required': False,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(1,1)
                ],
                'keywords': ['etat', 'state']
            },
            'param_class': Quoted
        }
    ]
