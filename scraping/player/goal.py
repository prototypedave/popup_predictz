from .player import scrape_player_data
from playwright.sync_api import Page
from ..data_def.Match import GoalData, PlayerData

# ================================================================
# Get player who scored

# get_player_scored: (page: Page, event) -> PlayerData
# interp. Returns PlayerData object of the player who scored by scraping
#       the player link from the events locator.

def get_player_scored(page: Page, event) -> PlayerData:
    try:
        player_link = event.locator(".smv__playerName").get_attribute("href")
        player = scrape_player_data(page, player_link)
        return player
    except Exception as e:
        return None


# =================================================================
# Get player who assisted a goal

# get_player_assisted: (page: Page, event) -> PlayerData
# interp. Returns PlayerData object of the player who assisted by scraping
#       the player link from the events locator.

def get_player_assisted(page: Page, event) -> PlayerData:
    try:
        player_link = event.locator(".smv__assist").get_attribute("href")
        player = scrape_player_data(page, player_link)
        return player
    except Exception as e:
        return None


# =================================================================
# check if goal was a penalty

# is_goal_penalty: Locator -> bool
# checks if the goal was a penalty by checking the class of the element returns True 
#       if it was a penalty else returns False

def is_goal_penalty(event) -> bool:
    try:
        penalty = event.locator(".smv__subIncident").inner_text().strip()
        if penalty:
            return True if "penalty" in penalty else False
    except Exception:
        return False


# =================================================================
# Check if it was a goal and return goal data if it was
# =================================================================

# get_goal: (page: Page, event) -> bool
# interp. checks if the event is a goal by checking the class of the element
#       returns GoalData object if it was a goal else returns None

def get_goal(page: Page, event) -> GoalData:
    try:
        goal_check = event.locator(".smv__incidentIcon svg").get_attribute("data-testid")
        if goal_check and "soccer" in goal_check:
            scorer = get_player_scored(page, event)

            if scorer is not None:
                assist = get_player_assisted(page, event)
                if assist is not None:
                    return GoalData(scorer=scorer, assist=assist, penalty=False) 
                else:
                    return GoalData(scorer=scorer, assist=None, penalty=is_goal_penalty(event))
            
        return None
    except Exception as e:
        return None