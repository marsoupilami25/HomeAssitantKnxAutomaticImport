from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice, KNXDeviceParameterType
from HAKNXObjectCreator.HAKNXValueType import HAKNXValueType
from KNXProjectManagement.KNXDPTType import KNXDPTType
from Utils.Serializable import Quoted


class HAKNXExpose(HAKNXDevice):
    keyname = 'expose'
    keywords = ['expose', 'update']
    parameters = [
        {
            'name': 'address',
            'required': True,
            'type': KNXDeviceParameterType.GA,
            'configuration': {
                'dpts': [
                KNXDPTType.constructor_from_ints(1,None),
                KNXDPTType.constructor_from_ints(5,None),
                KNXDPTType.constructor_from_ints(6,None),
                KNXDPTType.constructor_from_ints(7,None),
                KNXDPTType.constructor_from_ints(8,None),
                KNXDPTType.constructor_from_ints(9,None),
                KNXDPTType.constructor_from_ints(12,None),
                KNXDPTType.constructor_from_ints(13,None),
                KNXDPTType.constructor_from_ints(14,None),
                KNXDPTType.constructor_from_ints(16,None),
                KNXDPTType.constructor_from_ints(17,None),
                KNXDPTType.constructor_from_ints(29,None),
                KNXDPTType.constructor_from_ints(10,1),
                KNXDPTType.constructor_from_ints(11,1),
                KNXDPTType.constructor_from_ints(19,1)
                ],
                'keywords': []
            }
        },
        {
            'name': 'type',
            'required': True,
            'type': KNXDeviceParameterType.VT,
            'configuration': {
                'param_for_state_address': 'address'
            }
        }
    ]

    address: str
    type: HAKNXValueType

    def to_dict(self):
        produced_dict = {}
        produced_dict["type"] = self.type.__str__()
        # produced_dict["address"] = '\"' + self.address.__str__() + '\" # ' + self.name.__str__()
        produced_dict["address"] = Quoted(self.address.__str__())

        return produced_dict