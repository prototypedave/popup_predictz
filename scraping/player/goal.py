from .player import scrape_player_data
from playwright.sync_api import Page
from ..data_def.Match import GoalData, PlayerData
from ..utils.util import safe_get_attribute, safe_get_text

# ===============================================================
# get goal attributes

# get_goal_attributes: (event: Locator) -> dict
# interp. cache all possible goal attributes
#       - goal -> str        # scorer link
#       - assist -> str      # assist link
#       - pen -> str         # penality data

def get_goal_attributes(event) -> dict:
    return {
        "goal": safe_get_attribute(event, ".smv__playerName", "href"),
        "assist": safe_get_attribute(event, ".smv__assist a", "href"),
        "pen": safe_get_text(event, ".smv__subIncident")
    }

# =================================================================
# Check if it was a goal and return goal data if it was
# =================================================================

# get_goal: (page: Page, event) -> bool
# interp. checks if the event is a goal by checking the class of the element
#       returns GoalData object if it was a goal else returns None

def get_goal(page: Page, event) -> GoalData:
    goal_attributes = get_goal_attributes(event)
    scorer_link = goal_attributes['goal']

    if scorer_link is not None:
        pen =  True if "penalty" in goal_attributes['pen'] else False
        scorer = scrape_player_data(page, scorer_link)
        assist_link = goal_attributes['assist']

        if assist_link is not None:
            assist = scrape_player_data(page, assist_link)
        else:
            assist = None

        return GoalData(scorer=scorer, assist=assist, penality=pen)    