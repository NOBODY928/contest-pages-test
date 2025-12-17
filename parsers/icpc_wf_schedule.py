import re
from bs4 import BeautifulSoup
from datetime import datetime

DATE_PATTERNS = [
    # 2025-03-10 / 2025/03/10
    r"(20\d{2})[/-](\d{1,2})[/-](\d{1,2})",
    # March 10, 2025
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+20\d{2}",
]

def extract_dates(text: str):
    dates = []
    for p in DATE_PATTERNS:
        for m in re.findall(p, text):
            dates.append(" ".join(m) if isinstance(m, tuple) else m)
    return dates

def parse(html: str, base_url: str, selectors=None, limit: int = 100):
    soup = BeautifulSoup(html, "lxml")
    results = []

    # 抓所有标题 + 段落 + 列表项
    candidates = soup.find_all(["h1", "h2", "h3", "p", "li", "tr"])

    for el in candidates:
        text = el.get_text(" ", strip=True)
        if not text or len(text) < 10:
            continue

        dates = extract_dates(text)
        if not dates:
            continue

        results.append({
            "title": text[:120],     # 防止过长
            "link": base_url,
            "date": ", ".join(dates),
        })

        if len(results) >= limit:
            break

    return results
