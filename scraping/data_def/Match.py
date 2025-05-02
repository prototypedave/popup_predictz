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
# PlayerData
# ========================================================

# PlayerData  -> Data Class
# interp. represents player data
#     name -> str
#     position -> str
#     team -> str
#     nationality -> str
#     date_of_birth -> str

@dataclass
class PlayerData:
    name: str
    position: str
    team: str
    nationality: str
    date_of_birth: str


# =========================================================
# GoalData
# =========================================================

# GoalData  -> Data Class
# interp. represents goal scored data
#     scorer -> PlayerData
#     assist -> PlayerData
#     penalty -> bool

@dataclass
class GoalData:
    scorer: PlayerData
    assist: Optional[PlayerData] = None
    penalty: bool = False


# =========================================================
# CardData
# =========================================================

# CardData  -> Data Class
# interp. represents card awarded data
#     player -> PlayerData
#     card_type -> str

@dataclass
class CardData:
    player: PlayerData
    card_type: str


# =========================================================
# SubstitutionData
# =========================================================

# SubstitutionData  -> Data Class
# interp. represents substitution made
#     player_out -> PlayerData
#     player_in -> PlayerData

@dataclass
class SubstitutionData:
    player_out: PlayerData
    player_in: PlayerData


# =========================================================
# InjuredData
# =========================================================

# InjuredData -> Data Class
# interp. represents a dict of players missing in a given match
#       player: PlayerData
#       reason: str

@dataclass
class InjuredData:
    player: PlayerData
    reason: str


# =========================================================
# MissingPlayersData
# =========================================================

# MissingPlayersData  -> Data Class
# interp. represents a list of players (InjuredData) that will not play a given match
#       injured: List[InjuredData]

@dataclass
class MissingPlayersData:
    home: Optional[InjuredData] = field(default_factory=list)
    away: Optional[InjuredData] = field(default_factory=list)


# =========================================================
# IncidentData
# =========================================================

# IncidentData  -> Data Class
# interp. represents match incident data at a given time during the match
#     time -> int
#     one of:
#         - goal -> GoalData
#         - card -> CardData
#         - substitution -> SubstitutionData

@dataclass
class IncidentData:
    time: int
    goal: Optional[GoalData] = None
    card: Optional[CardData] = None
    substitution: Optional[SubstitutionData] = None


# ========================================================
# GameIncidents
# ========================================================

# GameIncidents -> Data Class
# interp. represents full time match report of incidents
#       home -> List[IncidentData]
#       away -> List[IncidentData]

@dataclass
class GameIncidents:
    home: List[IncidentData] = field(default_factory=list)
    away: List[IncidentData] = field(default_factory=list)