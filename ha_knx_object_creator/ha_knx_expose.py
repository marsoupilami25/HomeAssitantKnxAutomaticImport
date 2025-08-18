import logging

from ruamel.yaml import CommentedMap

from ha_knx_object_creator.ha_knx_device import HAKNXDevice, KNXDeviceParameterType
from ha_knx_object_creator.ha_knx_value_type import HAKNXValueType
from knx_project_management.knx_dpt_type import KNXDPTType
from utils.serializable import Quoted

# pylint: disable=R0801

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
            },
            'param_class': Quoted
        },
        {
            'name': 'type',
            'required': True,
            'type': KNXDeviceParameterType.VT,
            'configuration': {
                'param_for_state_address': 'address'
            },
            'param_class': HAKNXValueType
        },
        {
            'name': 'respond_to_read',
            'required': False,
            'type': KNXDeviceParameterType.RTR,
            'configuration': {
                'param_for_address': 'address',
                'param_for_state_address': None

    },
            'param_class': bool
        }
    ]

    def to_yaml(self, representer):
        if (self.name is None) or (self.name == ''):
            raise ValueError(f"The object {self} shall have a name")
        intermediate_mapping = self.pre_convert()
        intermediate_mapping.pop('name')
        key='type'
        if key in intermediate_mapping.ca.items:
            intermediate_mapping.ca.items.pop(key)
        intermediate_mapping.yaml_add_eol_comment(f"!DO NOT REMOVE!{self.name}", key = key)
        output_node = representer.represent_mapping('tag:yaml.org,2002:map', intermediate_mapping)
        return output_node

    def from_dict(self, dict_obj: CommentedMap):
        comment = dict_obj.ca.items['type']
        comment_found = False
        value = None
        if comment is not None:
            for element in comment:
                if element is not None:
                    comment_found = True
                    value = element.value
        if comment_found:
            dict_obj['name'] = value.replace("# !DO NOT REMOVE!","").strip()
        else:
            logging.warning("No name found in a comment for the object %s. Default name used",
                            self)
            dict_obj['name'] = self.__class__.__name__
        super().from_dict(dict_obj)
