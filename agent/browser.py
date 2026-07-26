import os

from dotenv import load_dotenv

load_dotenv()


def get_browser(playwright, headless=None):
    if headless is None:
        headless = os.getenv("HEADLESS", "false").strip().lower() in ("1", "true", "yes")
    return playwright.chromium.launch(headless=headless)


def search_bing_maps(page, query: str):
    page.goto("https://www.bing.com/maps", timeout=30000)
    page.wait_for_selector("#searchBoxInput", timeout=10000)
    page.fill("#searchBoxInput", query)
    page.press("#searchBoxInput", "Enter")
    page.wait_for_selector("#localSearchContent", timeout=15000)
    page.wait_for_function(
        """() => {
            const items = document.querySelectorAll('[id^="listingItem_"]');
            if (items.length === 0) return false;
            return Array.from(items).some(el => el.innerText && el.innerText.trim().length > 10);
        }""",
        timeout=15000
    )
    return page