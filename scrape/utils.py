from playwright.sync_api import Page, Locator
from typing import List
import asyncio

# Page, Str -> list
# scrape and return a list of playwright locator
async def scrape_locator_lists(page: Page, selector: str) -> List[Locator]:
    await page.wait_for_selector(selector)
    locator = page.locator(selector)
    count = await locator.count()
    return [locator.nth(i) for i in range(count)]


# Locator, Str, Str -> Str
# return a string value for the given attribute
async def scrape_attributes(loc, cls_name: str, attr: str) -> str | None:
    try:
        return await loc.locator(cls_name).first.get_attribute(attr)
    except:
        return None

    
# Locator, Str -> Str
# returns text content of the given locator
async def scrape_text_content(loc, cls_name: str) -> str:
    try:
        return await loc.locator(cls_name).first.text_content()
    except Exception as e:
        return None
    

# Locator -> str
# helper function to strip text content from a given locator returns None if error
async def text_content_helper(loc) -> str:
    try:
        return await loc.inner_text().strip().lower()
    except Exception as e:
        return None
    

# List -> List
# strip text content for the locators in the given list and return a new list containing
#   the text content
async def scrape_text_to_list(items: list) -> list:
    tasks = [text_content_helper(item) for item in items]
    return await asyncio.gather(*tasks)
    