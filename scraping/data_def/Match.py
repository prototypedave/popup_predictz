from dataclasses import dataclass
from typing import Optional

# ========================================================
# MatchInfo
# ========================================================

# MatchInfo  -> Data Class
# interp. MatchInfo represents information about a sports match

@dataclass
class MatchInfo:
    home_team: str                          # Home team name
    away_team: str                          # Away team name
    match_time: str                         # Match time
    referee: str                            # Referee name
    venue: str                              # Venue name
    league: str                             # League name
    game_round: str                         # Game round
    capacity: Optional[int] = None          # Venue capacity
    weather: Optional[str] = None           # Weather conditions
    home_score: Optional[int] = None        # Home team score
    away_score: Optional[int] = None        # Away team score