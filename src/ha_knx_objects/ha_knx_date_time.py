from ha_knx_objects_common import HAKNXDevice, KNXDeviceParameterType
from knx_project_objects import KNXDPTType
from knx_utils import Quoted

# pylint: disable=R0801

class HAKNXDateTime(HAKNXDevice):
    keyname = 'datetime'
    keywords = ['datetime', 'dateheure', 'fulltime', 'tempscomplet']
    parameters = [
        {
            'name': 'address',
            'required': True,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(19,1)
                ],
                'keywords': keywords
            },
            'param_class': Quoted
        },
        {
            'name': 'state_address',
            'required': False,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(19,1)
                ],
                'keywords': ['etat', 'status']
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
