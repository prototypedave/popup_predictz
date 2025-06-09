# All helper functions for formating strings

# Split a string into two parts based on a hyphen
# split_string: (str) -> tuple
# interp. split_string takes a string and splits it into two 
#       parts based on the first hyphen found

def split_string_with_hyphen(input_str: str) -> tuple:
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

def split_score_string(score_text: str):
    scores = score_text.split("-")
    if len(scores) == 2:
        home_raw, away_raw = scores
        home_score = int(home_raw) if home_raw.isdigit() else None
        away_score = int(away_raw) if away_raw.isdigit() else None

        if home_score is not None and away_score is not None:
            return home_score, away_score

    return None, None
