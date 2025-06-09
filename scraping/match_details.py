# Scrape Country, League and Round
from playwright.sync_api import Page
from utilities.locator_lists import get_locator_lists
from utilities.strings import split_string_with_hyphen

# Page -> tuple
# scrape league name, country name and game round from page and 
#   return a tuple of these items
async def get_match_details(page: Page) -> tuple:
    header_items = await get_locator_lists(page, ".detail__breadcrumbs li")

    if len(header_items) < 3:
        return None, None, None
    
    country = (await header_items[1].inner_text()).strip().lower()
    league_round = (await header_items[2].inner_text()).strip().lower()
    league, round = split_string_with_hyphen(league_round)

    return country, league, round