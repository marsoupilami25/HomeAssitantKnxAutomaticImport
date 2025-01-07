from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice, KNXDeviceParameterType
from KNXProjectManagement.KNXDPTType import KNXDPTType


class HAKNXTime(HAKNXDevice):
    keyname = 'time'
    keywords = ['time', 'heure']
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
            }
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
            }
        },
        {
            'name': 'respond_to_read',
            'required': False,
            'type': KNXDeviceParameterType.RtR,
            'configuration': {
                'param_for_address': 'address'
            }
        }
    ]

    address: str
    state_address: str
    respond_to_read: bool

