import os

from dotenv import load_dotenv

load_dotenv()


def get_browser(playwright, headless=None):
    if headless is None:
        headless = os.getenv("HEADLESS", "false").strip().lower() in ("1", "true", "yes")
    return playwright.chromium.launch(headless=headless)