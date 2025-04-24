from playwright.sync_api import Page

# ==============================================
# Scraping Events Links
# ==============================================

# Navigate to the Events website and scrape the data
# scrape_events: (page: Page) -> list

# len(scrape_events(page)) => 0

def scrape_events(page: Page) -> list:
    """
    Scrape events from the provided page.

    Args:
        page (Page): The Playwright page object to scrape data from.

    Returns:
        list: A list of scraped events links.
    """
    links = []
    # Wait for the events section to load
    page.wait_for_selector(".event__match")

    # Locate all event elements
    events = page.locator(".event__match").all()

    for event in events:
        match_link = scrape_match_link(event)
        if match_link:
            links.append(match_link)
    return links


# Scrape match link from given event
# scrape_match_link: (event: playwright.sync_api._generated.Locator) -> str

def scrape_match_link(event):
    """
    Scrape match link from the given event.

    Args:
        event (Locator): The event locator to scrape the match link from.

    Returns:
        str: The scraped match link.
    """
    try:
        match_link = event.locator("a").first
        href = match_link.get_attribute("href")   
        return href

    except Exception as e:
        return None