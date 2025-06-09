# Returns the text contained in the given locator

from playwright.sync_api import Page, Locator
import asyncio

# Locator, Str -> Str
# returns text content of the given locator
async def get_text_content(loc: Page | Locator, cls_name: str) -> str:
    try:
        return await loc.locator(cls_name).first.text_content()
    except Exception as e:
        return None
    

# Locator -> str
# helper function to strip text content from a given locator returns None if error
async def text_content_helper(loc) -> str | None:
    try:
        if loc:
            text = await loc.inner_text()
            return text.strip().lower() if text else None
    except Exception:
        return None
    

# List -> List
# strip text content for the locators in the given list and return a new list containing
#   the text content
async def get_text_to_list(items: list) -> list:
    tasks = [text_content_helper(item) for item in items]
    return await asyncio.gather(*tasks)