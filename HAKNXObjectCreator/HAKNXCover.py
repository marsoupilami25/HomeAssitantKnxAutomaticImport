from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice, KNXDeviceParameterType
from KNXProjectManagement.KNXDPTType import KNXDPTType


class HAKNXCover(HAKNXDevice):
    keyname = 'cover'
    keywords = ['cover', 'volet roulant', 'volet']
    parameters = [
        {
            'name': 'move_long_address',
            'required': False,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(1,None)
                ],
                'keywords': ['haut&bas', 'up&down', 'move_long', 'move long']
            }
        },
        {
            'name': 'move_short_address',
            'required': False,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(1, None)
                ],
                'keywords': ['move_short', 'move short']
            }
        },
        {
            'name': 'stop_address',
            'required': False,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                    KNXDPTType.constructor_from_ints(1, None)
                ],
                'keywords': ['stop', 'arret']
            }
        },
        {
            'name': 'position_address',
            'required': False,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                    KNXDPTType.constructor_from_ints(5,1)
                ],
                'keywords': ['position (fixer)', 'position (set)']
            }
        },
        {
            'name': 'position_state_address',
            'required': False,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                    KNXDPTType.constructor_from_ints(5, 1)
                ],
                'keywords': ['position (etat)', 'position state', 'position (state)']
            }
        }
    ]

    move_long_address: str
    move_short_address: str
    stop_address: str
    position_address: str
    position_state_address: str

