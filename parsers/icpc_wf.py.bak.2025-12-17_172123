import re
from bs4 import BeautifulSoup

MONTHS = r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"

DATE_REGEXES = [
    re.compile(r"\b(20\d{2})[/-](\d{1,2})[/-](\d{1,2})\b"),
    re.compile(rf"\b{MONTHS}\s+\d{{1,2}}(?:\s*[-–]\s*\d{{1,2}})?(?:,)?\s+20\d{{2}}\b", re.IGNORECASE),
    re.compile(rf"\b{MONTHS}\s+\d{{1,2}}(?:,)?\s*(?:[-–]\s*{MONTHS}\s+\d{{1,2}})?(?:,)?\s+20\d{{2}}\b", re.IGNORECASE),
]

def _extract_dates(text: str):
    hits = []
    for rx in DATE_REGEXES:
        for m in rx.finditer(text):
            hits.append(m.group(0))
    seen = set()
    out = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out

def parse(html: str, base_url: str, selectors=None, limit: int = 80):
    soup = BeautifulSoup(html, "lxml")
    main = soup.find("main") or soup.body or soup

    results = []

    for tr in main.find_all("tr"):
        text = tr.get_text(" ", strip=True)
        if not text or len(text) < 10:
            continue
        dates = _extract_dates(text)
        if not dates:
            continue
        results.append({
            "title": re.sub(r"\s+", " ", text)[:160],
            "link": base_url,
            "date": "; ".join(dates),
        })
        if len(results) >= limit:
            return results

    for el in main.find_all(["li", "p", "h2", "h3", "h4"]):
        text = el.get_text(" ", strip=True)
        if not text or len(text) < 8:
            continue
        dates = _extract_dates(text)
        if not dates:
            continue
        results.append({
            "title": re.sub(r"\s+", " ", text)[:160],
            "link": base_url,
            "date": "; ".join(dates),
        })
        if len(results) >= limit:
            break

    return results
