# Get other relevant information for a given match

from playwright.sync_api import Page
from utilities.locator_lists import get_locator_lists
from utilities.locator_text import get_text_to_list

# Page -> dict
# scrape and return referee, venue and stadium capacity info from the given match
#   page
async def get_extra_match_info(page: Page) -> dict:
    extra_locators = await get_locator_lists(page, ".loadable__section .wclDetailSection .wcl-content_J-1BJ")

    for extra in extra_locators:
        head = await extra.locator(".wcl-overline_rOFfd").all()
        value = await extra.locator(".wcl-simpleText_Asp-0").all()
        
        header_texts = await get_text_to_list(head)
        value_texts = await get_text_to_list(value)

        # Filter out tv or live streams values
        if 'tv channel:' in header_texts or 'live streaming:' in value_texts:
            continue
        
        return organize_extra_match_info(header_texts, value_texts)
    

# List, List -> Dict
# produce a dictionary containing referee's name, venue name and capacity value
#   from the provided List items which contains header and value for this fields
def organize_extra_match_info(head: list, value: list) -> dict:
    result, i = {}, 0
    for key in head:
        stripped_key = key.rstrip(':')
        if stripped_key in ('referee', 'venue'):
            if i + 1 < len(value):
                result[stripped_key] = value[i] + ' ' + value[i + 1]  
                i += 2
            else:
                result[stripped_key] = value[i]
                i += 1
        else:
            if i < len(value):
                result[stripped_key] = value[i]

    return result