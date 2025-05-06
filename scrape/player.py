# Scrapper to get player's data
from playwright.sync_api import Page
from .data import Player, SubInfo, CardInfo
from .constants import FLASHSCORE
from .utils import scrape_text_content, scrape_locator_lists, scrape_attributes
from .func_util import parse_bracket
from typing import List

# !!!
def scrape_player_data(page: Page, player_link: str) -> Player:
    try:
        link = FLASHSCORE + player_link
        page.goto(link)
        page.wait_for_selector(".player-profile-heading")
        country = page.locator(".player-profile-heading nav li").last.text_content().lower()
        name = scrape_text_content(page, ".playerHeader__nameWrapper h2")
        position = scrape_text_content(page, ".playerTeam strong")
        team = scrape_text_content(page, ".playerTeam a")
        player_info = scrape_locator_lists(page, ".playerInfoItem span")
        dob = player_info[1].text_content().lower() 

        return  PlayerData(name=name, position=position,
                nationality=country, team=parse_bracket(team), dob=parse_bracket(dob))
    
    except Exception as e:
        return None


# Page, Locator, min -> SubInfo
# populate the SubInfo data type from the given event locator getting the player subbed in
#   and player subbed out
def populate_sub_info(page: Page, loc, min) -> SubInfo:
    out_href = scrape_attributes(loc, ".smv__incidentSubOut a", 'href')
    in_href = scrape_attributes(loc, ".smv__incident a", 'href')
    reason = scrape_text_content(loc, ".smv__subIncident")

    if out_href and in_href:
        player_out = scrape_player_data(page, out_href)
        player_in = scrape_player_data(page, in_href)
        if player_out and player_in:
            return SubInfo(player_in=player_in, player_out=player_out, time=min, reason=reason)


# Page, Locator, min, type -> CardInfo
# populate CardInfo class data with the scraped info getting the player who received a card
#   type of the card and the minute the card was awarded
def populate_card_info(page: Page, loc, min, tpye) -> CardInfo:
    href = scrape_attributes(loc, ".smv__playerName", "href")
    player = scrape_player_data(page, href)
    reason = scrape_text_content(loc, ".smv__subIncident")
    if player:
        return CardInfo(player=player, card_type=tpye, time=min, reason=reason)


# Page, Locator -> tuple
# From the events locator return the possible events and return a tuple of Goal,
#   Card and Substitution which two might contain None values
def get_possible_event(page: Page, loc) -> tuple:
    time = scrape_text_content(loc, ".smv__incident .smv__timeBox")
    print(time)
    
    sub_class_name = scrape_attributes(loc, ".smv__incident .smv__incidentIconSub", "class")
    if sub_class_name and 'smv__incidentIconSub' in sub_class_name:
        sub = populate_sub_info(page, loc, time)
        print(sub)
6
    card_class_name = scrape_attributes(loc, ".smv__incidentIcon svg", "class")
    if card_class_name and "card-ico yellowCard-ico" in card_class_name:
        card = populate_card_info(page, loc, time, 'yellow')
        print(card)
    elif card_class_name and "card-ico redCard-ico" in card_class_name:
        card = populate_card_info(page, loc, time, 'red')
        print(card)


# List -> List
# From the Lists of events locators (home or away) identify the type of event
#   Goal, Sub or Card and return a tuple of lists containing the home and away
#   events
def match_events(page: Page, events: List) -> List:
    for event in events:
        if event:
            get_possible_event(page, event)


