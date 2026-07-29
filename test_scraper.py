from playwright.sync_api import sync_playwright
from agent.parser import parse_prompt
from agent.browser import get_browser, search_bing_maps
from agent.scraper import scrape_first_result

def main():
    parsed = parse_prompt("coffee shops in Karachi")
    query = f"{parsed['category']} {parsed['location']}"
    print(f"Parsed: {parsed}")
    with sync_playwright() as p:
        browser = get_browser(p, headless=False)
        try:
            page = browser.new_page()
            search_bing_maps(page, query)
            result = scrape_first_result(page)
            print("Scraped result:", result)
            for key, value in result.items():
                status = "OK" if value else "MISSING"
                print(f"  {key}: {status} -> {value!r}")
            page.wait_for_timeout(2000)
        finally:
            browser.close()

if __name__ == "__main__":
    main()