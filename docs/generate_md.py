from typing import List

from hakai_packages.ha_knx_objects_common.ha_knx_device import HAKNXDevice, KNXDeviceParameterType
from hakai_packages.ha_knx_objects_factory import HAKNXFactory
from hakai_packages.ha_knx_objects_common.ha_knx_value_type import HAKNXValueType

markdown : str = ""

def entity_header():
    global markdown # pylint: disable=global-statement
    markdown += "|Entity|keywords|managed configuration variables|\n"
    markdown += "|--|--|--|\n"

def entity_line(ent: HAKNXDevice):
    global markdown # pylint: disable=global-statement
    markdown += f"|{ent.keyname.capitalize()}|"
    for loc_key in ent.keywords:
        markdown += f"{loc_key}<br>"
    markdown += "|"
    for loc_var in ent.parameters:
        markdown += f"{loc_var['name']} ({loc_var['type']})<br>"
    markdown += "|\n"


with open("docs/description.md", "r", encoding="utf-8") as file:
    markdown += file.read()

markdown += "\n"
markdown += "## Entities\n"
markdown += ("This section identifies the "
             "[Home Assistant KNX integration](https://www.home-assistant.io/integrations/knx/) "
             "entities that are currently managed by HomeAssistantKNXAutomaticImport.\n")
markdown += "\n"
entity_header()
for entity in HAKNXFactory.ha_knx_objects_list:
    entity_line(entity)

for entity in HAKNXFactory.ha_knx_objects_list:
    markdown += f"### {entity.keyname.capitalize()}\n"
    entity_header()
    entity_line(entity)
    types : List[str] = []
    for var in entity.parameters:
        element = var['type'].name
        types.append(element)
    if 'GA' in types:
        markdown += "#### Group Address (GA) configuration variables\n"
        markdown += "|configuration variables|required|keywords|accepted DPT|\n"
        markdown += "|--|--|--|--|\n"
        for var in entity.parameters:
            if var['type'] == KNXDeviceParameterType.GA:
                markdown += f"|{var['name']}"
                markdown += f"|{var['required']}"
                conf = var['configuration']
                markdown += "|"
                for key in conf['keywords']:
                    markdown += f"{key}<br>"
                markdown += "|"
                for dpt in conf['dpts']:
                    vt = HAKNXValueType()
                    vt.dpt = dpt
                    markdown += f"{dpt}: "
                    markdown += f"{vt.type}<br>"
                markdown += "|\n"
    if 'RTR' in types:
        markdown += "#### Response to Read (RtR) configuration variables\n"
        markdown += "|configuration variables|required|associated GA|state GA|\n"
        markdown += "|--|--|--|--|\n"
        for var in entity.parameters:
            if var['type'] == KNXDeviceParameterType.RTR:
                markdown += f"|{var['name']}"
                markdown += f"|{var['required']}"
                conf = var['configuration']
                markdown += f"|{conf['param_for_address']}"
                markdown += f"|{conf['param_for_state_address']}|\n"
    if 'VT' in types:
        markdown += "#### Value Type (VT) configuration variables\n"
        markdown += "|configuration variables|required|associated GA|\n"
        markdown += "|--|--|--|\n"
        for var in entity.parameters:
            if var['type'] == KNXDeviceParameterType.VT:
                markdown += f"|{var['name']}"
                markdown += f"|{var['required']}"
                conf = var['configuration']
                markdown += f"|{conf['param_for_state_address']}|\n"
markdown += "\n"
markdown += "## Data Point Types\n"
markdown += "This section described the Data Point Types supported by the tool.\n"
markdown += "\n"
markdown += "|Data Points|Type|\n"
markdown += "|--|--|\n"
for key, value in HAKNXValueType._value_types.items(): # pylint: disable=protected-access
    markdown += f"|{value}"
    markdown += f"|{key}|\n"

with open("docs/versions.md", "r", encoding="utf-8") as file:
    markdown += file.read()

with open("README.md", "w", encoding="utf-8") as file:
    file.write(markdown)
