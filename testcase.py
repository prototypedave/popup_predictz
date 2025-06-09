from playwright.async_api import async_playwright, Page, ChromiumBrowserContext, Locator
import asyncio, time

async def page_handler(event: Locator, semaphore, browser) -> None:
    async with semaphore:
        href = await event.locator("a").first.get_attribute('href')
        if href:
            start = time.time()
            new_page = await browser.new_page()
            await new_page.goto(href, wait_until="domcontentloaded")
            header_items = await new_page.locator(".detail__breadcrumbs li").all()
            home_team = await new_page.locator(".duelParticipant__home .participant__participantName a").first.text_content()
            away_team = await new_page.locator(".duelParticipant__away .participant__participantName a").first.text_content()
            score = await new_page.locator(".detailScore__wrapper").first.text_content()
            time_str = await new_page.locator(".duelParticipant__startTime div").first.text_content()

            home_link = await new_page.locator(".duelParticipant__home .participant__participantName a").first.get_attribute('href')
            away_link = await new_page.locator(".duelParticipant__away .participant__participantName a").first.get_attribute('href')

            await previous_team_games(browser, home_link, new_page, semaphore)
            await previous_team_games(browser, away_link, new_page, semaphore)
            #await new_page.wait_for_selector(".duelParticipant")
            print("Loaded in:", time.time() - start, "seconds")
            #is_selected = await self.select_games_for_prediction(page=new_page)
            #if is_selected:
            #    await new_page.goto(href)
            #    await new_page.wait_for_selector(".duelParticipant")
            #    await self.game_to_predict_today(new_page)
            await new_page.close()

async def get_all_match_details(event: Locator, browser) -> None:
    href = await event.locator("a").first.get_attribute('href')
    page = await browser.new_page()
    await page.goto(href, wait_until="domcontentloaded")
    header_items = await page.locator(".detail__breadcrumbs li").all()
    print(len(header_items))

async def previous_team_games(browser, link, page, semaphore):
    await page.goto("https://www.flashscore.com"+link+"results/")
    events = await page.locator(".event__match").all()
    #tasks = [get_all_match_details(event, browser) for event in events[:24]]
    #await asyncio.gather(*tasks)
    for event in events:
            href = await event.locator("a").first.get_attribute('href')
            new_page = await browser.new_page()
            await new_page.goto(href)
            header_items = await new_page.locator(".detail__breadcrumbs li").all()
            home_team = await new_page.locator(".duelParticipant__home .participant__participantName a").first.text_content()
            away_team = await new_page.locator(".duelParticipant__away .participant__participantName a").first.text_content()
            score = await new_page.locator(".detailScore__wrapper").first.text_content()
            time_str = await new_page.locator(".duelParticipant__startTime div").first.text_content()
            
            extra_locators = await new_page.locator(".loadable__section .wclDetailSection .wcl-content_J-1BJ").all()
            for extra in extra_locators:
                head = await extra.locator(".wcl-overline_rOFfd").all()
                value = await extra.locator(".wcl-simpleText_Asp-0").all()

            stats_url = assemble_url(new_page.url, "/match-summary", 'match-statistics/0')
            #print(stats_url)
            try:
                stat_page = await browser.new_page()
                await stat_page.goto(stats_url)
                await stat_page.wait_for_selector(".container__livetable .container__detailInner .section")
                print(stat_page.url)
                stats_rows = await stat_page.locator(".wcl-row_OFViZ").all()
                print(len(stats_rows))
                await stat_page.close()
            except Exception as e:
                await new_page.close()
           
#def click_into_h2h_games(page, start):



def is_valid_url(url: str, destination: str) -> bool:
    return url.find(destination) != -1

# Assemble url to the required page
# assemble_url: (str, str) -> str
# interp. assemble_url takes a base url removes any text and adds a destination and returns the full url
def assemble_url(base_url: str, remove: str, destination: str) -> str:
    base_url = base_url.replace(remove, "", 1)
    return f"{base_url}/{destination}"


if __name__ == "__main__":
    async def main():
        start = time.time()
        semaphore = asyncio.Semaphore(1)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://www.flashscore.com/")
            #await page.wait_for_selector(".event__match")
            events = await page.locator(".event__match").all()
            #await page.close()
            tasks = [page_handler(event, semaphore, browser) for event in events[:24]]
            await asyncio.gather(*tasks)
            
            await browser.close()
        print("Saved in:", time.time() - start, "seconds")
    asyncio.run(main())