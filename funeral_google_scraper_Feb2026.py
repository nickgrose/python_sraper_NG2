from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import csv
import time

# ---- Configuration ----
REGION = "Fairfax County, Virginia"
SEARCH_TERMS = [
    "funeral home",
    "cremation service",
    "mortuary",
    "memorial park",
    "cemetery",
    "direct cremation",
]
MAX_RESULTS_PER_QUERY = 120
HEADLESS = False


def safe_inner_text(locator, timeout=2500):
    """Return locator text or empty string if not found."""
    try:
        locator.first.wait_for(timeout=timeout)
        return locator.first.inner_text().strip()
    except Exception:
        return ""


def safe_attr(locator, attr, timeout=2500):
    """Return locator attribute or empty string if not found."""
    try:
        locator.first.wait_for(timeout=timeout)
        return (locator.first.get_attribute(attr) or "").strip()
    except Exception:
        return ""


def run_query(page, query):
    """Scrape one Google Maps search query and return records."""
    records = []
    seen = set()

    search_box = page.locator('input[id="searchboxinput"]')
    search_box.wait_for(timeout=60000)
    search_box.fill(query)
    page.keyboard.press("Enter")
    time.sleep(5)

    results_panel = page.locator('div[role="feed"]')
    results_panel.wait_for(timeout=20000)

    # Scroll to load more listings
    for _ in range(22):
        results_panel.evaluate("el => el.scrollTop = el.scrollHeight")
        time.sleep(1.2)

    cards = page.locator('div[role="feed"] > div')
    total = cards.count()
    print(f"Query: {query} | visible cards: {total}")

    for i in range(min(total, MAX_RESULTS_PER_QUERY)):
        card = cards.nth(i)
        try:
            card.click(timeout=4500)
            time.sleep(1.7)
        except Exception:
            continue

        name = safe_inner_text(page.locator("h1.DUwDvf"))
        if not name or name in seen:
            continue
        seen.add(name)

        address = safe_inner_text(page.locator('button[data-item-id="address"] .Io6YTe'))

        website = safe_attr(page.locator('a[data-item-id="authority"]'), "href")
        phone = safe_inner_text(page.locator('button[data-item-id^="phone"] .Io6YTe'))

        # Business category is often visible under title area
        category = safe_inner_text(page.locator("button.DkEaL"))

        records.append(
            {
                "query": query,
                "name": name,
                "category": category,
                "phone": phone,
                "address": address,
                "website": website,
                "region": REGION,
            }
        )

    return records


def main():
    all_records = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=200)
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)

        # Cookie banner is region-dependent; ignore if missing
        try:
            page.locator("button:has-text('Accept all')").click(timeout=4500)
        except PlaywrightTimeoutError:
            pass

        for term in SEARCH_TERMS:
            query = f"{term} in {REGION}"
            try:
                rows = run_query(page, query)
                all_records.extend(rows)
            except Exception as exc:
                print(f"Skipped query '{query}' due to error: {exc}")

        browser.close()

    # De-duplicate by (name, address)
    unique = {}
    for row in all_records:
        unique[(row["name"], row["address"])] = row

    final_rows = list(unique.values())
    print(f"Total unique companies: {len(final_rows)}")

    with open("funeral_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["query", "name", "category", "phone", "address", "website", "region"],
        )
        writer.writeheader()
        writer.writerows(final_rows)

    print("Saved: funeral_results.csv")


if __name__ == "__main__":
    main()
