from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice

class HAKNXLight(HAKNXDevice):
    keyname = 'light'
    keywords = ['light', 'lumiere']
    parameters = [
        {
            'name': 'address',
            'required': True,
            'keywords': ['on', 'off', 'switch']
        },
        {
            'name': 'state_address',
            'required': False,
            'keywords': ['etat', 'state']
        }
    ]

    address: str
    state_address: str

