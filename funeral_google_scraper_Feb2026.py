from playwright.sync_api import sync_playwright
import time
import csv

SEARCH = "funeral homes in Fairfax, Virginia"
MAX_RESULTS = 50


def main():

    with sync_playwright() as p:

        print("Launching browser...")

        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )

        page = browser.new_page()

        print("Opening Google Maps...")
        page.goto("https://www.google.com/maps", timeout=60000)

        # Accept cookies if prompted
        try:
            page.locator("button:has-text('Accept all')").click(timeout=5000)
            print("Accepted cookies")
        except:
            pass

        print("Waiting for search box...")

        # ✅ NEW WORKING SELECTOR
        search_box = page.locator('input[id="searchboxinput"]')

        search_box.wait_for(timeout=60000)

        print("Typing search...")

        search_box.fill(SEARCH)

        page.keyboard.press("Enter")

        print("Waiting for results...")
        time.sleep(5)

        print("Scrolling results...")

        results_panel = page.locator('div[role="feed"]')

        for i in range(10):
            results_panel.evaluate("el => el.scrollTop += 1000")
            time.sleep(2)

        print("Collecting listings...")

        listings = page.locator('div[role="feed"] > div')

        count = listings.count()

        print("Found:", count)

        data = []

        for i in range(min(count, MAX_RESULTS)):

            try:

                listing = listings.nth(i)

                name = listing.locator("div.fontHeadlineSmall").inner_text()

                print(name)

                data.append([name])

            except:
                pass

        print("Saving CSV...")

        with open("funeral_results.csv", "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow(["Name"])

            writer.writerows(data)

        print("DONE")

        browser.close()


main()
