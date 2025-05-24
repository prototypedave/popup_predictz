# All constants for scraping

# Url
FLASHSCORE = "https://www.flashscore.com"

# Match summary
SUMMARY = 'match-summary/match-summary'

# stats
STATS_FULL_TIME = 'match-statistics/0'
STATS_FIRST_HALF = '/match-statistics/1'
STATS_SECOND_HALF = '/match-statistics/2'
LINEUP = 'lineups'

# Odds
ODDS_1X2_FULL_TIME = 'odds-comparison/1x2-odds/full-time'
ODDS_1X2_FIRST_HALF = 'odds-comparison/1x2-odds/1st-half'
ODDS_1X2_SECOND_HALF = 'odds-comparison/1x2-odds/2nd-half'
ODDS_OVER_UNDER_FULL_TIME = 'odds-comparison/over-under/full-time'
ODDS_OVER_UNDER_FIRST_HALF = 'odds-comparison/over-under/1st-half'
ODDS_OVER_UNDER_SECOND_HALF = 'odds-comparison/over-under/2nd-half'
ODDS_HANDICAP_FULL_TIME = 'odds-comparison/asian-handicap/full-time' 
ODDS_HANDICAP_FIRST_HALF = 'odds-comparison/asian-handicap/1st-half'
ODDS_HANDICAP_SECOND_HALF = 'odds-comparison/asian-handicap/2nd-half'
ODDS_BTTS_FULL_TIME = 'odds-comparison/both-teams-to-score/full-time'
ODDS_BTTS_FIRST_HALF = 'odds-comparison/both-teams-to-score/1st-half'
ODDS_BTTS_SECOND_HALF = 'odds-comparison/both-teams-to-score/2nd-half'
ODDS_DC_FULL_TIME = 'odds-comparison/double-chance/full-time'
ODDS_DC_HALF_HALF = 'odds-comparison/double-chance/1st-half'
ODDS_DC_SECOND_HALF = 'odds-comparison/double-chance/2nd-half'
ODDS_DNB_FULL_TIME = 'odds-comparison/draw-no-bet/full-time'
ODDS_DNB_FIRST_HALF = 'odds-comparison/draw-no-bet/1st-half'
ODDS_CS_FULL_TIME = 'odds-comparison/correct-score/full-time'
ODDS_HT_AND_FT = 'odds-comparison/ht-ft/full-time'
ODDS_ODD_EVEN_FULL_TIME = 'odds-comparison/odd-even/full-time'
ODDS_ODD_EVEN_FIRST_HALF = 'odds-comparison/odd-even/1st-half'
ODDS_ODD_EVEN_SECOND_HALF = 'odds-comparison/odd-even/2nd-half'

# h2h
H2H_OVERALL = 'h2h/overall'
H2H_HOME = '/h2h/home'
H2H_AWAY = 'h2h/away'

# stats variables
STAT_MAP = {
        "expected goals": ["xG_home", "xG_away"],  
        "total shots": ["total_shots_home", "total_shots_away"],
        "shots on target": ["shots_on_target_home", "shots_on_target_away"],
        "big chances": ["big_chances_home", "big_chances_away"],
        "corner kicks": ["corners_home", "corners_away"], 
        "xg on target": ["xG_on_target_home", "xG_on_target_away"],
        "shots off target": ["shots_off_target_home", "shots_off_target_away"],
        "blocked shots": ["blocked_shots_home", "blocked_shots_away"],
        "shots inside": ["shots_inside_the_box_home", "shots_inside_the_box_away"],
        "shots outside": ["shots_outside_the_box_home", "shots_outside_the_box_away"],
        "woodwork": ["woodwork_home", "woodwork_away"],
        "possession": ["possession_home", "possession_away"],
        "touches in opposition": ["touches_in_opposition_home, touches_in_opposition_away"],
        "expected assists": ["xA_home", "xA_away"],
        "xgot faced": ["xGOT_faced_home", "xGOT_faced_away"],
        "offsides": ["offsides_home", "offsides_away"],
        "free kicks": ["free_kicks_home", "free_kicks_away"],  
        "throw ins": ["throw_ins_home", "throw_ins_away"],
        "fouls": ["fouls_home", "fouls_away"],
        "tackles": ["tackles_home", "tackles_away"],
        "duels won": ["duels_won_home", "duels_won_away"],
        "clearances": ["clearances_home", "clearances_away"],
        "interceptions": ["interceptions_home", "interceptions_away"],
        "errors leading to goal": ["errors_leading_to_goal_home", "errors_leading_to_goal_away"],
        "errors leading to shot": ["errors_leading_to_shot_home", "errors_leading_to_shot_away"],
        "goalkeeper saves": ["goalkeeper_saves_home", "goalkeeper_saves_away"],
        "goals prevented": ["goals_prevented_home", "goals_prevented_away"],  
        "yellow cards": ["yellow_cards_home", "yellow_cards_away"],
        "red cards": ["red_cards_home", "red_cards_away"],
        "penalty": ["penalty_home", "penalty_away"],
}

# stats that are not in the same order
EXTRA_STATS_MAP = {
        "passes": {
            "home": ["passes_percentage_home", "successful_passes_home", "total_passes_home"],
            "away": ["passes_percentage_away", "successful_passes_away", "total_passes_away"]
        },
        "through passes": {
            "home": ["through_passes_percentage_home", "successful_through_passes_home", "total_through_passes_home"],
            "away": ["through_passes_percentage_away", "successful_through_passes_away", "total_through_passes_away"]
        },
        "long passes": {
            "home": ["long_passes_percentage_home", "successful_long_passes_home", "total_long_passes_home"],
            "away": ["long_passes_percentage_away", "successful_long_passes_away", "total_long_passes_away"]
        },
        "passes in final third": {
            "home": ["passes_in_final_third_percentage_home", "successful_passes_in_final_third_home", "total_passes_in_final_third_home"],
            "away": ["passes_in_final_third_percentage_away", "successful_passes_in_final_third_away", "total_passes_in_final_third_away"]
        },
        "crosses": {
            "home": ["crosses_percentage_home", "successful_crosses_home", "total_crosses_home"],
            "away": ["crosses_percentage_away", "successful_crosses_away", "total_crosses_away"]
        },
}
