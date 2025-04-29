from dataclasses import dataclass, field
from typing import Optional, List

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


# ========================================================
# PlayerName
# ========================================================

# PlayerName  -> Data Class
# interp. PlayerName represents a player's name

@dataclass
class PlayerName:
    full_name: str                          # Player's full name
    position: Optional[str] = None          # Player's position


# ========================================================
# GoalInfoData
# ========================================================

# GoalInfoData  -> Data Class
# interp. GoalInfoData represents information about a goal in a match
#     Scorer -> PlayerName
#     Assist -> PlayerName
#     Penalty -> bool

@dataclass
class GoalInfoData:
    scorer: PlayerName                      # Player who scored the goal
    assist: Optional[PlayerName] = None     # Player who assisted the goal
    penalty: bool = False                   # Whether the goal was a penalty


# ========================================================
# SubstitutionData
# ========================================================

# SubstitutionData  -> Data Class
# interp. SubstitutionData represents information about substitution made player in and player out
#     player_in -> PlayerName
#     player_out -> PlayerName

@dataclass
class SubstitutionData:
    player_in: PlayerName                   # Player subbed in
    player_out: PlayerName                  # Player subbed out


# ========================================================
# CardInfoData
# ========================================================

# CardInfoData  -> Data Class
# interp. CardInfoData represents type of card given to a player
#     yellow_card -> bool
#     red_card -> bool
#     player -> PlayerName

@dataclass
class CardInfoData:
    yellow_card: bool                       # Whether a yellow card was given
    red_card: bool                          # Whether a red card was given
    player: PlayerName                      # Player who received the card


# ========================================================
# MatchIncident
# ========================================================

# MatchIncident  -> Data Class
# interp. represents information about a match incident
#     time -> int
#     yellow_card -> PlayerName
#     red_card -> PlayerName
#     substitution -> SubstitutionData
#     goal -> GoalInfoData

@dataclass
class MatchIncident:
    time: int                               
    card: Optional[CardInfoData] = None
    substitution: Optional[SubstitutionData] = None
    goal: Optional[GoalInfoData] = None


# =======================================================
# FullTimeData
# =======================================================

# FullTimeData  -> Data Class
# interp. represents full time match incidents
#     home_incidents -> list
#     away_incidents -> list

@dataclass
class FullTimeData:
    home_incidents: List[MatchIncident] = field(default_factory=list)
    away_incidents: List[MatchIncident] = field(default_factory=list)