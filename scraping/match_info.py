# Gets match information like team and start time

from playwright.sync_api import Page
from datetime import datetime
from utilities.locator_text import get_text_content
from utilities.strings import split_score_string

# Page -> tuple
# scrape home and away team name, home and away score and time of the match
async def get_match_info(page: Page) -> tuple:
    home_team = await get_text_content(page, ".duelParticipant__home .participant__participantName a")
    away_team = await get_text_content(page, ".duelParticipant__away .participant__participantName a")
    score = await get_text_content(page, ".detailScore__wrapper")
    time_str = await get_text_content(page, ".duelParticipant__startTime div")
    home_score, away_score = split_score_string(score_text=score)
    time = datetime.strptime(time_str, "%d.%m.%Y %H:%M")

    return home_team, away_team, home_score, away_score, time