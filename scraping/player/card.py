from playwright.sync_api import Page
from .player import scrape_player_data
from ..data_def.Match import CardData, PlayerData


# =================================================================
# Get player who received a card

# get_player_card: (page: Page, event) -> PlayerData
# interp. Returns PlayerData object of the player who received a card by scraping
#       the player link from the events locator.

def get_player_card(page: Page, event) -> PlayerData:
    try:
        player_link = event.locator(".smv__playerName").get_attribute("href")
        player = scrape_player_data(page, player_link)
        return player
    except Exception as e:
        return None


# =================================================================
# Check if it was a card and return card data if it was
# =================================================================

# get_card: (page: Page, event) -> CardData
# interp. checks if the event is a card by checking the class of the element
#       returns CardData object if it was a card else returns None

def get_card(page: Page, event) -> CardData:
    try:
        card_check = event.locator(".smv__incident .smv__incidentIcon svg").get_attribute("class")
        if card_check and "yellow" in card_check:
            player = get_player_card(page, event)
            
            if player is not None:        
                return CardData(player=player, card_type="yellow")

        elif card_check and "red" in card_check:
            player = get_player_card(page, event)

            if player is not None:
                return CardData(player=player, card_type="red")

        return None
    except Exception as e:
        return None
