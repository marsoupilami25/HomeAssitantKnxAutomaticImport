import logging
from typing import cast

from ruamel.yaml import CommentedMap
from ruamel.yaml.scalarbool import ScalarBoolean
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice, KNXDeviceParameterType
from HAKNXObjectCreator.HAKNXValueType import HAKNXValueType
from KNXProjectManagement.KNXDPTType import KNXDPTType

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
        },
        {
            'name': 'respond_to_read',
            'required': False,
            'type': KNXDeviceParameterType.RtR,
            'configuration': {
                'param_for_address': 'address'
            }
        }
    ]

    address: str
    type: HAKNXValueType
    respond_to_read: bool

    @classmethod
    def to_yaml(cls, representer, node):
        node = cast(HAKNXExpose, node)
        if (node.name is None) or (node.name == ''):
            raise ValueError(f"The object {node} shall have a name")
        produced_dict = CommentedMap()
        produced_dict["type"] = node.type.__str__()
        produced_dict.yaml_add_eol_comment(f"{node.name}", key = 'type')
        produced_dict["address"] = DoubleQuotedScalarString(node.address.__str__())
        produced_dict["respond_to_read"] = ScalarBoolean(node.respond_to_read)
        output_node = representer.represent_mapping('tag:yaml.org,2002:map', produced_dict)
        return output_node

    def from_dict(self, dict_obj: CommentedMap):
        super().from_dict(dict_obj)
        comment = dict_obj.ca.items['type']
        comment_found = False
        value = None
        if comment is not None:
            for element in comment:
                if element is not None:
                    comment_found = True
                    value = element.value
        if comment_found:
            self.name = value.replace("# ","").strip()
        else:
            logging.warning(f"No name found in a comment for the object {self}. Default name used")
            self.name = self.__class__.__name__