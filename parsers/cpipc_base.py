import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}

def get_data(comp_id, comp_name):
    comp_id = str(comp_id).strip()
    url = f"https://cpipc.acge.org.cn/cw/hp/{comp_id}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")

        status_tag = soup.select_one(".state") or soup.select_one(".status-tag")
        raw_text = status_tag.get_text(strip=True) if status_tag else "查看官网"

        status_color = "green" if "报名" in raw_text else "blue"
        status_text = raw_text

        notice_tag = soup.select_one(".news-list-item a") or soup.select_one(".notice-list a")
        latest_notice = notice_tag.get_text(strip=True) if notice_tag else "点击官网查看详情"

        return {
            "status": {"text": status_text, "color": status_color},
            "info_grid": [
                {"label": "赛事名称", "value": comp_name},
                {"label": "最新动态", "value": latest_notice[:25] + "..."},
            ],
        }

    except Exception:
        return {
            "status": {"text": "待更新", "color": "yellow"},
            "info_grid": [
                {"label": "赛事名称", "value": comp_name},
                {"label": "状态", "value": "数据同步中"},
            ],
        }

