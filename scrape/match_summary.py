# Functions to scrape match summary from flashscore

from playwright.sync_api import Page
from .utils import scrape_locator_lists, scrape_attributes, scrape_text_content, scrape_text_to_list
from .func_util import split_string, parse_score, is_past_two_hours
from datetime import datetime
from .player import match_events, populate_missing_player_info
from .data import MatchSummary


# Page -> tuple
# scrape league name, country name and game round from page and 
#   return a tuple of these items
def game_country_and_league(page: Page) -> tuple:
    header_items = scrape_locator_lists(page, ".detail__breadcrumbs li")
    country = header_items[1].inner_text().strip().lower()
    league, round = split_string(header_items[2].inner_text().strip().lower())
    return country, league, round

    # Tests, ensure the returned values contain relevant data or None
    # Tests, to ensure the function will not fail under different circumstances eg. incorate page or missing locators
    # Tests, correct calls for the helper functions


# Page -> tuple
# scrape home and away team name, home and away score and time of the match
def match_info(page: Page) -> tuple:
    home_team = scrape_text_content(page, ".duelParticipant__home .participant__participantName a")
    away_team = scrape_text_content(page, ".duelParticipant__away .participant__participantName a")
    home_score, away_score = parse_score(scrape_text_content(page, ".detailScore__wrapper"))
    time = datetime.strptime(scrape_text_content(page, ".duelParticipant__startTime div"), "%d.%m.%Y %H:%M")
    return home_team, away_team, home_score, away_score, time

    # Tests, ensure the returned values contain relevant data or None
    # Tests, to ensure the function will not fail under different circumstances eg. incorate page or missing locators
    # Tests, correct calls for the helper functions


# Page -> tuple
# scrape missing or injured players that will/ did not play a given match and return a tuple
#   of list for home and away players 
def absent_players_info(page: Page) -> tuple:
    absent_locators = scrape_locator_lists(page, ".loadable__section .lf__sidesBox .lf__sides .lf__side .wcl-participant_QKIld")
    home, away = [], []
    if absent_locators:
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

                    # Away Players
                    elif "wcl-lineupsParticipantGeneral-right" in absent_attr:
                        href = scrape_attributes(absent, "a", "href")
                        if href:
                            reason = scrape_text_content(absent, "span")
                            away.append({'href': href, 'reason': reason})
    
    home_data = populate_missing_player_info(page, home)
    away_data = populate_missing_player_info(page, away)

    return home_data, away_data

    # Tests each step in this function as its critical for failure


# Page -> dict
# scrape and return referee, venue and stadium capacity info from the given match
#   page
def scrape_additional_match_info(page: Page) -> dict:
    extra_locators = scrape_locator_lists(page, ".loadable__section .wclDetailSection .wcl-content_J-1BJ")
    for extra in extra_locators:
        head = extra.locator(".wcl-overline_rOFfd").all()
        value = extra.locator(".wcl-simpleText_Asp-0").all()
        
        header_texts = scrape_text_to_list(head)
        value_texts = scrape_text_to_list(value)

        # Filter out tv or live streams values
        if 'tv channel:' in header_texts or 'live streaming:' in value_texts:
            continue
        
        return organize_additional_match_info(header_texts, value_texts)


# List, List -> Dict
# produce a dictionary containing referee's name, venue name and capacity value
#   from the provided List items which contains header and value for this fields
def organize_additional_match_info(head: list, value: list) -> dict:
    result, i = {}, 0
    for key in head:
        stripped_key = key.rstrip(':')
        if stripped_key in ('referee', 'venue'):
            if i + 1 < len(value):
                result[stripped_key] = value[i] + ' ' + value[i + 1]  # Name and Nationality are splitted
                i += 2
            else:
                result[stripped_key] = value[i]
                i += 1
        else:
            if i < len(value):
                result[stripped_key] = value[i]

    return result


# Page -> tuple
# scrape match report of key events goal, sub, card and return a tuple of list
#   for home and away events
def in_play_match_info(page: Page) -> tuple:
    in_play_list = scrape_locator_lists(page, ".loadable__section .smv__verticalSections")
    if in_play_list:
        home_locs = in_play_list[0].locator(".smv__homeParticipant").all()
        away_locs = in_play_list[0].locator(".smv__awayParticipant").all()
        
        home_events = match_events(page, home_locs)
        away_events = match_events(page, away_locs)

        return home_events, away_events


# Page -> dict
# scrape and organizes match information for easier retrieval of different data
def get_match_summary(page: Page):
    country, league, round = game_country_and_league(page)
    home, away, home_score, away_score, time = match_info(page)
    home_players_missing, away_players_missing = absent_players_info(page)
    additional_info = scrape_additional_match_info(page)

    referee, venue, capacity = None, None, None
    if additional_info:
        referee, venue, capacity = additional_info['referee'], additional_info['venue'], additional_info['capacity']
    
    home_events, away_events = None, None
    if is_past_two_hours(time):
        home_events, away_events = in_play_match_info(page)

    return {
        'summary': MatchSummary(
            competition=country, league=league, round=round,
            home=home, away=away, home_score=home_score, away_score=away_score, date=time,
            absent_home_players=home_players_missing, absent_away_players=away_players_missing,
            referee=referee, venue=venue, capacity=capacity,
        ),
        'home_events': home_events,
        'away_events': away_events
    }
        