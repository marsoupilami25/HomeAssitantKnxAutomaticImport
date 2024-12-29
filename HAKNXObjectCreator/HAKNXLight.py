from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice
from KNXProjectManagement.KNXDPTType import KNXDPTType


class HAKNXLight(HAKNXDevice):
    keyname = 'light'
    keywords = ['light', 'lumiere']
    parameters = [
        {
            'name': 'address',
            'required': True,
            'dpts': [
                KNXDPTType.constructor_from_ints(1,1)
            ],
            'keywords': ['on', 'off', 'switch']
        },
        {
            'name': 'state_address',
            'required': False,
            'dpts': [
                KNXDPTType.constructor_from_ints(1,1)
            ],
            'keywords': ['etat', 'state']
        }
    ]

    address: str
    state_address: str

