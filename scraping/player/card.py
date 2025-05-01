from playwright.sync_api import Page
from .player import scrape_player_data
from ..data_def.Match import CardData
from ..utils.util import safe_get_attribute


# =================================================================
# Check if it was a card and return card data if it was
# =================================================================

# get_card: (page: Page, event, c_type) -> CardData
# interp. checks if the event is a card by checking the class of the element
#       returns CardData object if it was a card else returns None

def get_card(page: Page, event, c_type: str) -> CardData:
    player_link = safe_get_attribute(event, ".smv__playerName", "href")
    player = scrape_player_data(page, player_link)
    return CardData(player=player, card_type=c_type)
