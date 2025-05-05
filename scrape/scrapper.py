# Class to scrape flashscore data
from playwright.sync_api import sync_playwright
from .utils import scrape_locator_lists, scrape_attributes
from .match_summary import get_match_summary
import time

# Flashscore -> Matches
# scrape a list of matches with there data

class FlashScoreScraper:

    # Initialize the Scraper
    def __init__(self):
        self.browser = sync_playwright().start().chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    # URL -> list
    # scrape and return list of matche urls
    def scrape_match_links(self, url):
        self.page.goto(url)
        events = scrape_locator_lists(self.page, ".event__match")
        
        links = []
        for event in events:
            href = scrape_attributes(event, "a", "href")
            links.append(href)

        return links

    # URL -> Summary
    # scrape and return match info summary
    def scrape_match_summary(self, url):
        links = self.scrape_match_links(url)
        for link in links:
            if link is not None:
                self.page.goto(link)
                self.page.wait_for_selector(".duelParticipant")
                get_match_summary(self.page)


    # URL -> Stats
    # scrape and return match stats
    # !!!

    # URK -> h2h
    # scrape and return h2h data
    # !!!

    def scrape_match(self, url):
        self.page.goto(url)
        self.page.wait_for_selector(".event__match")
        print("Test run")

    def close(self):
        self.browser.close()


flash = FlashScoreScraper()

start = time.time()
flash.scrape_match_summary("https://www.flashscore.com/")
end = time.time()

print(f"Time taken: {end - start:.2f} seconds")

