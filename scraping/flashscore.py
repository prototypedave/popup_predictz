from playwright.sync_api import sync_playwright
from .events import scrape_events
from .match import scrape_match_data_from_link

# =============================================
# Scraping Flashscore
# =============================================

# Navigate to the Flashscore website and scrape the data
# scrape_flashscore: () -> list

def scrape_flashscore():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.flashscore.com/")

        links = scrape_events(page)
        for link in links:
            match_info = scrape_match_data_from_link(page, link)


if __name__ == "__main__":
    scrape_flashscore()