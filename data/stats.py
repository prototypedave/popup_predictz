# Dataclasses for stats

from typing import Optional
from dataclasses import dataclass

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
    through_passes_home: Optional[int] = None                         # Total through passes for home team
    through_passes_away: Optional[int] = None                         # Total through passes for away team
    total_long_passes_home: Optional[int] = None                            # Total long passes for home team
    total_long_passes_away: Optional[int] = None                            # Total long passes for away team
    successful_long_passes_home: Optional[int] = None                       # Successful long passes for home team
    successful_long_passes_away: Optional[int] = None                       # Successful long passes for away team
    long_passes_percentage_home: Optional[int] = None                       # Long passes percentage for home team
    long_passes_percentage_away: Optional[int] = None                       # Long passes percentage for away team
    passes_in_final_third_home: Optional[int] = 0                        # Passes in final third for home team
    passes_in_final_third_away: Optional[int] = 0                        # Passes in final third for away team
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
    throw_ins_home: Optional[int] = 0                                    # Throw ins for home team
    throw_ins_away: Optional[int] = 0                                    # Throw ins for away
    fouls_home: Optional[int] = None                                        # Fouls for home team
    fouls_away: Optional[int] = None                                        # Fouls for away team
    tackles_home: Optional[int] = None                                      # Tackles for home team
    tackles_away: Optional[int] = None                                      # Tackles for away team
    successful_tackles_home: Optional[int] = None                           # Successful tackles attempted
    successful_tackles_away: Optional[int] = None                           # Successful tackles attempted
    tackles_percentage_home: Optional[int] = None                           # Percentage of successful tackles made
    tackles_percentage_away: Optional[int] = None                           # Percentage of successful tackles made
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
    yellow_cards_home: Optional[int] = 0                                # Yellow cards for home team
    yellow_cards_away: Optional[int] = 0                                 # Yellow cards for away team
    red_cards_home: Optional[int] = 0                                    # Red cards for home team
    red_cards_away: Optional[int] = 0                                    # Red cards for away team
    penalty_home: Optional[int] = 0                                    # Penalties for home team
    penalty_away: Optional[int] = 0                                    # Penalties for away team