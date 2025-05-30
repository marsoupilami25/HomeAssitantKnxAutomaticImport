from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice, KNXDeviceParameterType
from KNXProjectManagement.KNXDPTType import KNXDPTType
from Utils.Serializable import Quoted


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
            }
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
            }
        }
    ]

    address: Quoted
    state_address: Quoted

