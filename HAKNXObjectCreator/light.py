import logging
from turtledemo.sorting_animate import start_ssort

from HAKNXObjectCreator.HAKNXObject import HAKNXObject

class light(HAKNXObject):
    keywords = ['light', 'lumiere']
    parameters = {
        'address' : ['on', 'off', 'switch'],
        'state_address': ['etat', 'state']
    }

    address: str
    state_address: str

