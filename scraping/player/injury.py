from playwright.sync_api import Page
from ..data_def.Match import InjuredData, MissingPlayersData
from .player import scrape_player_data


# ===========================================================
# Injured or Missing Players
# ===========================================================

# get_missing_or_injured_players: page -> MissingPlayersData
# produces a list of players who will not play a given match

def get_missing_or_injured_players(page: Page) -> MissingPlayersData:
    try:
        page.wait_for_selector(".loadable__section .lf__sidesBox .lf__sides .lf__side .wcl-participant_QKIld")
        lf_side = page.locator(".lf__sidesBox .lf__sides .lf__side .wcl-participant_QKIld").all()
        if lf_side:
            home, away = [], []
            for lf in lf_side:
                attr = lf.get_attribute('data-testid')
                if attr:
                    if 'left' in attr:
                        link = lf.locator('a').get_attribute('href')
                        reason = lf.locator('span').text_content().lower()
                        player = scrape_player_data(page, link)
                        home.append(InjuredData(player=player, reason=reason))
                    elif 'right' in attr:
                        link = lf.locator('a').get_attribute('href') 
                        player = scrape_player_data(page, link)
                        away.append(InjuredData(player=player, reason=reason))
            if home or away:
                return MissingPlayersData(home=home, away=away)

        return None
    except Exception as e:
        print(f"Error injured {e}")
        return None        
