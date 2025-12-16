import json
import time
import yaml
import requests
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

from parsers import demo_parser

PARSERS = {
    "demo_parser": demo_parser,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; contest-bot/1.0; +https://zihguo.me)"
}

def fetch(url: str, timeout: int = 15) -> str:
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.text

def load_sources(path="sources.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg.get("sources", [])

def render_index(items, generated_at: str):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"])
    )
    tpl = env.get_template("index.html.j2")
    return tpl.render(items=items, generated_at=generated_at)

def main():
    sources = load_sources()
    all_items = []
    errors = []

    for s in sources:
        sid = s["id"]
        name = s["name"]
        url = s["url"]
        parser_name = s.get("parser", "demo_parser")
        limit = int(s.get("limit", 20))
        selectors = s.get("selectors", {}) or {}

        parser = PARSERS.get(parser_name)
        if not parser:
            errors.append(f"{sid}: parser not found: {parser_name}")
            continue

        try:
            html = fetch(url)
            parsed = parser.parse(html, base_url=url, selectors=selectors, limit=limit)

            for it in parsed[:limit]:
                all_items.append({
                    "source_id": sid,
                    "source_name": name,
                    "title": (it.get("title") or "").strip(),
                    "link": (it.get("link") or "").strip(),
                    "date": (it.get("date") or "").strip(),
                })

            time.sleep(0.5)

        except Exception as e:
            errors.append(f"{sid}: {type(e).__name__}: {e}")

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 输出 data.json 便于排错
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(
            {"generated_at": generated_at, "count": len(all_items), "errors": errors, "items": all_items},
            f, ensure_ascii=False, indent=2
        )

    html_out = render_index(all_items, generated_at)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_out)

if __name__ == "__main__":
    main()
