from datetime import datetime


# This file is part of the Football Data API project.

# ========================================================
# Format score of a match into meaningful data
# parse_score: (score_text: str) -> tuple
# interp. parse_score takes a string representation of a score and returns a tuple representing the home and away scores

def parse_score(score_text: str):
    lines = score_text.strip().splitlines()
    
    if len(lines) == 3:
        home_raw, dash, away_raw = lines
    elif len(lines) == 1 and lines[0] == "-":
        return None, None
    else:
        # fallback for unexpected format
        return None, None

    home_score = int(home_raw) if home_raw.isdigit() else None
    away_score = int(away_raw) if away_raw.isdigit() else None
    return home_score, away_score


# =========================================================
# Format list details into an object
# parse_list_details: (details: list) -> dict
# Given two lists with referee, stadium and capacity information
# returns a dictionary with the information

def parse_list_details(keys: list, values: list) -> dict:
    result = {}
    i = 0 

    for key in keys:
        cleaned_key = key.rstrip(':')
        # If the key is "referee" or "venue", concatenate 2 items
        if cleaned_key in ('referee', 'venue'):
            if i + 1 < len(values):
                result[cleaned_key] = values[i] + ' ' + values[i + 1]
                i += 2
            else:
                result[cleaned_key] = values[i] 
                i += 1
        else:
            # Just take the next value
            if i < len(values):
                result[cleaned_key] = values[i]
                i += 1

    return result


# ===============================================================
# Format date into weather api format DD-MM-YYYY
# parse_date_dd_mm_yyyy: (str) -> tuple(str, str)
# given a string of date and time return a tuple strings containing date in the format DD-MM-YYYY and time HH:MM

def parse_date_dd_mm_yyyy(input_str: str) -> tuple:
    try:
        dt = datetime.strptime(input_str, "%d.%m.%Y %H:%M")
        date_str = dt.strftime("%Y-%m-%d")
        hour = dt.hour
        return date_str, hour
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {input_str}") from e


# ==============================================================
# Split a string into two parts based on a hyphen
# split_string: (str) -> tuple
# interp. split_string takes a string and splits it into two parts based on the first hyphen found

def split_string(input_str: str) -> tuple:
    parts = [p.strip() for p in input_str.split(" - ")]
    if len(parts) == 2:
        return parts[0], parts[1]
    elif len(parts) == 3:
        return parts[0], parts[1] + " - " + parts[2]
    else:
        return parts[0], None