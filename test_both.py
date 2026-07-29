from playwright.sync_api import sync_playwright
from agent.browser import get_browser, search_bing_maps
from agent.scraper import scrape_first_result

def run_test(query):
    print(f"\n=== Testing: {query} ===")
    with sync_playwright() as p:
        browser = get_browser(p, headless=False)
        try:
            page = browser.new_page()
            search_bing_maps(page, query)
            result = scrape_first_result(page)
            for key, value in result.items():
                status = "OK" if value else "MISSING"
                print(f"  {key}: {status} -> {value!r}")
            page.wait_for_timeout(1000)
        finally:
            browser.close()

if __name__ == "__main__":
    run_test("coffee shops Karachi")
    run_test("hotels Karachi")
