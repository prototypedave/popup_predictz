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


# ==============================================================
# Match Stats - all statistics for a given match
# ==============================================================

# MatchStats is Dict
# interp. data class to represent match statistics data

@dataclass
class MatchStats:
    # Attacking
    xG_home: Optional[float] = None                                         # Expected goals for home team
    xG_away: Optional[float] = None                                         # Expected goals for away team  
    total_shots_home: Optional[int] = None                                  # Total shots for home team
    total_shots_away: Optional[int] = None                                  # Total shots for away team
    shots_on_target_home: Optional[int] = None                              # Shots on target for home team
    shots_on_target_away: Optional[int] = None                              # Shots on target for away team
    big_chances_home: Optional[int] = None                                  # Big chances for home team
    big_chances_away: Optional[int] = None                                  # Big chances for away team
    corners_home: Optional[int] = None                                      # Corners for home team
    corners_away: Optional[int] = None                                      # Corners for away team
    xG_on_target_home: Optional[float] = None                               # Expected goals on target for home team
    xG_on_target_away: Optional[float] = None                               # Expected goals on target for away team
    shots_off_target_home: Optional[int] = None                             # Shots off target for home team
    shots_off_target_away: Optional[int] = None                             # Shots off target for away team
    blocked_shots_home: Optional[int] = None                                # Blocked shots for home team
    blocked_shots_away: Optional[int] = None                                # Blocked shots for away team
    shots_inside_the_box_home: Optional[int] = None                         # Shots inside the box for home team
    shots_inside_the_box_away: Optional[int] = None                         # Shots inside the box for away team
    shots_outside_the_box_home: Optional[int] = None                        # Shots outside the box for home team
    shots_outside_the_box_away: Optional[int] = None                        # Shots outside the box for away team
    woodwork_home: Optional[int] = None                                     # Woodwork for home team
    woodwork_away: Optional[int] = None                                     # Woodwork for away team
    xA_home: Optional[float] = None                                         # Expected assists for home team
    xA_away: Optional[float] = None                                         # Expected assists for away team
    xGOT_faced_home: Optional[float] = None                                 # Expected goals on target faced for home team
    xGOT_faced_away: Optional[float] = None                                 # Expected goals on target faced for away team

    # Game play tactics
    possession_home: Optional[int] = None                                   # Possession for home team
    possession_away: Optional[int] = None                                   # Possession for away team
    touches_in_opposition_home: Optional[int] = None                        # Touches in opposition for home team
    touches_in_opposition_away: Optional[int] = None                        # Touches in opposition for away team
    total_passes_home: Optional[int] = None                                 # Passes for home team
    total_passes_away: Optional[int] = None                                 # Passes for away team
    successful_passes_home: Optional[int] = None                            # Successful passes for home team
    successful_passes_away: Optional[int] = None                            # Successful passes for away team
    passes_percentage_home: Optional[int] = None                            # Passes percentage for home team
    passes_percentage_away: Optional[int] = None                            # Passes percentage for away team
    total_through_passes_home: Optional[int] = None                         # Total through passes for home team
    total_through_passes_away: Optional[int] = None                         # Total through passes for away team
    successful_through_passes_home: Optional[int] = None                    # Successful through passes for home team
    successful_through_passes_away: Optional[int] = None                    # Successful through passes for away team
    through_passes_percentage_home: Optional[int] = None                    # Through passes percentage for home team
    through_passes_percentage_away: Optional[int] = None                    # Through passes percentage for away team 
    total_long_passes_home: Optional[int] = None                            # Total long passes for home team
    total_long_passes_away: Optional[int] = None                            # Total long passes for away team
    successful_long_passes_home: Optional[int] = None                       # Successful long passes for home team
    successful_long_passes_away: Optional[int] = None                       # Successful long passes for away team
    long_passes_percentage_home: Optional[int] = None                       # Long passes percentage for home team
    long_passes_percentage_away: Optional[int] = None                       # Long passes percentage for away team
    passes_in_final_third_home: Optional[int] = None                        # Passes in final third for home team
    passes_in_final_third_away: Optional[int] = None                        # Passes in final third for away team
    successful_passes_in_final_third_home: Optional[int] = None             # Successful passes in final third for home team
    successful_passes_in_final_third_away: Optional[int] = None             # Successful passes in final third for away team
    passes_in_final_third_percentage_home: Optional[float] = None           # Passes in final third percentage for home team
    passes_in_final_third_percentage_away: Optional[float] = None           # Passes in final third percentage for away team
    total_crosses_home: Optional[int] = None                                # Total crosses for home team
    total_crosses_away: Optional[int] = None                                # Total crosses for away team
    successful_crosses_home: Optional[int] = None                           # Successful crosses for home team
    successful_crosses_away: Optional[int] = None                           # Successful crosses for away team
    crosses_percentage_home: Optional[int] = None                           # Crosses percentage for home team
    crosses_percentage_away: Optional[int] = None                           # Crosses percentage for away team

    # Defensive
    offsides_home: Optional[int] = None                                     # Offsides for home team
    offsides_away: Optional[int] = None                                     # Offsides for away team
    free_kicks_home: Optional[int] = None                                   # Free kicks for home team
    free_kicks_away: Optional[int] = None                                   # Free kicks for away
    throw_ins_home: Optional[int] = None                                    # Throw ins for home team
    throw_ins_away: Optional[int] = None                                    # Throw ins for away
    fouls_home: Optional[int] = None                                        # Fouls for home team
    fouls_away: Optional[int] = None                                        # Fouls for away team
    tackles_home: Optional[int] = None                                      # Tackles for home team
    tackles_away: Optional[int] = None                                      # Tackles for away team
    duels_won_home: Optional[int] = None                                    # Duels won for home team
    duels_won_away: Optional[int] = None                                    # Duels won for away team
    clearances_home: Optional[int] = None                                   # Clearances for home team
    clearances_away: Optional[int] = None                                   # Clearances for away team
    interceptions_home: Optional[int] = None                                # Interceptions for home team
    interceptions_away: Optional[int] = None                                # Interceptions for away team
    errors_leading_to_goal_home: Optional[int] = None                       # Errors leading to goal for home team
    errors_leading_to_goal_away: Optional[int] = None                       # Errors leading to goal for away team
    errors_leading_to_shot_home: Optional[int] = None                       # Errors leading to shot for home team
    errors_leading_to_shot_away: Optional[int] = None                       # Errors leading to shot for away team
    goalkeeper_saves_home: Optional[int] = None                             # Goalkeeper saves for home team
    goalkeeper_saves_away: Optional[int] = None                             # Goalkeeper saves for away team
    goals_prevented_home: Optional[float] = None                            # Goals prevented for home team
    goals_prevented_away: Optional[float] = None                            # Goals prevented for away team
    yellow_cards_home: Optional[int] = None                                 # Yellow cards for home team
    yellow_cards_away: Optional[int] = None                                 # Yellow cards for away team
    red_cards_home: Optional[int] = None                                    # Red cards for home team
    red_cards_away: Optional[int] = None                                    # Red cards for away team
    penalty_home: Optional[int] = None                                    # Penalties for home team
    penalty_away: Optional[int] = None                                    # Penalties for away team


