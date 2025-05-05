# Functions to scrape match summary from flashscore
from playwright.sync_api import Page
from .utils import scrape_locator_lists, scrape_attributes, scrape_text_content
from .func_util import split_string, parse_score
from datetime import datetime

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


# Page -> 
# scrape in play match data
def in_play_match_info(page: Page):
    in_play_list = scrape_locator_lists(page, ".loadable__section .smv__verticalSections")
    print(in_play_list)


# Page -> GameInfo
# !!!
# !!!
def get_match_summary(page: Page):
    country, league, round = game_country_and_league(page)
    home, away, home_score, away_score, time = match_info(page)
    in_play_match_info(page)
        