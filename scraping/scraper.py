# Main class for scraping all football data and saving to database

from playwright.async_api import async_playwright, Page, ChromiumBrowserContext, Locator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database.model import setup_database, ASYNC_DATABASE_URL
from database.team import get_team_by_name, add_team
from database.game import is_game_already_saved, add_game
from database.stats import add_stats
from database.queries import *
from scrape.utils import scrape_attributes
from .match_stats import get_match_stats
from .match_details import get_match_details
from .match_info import get_match_info
from .extra_match_info import get_extra_match_info
from utilities.url import *
from data.links import H2H_OVERALL, STATS_FULL_TIME
from data.util import has_none_values

import re
import asyncio, time

class Scraper:
    # ChromiumBrowserContext, int -> None
    # It initializes the scraper context by passing the browser context and the number of 
    #       concurrent pages the browser will load at a time (default is 2)
    def __init__(self, browser: ChromiumBrowserContext, concurrency: int = 1) -> None:
        self.browser = browser
        self.semaphore = asyncio.Semaphore(concurrency)
        self.engine = create_async_engine(ASYNC_DATABASE_URL, echo=False) # Enable for debugging
        self.AsyncSessionLocal = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False) # Ensure db stays on after commiting

    # Self -> None
    # starts database instance and create db if its not present (check database.base)
    async def startup(self) -> None:
        await setup_database()

    # Locator -> None
    # Handles page navigation by creating and closing a page for each event and ensuring
    #       concurrent pages are opened at the same time for faster processing. Note: the number
    #       of concurrent pages is toggled by the concurrency parameter in the class initialization
    #       having more pages may affect the performance of the machine with limited resources
    async def page_handler(self, event: Locator) -> None:
        async with self.AsyncSessionLocal() as session:
            async with self.semaphore:
                href = await scrape_attributes(event, "a", "href")
                if href:
                    try:
                        start = time.time()
                        new_page = await self.browser.new_page()
                        await new_page.goto(href, wait_until="domcontentloaded")
                        country, league, round = await get_match_details(page=new_page)
                        home, away, home_score, away_score, start_time = await get_match_info(page=new_page)
                        home_team = await get_team_by_name(session, home, country)
                        away_team = await get_team_by_name(session, away, country)
                            
                        home_link = await new_page.locator(".duelParticipant__home .participant__participantName a").first.get_attribute('href')
                        #await new_page.goto("https://www.flashscore.com"+home_link+"results/")
                        #home_events =  await page.locator(".event__match").all()
                        away_link = await new_page.locator(".duelParticipant__away .participant__participantName a").first.get_attribute('href')
                        print(away_link)
                        await self.previous_team_games(home_link, new_page, session)
                        await self.previous_team_games(away_link, new_page, session)

                        
                        print("Loaded in:", time.time() - start, "seconds")
                        #is_selected = await self.select_games_for_prediction(page=new_page)
                    # if is_selected:
                        #    await new_page.goto(href)
                        #    await new_page.wait_for_selector(".duelParticipant")
                        #    await self.game_to_predict_today(new_page)
                        await new_page.close()
                    except Exception as e:
                        return

    # Str -> None
    # Retrieves all the possible games found from the default flashscore link and tries to process
    #       each game independently
    async def get_todays_game_events(self, url: str = "https://www.flashscore.com/") -> None:
            await asyncio.sleep(0.5)
            page = await self.browser.new_page()
            await page.goto(url)
            #await page.wait_for_selector(".event__match")
            events = await page.locator(".event__match").all()
            
            
            BATCH_SIZE = 10
            tasks = []
            for i, event in enumerate(events):
                tasks.append(asyncio.create_task(self.page_handler(event)))
                if len(tasks) == BATCH_SIZE or i == len(events) - 1:
                    await asyncio.gather(*tasks)
                    tasks = []

            await page.close()

    async def previous_team_games(self, link, page, session):
        await page.goto("https://www.flashscore.com" + link + "results/")
        events = await page.locator(".event__match").all()
        consecutive_failures = 0

        for event in events:
            if consecutive_failures >= 3:
                print("Stopped due to 3 consecutive failures.")
                break

            new_page = None
            stat_page = None
            try:
                href = await event.locator("a").first.get_attribute('href')
                new_page = await self.browser.new_page()
                await new_page.goto(href, wait_until="domcontentloaded")

                country, league, round = await get_match_details(page=new_page)
                home, away, home_score, away_score, start_time = await get_match_info(page=new_page)

                home_team = await get_team_by_name(session, home, country)
                away_team = await get_team_by_name(session, away, country)

                if home_team and away_team:
                    game_present = await is_game_already_saved(session, home_team.id, away_team.id)
                    if game_present:
                        await new_page.close()
                        continue

                home_team_info = { "name": home, "country": country }
                away_team_info = { "name": away, "country": country }

                if not home_team:
                    home_team = await add_team(session, home_team_info)
                if not away_team:
                    away_team = await add_team(session, away_team_info)

                extra_info = await get_extra_match_info(page=new_page)
                if not extra_info:
                    await new_page.close()
                    consecutive_failures += 1
                    continue

                venue = extra_info.get('venue')
                referee = extra_info.get('referee')
                capacity = extra_info.get('capacity')
                if not venue and not referee and not capacity:
                    await new_page.close()
                    consecutive_failures += 1
                    continue

                if capacity:
                    capacity = re.sub(r'\s', '', capacity)

                stats_url = assemble_url(new_page.url, "/match-summary", STATS_FULL_TIME)
                stat_page = await self.browser.new_page()
                await stat_page.goto(stats_url)
                await stat_page.wait_for_selector(".container__livetable .container__detailInner .section")

                stats = await get_match_stats(stat_page)
                if not stats or has_none_values(stats):
                    await stat_page.close()
                    await session.rollback()
                    consecutive_failures += 1
                    continue

                game = {
                    "start_time": start_time, "league": league, "home_team": home_team,
                    "away_team": away_team, "home_score": home_score, "away_score": away_score,
                    "round": round, "capacity": int(capacity), "referee": referee,
                    "venue": venue, "country": country
                }

                db_game = await add_game(session, game)
                await add_stats(session, stats, game_id=db_game.id)
                await session.commit()
                await stat_page.close()
                await new_page.close()

                # ✅ SUCCESS: reset failure counter
                consecutive_failures = 0

            except Exception as e:
                print(f"Error: {e}")
                await session.rollback()
                consecutive_failures += 1

            finally:
                if stat_page and not stat_page.is_closed():
                    await stat_page.close()
                if new_page and not new_page.is_closed():
                    await new_page.close()
                

    async def get_starts_df(self):
        async with self.AsyncSessionLocal() as session:
            df = await get_all_game_stats_df(session)
            print(df.head())
            df.to_csv("work.csv", index=False)
                

if __name__ == "__main__":
    async def main():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            scraper = Scraper(browser)
            await scraper.startup()
            await scraper.get_todays_game_events()
            #await scraper.get_starts_df()
            
            await browser.close()

    asyncio.run(main())
