from datetime import datetime


# This file is part of the Football Data API project.

# ========================================================
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


# =========================================================
# Format list details into an object
# parse_list_details: (details: list) -> dict
# Given two lists with referee, stadium and capacity information
#       returns a dictionary with the information

def parse_list_details(keys: list, values: list) -> dict:
    result = {}
    i = 0 

    for key in keys:
        cleaned_key = key.rstrip(':')
        if cleaned_key in ('referee', 'venue'):
            if i + 1 < len(values):
                result[cleaned_key] = values[i] + ' ' + values[i + 1]
                i += 2
            else:
                result[cleaned_key] = values[i] 
                i += 1
        else:
            if i < len(values):
                result[cleaned_key] = values[i]
                i += 1

    return result


# ===============================================================
# Format date into weather api format DD-MM-YYYY
# parse_date_dd_mm_yyyy: (str) -> tuple(str, str)
# given a string of date and time (DDMMYYYY HHMM) return a tuple strings containing 
#       date in the format DD-MM-YYYY and time HH:MM

def parse_date_dd_mm_yyyy(input_str: str) -> tuple:
    try:
        dt = datetime.strptime(input_str, "%d.%m.%Y %H:%M")
        date_str = dt.strftime("%Y-%m-%d")
        time = dt.strftime("%H:%M")
        return date_str, time
    except ValueError as e:
        return None, None


# ==============================================================
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