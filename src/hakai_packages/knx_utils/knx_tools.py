from hakai_packages.hakai_conf import HAKAIConfiguration

def knx_flat_string(string : str) -> str:
    return string.lower()

def knx_transformed_string(string : str) -> str:
    new_char = HAKAIConfiguration.get_instance().replace_spaces
    string = knx_flat_string(string)
    if new_char == ' ':
        return string
    if new_char == '/':
        return string.replace(' ', '')
    return string.replace(' ', new_char)
