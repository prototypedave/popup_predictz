# Scrape all odds data

from playwright.sync_api import Page
from .utils import scrape_locator_lists, scrape_text_content
from .data import ODDS_DICT
import re

# Used to get respective dataclasses, links and dataclass names
ODD_LINK_NAMES = ["1x2", "over_under", "asian_handicap", "btts", "double_chance", "ood_even", "draw_no_bet", "correct_score", "halftime_fulltime"]

# Dict for respective dataclass names
ODD_TYPES = {
    "halftime_fulltime": {
        "1/1" : "home_home",
        "1/x" : "home_draw",
        "1/2" : "home_away",
        "x/1" : "draw_home",
        "x/x" : "draw_draw",
        "x/2" : "draw_away",
        "2/1" : "away_home",
        "2/2" : "away_away",
        "2/x" : "away_draw"
    },
    "correct_score": {
        "1:0" : "home_one_zero",
        "2:0" : "home_two_zero",
        "2:1" : "home_two_one",
        "3:0" : "home_three_zero",
        "3:1" : "home_three_one",
        "3:2" : "home_three_two",
        "4:0" : "home_four_zero",
        "4:1" : "home_four_one",
        "4:2" : "home_four_two",
        "4:3" : "home_four_three",
        "0:0" : "draw_zero_zero",
        "1:1" : "draw_one_one",
        "2:2" : "draw_two_two",
        "3:3" : "draw_three_three",
        "0:1" : "away_zero_one",
        "0:2" : "away_zero_two",
        "1:2" : "away_one_two",
        "0:3" : "away_zero_three",
        "1:3" : "away_one_three",
        "2:3" : "away_two_three",
        "0:4" : "away_zero_four",
        "1:4" : "away_one_four",
        "2:4" : "away_two_four",
        "3:4" : "away_three_four",
    },
    "draw_no_bet": {
        "full_home" : "full_time_home",
        "full_away" : "full_time_away",
        "1st_half_home" : "half_time_home",
        "1st_half_away" : "half_time_away" 
    },
    "odd_even": {
        "full_home": "odd",   # use home for odd and away even for code refactor
        "full_away": "even",
        "1st_half_home": "first_half_odd",
        "1st_half_away": "first_half_even",
        "2nd_half_home": "second_half_odd",
        "2nd_half_away": "second_half_even"
    },
    "double_chance" : {
        "full_home": "full_time_home_draw",
        "full_draw": "full_time_home_away",
        "full_away": "full_time_draw_away",
        "1st_half_home": "first_half_home_draw", 
        "1st_half_away": "first_half_draw_away",
        "1st_half_draw": "first_half_home_away",
        "2nd_half_home": "second_half_home_draw", 
        "2nd_half_away": "second_half_draw_away",
        "2nd_half_draw": "second_half_home_away",
    },
    "btts": {
        "full_home": "yes",
        "full_away": "no",
        "1st_half_home": "first_half_yes",
        "1st_half_away": "first_half_no",
        "2nd_half_home": "second_half_yes",
        "2nd_half_away": "second_half_no",
    },
    "asian_handicap": {
        "full_home-2": "home_two_goals",
        "full_home-1": "home_one_goal",
        "full_away-2": "away_two_goals",
        "full_away-1": "away_one_goal",
        "1st_half_home-1": "first_half_home_one_goal",
        "1st_half_away-1": "first_half_away_one_goal",
        "2nd_half_home-1": "second_half_home_one_goal",
        "2nd_half_away-1": "second_half_away_one_goal", 
    },
    "over_under": {
        "full_home0.5": "over_zero_five",
        "full_home1.5": "over_one_five",
        "full_home2.5": "over_two_five",
        "full_home3.5": "over_three_five",
        "full_home4.5": "over_four_five",
        "full_home5.5": "over_five_five",
        "full_home6.5": "over_six_five",
        "1st_half_home0.5": "first_half_over_zero_five",
        "1st_half_home1.5": "first_half_over_one_five",
        "1st_half_home2.5": "first_half_over_two_five",
        "2nd_half_home0.5": "second_half_over_one_five",
        "2nd_half_home1.5": "second_half_over_one_five",
        "2nd_half_home2.5": "second_half_over_two_five",
        "full_away0.5": "under_zero_five",
        "full_away1.5": "under_one_five",
        "full_away2.5": "under_two_five",
        "full_away3.5": "under_three_five",
        "full_away4.5": "under_four_five",
        "full_away5.5": "under_five_five",
        "full_away6.5": "under_six_five",
        "1st_half_away0.5": "first_half_under_zero_five",
        "1st_half_away1.5": "first_half_under_one_five",
        "1st_half_away2.5": "first_half_under_two_five",
        "2nd_half_away0.5": "second_half_under_one_five",
        "2nd_half_away1.5": "second_half_under_one_five",
        "2nd_half_away2.5": "second_half_under_two_five",
    },
    "1x2": {
        "full_home" : "fulltime_home",
        "full_away" : "fulltime_away",
        "full_draw" : "fulltime_draw",
        "1st_half_home" : "first_half_home",
        "1st_half_draw" : "first_half_draw",
        "1st_half_away" : "first_half_away",
        "2nd_half_home" : "second_half_home",
        "2nd_half_away" : "second_half_away",
        "2nd_half_draw" : "second_half_draw",
    }
}

