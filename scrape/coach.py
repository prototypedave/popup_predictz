# Scrape the coach page of a website

from playwright.sync_api import Page
from .data import Coach
from .constants import FLASHSCORE
from .utils import scrape_text_content
from .func_util import parse_bracket

# Page, str -> CoachInfo
# scrapes coaches information from the provided link if its a valid link
#   returns CoachInfo
async def scrape_coach_data(page: Page, coach_link: str) -> Coach | None:
    try:
        link = FLASHSCORE + coach_link
        await page.goto(link)
        await page.wait_for_selector(".player-profile-heading")

        country_el = page.locator(".player-profile-heading nav li").last
        country_text = await country_el.text_content()
        country = country_text.strip().lower() if country_text else None

        name = await scrape_text_content(page, ".playerHeader__nameWrapper h2")
        team = await scrape_text_content(page, ".playerTeam a")

        player_info = await page.locator(".playerInfoItem span").all()
        dob = None
        if len(player_info) >= 2:
            dob_raw = await player_info[1].text_content()
            dob = parse_bracket(dob_raw.strip()) if dob_raw else None

        return Coach(
            name=name,
            dob=dob,
            team=parse_bracket(team),
            country=country
        )
    except Exception as e:
        return None

