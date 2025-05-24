# Helper functions
from datetime import datetime, timedelta
import re

# Split a string into two parts based on a hyphen
# split_string: (str) -> tuple
# interp. split_string takes a string and splits it into two 
#       parts based on the first hyphen found

def split_string(input_str: str) -> tuple:
    parts = [p.strip() for p in input_str.split(" - ")]
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) == 3:
        return parts[0], parts[1] + " - " + parts[2]
    else:
        return parts[0], None


# Format score of a match into meaningful data
# parse_score: (score_text: str) -> tuple
# interp. parse_score takes a string representation of a score and returns a tuple 
#         representing the home and away scores, returns None if the score is not valid

def parse_score(score_text: str):
    lines = score_text.strip().splitlines()

    if len(lines) == 3:
        home_raw, dash, away_raw = lines
        home_score = int(home_raw) if home_raw.isdigit() else None
        away_score = int(away_raw) if away_raw.isdigit() else None

        if home_score is not None and away_score is not None:
            return home_score, away_score

    return None, None


# Format bracket string into a string
# parse_bracket: (str) -> str
# interp. parse_bracket removes brackets from a string and returns the cleaned string

def parse_bracket(text: str) -> str:
    match = re.match(r"\((.*?)\)", text.strip())
    return match.group(1) if match else text


# Return True or False if time is 2 hours and earlier from now
# is_past_two_hours: (datetime) -> bool
# produce true if its past else false

def is_past_two_hours(time: datetime) -> bool:
    check_time = datetime.now() - timedelta(hours=2)
    return time <= check_time


# Check for required url
# is_valid_url: (str, str) -> bool
# interp. is_valid_url checks if a given url has the required destination and returns 
#         true if it does, else false
def is_valid_url(url: str, destination: str) -> bool:
    return url.find(destination) != -1


# Assemble url to the required page
# assemble_url: (str, str) -> str
# interp. assemble_url takes a base url removes any text and adds a destination and returns the full url
def assemble_url(base_url: str, remove: str, destination: str) -> str:
    base_url = base_url.replace(remove, "", 1)
    return f"{base_url}/{destination}"


# Remove characters from a digit string
# remove_ambigious_characters: (str) -> str
# interp. remove_ambigious_characters takes a string and removes any characters that are not digits
def remove_ambigious_characters(text: str) -> str:
    text = re.sub(r"[%()/]", "", text)
    return text.strip()


# Split a string into three parts based on occurrence of '(', '%', and '/'
# split_string: (str) -> tuple
# interp. split_string takes a string and splits it into three parts based on occurrence of '('
def split_string(string: str) -> tuple:
    match = re.match(r"(\d+)%\s*\(\s*(\d+)\s*/\s*(\d+)\s*\)", string)
    if match:
        percentage, first_value, second_value = match.groups()
        return percentage.strip(), first_value.strip(), second_value.strip()
    
    match = re.match(r"(\d+)\s*/\s*(\d+)\s*\(\s*(\d+)%\s*\)", string)
    if match:
        first_value, second_value, percentage = match.groups()
        return percentage.strip(), first_value.strip(), second_value.strip()
    
    return None, None, None


# Split strings into two if they contain an hyphen and the next string starts with a capital letter
# split_capital_string: (str) -> tuple
# interp. split_capital_string takes a string and splits it into two parts based on the first occurrence of '.'
#         if the next string starts with a capital letter
def split_capital_string(string: str) -> tuple:
    string = re.sub(r'\.(?!\s|$)', '. ', string)
    string = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', string)
    string = re.sub(r'\s+', ' ', string).strip()
    parts = string.split(". ")
    if len(parts) >= 2:
        last_part = parts[-1]
        first_part = "".join(parts[:-1])
        return first_part.strip(), last_part.strip()
    return string.strip(), ""


# Seperate and remove merged (copy of original) text based on the merged text starting with capital letter
# remove_duplicate_strings: (str) -> str
# interp. seperates and returns only one string from the duplicated string
def remove_duplicate_strings(string: str) -> str:
    return re.sub(r'(.+?)\1', r'\1', string).strip()
    