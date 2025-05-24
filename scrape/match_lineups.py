# Functions to retrieve lineups from a match page

from playwright.sync_api import Page, Locator
from .utils import scrape_locator_lists, scrape_text_content, scrape_attributes
from .player import scrape_player_data
from .coach import scrape_coach_data
from .data import Player, MatchLineups, Coach
import re

SUB_IDENTIFIER = {
    "home": "wcl-lineupsParticipantsSubstitution-left", 
    "away": "wcl-lineupsParticipantsSubstitution-right"
}

SUB_CLASS = ".lf__sidesBox .lf__sides .lf__side div .wcl-container_sFO2v"

LINEUP_IDENTIFIER = {
    "home": "wcl-lineupsParticipantGeneral-left",
    "away": "wcl-lineupsParticipantGeneral-right"
}

LINEUP_CLASS = ".lf__sidesBox .lf__sides .lf__side div .wcl-participant_QKIld"


# Page -> tuple
# scrape and return team formations return None if error
async def get_formations(page: Page) -> tuple:
    team_formation = await scrape_text_content(page, ".section .wcl-headerSection_5507A")
    if "formation" in team_formation.lower():
        formations = re.split(r"formation", team_formation.lower())
        return formations[0], formations[1]
    
    return None, None
    

# Page -> tuple
# scrape and return team ratings return None if error
async def get_team_ratings(page: Page) -> tuple:
    team_ratings = await page.locator(".section .lf__fieldWrap .lf__field .lf__teamRatingWrapper--WCL").all_text_contents()
    if team_ratings:
        return team_ratings[0], team_ratings[1]
    
    return None, None

# Page, Locator -> Player
# scrape player data from the given locator    
async def get_player_data(page: Page, link_locator: Locator, func) -> Player | Coach:
    try:
        player_link = await scrape_attributes(link_locator, "a", "href")
        player = await func(page, player_link)
        return player
    except Exception as e:
        return None


# Page, Locator -> list
# scrape player data from the given locator and assign to a list based on home/away
#     return None if error
async def get_tuple_list_of_players(page: Page, player_locator: Locator, cls_name: str, identifier: str, func) -> tuple:
    try:
        home_players, away_players = [], []
        home, away = identifier["home"], identifier["away"]

        player_rows = await player_locator.locator(cls_name).all()
        for row in player_rows:
            side = await row.get_attribute("data-testid")
            if home in side:
                player = await get_player_data(page=page, link_locator=row, func=func)
                if player:
                    home_players.append(player)
            
            elif away in side:
                player = await get_player_data(page=page, link_locator=row, func=func)
                if player:
                    away_players.append(player)
        
        return home_players, away_players
    except Exception as e:
        return None, None
    
        
# Page, Page -> MatchLineups
# scrape match lineups from the given page and player page
#     return MatchLineups object with all the data
async def get_match_lineups(page: Page, player_page: Page) -> MatchLineups:
    match_lineups = MatchLineups()

    home_formation, away_formation = await get_formations(page=page)
    home_team_rating, away_team_rating = await get_team_ratings(page=page)

    match_lineups.home_formation = home_formation
    match_lineups.away_formation = away_formation
    match_lineups.home_team_rating = home_team_rating
    match_lineups.away_team_rating = away_team_rating

    header_mapping = {
        "starting":      ("starting", LINEUP_CLASS, LINEUP_IDENTIFIER, scrape_player_data),
        "substituted":   ("substituted", SUB_CLASS, SUB_IDENTIFIER, scrape_player_data),
        "substitutes":   ("substitutes", LINEUP_CLASS, LINEUP_IDENTIFIER, scrape_player_data),
        "missing":       ("missing", LINEUP_CLASS, LINEUP_IDENTIFIER, scrape_player_data),
        "coaches":       ("coaches", LINEUP_CLASS, LINEUP_IDENTIFIER, scrape_coach_data),
        "predicted":     ("predicted", LINEUP_CLASS, LINEUP_IDENTIFIER, scrape_player_data),
        "questionable":  ("questionable", LINEUP_CLASS, LINEUP_IDENTIFIER, scrape_player_data),
        "will not play": ("will_not_play", LINEUP_CLASS, LINEUP_IDENTIFIER, scrape_player_data),
    }
    
    lineups_locators = await scrape_locator_lists(page=page, selector=".lf__lineUp .section")
    for lineup_row in lineups_locators:
        header = await scrape_text_content(loc=lineup_row, cls_name=".wcl-headerSection_5507A")
        header = header.lower()

        for keyword, (key, cls_name, identifier, func) in header_mapping.items():
            if keyword in header:
                home_data, away_data = await get_tuple_list_of_players(
                    page=player_page,
                    player_locator=lineup_row,
                    cls_name=cls_name,
                    identifier=identifier,
                    func=func,
                )
                home, away = "home_" + key, "away_" + key
                setattr(match_lineups, home, home_data)
                setattr(match_lineups, away, away_data)

                if key == "starting":
                    print(f"Home Starting: {home_data}, Away Starting: {away_data}")
                break
    
    return match_lineups