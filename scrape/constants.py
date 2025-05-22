# All constants for scraping

# Url
FLASHSCORE = "https://www.flashscore.com"

# Match summary
SUMMARY = 'match-summary/match-summary'

# stats
STATS_FULL_TIME = '/match-statistics/0'
STATS_FIRST_HALF = '/match-statistics/1'
STATS_SECOND_HALF = '/match-statistics/2'
LINEUP = 'match-summary/lineups'

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
            "expected goals": "expected_goals",
            "possession": "possession",
            "total shots": "total_shots",
            "shots on target": "shots_on_target",
            "big chances": "big_chances",
            "corner kicks": "corner_kicks",
            "yellow cards": "yellow_cards",
            "red cards": "red_cards",
            "penalty": "penalties",
            "xg on target": "xg_on_target",
            "shots off target": "shots_off_target",
            "blocked shots": "blocked_shots",
            "shots inside": "shots_inside_the_box",
            "shots outside": "shots_outside_the_box",
            "woodwork": "woodwork",
            "touches in opposition": "touches_in_opposition",
            "offsides": "offsides",
            "free kicks": "free_kicks",
            "expected assists": "expected_assists",
            "throw ins": "throw_ins",
            "fouls": "fouls",
            "tackles": "tackles",
            "duels won": "duels_won",
            "clearances": "clearances",
            "interceptions": "interceptions",
            "errors leading to goal": "errors_leading_to_goal",
            "errors leading to shot": "errors_leading_to_shot",
            "goalkeeper saves": "goalkeeper_saves",
            "xgot faced": "xgot_faced",
            "goals prevented": "goals_prevented"
}

# stats that are not in the same order
EXTRA_STATS_MAP = {
            "passes": "passes",
            "through passes": "through_passes",
            "long passes": "long_passes",
            "passes in final third": "passes_in_final_third",
            "crosses": "crosses",
}