from playwright.sync_api import sync_playwright
from agent.browser import get_browser, search_bing_maps
with sync_playwright() as p:
    browser = get_browser(p, headless=False)
    try:
        page = browser.new_page()
        search_bing_maps(page, 'coffee shops Karachi')
        page.locator('[id^="listingItem_"]').first.click()
        page.wait_for_selector('h2.eh_title.b_entityTitle', timeout=10000)
        page.wait_for_timeout(2000)
        links = page.locator('a[href^="http"]')
        for i in range(links.count()):
            href = links.nth(i).get_attribute('href') or ''
            text = links.nth(i).text_content() or ''
            print(f'Link #{i}: href={href!r}  text={text.strip()!r}')
        page.wait_for_timeout(2000)
    finally:
        browser.close()
