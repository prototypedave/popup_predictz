# Scrapper to get player's data
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from .data import Player, SubInfo, CardInfo, GoalInfo
from .constants import FLASHSCORE
from .utils import scrape_text_content, scrape_locator_lists, scrape_attributes
from .func_util import parse_bracket
from typing import List


# Page, str -> Player
# scrapes players information from the provided link if its a valid link
#   returns Player 
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

        return  Player(name=name, position=position,
                nationality=country, team=parse_bracket(team), dob=parse_bracket(dob))

    except PlaywrightTimeoutError:
        return None

    except Exception as e:
        print(e)
        return None


# Page, Locator, min -> SubInfo
# scrapes and represents relevant substitution information to SubInfo
def populate_sub_info(page: Page, loc, min) -> SubInfo:
    out_href = scrape_attributes(loc, ".smv__incidentSubOut a", 'href')
    in_href = scrape_attributes(loc, ".smv__incident a", 'href')
    reason = scrape_text_content(loc, ".smv__subIncident")
    if reason:
        reason = parse_bracket(reason)

    if out_href and in_href:
        player_out = scrape_player_data(page, out_href)
        player_in = scrape_player_data(page, in_href)
        if player_out and player_in:
            return SubInfo(player_in=player_in, player_out=player_out, time=min, reason=reason)


# Page, Locator, min, type -> CardInfo
# scrapes and assign relevant Card data to the CardInfo
def populate_card_info(page: Page, loc, min, tpye) -> CardInfo:
    href = scrape_attributes(loc, ".smv__playerName", "href")
    if href is None:
        return None

    reason = scrape_text_content(loc, ".smv__subIncident")
    if reason:
        reason = parse_bracket(reason)

    player = scrape_player_data(page, href)   
    if player:
        return CardInfo(player=player, card_type=tpye, time=min, reason=reason)

    
# Page, Locator, min -> GoalInfo
# scrapes and assigns relevant Goal information to GoalInfo
def populate_goal_info(page: Page, loc, min) -> GoalInfo:
    scorer_href = scrape_attributes(loc, ".smv__playerName", "href")
    if scorer_href is None:
        return None

    scorer = scrape_player_data(page, scorer_href)
    if scorer:
        assist_href = scrape_attributes(loc, ".smv__assist a", "href")
        if assist:
            assist = scrape_player_data(page, assist_href)
            return GoalInfo(scorer=scorer, assist=assist, time=min, goal_type=None)
        
        goal_type = scrape_attributes(loc, ".smv__subIncident")
        if goal_type:
            return GoalInfo(scorer=scorer, assist=None, time=min, goal_type=goal_type)

        return GoalInfo(scorer=scorer, assist=None, time=min, goal_type=None)


# Page, Locator -> Dict
# checks whether an event is substition, card or goal and returns a dictionary
#   indicating the type of the event with the subsequent data type
def get_possible_event(page: Page, loc) -> dict:
    time = scrape_text_content(loc, ".smv__incident .smv__timeBox")
    if time is None:
        return None

    sub_class_name = scrape_attributes(loc, ".smv__incident .smv__incidentIconSub", "class")
    if sub_class_name and 'smv__incidentIconSub' in sub_class_name:
        sub = populate_sub_info(page, loc, time)
        return {'type': 'sub', 'value': sub}                         
    
    card_class_name = scrape_attributes(loc, ".smv__incidentIcon svg", "class")
    if card_class_name: 
        if "card-ico yellowCard-ico" in card_class_name:
            card = populate_card_info(page, loc, time, 'yellow')
            return {'type': 'card', 'value': card}
        
        elif "card-ico redCard-ico" in card_class_name:
            card = populate_card_info(page, loc, time, 'red')
            return {'type': 'card', 'value': card}
    
    goal_attr = scrape_attributes(loc, ".smv__incidentIcon svg", "data-testid")
    if goal_attr and "wcl-icon-soccer" in goal_attr:
        goal = populate_goal_info(page, loc, time)
        return {'type': 'goal', 'value': goal}


# List -> List
# Classifies events from the provided link assigning data to their respective
#   classes
def match_events(page: Page, events: List) -> tuple:
    classified_events = []
    for event in events:
        incident = get_possible_event(page, event)
        classified_events.append(incident)

    return classified_events
        