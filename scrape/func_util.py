# Helper functions
from datetime import datetime, timedelta

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