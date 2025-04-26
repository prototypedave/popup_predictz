from .data_def.Match import MatchInfo
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from .utils.data_rep import parse_score, parse_list_details, parse_date_dd_mm_yyyy, split_string
from .utils.util import append_to_list
from API.weather import get_weather
from dotenv import load_dotenv
import os

load_dotenv()

# ==============================================================
# Scraper for match data
# ==============================================================

# Scrape match data from the provided link
# scrape_match_data_from_link: (page: Page, link: str) -> MatchInfo

def scrape_match_data_from_link(page: Page, link: str) -> MatchInfo:
    """
        Scrape match data from the provided link.

        Args:
            page (Page): The Playwright page object to scrape data from.
            link (str): The link to the match page.

        Returns:
            MatchInfo: An instance of MatchInfo containing the scraped data.
    """
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
    """
        Scrape loadable match data from the provided page.

        Args:
            page (Page): The Playwright page object to scrape data from.

        Returns:
            MatchInfo: An instance of MatchInfo containing the scraped data.
    """
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
        print("Timeout error while scraping match data.")
        return None

   
# Page, str, str, str, str, str -> MatchInfo
# create_match_info: Page, str, str, str, str, str -> MatchInfo
# Create a MatchInfo object from the scraped data and additional information.

def create_match_info(page: Page, home_team: str, away_team: str, match_time: str, home_score: str, away_score: str) -> MatchInfo:
    """
        Create a MatchInfo object from the scraped data and additional information.

        Args:
            page (Page): The Playwright page object to scrape data from.
            home_team (str): The home team name.
            away_team (str): The away team name.
            match_time (str): The match time.
            extra_match_info (dict): Additional match information.

        Returns:
            MatchInfo: An instance of MatchInfo containing the scraped data.
    """
    details = page.locator(".detail__breadcrumbs li").all()
    country = details[1].inner_text().strip().lower()
    league, game_round = split_string(details[2].inner_text().strip().lower())
    date, time = parse_date_dd_mm_yyyy(match_time)

    extra_match_info = scrape_loadable_match_data(page)
    
    if extra_match_info is None:
        return None
      
    try:
        condition = get_weather(os.getenv("WEATHER_API"), extra_match_info.get('venue'), date, time)
    except Exception as e:
        print(f"Error fetching weather data: {e}")
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
