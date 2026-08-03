from playwright.sync_api import sync_playwright
from agent.parser import parse_prompt
from agent.browser import get_browser, search_bing_maps
from agent.scraper import scrape_results
from agent.email_finder import find_email
from agent.excel_writer import save_leads_to_excel


def run_pipeline(user_prompt: str, max_results: int = 10, headless: bool = True) -> dict:
    """
    Runs the full lead-gen pipeline for a given natural language prompt.
    Returns a dict: {
        "category": str, "location": str, "query": str,
        "leads": list[dict], "filepath": str, "error": str or None
    }
    Never raises — any failure is captured in the "error" key so callers (CLI or
    Streamlit) can display it without crashing.
    """
    result = {"category": "", "location": "", "query": "", "leads": [], "filepath": "", "error": None}
    try:
        parsed = parse_prompt(user_prompt)
        category = parsed.get("category", "").strip()
        location = parsed.get("location", "").strip()
        result["category"] = category
        result["location"] = location

        if not category:
            result["error"] = "Could not identify a business category from your prompt."
            return result

        query = f"{category} {location}".strip()
        result["query"] = query

        with sync_playwright() as p:
            browser = get_browser(p, headless=headless)
            try:
                page = browser.new_page()
                search_bing_maps(page, query)
                leads = scrape_results(page, max_results=max_results)
            finally:
                browser.close()

        result["leads"] = leads
        if not leads:
            result["error"] = "No leads were found for this search."
            return result

        for lead in leads:
            if lead.get("website"):
                lead["email"] = find_email(lead["website"])
            else:
                lead["email"] = ""

        filepath = save_leads_to_excel(leads, category, location)
        result["filepath"] = filepath
        return result

    except Exception as e:
        result["error"] = f"Something went wrong: {e}"
        return result
