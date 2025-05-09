from playwright.sync_api import sync_playwright


def scrape_flashscore():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.flashscore.co.ke/match/football/KOJsLbH7/#/match-summary/match-summary")

        page.wait_for_selector(".loadable__section .wclDetailSection .wcl-content_J-1BJ")
        print("SADR")
        #lf_side = page.locator(".container__livetable .container__detailInner .section").all()

        #for lf in lf_side:
        #    header = lf.locator(".sectionHeader").text_content()
              

        browser.close()


if __name__ == "__main__":
    scrape_flashscore()


   