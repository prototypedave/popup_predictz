from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from .player.injury import get_missing_or_injured_players

from .utils.util import append_to_list, is_event_already_played
from API.weather import get_weather
from dotenv import load_dotenv
import os

from .match_incident import get_match_incident
from .data_def.Match import GameIncidents


from .utils.data_rep import ( parse_score, 
            parse_list_details, parse_date_dd_mm_yyyy, 
            split_string, parse_minute, parse_bracket
)

load_dotenv()

# ==============================================================
# Scraper for match data
# ==============================================================

# Scrape match data from the provided link
# scrape_match_data_from_link: (page: Page, link: str) -> MatchInfo

def scrape_match_data_from_link(page: Page, link: str):
    try:
        page.goto(link)
        missing_players = get_missing_or_injured_players(page)
        page.wait_for_selector(".duelParticipant")
        country, league, game_round = get_country_and_league(page)
        home, away, score, date, time = get_teams_info(page)
        
        print(f"Team {home} injury {missing_players}")



        

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
                incident = get_match_incident(page, event)
                if incident is not None:
                    home.append(incident)

            for event in away_team_data:
                incident = get_match_incident(page, event)
                if incident is not None:
                    away.append(incident)

            return GameIncidents(home=home, away=away)
                   
    except PlaywrightTimeoutError:
        return None

                
# Page, str, str, str, str, str -> MatchInfo
# create_match_info: Page, str, str, str, str, str -> MatchInfo
# Create a MatchInfo object from the scraped data and additional information.

def create_match_info(page: Page, home_team: str, away_team: str, match_time: str, home_score: str, away_score: str):
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

    """return MatchInfo(
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
    )"""


# ============================================================
# Country, League, Match round

# get_country_and_league: Page -> tuple
# scrape a given page and return a tuple of strings containing the country the league
#       is in, league name and the match round

def get_country_and_league(page: Page) -> tuple:
    details = page.locator(".detail__breadcrumbs li").all()
    country = details[1].inner_text().strip().lower()
    league, game_round = split_string(details[2].inner_text().strip().lower())
    return country, league, game_round


# ===========================================================
# Home team, Away team, score, date, time

# get_teams_info: Page -> tuple
# scrape a given page and return a tuple of strings containing the home team name,
#       away team name, date and time the match will play or played

def get_teams_info(page: Page) -> tuple:
    home_team = page.locator(".duelParticipant__home .participant__participantName a").first.inner_text().strip()
    away_team = page.locator(".duelParticipant__away .participant__participantName a").first.inner_text().strip()
    home_score, away_score = parse_score(page.locator(".detailScore__wrapper").inner_text().strip())
    match_time = page.locator(".duelParticipant__startTime div").first.inner_text().strip()
    date, time = parse_date_dd_mm_yyyy(match_time)

    return home_team, away_team, home_score, date, time