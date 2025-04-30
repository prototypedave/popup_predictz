from playwright.sync_api import Page
from .data_def.Match import IncidentData
from .player.goal import get_goal
from .player.card import get_card
from .player.sub import get_player_substituted


# =================================================================
# Get match incident data
# =================================================================

# get_match_incident: (page: Page, event) -> MatchIncident
# interp. returns MatchIncident object if it was a goal, card or
#       substitution else returns None

def get_match_incident(page: Page, event):
    try:
        minute = event.locator(".smv__incident .smv__timeBox").inner_text().strip()
        goal = get_goal(page, event)
        if goal is None:
            card = get_card(page, event)
            if card is None:
                substitution = get_player_substituted(page, event)
                return IncidentData(time=minute, card=None, substitution=substitution, goal=None)
            else:
                return IncidentData(time=minute, card=card, substitution=None, goal=None)
        else:
            return IncidentData(time=minute, card=None, substitution=None, goal=goal)
    except Exception as e:
        return None


