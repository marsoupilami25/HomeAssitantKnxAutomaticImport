import logging
from turtledemo.sorting_animate import start_ssort

from HAKNXObjectCreator.HAKNXObject import HAKNXObject
from KNXProjectManagement.KNXFunction import KNXFunction
from KNXProjectManagement.KNXGroupAddress import KNXGroupAddress
from KNXProjectManagement.KNXProjectManager import knx_project_manager


class light(HAKNXObject):
    keywords = ['light', 'lumiere']
    parameters = {
        'address' : ['on', 'off', 'switch'],
        'state_address': ['etat', 'state']
    }

    address: str
    state_address: str