# ==============================================================
# Coach Info - coach data
# ==============================================================

# Coach is Dict
# interp. data class representing data for a coach

@dataclass
class Coach:
    name: str                               # Name of the coach
    team: str                               # Team the coach is managing
    dob: str                                # Date of birth
    country: str                            # Country of origin


# ==============================================================
# Match Lineups - all information for a given match
# ==============================================================

# MatchLineups is Dict
# interp. data class to represent match lineups data

@dataclass
class MatchLineups:
    home_formation: Optional[str] = None                               # Home team formation
    away_formation: Optional[str] = None                               # Away team formation
    home_team_rating: Optional[float] = None                           # Home team rating
    away_team_rating: Optional[float] = None                           # Away team rating
    home_starting: list[Player] = field(default_factory=list)          # Home team starting players
    home_substituted: list[Player] = field(default_factory=list)       # Home team substituted players
    home_substitutes: list[Player] = field(default_factory=list)       # Home team substitutes
    home_missing: list[Player] = field(default_factory=list)           # Home team missing players
    home_coaches: list[Coach] = field(default_factory=list)            # Home team coaches
    home_predicted: list[Player] = field(default_factory=list)         # Home team predicted players
    home_questionable: list[Player] = field(default_factory=list)      # Home team questionable players
    home_will_not_play: list[Player] = field(default_factory=list)     # Home team players that will not play
    away_starting: list[Player] = field(default_factory=list)          # Away team starting players
    away_substituted: list[Player] = field(default_factory=list)       # Away team substituted players
    away_substitutes: list[Player] = field(default_factory=list)       # Away team substitutes
    away_missing: list[Player] = field(default_factory=list)           # Away team missing players
    away_coaches: list[Coach] = field(default_factory=list)            # Away team coaches
    away_predicted: list[Player] = field(default_factory=list)         # Away team predicted players
    away_questionable: list[Player] = field(default_factory=list)      # Away team questionable players
    away_will_not_play: list[Player] = field(default_factory=list)     # Away team players that will not play


