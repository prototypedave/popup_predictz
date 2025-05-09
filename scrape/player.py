# Scrapper to get player's data
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from .data import Player, SubInfo, CardInfo, GoalInfo, MissingPlayer
from .constants import FLASHSCORE
from .utils import scrape_text_content, scrape_attributes
from .func_util import parse_bracket
from typing import List


# Page, str -> Player
# scrapes players information from the provided link if its a valid link
#   returns Player 
async def scrape_player_data(page: Page, player_link: str) -> Player | None:
    try:
        link = FLASHSCORE + player_link
        await page.goto(link)
        await page.wait_for_selector(".player-profile-heading", timeout=8000)

        # Safe extraction with await
        country_el = page.locator(".player-profile-heading nav li").last
        country_text = await country_el.text_content()
        country = country_text.strip().lower() if country_text else None

        name = await scrape_text_content(page, ".playerHeader__nameWrapper h2")
        position = await scrape_text_content(page, ".playerTeam strong")
        team = await scrape_text_content(page, ".playerTeam a")

        # DOB from player info
        player_info = await page.locator(".playerInfoItem span").all()
        dob = None
        if len(player_info) >= 2:
            dob_raw = await player_info[1].text_content()
            dob = parse_bracket(dob_raw.strip()) if dob_raw else None

        return Player(
            name=name,
            position=position,
            nationality=country,
            team=parse_bracket(team),
            dob=dob
        )

    except Exception as e:
        return None


# Page, Locator -> MissingPlayer
# scrape and populate information for missing or injured player and return MissingPlayer class
async def populate_missing_player_info(page: Page, team) -> MissingPlayer:
    data = []
    for tm in team:
        href = tm['href']
        player = await scrape_player_data(page, href)
        data.append(MissingPlayer(player=player, reason=tm['reason']))
    return data


# Page, Locator, min -> SubInfo
# scrapes and represents relevant substitution information to SubInfo
async def populate_sub_info(page: Page, loc, min) -> SubInfo:
    out_href = await scrape_attributes(loc, ".smv__incidentSubOut a", 'href')
    in_href = await scrape_attributes(loc, ".smv__incident a", 'href')
    reason = await scrape_text_content(loc, ".smv__subIncident")
    if reason:
        reason = parse_bracket(reason)

    if out_href and in_href:
        player_out = await scrape_player_data(page, out_href)
        player_in = await scrape_player_data(page, in_href)
        if player_out and player_in:
            return SubInfo(player_in=player_in, player_out=player_out, time=min, reason=reason)


# Page, Locator, min, type -> CardInfo
# scrapes and assign relevant Card data to the CardInfo
async def populate_card_info(page: Page, loc, min, tpye) -> CardInfo:
    href = await scrape_attributes(loc, ".smv__playerName", "href")
    if href is None:
        return None

    reason = await scrape_text_content(loc, ".smv__subIncident")
    if reason:
        reason = parse_bracket(reason)

    player = await scrape_player_data(page, href)   
    if player:
        return CardInfo(player=player, card_type=tpye, time=min, reason=reason)

    
# Page, Locator, min -> GoalInfo
# scrapes and assigns relevant Goal information to GoalInfo
async def populate_goal_info(page: Page, loc, min) -> GoalInfo:
    scorer_href = await scrape_attributes(loc, ".smv__playerName", "href")
    if scorer_href is None:
        return None

    scorer = await scrape_player_data(page, scorer_href)
    if scorer:
        assist_href = await scrape_attributes(loc, ".smv__assist a", "href")
        if assist_href:
            assist = await scrape_player_data(page, assist_href)
            return GoalInfo(scorer=scorer, assist=assist, time=min, goal_type=None)
        
        goal_type = await scrape_text_content(loc, ".smv__subIncident")
        if goal_type:
            return GoalInfo(scorer=scorer, assist=None, time=min, goal_type=goal_type)

        return GoalInfo(scorer=scorer, assist=None, time=min, goal_type=None)


# Page, Locator -> Dict
# checks whether an event is substition, card or goal and returns a dictionary
#   indicating the type of the event with the subsequent data type
async def get_possible_event(page: Page, loc) -> dict:
    time = await scrape_text_content(loc, ".smv__incident .smv__timeBox")
    if time is None:
        return None

    sub_class_name = await scrape_attributes(loc, ".smv__incident .smv__incidentIconSub", "class")
    if sub_class_name and 'smv__incidentIconSub' in sub_class_name:
        sub = await populate_sub_info(page, loc, time)
        return {'type': 'sub', 'value': sub}                         
    
    card_class_name = await scrape_attributes(loc, ".smv__incidentIcon svg", "class")
    if card_class_name: 
        if "card-ico yellowCard-ico" in card_class_name:
            card = await populate_card_info(page, loc, time, 'yellow')
            return {'type': 'card', 'value': card}
        
        elif "card-ico redCard-ico" in card_class_name:
            card = await populate_card_info(page, loc, time, 'red')
            return {'type': 'card', 'value': card}
    
    goal_attr = await scrape_attributes(loc, ".smv__incidentIcon svg", "data-testid")
    if goal_attr and "wcl-icon-soccer" in goal_attr:
        goal = await populate_goal_info(page, loc, time)
        return {'type': 'goal', 'value': goal}


# List -> List
# Classifies events from the provided link assigning data to their respective
#   classes
async def match_events(page: Page, events: List) -> tuple:
    classified_events = []
    for event in events:
        incident = await get_possible_event(page, event)
        classified_events.append(incident)

    return classified_events
        