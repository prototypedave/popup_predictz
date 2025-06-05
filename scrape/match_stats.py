# Functions to scrape stats from matches that have already played
from .constants import STAT_MAP, EXTRA_STATS_MAP
from playwright.sync_api import Page
from .utils import scrape_locator_lists, scrape_text_content
from .func_util import remove_ambigious_characters, split_digit
from .data import MatchStats

# Page -> MatchStats
# scrape match stats from the page and return a dictionary of stats
async def get_match_stats(page: Page) -> MatchStats:
    try:
        stats = MatchStats()
        stats_rows = await scrape_locator_lists(page, (".container__livetable .container__detailInner .section .wcl-row_OFViZ"))
        print(len(stats_rows))
        
        # Avoid matches that start with this, as they dont have full stats
        first_value = "ball possession"
        for row in stats_rows:
            home_val = await scrape_text_content(row, ".wcl-homeValue_-iJBW") 
            category = await scrape_text_content(row, ".wcl-category_ITphf .wcl-category_7qsgP")
            away_val = await scrape_text_content(row, ".wcl-awayValue_rQvxs")

            if first_value == category.lower():
                return None  # Early termination
            first_value = "Unknown"

            for keyword, key in STAT_MAP.items():
                if keyword in category.lower():
                    if "x" in key[0] or "prevented" in category.lower():
                        setattr(stats, key[0], float(remove_ambigious_characters(home_val)))
                        setattr(stats, key[1], float(remove_ambigious_characters(away_val)))
                    else:
                        setattr(stats, key[0], int(remove_ambigious_characters(home_val)))
                        setattr(stats, key[1], int(remove_ambigious_characters(away_val)))
                    break

            for keyword, key in EXTRA_STATS_MAP.items():
                if keyword == category.lower():
                    home_percentage, home_successful_passes, home_total_passes = split_digit(home_val)
                    away_percentage, away_successful_passes, away_total_passes = split_digit(away_val)
                    setattr(stats, key['home'][0], int(home_percentage))
                    setattr(stats, key['home'][1], int(home_successful_passes))
                    setattr(stats, key['home'][2], int(home_total_passes))
                    setattr(stats, key['away'][0], int(away_percentage))
                    setattr(stats, key['away'][1], int(away_successful_passes))
                    setattr(stats, key['away'][2], int(away_total_passes))
                    break
        return stats
    except Exception as e:
        print(e)