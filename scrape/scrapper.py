# Class to scrape flashscore data
import asyncio
from playwright.async_api import async_playwright, Page
from .utils import scrape_locator_lists, scrape_attributes
from .match_summary import get_match_summary
from .constants import STATS_FULL_TIME, LINEUP, PLAYER_STATS
from .func_util import is_valid_url, assemble_url
from .match_stats import get_match_stats
from .match_lineups import get_match_lineups
from .player_stats import get_player_stats
from .match_odds import get_match_odds
import time, re



# Flashscore -> Matches
# scrape a list of matches with there data
class FlashScoreScraper:

    # Initialize the Scraper
    def __init__(self, max_concurrent=10):
        self.browser = None
        self.context = None
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()

    async def close(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    # URL -> list
    # scrape and return list of matches urls
    async def scrape_match_links(self, url: str) -> list[str]:
        page = await self.context.new_page()
        await page.goto(url)
        await page.wait_for_selector(".event__match")
        events = await page.locator(".event__match").all()
        tasks = [scrape_attributes(event, "a", "href") for event in events]
        raw_links = await asyncio.gather(*tasks)

        links = [href for href in raw_links if href]
        
        await page.close()
        return links
    
    
    # URL -> dict
    # !!!
    async def scrape_match_details(self, url:str):
        async with self.semaphore:
            summary_page = await self.context.new_page()
            odds_page = await self.context.new_page()
            
            try: 
                await summary_page.goto(url)
                await summary_page.wait_for_selector(".duelParticipant")

                """if is_valid_url(summary_page.url, "/match-summary/match-summary"):
                    stats_url = assemble_url(summary_page.url, "/match-summary", STATS_FULL_TIME)
                    lineup_url = assemble_url(summary_page.url, "/match-summary", LINEUP)
                    player_stats_url = assemble_url(summary_page.url, "/match-summary", PLAYER_STATS)
                    print(f"Stats URL: {player_stats_url}")
                    
                    #await stats_page.goto(stats_url)
                    #await stats_page.wait_for_selector(".container__livetable .container__detailInner .section")

                    #await lineups_page.goto(lineup_url)
                    #await lineups_page.wait_for_selector(".container__livetable .container__detailInner .section")

                    selector = ".container__livetable .container__detailInner .section .wcl-tableWrapper_Z9oKt .wcl-table_tQq-F"
                    await self.helper_scrape(url=player_stats_url, selector=selector, function=get_player_stats)
                   
                    
                    #stats_tasks = get_match_stats(stats_page)
                    #stats = await asyncio.gather(stats_tasks)

                    #lineup_tasks = get_match_lineups(lineups_page, players_page)
                    #lineups = await asyncio.gather(lineup_tasks)"""
    
                await get_match_odds(page=odds_page, url=url)

                    

                #summary_tasks = get_match_summary(summary_page)
                #summary = await asyncio.gather(summary_tasks)
                
                #return {'summary': summary, 'stats': stats}

            except Exception as e:
                return {}

            finally:
                await summary_page.close()
                await odds_page.close()
                
    
    async def helper_scrape(self, url: str, selector: str, function: callable):
        page = self.context.new_page()
        try:
            await page.goto(url)
            print("Its working")
            await page.wait_for_selector(selector)
            print("Even this")
            element = await function(page)
            return element
        except Exception as e:
            return None
        finally:
            await page.close()
                

    async def run(self, home_url: str):
        await self.start()
        links = await self.scrape_match_links(home_url)
        print(f"Found {len(links)} matches")  

        tasks = [self.scrape_match_details(link) for link in links]  
        results = await asyncio.gather(*tasks)

        await self.close()
        return results


if __name__ == "__main__":
    async def main():
        scraper = FlashScoreScraper()
        start = time.time()
        results = await scraper.run("https://www.flashscore.com/")
        for res in results:
            print(res)
        end = time.time()
        print(f"Time taken: {end - start:.2f} seconds")


    asyncio.run(main())




