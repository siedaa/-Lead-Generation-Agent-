from playwright.sync_api import sync_playwright
from agent.parser import parse_prompt
from agent.browser import get_browser, search_bing_maps
from agent.scraper import scrape_results

def main():
    parsed = parse_prompt("coffee shops in Karachi")
    query = f"{parsed['category']} {parsed['location']}"
    print(f"Parsed: {parsed}")
    with sync_playwright() as p:
        browser = get_browser(p, headless=False)
        try:
            page = browser.new_page()
            search_bing_maps(page, query)
            results = scrape_results(page, max_results=10)
            print(f"\nCollected {len(results)} leads:\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['name']}")
                print(f"   phone:   {r['phone'] or '(missing)'}")
                print(f"   website: {r['website'] or '(missing)'}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
