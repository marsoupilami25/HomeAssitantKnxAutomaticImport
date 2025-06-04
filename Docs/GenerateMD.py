from typing import List

from HAKNXObjectCreator.HAKNXDevice import HAKNXDevice, KNXDeviceParameterType
from HAKNXObjectCreator.HAKNXFactory import HAKNXFactory
from HAKNXObjectCreator.HAKNXValueType import HAKNXValueType

markdown = ""

def entity_header():
    global markdown
    markdown += "|Entity|keywords|managed configuration variables|\n"
    markdown += "|--|--|--|\n"

def entity_line(ent: HAKNXDevice):
    global markdown
    markdown += f"|{ent.keyname.capitalize()}|"
    for key in ent.keywords:
        markdown += f"{key}<br>"
    markdown += "|"
    for var in ent.parameters:
        markdown += f"{var['name']} ({var['type']})<br>"
    markdown += "|\n"


with open("Docs/description.md", "r") as file:
    markdown = file.read()

markdown += "\n"
markdown += "## Entities\n"
markdown += "This section identifies the [Home Assistant KNX integration](https://www.home-assistant.io/integrations/knx/) entities that are currently managed by HomeAssistantKNXAutomaticImport.\n"
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
                    markdown += (f"{dpt}: ")
                    markdown += (f"{vt.type}<br>")
                markdown += "|\n"
    if 'RtR' in types:
        markdown += "#### Response to Read (RtR) configuration variables\n"
        markdown += "|configuration variables|required|associated GA|\n"
        markdown += "|--|--|--|\n"
        for var in entity.parameters:
            if var['type'] == KNXDeviceParameterType.RtR:
                markdown += f"|{var['name']}"
                markdown += f"|{var['required']}"
                conf = var['configuration']
                markdown += f"|{conf['param_for_address']}|\n"
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
for key in HAKNXValueType._value_types.keys():
    markdown += f"|{HAKNXValueType._value_types[key]}"
    markdown += f"|{key}|\n"
with open("README.md", "w") as file:
    file.write(markdown)