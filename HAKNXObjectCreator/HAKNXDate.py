from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice, KNXDeviceParameterType
from KNXProjectManagement.KNXDPTType import KNXDPTType
from Utils.Serializable import Quoted


class HAKNXDate(HAKNXDevice):
    keyname = 'date'
    keywords = ['date']
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
            'type': KNXDeviceParameterType.RtR,
            'configuration': {
                'param_for_address': 'address',
                'param_for_state_address': 'state_address'
    },
            'param_class': bool
        }
    ]