# ====================================================================
# General Player Statistics - player statistics data
# ====================================================================

# GenralPlayerStats is Dict
# interp. data class representing general player statistics data

@dataclass
class GeneralPlayerStats:
    player_name: str                          # Name of the player
    position: str                             # Position of the player
    rating: Optional[float] = None            # Player rating
    minutes_played: Optional[int] = None      # Minutes played by the player
    goals: Optional[int] = None               # Goals scored by the player
    assists: Optional[int] = None             # Assists made by the player
    own_goals: Optional[int] = None           # Assists made by the player
    yellow_cards: Optional[int] = None        # Yellow cards received by the player
    red_cards: Optional[int] = None           # Red cards received by the player


# ====================================================================
# GoalKeeping Statistics - goalkeeper statistics data
# ====================================================================

# GoalKeepingStats is Dict
# interp. data class representing goalkeeper statistics data

@dataclass
class GoalKeepingStats:
    player_name: str                          # Name of the goalkeeper
    position: str                             # Default position is goalkeeper
    saves: Optional[int] = None               # Saves made by the goalkeeper
    goals_conceded: Optional[int] = None      # Goals conceded by the goalkeeper
    goals_prevented: Optional[float] = None   # Goals prevented by the goalkeeper
    xGOT_faced: Optional[float] = None        # Expected goals on target faced by the goalkeeper
    punches: Optional[int] = None             # Punches made by the goalkeeper
    throws: Optional[int] = None              # Throws made by the goalkeeper
    act_as_sweeper: Optional[int] = None      # Actions as a sweeper made by the goalkeeper


# ====================================================================
# Defensive Statistics - player defensive statistics data
# ====================================================================

# DefensiveStats is Dict
# interp. data class representing player defensive statistics data

@dataclass
class DefensiveStats:
    player_name: str                                        # Name of the player
    position: str                                           # Position of the player
    total_duels: Optional[int] = None                       # Total duels attempted by the player
    successful_aerial_duels: Optional[int] = None           # Successful aerial duels by the player
    total_aerial_duels: Optional[int] = None                # Total aerial duels attempted by the player
    percentage_aerial_duels_won: Optional[float] = None     # Percentage of aerial duels won by the player
    successful_ground_duels: Optional[int] = None           # Successful ground duels by the player
    total_ground_duels: Optional[int] = None                # Total ground duels attempted by the player
    percentage_ground_duels_won: Optional[float] = None     # Percentage of ground duels won by the player
    successful_tackles: Optional[int] = None                # Tackles made by the player
    total_tackles: Optional[int] = None                     # Total tackles attempted by the player
    percentage_tackles_won: Optional[float] = None          # Percentage of tackles won by the player
    fouls_committed: Optional[int] = None                   # Fouls committed by the player
    interceptions: Optional[int] = None                     # Interceptions made by the player
    clearances: Optional[int] = None                        # Clearances made by the player
    errors_leading_to_goal: Optional[int] = None            # Errors leading to a goal by the player
    errors_leading_to_shot: Optional[int] = None            # Errors leading to a shot by the player


