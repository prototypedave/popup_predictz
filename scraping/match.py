from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from .utils.util import append_to_list, is_event_already_played
from API.weather import get_weather
from dotenv import load_dotenv
import os

from .utils.data_rep import ( parse_score, 
            parse_list_details, parse_date_dd_mm_yyyy, 
            split_string, parse_minute, parse_bracket
)

from .data_def.Match import ( MatchInfo, PlayerName, 
                    GoalInfoData, SubstitutionData, MatchIncident, 
                    CardInfoData, FullTimeData
)


load_dotenv()

# ==============================================================
# Scraper for match data
# ==============================================================

# Scrape match data from the provided link
# scrape_match_data_from_link: (page: Page, link: str) -> MatchInfo

def scrape_match_data_from_link(page: Page, link: str) -> MatchInfo:
    try:
        page.goto(link)
        page.wait_for_selector(".duelParticipant")
        home_team = page.locator(".duelParticipant__home .participant__participantName a").first.inner_text().strip()
        away_team = page.locator(".duelParticipant__away .participant__participantName a").first.inner_text().strip()
        home_score, away_score = parse_score(page.locator(".detailScore__wrapper").inner_text().strip())
        match_time = page.locator(".duelParticipant__startTime div").inner_text().strip()

        match_data = create_match_info(page, home_team, away_team, match_time, home_score, away_score)
        return match_data

    except PlaywrightTimeoutError:
        print("Timeout error while scraping match data.")
        return None


# scrape_loadable_match_data: Page -> Dict
# From the provided match page, scrape additional match data (referee, venue, capacity)and return it as a dictionary.

def scrape_loadable_match_data(page: Page):
    try:
        page.wait_for_selector(".loadable__section")
        extra_match_info = page.locator(".wclDetailSection .wcl-content_J-1BJ").all()
        for match in extra_match_info:
            header = match.locator(".wcl-overline_rOFfd").all()
            value = match.locator(".wcl-simpleText_Asp-0").all()
            head = []
            val = []
            if len(header) > 0:
                head = append_to_list(header)
            if len(value) > 0:
                val = append_to_list(value)
            
            if 'tv channel:' in head or 'live streaming:' in head:
                continue
            
            return parse_list_details(head, val)  
            
    except PlaywrightTimeoutError:
        return {}


# ==============================================================
# Scrape in-play match data
# ==============================================================

# scrape_in_play_match_data: Page -> Dict
# Scrape in-play match data from the provided page and return a dictionary of match data
#    like player scores, yellow cards, red cards, and substitutions.

def scrape_in_play_match_data(page: Page) -> dict:
    try:
        page.wait_for_selector(".loadable__section")
        page.wait_for_selector(".smv__verticalSections")
        
        # Home team data
        overall_data = page.locator(".smv__verticalSections").all()
        if overall_data:
            home_team_data = overall_data[0].locator(".smv__homeParticipant").all()
            away_team_data = overall_data[0].locator(".smv__awayParticipant").all()
            
            home, away = [], []
            for event in home_team_data:
                incident = get_match_incident(event)
                home.append(incident)

            for event in away_team_data:
                incident = get_match_incident(event)
                away.append(incident)

            print(len(home))
            return FullTimeData(home_incidents=home, away_incidents=away)
                        
    except PlaywrightTimeoutError:
        return None


# ==================================================================
# Get team scoring data
# ==================================================================

# get_team_scoring_data: Locator -> GoalInfoData
# Get team scoring data from the provided locator and return a dictionary of player who scored with 
#    time of scoring and type of scoring (goal, penalty, own goal), player who assisted, and time of assist.

def get_team_scoring_data(event):
    try:
        goal_check = event.locator(".smv__incidentIcon svg").get_attribute("data-testid")
        scorer = get_goal_scorer(event) 
        if goal_check and "soccer" in goal_check:
            if scorer is not None:
                assist = get_goal_assist(event)
                if assist is not None:
                    return GoalInfoData(
                        scorer=scorer,
                        assist=assist,
                        penalty=False
                    )
                else:
                    return GoalInfoData(
                        scorer=scorer,
                        assist=None,
                        penalty=get_goal_penalty(event)
                    )
        return None
    except Exception as e:
        return None


# =========================================================
# Get goal scorer name
# =========================================================

# get_goal_scorer: Locator -> PlayerName
# Get team scoring data from the provided locator and return a player who scored a goal
def get_goal_scorer(event):
    try:
        player = event.locator(".smv__playerName").inner_text().strip()
        return PlayerName(full_name=player)
    except Exception as e:
        return None


# =========================================================
# Get goal assist name
# =========================================================

