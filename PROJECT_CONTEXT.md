# LeadGenAgent — Project Context

## What this is
A bootcamp assignment: build an AI agent that takes a natural language prompt
(e.g. "coffee shops in Karachi"), extracts business category + location, uses
browser automation to search Bing Maps, scrapes business leads (name, phone,
website, email), and exports them to an Excel file.

## Tech stack
- Python 3.14, Playwright (sync API) for browser automation
- Groq API (llama-3.3-70b-versatile) for parsing the user's natural language prompt
- openpyxl for Excel export
- Target site: Bing Maps (https://www.bing.com/maps) — chosen because Google Maps
  has heavy bot detection that makes it unsuitable for a learning project

## Confirmed selectors (DO NOT re-discover these, they are verified working)
- Search input: #searchBoxInput
- Results container: #localSearchContent
- Individual listing cards: [id^="listingItem_"]
- Business name in detail panel (after clicking a listing card):
  h2.eh_title.b_entityTitle > span.eh_title_container
- Phone/website selectors: NOT YET CONFIRMED — this is the current task

## Files that exist and what they do
- agent/parser.py — parse_prompt(user_text) -> {"category": str, "location": str}
  using Groq with a regex fallback if the API fails
- agent/browser.py — get_browser(playwright, headless) launches Chromium;
  search_bing_maps(page, query) navigates to Bing Maps, searches, and waits for
  real (non-skeleton) results to load
- agent/scraper.py — IN PROGRESS. Will contain scrape_first_result(page) -> dict
  with keys name/phone/website, using try/except so missing fields become ""
  rather than crashing
- test_parser.py, test_browser.py, test_search.py — working test scripts for
  earlier steps, all passing
- detail_dump.html — a saved copy of the full page HTML after clicking a listing
  card's detail panel, captured once from a real browser session. Use this file
  to search for selectors with plain text/regex search — do NOT relaunch the
  browser to re-discover things already in this file.

## Project roadmap (9 steps total)
1. Project setup — DONE
2. Prompt parsing (agent/parser.py) — DONE
3. Browser automation smoke test — DONE
4. Search automation (agent/browser.py: search_bing_maps) — DONE
5. Single-result scraping (agent/scraper.py: scrape_first_result) — IN PROGRESS
   (name selector confirmed, phone/website selectors still needed)
6. Multi-result scraping loop (scrape multiple listings, not just one) — TODO
7. Excel export (openpyxl, columns: Business Name, Email, Phone Number, Website,
   Location) — TODO
8. Wire everything together into main.py with a clear summary printout — TODO
9. README + final polish + git push — TODO

## Working rules
- Always work in small, single-purpose scripts. Never write multiple exploratory
  scripts in one session — if inspecting page structure, use ONE script, run it
  ONCE, and read from saved files (like detail_dump.html) instead of relaunching
  the browser repeatedly.
- Every function must handle missing/failed data gracefully (empty string ""),
  never raise uncaught exceptions.
- Do not modify or replace working files (parser.py, browser.py, test_*.py for
  completed steps) unless explicitly asked to.