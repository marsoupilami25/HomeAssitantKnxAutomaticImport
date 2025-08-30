import re

from ruamel.yaml import CommentToken

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

def knx_remove_escape_comments(string : str) ->str :
    # regex explanation:
    # \s*   => zero or more spaces
    # #&    => literal "#&"
    # .*    => everything until...
    # (?:\n|$) => newline OR end of string
    pattern = r"\s*#&.*(?:\n|$)"
    return re.sub(pattern, "", string)

def knx_update_comment_token(comment : CommentToken) -> bool:
    if comment is None:
        return True
    comment.value = knx_remove_escape_comments(comment.value)
    if comment.value == "":
        return True
    return False

def is_empty_or_none_list(lst):
    # Check if list is empty or all elements are None/empty lists
    if (not isinstance(lst, list)) or (not lst):
        return False
    return not lst or all(
        (x is None) or (isinstance(x, list) and not x) for x in lst
    )

def knx_update_comment_list(comment_list : list) -> bool:
    if comment_list:
        for index, comment_sublist in enumerate(comment_list):
            if comment_sublist:
                elements_to_remove = []
                if isinstance(comment_sublist, CommentToken):
                    if knx_update_comment_token(comment_sublist):
                        comment_list[index] = None
                else:
                    comment: CommentToken
                    for comment in comment_sublist:
                        if knx_update_comment_token(comment):
                            elements_to_remove.append(comment)
                    for comment in elements_to_remove:
                        comment_sublist.remove(comment)
    if is_empty_or_none_list(comment_list):
        return False
    return True

def knx_build_string(content: str, fill_char: str = " ", final_char: str = "#", total_length: int = 100) -> str:
    # Trim content if it's too long
    trimmed = content[:total_length - 1]
    # Pad with chosen character so the length is consistent
    padded = trimmed.ljust(total_length - 1, fill_char)
    # Append final char at fixed position
    return padded + final_char + "\n"