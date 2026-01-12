import requests
from bs4 import BeautifulSoup
import datetime

def parse():
    url = "https://dasai.lanqiao.cn/notices/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    status_text = "报名进行中"
    status_color = "green"
    info_grid = [
        {"label": "竞赛名称", "value": "第十七届蓝桥杯全国软件大赛"},
        {"label": "主办单位", "value": "工信部人才交流中心"},
        {"label": "最新动态", "value": "同步中..."}
    ]

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 抓取第一条公告
        notice = soup.select_one('.notice-list-item a') or soup.select_one('.news-title')
        if notice:
            info_grid[2]["value"] = notice.get_text(strip=True)[:25] + "..."

        # 蓝桥杯 2026 赛季逻辑
        now = datetime.date.today()
        if now.month <= 3:
            status_text = "报名/校赛阶段"
            status_color = "green"
        elif now.month == 4:
            status_text = "省赛月"
            status_color = "blue"
        else:
            status_text = "备赛/国赛期"
            status_color = "gray"

    except Exception as e:
        print(f"Lanqiao Parser Error: {e}")

    return {
        "status": {"text": status_text, "color": status_color},
        "info_grid": info_grid,
        "detailed_schedule": [
            {"day": "2026 蓝桥杯时间表", "events": [
                {"time": "即日起-3月", "desc": "省赛报名截止", "loc": "官网"},
                {"time": "4月中旬", "desc": "省赛（软件/电子类）", "loc": "各校赛点"},
                {"time": "6月", "desc": "全国总决赛", "loc": "北京/线上"}
            ]}
        ]
    }