# Links for different odds
ODD_LINKS = {
    "halftime_fulltime" : "#/odds-comparison/ht-ft/full-time",
    "correct_score" : "#/odds-comparison/correct-score/full-time",
    "draw_no_bet": ["#/odds-comparison/draw-no-bet/full-time", "#/odds-comparison/draw-no-bet/1st-half"],
    "odd_even": ["#/odds-comparison/odd-even/full-time", "#/odds-comparison/odd-even/1st-half", "#/odds-comparison/odd-even/2nd-half"],
    "double_chance": ['#/odds-comparison/double-chance/full-time', '#/odds-comparison/double-chance/1st-half', '#/odds-comparison/double-chance/2nd-half'],
    "btts": ['#/odds-comparison/both-teams-to-score/full-time', '#/odds-comparison/both-teams-to-score/1st-half', '#/odds-comparison/both-teams-to-score/2nd-half'],
    "asian_handicap": ["#/odds-comparison/asian-handicap/full-time", "#/odds-comparison/asian-handicap/1st-half", "#/odds-comparison/asian-handicap/2nd-half"],
    "over_under": ["#/odds-comparison/over-under/full-time", "#/odds-comparison/over-under/1st-half", "#/odds-comparison/over-under/2nd-half"],
    "1x2": ["#/odds-comparison/1x2-odds/full-time", "#/odds-comparison/1x2-odds/1st-half", "#/odds-comparison/1x2-odds/2nd-half"]
}

# Classes for odds page
SELECTOR = ".container__livetable .container__detailInner .oddsTab__tableWrapper"


# Page, str, class, str, str, str, str 
# Scrapes odds from the provided link, sets the odds with the given respective key 
#       names to the provided dataclass set values
async def get_odds(page: Page, href: str, odd_class, odd_type: str, home_key: str, away_key: str, draw_key: str):
    await page.goto(href)
    await page.wait_for_selector(SELECTOR)
    odds_row = await scrape_locator_lists(page=page, selector=".ui-table__row")
    dup_checker = ""
        
    for row in odds_row:
        odds_locator = await row.locator(".oddsCell__odd").all()
        odd_name = await scrape_text_content(loc=row, cls_name=".wcl-oddsCell_djZ95")
        
        length_locator = len(odds_locator)
        if dup_checker and odd_name == dup_checker:
            continue

        dup_checker = odd_name
        
        # Get possible odds
        odd1 = await odds_locator[0].text_content()
        odd2, odd3 = None, None
        
        if length_locator == 2:
            odd2 = await odds_locator[1].text_content()
            if odd_name:
                if not hasattr(odd_class, ODD_TYPES[odd_type][home_key + odd_name]):
                    continue
                set_attr(odd_class=odd_class, key_home=ODD_TYPES[odd_type][home_key + odd_name], 
                    key_away=ODD_TYPES[odd_type][away_key + odd_name], odd1=float(odd1), odd2=float(odd2))
                continue
            
            set_attr(odd_class=odd_class, key_home=ODD_TYPES[odd_type][home_key], 
                    key_away=ODD_TYPES[odd_type][away_key], odd1=float(odd1), odd2=float(odd2))
            continue

        if length_locator == 3:
            odd2 = await odds_locator[1].text_content()
            odd3 = await odds_locator[2].text_content()
            set_attr(odd_class=odd_class, key_home=ODD_TYPES[odd_type][home_key], key_away=ODD_TYPES[odd_type][away_key], 
                    odd1=float(odd1), odd2=float(odd2), key_draw=ODD_TYPES[odd_type][draw_key], odd3=float(odd3))
            continue

        # Single Odds
        key = ODD_TYPES[odd_type][odd_name.lower()]
        setattr(odd_class, key, float(odd1))
    return odd_class


# dataclass, str, str, str, float, float, float
# Helper function to set attributes of a dataclass based on the given attributes 
def set_attr(odd_class=None, key_home=None, key_away=None, key_draw=None, odd1=None, odd2=None, odd3=None):
    setattr(odd_class, key_home, float(odd1))
    setattr(odd_class, key_away, float(odd2))
    if key_draw:
        setattr(odd_class, key_draw, float(odd3))


# Page, str -> dict
# Scrapes and return different match odds in a dictionary
async def get_match_odds(page: Page, url: str):
    odds_dict = {} 
    for odd_type in ODD_LINK_NAMES:
        link = ODD_LINKS[odd_type]
        odd_class = ODDS_DICT[odd_type]()

        home, away, draw = None, None, None
        href = None

        if type(link) == list:
            if len(link) == 2:
                for index, lnk in enumerate(link):
                    href = re.sub(r'([#]\/\w+[-]\w+)', lnk, url)
                    if index == 0:
                        home, away = "full_home", "full_away"
                        await get_odds(page, href, odd_class, odd_type, home, away, draw)
                        continue
                    home, away = "1st_half_home", "1st_half_away"
                    await get_odds(page, href, odd_class, odd_type, home, away, draw)
            elif len(link) == 3:
                for index, lnk in enumerate(link):
                    href = re.sub(r'([#]\/\w+[-]\w+)', lnk, url)
                    if index == 0:
                        home, away, draw = "full_home", "full_away", "full_draw"
                        await get_odds(page, href, odd_class, odd_type, home, away, draw)
                    elif index == 1:
                        home, away, draw = "1st_half_home", "1st_half_away", "1st_half_draw"
                        await get_odds(page, href, odd_class, odd_type, home, away, draw)
                        continue
                    home, away, draw = "2st_half_home", "2st_half_away", "2st_half_draw" 
                    await get_odds(page, href, odd_class, odd_type, home, away, draw)

        odds_dict[odd_type] = odd_class
    return odds_dict                   
           
        