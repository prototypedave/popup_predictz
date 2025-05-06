from typing import NewType, Optional
from datetime import datetime
from dataclasses import dataclass

Natural = NewType('Natural', int)

# ==============================================================
# Game info - match summary
# ==============================================================

# GameInfo is Dict
# interp. a data class representing game information

@dataclass
class GameInfo:
    league: str                             # League name
    country: str                            # Country name
    round: str                              # Competition round
    home: str                               # Home team name
    away: str                               # Away team name
    date: datetime                          # Date and time of the match
    home_score: Optional[Natural] = None    # Home team score
    away_score: Optional[Natural] = None    # Away team score
    referee: Optional[str] = None           # Referee name
    venue: Optional[str] = None             # Match venue
    capacity: Optional[Natural] = None      # Attendance or stadium capacity


# ================================================================
# Player data - player details
# ================================================================

# Player is Dict
# interp. information about a player

@dataclass
class Player:
    name: str                               # Name of the player
    position: str                           # Position where the player plays eg forward
    team: str                               # Current team the player plays at
    dob: str                                # Date of birth
    nationality: str                        # Country of origin


# ==============================================================
# Goal info -  match report on goal data
# ==============================================================

# GoalInfo is Dict
# interp. data class representing data for a goal scored

@dataclass
class GoalInfo:
    scorer: Player                          # Player
    time: str                               # Minute the goal was scored
    assist: Optional[str]                   # Player
    goal_type: Optional[str]                # Type of goal 


# ===============================================================
# Substitution info - match report on substitution made
# ===============================================================

# SubInfo is Dict
# interp. data class representing data for substitution made

@dataclass
class SubInfo:
    player_in: Player                       # Player
    player_out: Player                      # Player
    time: str                               # Minute the sub was made
    reason: Optional[str]                   # Reason the sub was made


# ================================================================
# Card Info - match report on a card given
# ================================================================

# CardInfo is Dict
# interp. data class representing data for cards awarded for offence

@dataclass
class CardInfo:
    player: Player                          # Player
    card_type: str                          # Either yellow or red
    time: str                               # Minute of the infringement
    reason: Optional[str]                   # Infringement 



