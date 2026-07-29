from urllib.parse import urlparse, parse_qs, unquote

def scrape_first_result(page) -> dict:
    try:
        first_card = page.locator('[id^="listingItem_"]').first
        first_card.click()

        page.wait_for_selector("h2.eh_title.b_entityTitle", timeout=10000)

        # Give the rest of the detail panel (phone, website links) time to render.
        # Poll for up to 5 seconds for a tel: link OR an external website link to
        # appear, since these can load slightly after the title.
        try:
            page.wait_for_function(
                """() => {
                    const hasTel = document.querySelector('a[href^="tel:"]');
                    const hasSubtitle = document.querySelector('.eh_subtitle a');
                    const links = Array.from(document.querySelectorAll('a[href^="http"]'));
                    const excluded = ["bingplaces.com", "maplibre.org", "tripadvisor.com"];
                    const hasSite = links.some(a => {
                        if (excluded.some(d => a.href.includes(d))) return false;
                        if (a.href.includes("bing.com") && !a.href.includes("alink/link")) return false;
                        return true;
                    });
                    return hasTel || hasSubtitle || hasSite;
                }""",
                timeout=5000
            )
        except Exception:
            pass  # it's OK if neither ever appears - business may genuinely lack both

        return _extract_current_panel(page)

    except Exception:
        return {"name": "", "phone": "", "website": ""}


def _extract_current_panel(page) -> dict:
    name_el = page.locator("h2.eh_title.b_entityTitle span.eh_title_container")
    name = name_el.text_content()
    name = name.strip() if name else ""

    phone_el = page.locator('a[href^="tel:"]')
    phone = ""
    if phone_el.count() > 0:
        raw = phone_el.get_attribute("href")
        if raw:
            phone = raw.replace("tel:", "").strip()

    website = ""
    all_links = page.locator("a[href^='http']")
    excluded = ["bing.com/aclick", "bingplaces.com", "maplibre.org", "tripadvisor.com", "microsoft.com", "live.com", "openstreetmap.org", "hereapi.com", "tomtom.com"]
    for i in range(all_links.count()):
        href = all_links.nth(i).get_attribute("href") or ""
        href = href.strip()
        if not href.startswith("http"):
            continue
        if href.startswith("https://www.bing.com/alink/link?url="):
            parsed = urlparse(href)
            params = parse_qs(parsed.query)
            if "url" in params:
                href = unquote(params["url"][0])
        else:
            if any(d in href for d in excluded):
                continue
        if not href.startswith("http"):
            continue
        if "›" in href:
            continue
        website = href
        break

    if not phone:
        with open("last_run_dump.html", "w", encoding="utf-8") as f:
            f.write(page.content())

    return {"name": name, "phone": phone, "website": website}


def scrape_results(page, max_results: int = 10) -> list[dict]:
    cards = page.locator('[id^="listingItem_"]').all()
    results = []
    seen_names = set()
    for i in range(min(max_results, len(cards))):
        try:
            cards[i].click()
            page.wait_for_selector("h2.eh_title.b_entityTitle", timeout=8000)
            try:
                page.wait_for_function(
                    """() => {
                        const hasTel = document.querySelector('a[href^="tel:"]');
                        const hasSubtitle = document.querySelector('.eh_subtitle a');
                        const links = Array.from(document.querySelectorAll('a[href^="http"]'));
                        const excluded = ["bingplaces.com", "maplibre.org", "tripadvisor.com"];
                        const hasSite = links.some(a => {
                            if (excluded.some(d => a.href.includes(d))) return false;
                            if (a.href.includes("bing.com") && !a.href.includes("alink/link")) return false;
                            return true;
                        });
                        return hasTel || hasSubtitle || hasSite;
                    }""",
                    timeout=5000
                )
            except Exception:
                pass
            data = _extract_current_panel(page)
            if data["name"] and data["name"] not in seen_names:
                seen_names.add(data["name"])
                results.append(data)
        except Exception as e:
            print(f"Skipped result {i}: {e}")
            continue
    return results