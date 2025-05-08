from typing import NewType, Optional
from datetime import datetime
from dataclasses import dataclass, field

Natural = NewType('Natural', int)

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


# ===============================================================
# Missing Player - info on a player that will not play
# ===============================================================

# MissingPlayer is Dict
# interp. data class representing data for absent players in a match

@dataclass
class MissingPlayer:
    player: Player                          # Player
    reason: Optional[str]                   # purpose of missing the match


# =============================================================
# Match Summary - all general information for a given match
# =============================================================

# MatchSummary is Dict
# interp. data class to represent match summary data

@dataclass
class MatchSummary:
    competition: str                                                            # Country or competition of the match
    league: str                                                                 # Tier of the competition
    round: str                                                                  # The level the competition is in
    home: str                                                                   # Home team
    away: str                                                                   # Away team
    home_score: str                                                             # Home team score
    away_score: str                                                             # Away team score
    date: datetime                                                              # Time and date the match played
    absent_home_players: list[MissingPlayer] = field(default_factory=list)      # Home team missing players
    absent_away_players: list[MissingPlayer] = field(default_factory=list)      # Away team missing players
    referee: Optional[str] = None                                               # Referee name
    venue: Optional[str] = None                                                 # Match venue
    capacity: Optional[Natural] = None                                          # Attendance or stadium capacity 