from playwright.sync_api import sync_playwright


def scrape_flashscore():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.flashscore.com/match/football/OCxRmFfE/#/match-summary")

        page.wait_for_selector(".lf__sidesBox")
        lf_side = page.locator(".lf__sidesBox .lf__sides .lf__side .wcl-participant_QKIld").all()

        if lf_side:
            home, away = [], []
            for lf in lf_side:
                attr = lf.get_attribute('data-testid')
                if attr:
                    if 'left' in attr:
                        link = lf.locator('a').get_attribute('href')
                        reason = lf.locator('span').text_content()
                        home.append(link)
                        print(reason)
                    elif 'right' in attr:
                        link = lf.locator('a').get_attribute('href') 
            if home or away:
                print('TRUE')        

        browser.close()


if __name__ == "__main__":
    scrape_flashscore()


   