import re
import requests

EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def find_email(website_url: str, timeout: int = 5) -> str:
    if not website_url or not website_url.startswith("http"):
        return ""

    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; LeadGenAgent/1.0)"}
        resp = requests.get(website_url, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return ""

        html = resp.text

        mailto_match = re.search(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', html)
        if mailto_match:
            return mailto_match.group(1)

        excluded_domains = ["example.com", "sentry.io", "wixpress.com", "godaddy.com"]
        for match in EMAIL_PATTERN.finditer(html):
            email = match.group(0)
            if not any(domain in email for domain in excluded_domains):
                return email

        return ""

    except Exception:
        return ""
