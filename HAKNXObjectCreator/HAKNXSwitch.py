from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice, KNXDeviceParameterType
from KNXProjectManagement.KNXDPTType import KNXDPTType
from Utils.Serializable import Quoted


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
            'type': KNXDeviceParameterType.RtR,
            'configuration': {
                'param_for_address': 'address'
            },
            'param_class': bool
        }
    ]


