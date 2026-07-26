from playwright.sync_api import sync_playwright

from agent.browser import get_browser

try:
    with sync_playwright() as p:
        browser = get_browser(p, headless=False)
        try:
            page = browser.new_page()
            page.goto("https://www.bing.com/maps")
            page.wait_for_timeout(3000)
            print(f"Page title: {page.title()}")
        finally:
            browser.close()
except Exception as e:
    print(f"Browser test failed: {e}")