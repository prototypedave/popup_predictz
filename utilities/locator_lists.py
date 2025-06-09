# Scrapes and returns a list of locators
from playwright.sync_api import Page, Locator
from typing import List

# Page, Str -> list
# scrape and return a list of playwright locators
async def get_locator_lists(page: Page, selector: str) -> List[Locator]:
    await page.wait_for_selector(selector)
    locator = page.locator(selector)
    count = await locator.count()
    return [locator.nth(i) for i in range(count)]