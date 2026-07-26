import time

from playwright.sync_api import sync_playwright

from agent.parser import parse_prompt
from agent.browser import get_browser, search_bing_maps


def main():
    parsed = parse_prompt("coffee shops in Karachi")
    query = f"{parsed['category']} {parsed['location']}"
    print(f"Parsed: {parsed}")
    print(f"Search query: {query}")

    with sync_playwright() as p:
        browser = get_browser(p, headless=False)
        try:
            page = browser.new_page()
            start = time.time()
            search_bing_maps(page, query)
            elapsed = time.time() - start
            page.screenshot(path="search_result.png")
            print(f"Search completed in {elapsed:.2f}s")
            print("Screenshot saved as search_result.png")
            page.wait_for_timeout(3000)
        finally:
            browser.close()


if __name__ == "__main__":
    main()