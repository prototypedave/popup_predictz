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


# Split a string into three parts based on the first occurrence of '('
# split_string: (str) -> tuple
# interp. split_string takes a string and splits it into three parts based on the first occurrence of '('
def split_string(string: str) -> tuple:
    parts = string.split( "(")  
    if len(parts) == 2:
        parts[1] = parts[1].split("/")
        parts[1] = [remove_ambigious_characters(part) for part in parts[1]]
        parts[0] = remove_ambigious_characters(parts[0])
        return parts[0], parts[1][0], parts[1][1]
    return None