# Functions to scrape match summary from flashscore
from playwright.sync_api import Page
from .utils import scrape_locator_lists, scrape_attributes, scrape_text_content
from .func_util import split_string, parse_score, is_past_two_hours
from datetime import datetime
from .player import match_events, populate_missing_player_info

# Page -> tuple
# scrape league name, country name and game round from page and 
#   return a tuple of these items
def game_country_and_league(page: Page) -> tuple:
    header_items = scrape_locator_lists(page, ".detail__breadcrumbs li")
    country = header_items[1].inner_text().strip().lower()
    league, round = split_string(header_items[2].inner_text().strip().lower())
    return country, league, round


# Page -> tuple
# scrape home and away team name, home and away score and time of the match
def match_info(page: Page) -> tuple:
    home_team = scrape_text_content(page, ".duelParticipant__home .participant__participantName a")
    away_team = scrape_text_content(page, ".duelParticipant__away .participant__participantName a")
    home_score, away_score = parse_score(scrape_text_content(page, ".detailScore__wrapper"))
    time = datetime.strptime(scrape_text_content(page, ".duelParticipant__startTime div"), "%d.%m.%Y %H:%M")
    return home_team, away_team, home_score, away_score, time


# Page -> tuple
# scrape match report of key events goal, sub, card and return a tuple of list
#   for home and away events
def in_play_match_info(page: Page) -> tuple:
    in_play_list = scrape_locator_lists(page, ".loadable__section .smv__verticalSections")
    if in_play_list:
        home_locs = in_play_list[0].locator(".smv__homeParticipant").all()
        away_locs = in_play_list[0].locator(".smv__awayParticipant").all()
        
        home_events = match_events(page, home_locs)
        away_events = match_events(page, home_locs)

        return home_events, away_events


# Page -> tuple
# scrape missing or injured players that will/ did not play a given match and return a tuple
#   of list for home and away players 
def absent_players_info(page: Page) -> tuple:
    absent_locators = scrape_locator_lists(page, ".loadable__section .lf__sidesBox .lf__sides .lf__side .wcl-participant_QKIld")
    if absent_locators:
        home, away = [], []
        for absent in absent_locators:
            if absent:
                absent_attr = absent.get_attribute('data-testid')
                if absent_attr:
                    # Home Players
                    if "wcl-lineupsParticipantGeneral-left" in absent_attr:
                        href = scrape_attributes(absent, "a", "href")
                        if href:
                            reason = scrape_text_content(absent, "span")
                            home.append({'href': href, 'reason': reason})
                    elif "wcl-lineupsParticipantGeneral-right" in absent_attr:
                        href = scrape_attributes(absent, "a", "href")
                        if href:
                            reason = scrape_text_content(absent, "span")
                            away.append({'href': href, 'reason': reason})
        home_data = []
        for team in home:
            missing = populate_missing_player_info(page, team)
            home_data.append(missing)
        
        away_data = []
        for team in away:
            missing = populate_missing_player_info(page, team)
            away_data.append(missing)

        return home_data, away_data


# Page -> GameInfo
# !!!
# !!!
def get_match_summary(page: Page):
    country, league, round = game_country_and_league(page)
    home, away, home_score, away_score, time = match_info(page)
    home_players_missing, away_players_missing = absent_players_info(page)
    print(away_players_missing)
    if is_past_two_hours:
        in_play_match_info(page)
        