from playwright.sync_api import Page


# Page, Str -> list
# scrape and return a list of playwright locator
def scrape_locator_lists(page: Page, cls_name: str) -> list:
    try:
        page.wait_for_selector(cls_name)
        locators = page.locator(cls_name).all()
        return locators
    except Exception as e:
        print(e)
        return []


# Locator, Str, Str -> Str
# return a string value for the given attribute
def scrape_attributes(loc, cls_name: str, attr: str) -> str:
    try:
        attr_str = loc.locator(cls_name).first.get_attribute(attr)
        return attr_str
    except Exception as e:
        print(e)
        return None

    
# Locator, Str -> Str
# returns text content of the given locator
def scrape_text_content(loc, cls_name: str) -> str:
    try:
        text = loc.locator(cls_name).first.text_content()
        return text
    except Exception as e:
        print(e)
        return None