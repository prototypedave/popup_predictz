from playwright.sync_api import Page
from .data_def.Match import IncidentData
from .player.goal import get_goal
from .player.card import get_card
from .player.sub import get_player_substituted
from .utils.util import safe_get_attribute, safe_get_text

# =================================================================
# Get match incident data
# =================================================================

# get_match_incident: (page: Page, event) -> MatchIncident
# interp. returns IncidentData object if it was one of a goal, card or
#       substitution else returns None

def get_match_incident(page: Page, event):
    minute = safe_get_text(event, ".smv__incident .smv__timeBox")

    check_sub_class = safe_get_attribute(event, ".smv__incident .smv__incidentIconSub", "class")
    if check_sub_class is not None:
        sub = get_player_substituted(page, event)
        return IncidentData(time=minute, goal=None, card=None, substitution=sub)

    card_attr = safe_get_attribute(event, ".smv__incidentIcon svg", "class")
    if card_attr is not None:
        if "yellow" in card_attr:
            card = get_card(page, event, 'yellow')
            return IncidentData(time=minute, goal=None, card=card, substitution=None)
        elif "red" in card_attr:
            card = get_card(page, event, 'red')
            return IncidentData(time=minute, goal=None, card=card, substitution=None)

    goal_attr = safe_get_attribute(event, ".smv__incidentIcon svg", "data-testid")
    if "soccer" in goal_attr:  
        goal = get_goal(page, event)
        return IncidentData(time=minute, goal=goal, card=None, substitution=None)

    return None 
    


        
