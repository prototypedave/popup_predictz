from playwright.sync_api import Page
from ..data_def.Match import PlayerData
from ..utils.data_rep import parse_bracket
from dotenv import load_dotenv
import os

load_dotenv()

# ================================================================
# Scrape Player Data
# ================================================================

# scrape_player_data: (page: Page, player_link: str) -> PlayerData
# interp. Scrapes player data from the given player link and returns 
#       a PlayerData object containing name of the player, team,
#       position, country, and date of birth.

def scrape_player_data(page: Page, player_link: str) -> PlayerData:
    try:
        link = os.getenv("SITE") + player_link
        page.goto(link)
        page.wait_for_selector(".player-profile-heading")
        country = page.locator(".player-profile-heading nav li").last.text_content().lower()
        name = page.locator(".playerHeader__nameWrapper h2").text_content().lower()
        position = page.locator(".playerTeam strong").text_content().lower()
        team = page.locator(".playerTeam a").text_content().lower()   
        playerInfo = page.locator(".playerInfoItem span").all()
        dob = playerInfo[1].text_content().lower() 
        
        return  PlayerData(name=name, position=position,
                nationality=country, team=parse_bracket(team), date_of_birth=parse_bracket(dob))
    except Exception as e:
        print(f"Scraping player data error: {e}")
        return None