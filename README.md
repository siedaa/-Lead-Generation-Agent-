# LeadGenAgent

An AI-powered lead generation agent. Give it a natural language prompt like
"coffee shops in Karachi" and it automatically searches Bing Maps, collects
business leads (name, phone, website, email), and saves them to an Excel file.

## How it works

1. **Prompt parsing** — your natural language request is sent to Groq (LLM) to
   extract the business category and location (e.g. "coffee shops" + "Karachi"),
   with a regex-based fallback if the API call fails.
2. **Browser automation** — Playwright opens Bing Maps and searches using the
   parsed query.
3. **Scraping** — the agent clicks through multiple search results and extracts
   business name, phone number, and website for each one, skipping data that
   isn't available rather than failing.
4. **Email discovery** — for each business with a website, the agent visits that
   website and looks for a contact email (mailto: links first, then a pattern
   match on the page text).
5. **Excel export** — all collected leads are saved into a spreadsheet with
   columns: Business Name, Email, Phone Number, Website, Location.

## Setup

1. Clone this repo and navigate into it.
2. Create a virtual environment and activate it:
   python -m venv .venv
   (Windows) .venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Install Playwright's browser (one-time, downloads Chromium):
   playwright install chromium
5. Copy .env.example to .env and add your Groq API key:
   GROQ_API_KEY=your_key_here

## Running it

### Option A — Command line
python main.py
You'll be prompted to describe the leads you want. Example: "restaurants in Lahore"

### Option B — Web app (Streamlit)
streamlit run app.py
This opens a local web page where you can type a prompt, click Search, view
results in a table, and download the Excel file directly.

## Output

Leads are saved as an Excel file named leads_<category>_<location>.xlsx in the
project root, with columns: Business Name, Email, Phone Number, Website, Location.

## Known limitations

- Data availability varies per business — not every listing has a phone number,
  website, or discoverable email. Missing fields are left blank rather than
  causing errors, reflecting real-world data gaps rather than a bug.
- Bing Maps' search ranking sometimes returns nearby-but-not-exact-area results
  for very specific sub-area searches (e.g. a specific neighborhood within a
  large city).
- The email finder only checks a business's homepage; emails behind separate
  "Contact Us" pages may not be found.

## Tech stack

Python, Playwright (browser automation), Groq API / llama-3.3-70b-versatile
(prompt parsing), openpyxl (Excel export), Streamlit (web frontend), requests
(email discovery).
