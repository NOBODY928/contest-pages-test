import requests
from bs4 import BeautifulSoup
import datetime

def parse():
    # 大唐杯官网地址
    url = "http://dtcup.dtcenter.cn/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # 默认数据（防止爬取失败）
    status_text = "查看官网"
    status_color = "yellow"
    info_grid = [
        {"label": "赛事名称", "value": "第十三届大唐杯"},
        {"label": "主办单位", "value": "工信部人才交流中心"},
        {"label": "当前信息", "value": "请访问官网查看最新公告"}
    ]
    detailed_schedule = []

    try:
        # 获取首页内容
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. 尝试抓取标题或公告内容（此处根据大唐杯常见的CMS结构编写）
        # 寻找包含“报名”或“时间”字样的通知
        news_list = soup.find_all('li')
        latest_news = ""
        for li in news_list:
            text = li.get_text()
            if "报名" in text or "通知" in text:
                latest_news = text.strip()
                break
        
        if latest_news:
            info_grid[2]["value"] = latest_news[:25] + "..." # 截断过长文字

        # 2. 状态逻辑判定 (2026年通常在3-4月省赛，5-6月国赛)
        month = datetime.date.today().month
        if 1 <= month <= 3:
            status_text = "报名/备赛中"
            status_color = "green"
        elif 4 <= month <= 6:
            status_text = "赛季进行中"
            status_color = "blue"
        else:
            status_text = "非赛季/筹备中"
            status_color = "gray"

        # 3. 模拟一个简单的赛程表（如果官网结构复杂，我们先手动维护关键节点）
        detailed_schedule = [
            {
                "day": "2026年上半年",
                "events": [
                    {"time": "1月-3月", "desc": "院校赛/省赛报名", "loc": "各校/官网"},
                    {"time": "4月", "desc": "省赛阶段", "loc": "各省赛点"},
                    {"time": "5月-6月", "desc": "全国总决赛", "loc": "北京/线上"}
                ]
            }
        ]

    except Exception as e:
        print(f"大唐杯解析失败: {e}")

    return {
        "status": {"text": status_text, "color": status_color},
        "info_grid": info_grid,
        "detailed_schedule": detailed_schedule
    }
