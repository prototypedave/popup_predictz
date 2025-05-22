# Functions to scrape stats from matches that have already played
from collections import defaultdict
from .constants import STAT_MAP, EXTRA_STATS_MAP
from playwright.sync_api import Page
from .utils import scrape_locator_lists, scrape_text_content
from .func_util import remove_ambigious_characters, split_string

# Page -> dict
# scrape match stats from the page and return a dictionary of stats
async def get_match_stats(page: Page):
    stats = defaultdict(dict)
    stats_rows = await scrape_locator_lists(page, (".container__livetable .container__detailInner .section .wcl-row_OFViZ"))
    
    for row in stats_rows:
        home_val = await scrape_text_content(row, ".wcl-homeValue_-iJBW") 
        category = await scrape_text_content(row, ".wcl-category_ITphf .wcl-category_7qsgP")
        away_val = await scrape_text_content(row, ".wcl-awayValue_rQvxs")

        for keyword, key in STAT_MAP.items():
            if keyword in category:
                stats[key]["home"] = remove_ambigious_characters(home_val)
                stats[key]["away"] = remove_ambigious_characters(away_val)
                break

        for keyword, key in EXTRA_STATS_MAP.items():
            if keyword in category:
                stats[key]["home"] = split_string(home_val)
                stats[key]["away"] = split_string(away_val)
                break
    
    return stats