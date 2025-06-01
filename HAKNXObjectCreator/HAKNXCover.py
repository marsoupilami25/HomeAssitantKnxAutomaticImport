from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice, KNXDeviceParameterType
from KNXProjectManagement.KNXDPTType import KNXDPTType
from Utils.Serializable import Quoted


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
            },
            'param_class': Quoted
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
            },
            'param_class': Quoted
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
            },
            'param_class': Quoted
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
            },
            'param_class': Quoted
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
            },
            'param_class': Quoted
        }
    ]

