# Class to scrape flashscore data
import asyncio
from playwright.async_api import async_playwright, Page
from .utils import scrape_locator_lists, scrape_attributes
from .match_summary import get_match_summary
from .constants import STATS_FULL_TIME
from .func_util import is_past_two_hours
import time

# Flashscore -> Matches
# scrape a list of matches with there data

class FlashScoreScraper:

    # Initialize the Scraper
    def __init__(self, max_concurrent=20):
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
    # scrape and return list of matche urls
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
            extra_page = await self.context.new_page()

            try: 
                await summary_page.goto(url)
                await summary_page.wait_for_selector(".duelParticipant")

                summary_tasks = get_match_summary(summary_page)
                summary = await asyncio.gather(summary_tasks)
                
                return {'summsty': summary}

            except Exception as e:
                return {}

            finally:
                await summary_page.close()

    async def run(self, home_url: str):
        await self.start()
        links = await self.scrape_match_links(home_url)
        print(f"Found {len(links)} matches")  

        tasks = [self.scrape_match_details(link) for link in links[:10]]  
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