# get_goal_assist: Locator -> PlayerName
# Get team scoring data from the provided locator and return a player who assisted a goal
def get_goal_assist(event):
    try:
        assist = event.locator(".smv__assist").inner_text().strip()
        if assist:
            return PlayerName(full_name=parse_bracket(assist))
    except Exception as e:
        return None

    
# =========================================================
# Check if goal was a penalty
# =========================================================

# get_goal_penalty: Locator -> bool
# Get team scoring data from the provided locator and return a boolean indicating if the goal was a penalty
def get_goal_penalty(event):
    try:
        penalty = event.locator(".smv__subIncident").inner_text().strip()
        if penalty:
            return True if "penalty" in penalty else False
    except Exception:
        return False


# =========================================================
# Get card data
# =========================================================

# get_card_data: Locator -> CardInfoData
# Get team card data (type of card) from the provided locator and return a player who received a card
def get_card_type(event):
    try:
        card_check = event.locator(".smv__incident .smv__incidentIcon svg").get_attribute("class")
        if card_check and "yellow" in card_check:
            yellow_card = get_card_data(event)
            if yellow_card is not None:        
                return CardInfoData(
                    yellow_card=True,
                    red_card=False,
                    player=yellow_card
                )
        elif card_check and "red" in card_check:
            red_card = get_card_data(event)
            if red_card is not None:
                return CardInfoData(
                    yellow_card=False,
                    red_card=True,
                    player=red_card
                )
        return None
    except Exception as e:
        return None


# ==================================================================
# Get player name who received a card
# ==================================================================

# get_card_data: Locator -> PlayerName
# Get team card data from the provided locator and return a player who received a card

def get_card_data(event):
    try:
        player = event.locator(".smv__playerName").inner_text().strip()
        return PlayerName(full_name=player)
    except Exception as e:
        return None


# ==============================================================
# Get substitution data
# ==============================================================
# get_substitution_data: Locator -> SubstitutionData
# Get substitution data from the provided locator and return a dictionary of player who was subbed in and out.

def get_substitution_data(event):
    try:
        check_sub = event.locator(".smv__incident .smv__incidentIconSub")
        if check_sub:
            player_out = event.locator(".smv__incidentSubOut a").inner_text().strip()
            player_in = event.locator(".smv__incident a").first.inner_text().strip()
            if player_in and player_out:
                return SubstitutionData(player_in=player_in, player_out=player_out)
        
        return None
    except Exception as e:
        return None


# ==============================================================
# Return in play match data
# ==============================================================
# assemble_in_play_match_data: Locator -> MatchIncident
# Assemble in-play match data from the provided locator and return a dictionary of player scores, 
#     yellow cards, red cards, and substitutions. 

def get_match_incident(event):
    try:
        minute = parse_minute(event.locator(".smv__incident .smv__timeBox").inner_text().strip())
        goal = get_team_scoring_data(event)
        
        if goal is None:
            card = get_card_type(event)
            if card is None:
                substitution = get_substitution_data(event)
                return MatchIncident(time=minute, card=None, substitution=substitution, goal=None)
            else:
                return MatchIncident(time=minute, card=card, substitution=None, goal=None)
        else:
            return MatchIncident(time=minute, card=None, substitution=None, goal=goal)

    except Exception as e:
        return None
                
                
# Page, str, str, str, str, str -> MatchInfo
# create_match_info: Page, str, str, str, str, str -> MatchInfo
# Create a MatchInfo object from the scraped data and additional information.

def create_match_info(page: Page, home_team: str, away_team: str, match_time: str, home_score: str, away_score: str) -> MatchInfo:
    details = page.locator(".detail__breadcrumbs li").all()
    country = details[1].inner_text().strip().lower()
    league, game_round = split_string(details[2].inner_text().strip().lower())
    date, time = parse_date_dd_mm_yyyy(match_time)

    if is_event_already_played(date, time):
        jk = scrape_in_play_match_data(page)
        print(jk)

    extra_match_info = scrape_loadable_match_data(page)
    
    if extra_match_info is None:
        return None
      
    try:
        condition = get_weather(os.getenv("WEATHER_API"), extra_match_info.get('venue'), date, time)
    except Exception as e:
        condition = None

    return MatchInfo(
        home_team=home_team,
        away_team=away_team,
        match_time=match_time,
        referee=extra_match_info.get('referee', ''),
        venue=extra_match_info.get('venue', ''),
        league=league,
        game_round=game_round,
        capacity=extra_match_info.get('capacity', ''),
        weather=condition,
        home_score=home_score,
        away_score=away_score
    )
