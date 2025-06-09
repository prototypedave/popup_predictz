# Functions to format a digit string

import re

# Remove characters from a digit string
# remove_ambigious_characters: (str) -> str
# interp. remove_ambigious_characters takes a string and removes any characters that are not digits
def get_digit_string(text: str) -> str:
    text = re.sub(r"[%()/]", "", text)
    return text.strip()


# Split a string into three parts based on occurrence of '(', '%', and '/'
# split_string: (str) -> tuple
# interp. split_string takes a string and splits it into three parts based on occurrence of '('
def split_digit(string: str) -> tuple:
    match = re.match(r"(\d+)%\s*\(\s*(\d+)\s*/\s*(\d+)\s*\)", string)
    if match:
        percentage, first_value, second_value = match.groups()
        return percentage.strip(), first_value.strip(), second_value.strip()
    
    match = re.match(r"(\d+)\s*/\s*(\d+)\s*\(\s*(\d+)%\s*\)", string)
    if match:
        first_value, second_value, percentage = match.groups()
        return percentage.strip(), first_value.strip(), second_value.strip()
    
    return None, None, None