# ====================================================================
# Attacking Statistics - player attacking statistics data
# ====================================================================

# AttackingStats is Dict
# interp. data class representing player attacking statistics data

@dataclass
class AttackingStats:
    player_name: str                                        # Name of the player
    position: str                                           # Position of the player
    touches_in_opposition: Optional[int] = None             # Touches in opposition box by the player
    successful_dribbles: Optional[int] = None               # Successful dribbles by the player
    total_dribbles: Optional[int] = None                    # Total dribbles attempted by the player
    percentage_dribbles_won: Optional[float] = None         # Percentage of dribbles won by the player
    big_chances_missed: Optional[int] = None                # Big chances missed by the player
    touches: Optional[int] = None                           # Total touches by the player
    fouls_suffered: Optional[int] = None                    # Fouls suffered by the player
    offsides: Optional[int] = None                          # Offsides committed by the player


# ====================================================================
# Passing Statistics - player passing statistics data
# ====================================================================

# PassingStats is Dict
# interp. data class representing player passing statistics data

@dataclass
class PassingStats:
    player_name: str                                        # Name of the player
    position: str                                           # Position of the player
    accurate_passes: Optional[int] = None                   # Accurate passes made by the player
    total_passes: Optional[int] = None                      # Total passes attempted by the player
    passes_accuracy: Optional[float] = None                 # Passes accuracy percentage by the player
    big_chances_created: Optional[int] = None               # Big chances created by the player
    assists: Optional[int] = None                           # Assists made by the player
    xA: Optional[float] = None                              # Expected assists by the player
    accurate_passes_in_final_third: Optional[int] = None    # Accurate passes in final third by the player
    total_passes_in_final_third: Optional[int] = None       # Total passes in final third attempted by the player
    accuracy_passes_in_final_third: Optional[float] = None  # Passes accuracy in final third by the player 
    accurate_long_passes: Optional[int] = None              # Accurate long passes made by the player
    total_long_passes: Optional[int] = None                 # Total long passes attempted by the player
    accuracy_long_passes: Optional[float] = None            # Long passes accuracy percentage by the player
    accurate_crosses: Optional[int] = None                  # Accurate crosses made by the player
    total_crosses: Optional[int] = None                     # Total crosses attempted by the player
    accuracy_crosses: Optional[float] = None                # Crosses accuracy percentage by the player


# ====================================================================
# Shots Statistics - player shots statistics data
# ====================================================================

# ShotsStats is Dict
# interp. data class representing player shots statistics data

@dataclass
class ShotsStats:
    player_name: str                                        # Name of the player
    position: str                                           # Position of the player
    goals: Optional[int] = None                             # Goals scored by the player
    xG: Optional[float] = None                              # Expected goals by the player
    xGOT: Optional[float] = None                            # Expected goals on target by the player
    shots_on_target: Optional[int] = None                   # Shots on target by the player
    shots_off_target: Optional[int] = None                  # Shots off target by the player
    blocked_shots: Optional[int] = None                     # Blocked shots by the player
    shots_inside_the_box: Optional[int] = None              # Shots inside the box by the player
    shots_outside_the_box: Optional[int] = None             # Shots outside the box by the player
    headed_shots: Optional[int] = None                      # Headed shots by the player


# ====================================================================
# Player Statistics - all player statistics data
# ====================================================================

# PlayerStats is Dict
# interp. data class representing all player statistics data

@dataclass
class PlayerStats:
    general: GeneralPlayerStats = field(default_factory=GeneralPlayerStats)          # General player statistics
    goalkeeping: GoalKeepingStats = field(default_factory=GoalKeepingStats)          # Goalkeeping statistics
    defensive: DefensiveStats = field(default_factory=DefensiveStats)                # Defensive statistics
    attacking: AttackingStats = field(default_factory=AttackingStats)                # Attacking statistics
    passing: PassingStats = field(default_factory=PassingStats)                      # Passing statistics
    shots: ShotsStats = field(default_factory=ShotsStats)                            # Shots statistics