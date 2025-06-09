# Class to scrape flashscore data
import asyncio
from playwright.async_api import async_playwright, Page
from .utils import scrape_locator_lists, scrape_attributes
from .match_summary import get_match_summary, match_info, game_country_and_league, scrape_additional_match_info
from .constants import *
from .func_util import is_valid_url, assemble_url
from .match_stats import get_match_stats
from .match_lineups import get_match_lineups
from .player_stats import get_player_stats
from .match_odds import get_match_odds
import time, re
from database.model import setup_database, ASYNC_DATABASE_URL
from database.game import add_game, is_game_already_saved
from database.stats import add_stats
from database.team import add_team, get_team_by_name
from .data import has_none_values
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.queries import *

# Flashscore -> Matches
# scrape a list of matches with there data

from playwright.async_api import async_playwright
import asyncio


class Scraper:
    def __init__(self, browser, concurrency=2):
        self.browser = browser
        self.semaphore = asyncio.Semaphore(concurrency)
        self.engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
        self.AsyncSessionLocal = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def process_event(self, page):
        try:
            country, league, round = await game_country_and_league(page)
            if country in ["world", "africa", "europe", "asia", "south america"]:
                return
            
            h2h_url = ""
            if is_valid_url(page.url, "/match-summary/match-summary"):
                h2h_url = assemble_url(page.url, "/match-summary/match-summary", H2H_OVERALL)    
            else:
                h2h_url = assemble_url(page.url, "/match-summary", H2H_OVERALL)

            await page.goto(h2h_url)
            await page.wait_for_selector(".h2h__section")

            h2h_locator = await page.locator(".h2h__section").all()
            for h2h in h2h_locator:
                while True:
                    try:
                        await page.click(".showMore")
                    except Exception as e:
                        break
                h2h_games = await page.locator(".h2h__row").all()
                for i in range(len(h2h_games)):
                    try:
                        game_item = page.locator(".h2h__row").nth(i)

                        async with page.expect_navigation(timeout=5000):
                            await game_item.click()

                        saved_to_db = await self.scrape_match(page)
                        if not saved_to_db:
                            continue

                        await page.go_back()
                        await page.wait_for_selector(".h2h__row")
                    except Exception as e:
                        print(f"H2h head error: {e}")
                        break
            
            
            return country
        except Exception as e:
            print(f'{page.url}: {e}')

    async def scrape_match(self, page):
        try:
            async with self.AsyncSessionLocal() as session:
                await page.wait_for_selector(".duelParticipant")
                country, league, round = await game_country_and_league(page)
                home, away, home_score, away_score, start_time = await match_info(page)

                home_team = await get_team_by_name(session, home, country)
                away_team = await get_team_by_name(session, away, country)
                
                if home_team and away_team:
                    game_present = await is_game_already_saved(session, home_team.id, away_team.id)
                    if game_present:
                        return False
                    
                else:
                    home_team_info = {
                        "name": home,
                        "country": country,
                    }

                    away_team_info = {
                        "name": away,
                        "country": country
                    }
                    if not home_team:
                        home_team = await add_team(session, home_team_info)
                    if not away_team:
                        away_team = await add_team(session, away_team_info)


                # To be used later
                additional_info = await scrape_additional_match_info(page)

                if not additional_info:
                    return False
                
                venue = additional_info.get('venue')
                referee = additional_info.get('referee')
                capacity = additional_info.get('capacity')
                if not venue and not referee and not capacity:
                    return False
                
                if capacity:
                    capacity = re.sub(r'\s', '', capacity)

                stats_url = assemble_url(page.url, "/match-summary", STATS_FULL_TIME)
                try:
                    await page.goto(stats_url)
                    await page.wait_for_selector(".container__livetable .container__detailInner .section")
                        
                    stats = await get_match_stats(page)
                    if not stats or has_none_values(stats):
                        await page.go_back()
                        await page.wait_for_selector(".duelParticipant")
                        await session.rollback()
                        return False
                        
                    game = {"start_time":start_time, "league":league, "home_team":home_team, 
                        "away_team":away_team, "home_score":home_score, "away_score":away_score, 
                        "round":round, "capacity":int(capacity), "referee":referee, "venue":venue, "country":country}
                                                
                    db_game = await add_game(session, game)
                    await add_stats(session, stats, game_id=db_game.id)
                    await session.commit()

                    await page.go_back()
                    await page.wait_for_selector(".duelParticipant")
                    return True
                except Exception as e:
                    print(f"Stats : {e}")
                    await page.go_back()
                    await page.wait_for_selector(".duelParticipant")
                    await session.rollback()
                    return False

        except Exception as e:
            print(f"Match detail error: {e}")

    async def start_db(self):
        await setup_database()

    async def get_starts_df(self):
        async with self.AsyncSessionLocal() as session:
            df = await get_all_game_stats_df(session)
            print(df.head())
            df.to_csv("todays_stats.csv", index=False)


    async def scrape_flashscore(self, url):
        page = await self.browser.new_page()
        await page.goto(url)
        await page.wait_for_selector(".container__liveTableWrapper")
        await page.click(".calendar__navigation--yesterday")
        await page.wait_for_selector(".event__match")
        events = await page.locator(".event__match").all()

        #tasks = []
        for event in events:
            href = await scrape_attributes(event, "a", "href")
            if href:
                new_page = await self.browser.new_page()
                await new_page.goto(href)
                await new_page.wait_for_selector(".duelParticipant")
                await self.process_event(new_page)
                await new_page.close()

        #all_h2h_links = await asyncio.gather(*tasks)
        await page.close()

        # Flatten the list of lists
        #return [link for sublist in all_h2h_links for link in sublist]

    async def scrape_flashscore_today(self, url):
        async def process_event_with_semaphore(event):
            async with self.semaphore:  
                href = await scrape_attributes(event, "a", "href")
                if href:
                    new_page = await self.browser.new_page()
                    await new_page.goto(href)
                    await new_page.wait_for_selector(".duelParticipant")
                    await self.process_event(new_page)
                    await new_page.close()

        page = await self.browser.new_page()
        await page.goto(url)
        await page.wait_for_selector(".event__match")
        events = await page.locator(".event__match").all()

        # Create tasks for processing events with controlled concurrency
        tasks = [process_event_with_semaphore(event) for event in events]
        await asyncio.gather(*tasks)

        await page.close()

    async def scrape_multiple(self, urls):
        for url in urls:
            await self.scrape_flashscore(url)

    

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        scraper = Scraper(browser)
        await scraper.start_db()
        urls = ["https://www.flashscore.com/"]
        await scraper.scrape_multiple(urls)
        #await scraper.get_starts_df()
        
        await browser.close()



if __name__ == "__main__":
    """async def main():
        scraper = FlashScoreScraper()
        start = time.time()
        results = await scraper.run("https://www.flashscore.com/")
        #for res in results:
        #    print(res)
        end = time.time()
        print(f"Time taken: {end - start:.2f} seconds")
    """

    asyncio.run(main())




