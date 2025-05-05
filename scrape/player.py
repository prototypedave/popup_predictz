# Scrapper to get player's data
from playwright.sync_api import Page
from .data import Player
from .constants import FLASHSCORE
from .utils import scrape_text_content, scrape_locator_lists
from .func_util import parse_bracket

def scrape_player_data(page: Page, player_link: str) -> Player:
    try:
        link = FLASHSCORE + player_link
        page.goto(link)
        page.wait_for_selector(".player-profile-heading")
        country = page.locator(".player-profile-heading nav li").last.text_content().lower()
        name = scrape_text_content(page, ".playerHeader__nameWrapper h2")
        position = scrape_text_content(page, ".playerTeam strong")
        team = scrape_text_content(page, ".playerTeam a")
        player_info = scrape_locator_lists(page, ".playerInfoItem span")
        dob = player_info[1].text_content().lower() 

        return  PlayerData(name=name, position=position,
                nationality=country, team=parse_bracket(team), dob=parse_bracket(dob))





