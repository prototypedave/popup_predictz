from playwright.sync_api import Page
from .player import scrape_player_data
from ..data_def.Match import SubstitutionData
from ..utils.util import safe_get_attribute

# =================================================================
# Get player who substituted

# get_player_substituted: (page: Page, event) -> SubstitutionData
# interp. Returns PlayerData objects of the player who was substituted 
#       and the player who substituted

def get_player_substituted(page: Page, event) -> SubstitutionData:
    player_out_link = safe_get_attribute(event, ".smv__incidentSubOut a", "href")
    player_in_link = event.locator(".smv__incident a").first.get_attribute("href")
            
    if player_in_link and player_out_link:
        player_out = scrape_player_data(page, player_out_link)
        player_in = scrape_player_data(page, player_in_link)
        return SubstitutionData(player_out=player_out, player_in=player_in)
        