from playwright.sync_api import sync_playwright


def scrape_flashscore():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context()
        page = context.new_page()

        attr = {
            "goal": "https://www.flashscore.com/player/acuna-valentino/M1JJJMB3/",
            "assist": "https://www.flashscore.com/player/acuna-valentino/M1JJJMB3/",
            "pen": "(penalty)"
        }

        scorer = attr['assist']

        page.goto(scorer)

        page.wait_for_selector(".player-profile-heading")
        country = page.locator(".player-profile-heading nav li").last.text_content().lower()
        name = page.locator(".playerHeader__nameWrapper h2").text_content().lower()
        position = page.locator(".playerTeam strong").text_content().lower()
        team = page.locator(".playerTeam a").text_content().lower()   # format to remove brackets
        playerInfo = page.locator(".playerInfoItem span").all()
        dob = playerInfo[1].text_content().lower()   # format to remove brackets and ensure its in date format
        print(dob)


if __name__ == "__main__":
    scrape_flashscore()


   