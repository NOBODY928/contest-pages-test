import requests
from bs4 import BeautifulSoup
import datetime

def parse():
    # 使用正确的官网地址
    url = "https://dtcup.dtxiaotangren.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # 默认兜底数据
    status_text = "查看官网"
    status_color = "yellow"
    info_grid = [
        {"label": "当前届次", "value": "第十三届大唐杯"},
        {"label": "主办单位", "value": "工信部人才交流中心"},
        {"label": "最新动态", "value": "请点击详情查看公告"}
    ]
    detailed_schedule = []

    try:
        # 发起请求
        response = requests.get(url, headers=headers, timeout=15, verify=True)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. 尝试从新平台抓取公告标题
        # 小唐人平台的公告通常在带有 .notice-item 或 .list-item 类的元素中
        news_tag = soup.find(class_=lambda x: x and ('notice' in x or 'news' in x or 'list' in x))
        if news_tag:
            first_news = news_tag.find('a') or news_tag
            news_text = first_news.get_text(strip=True)
            if news_text:
                info_grid[2]["value"] = news_text[:28] + "..."

        # 2. 状态判定逻辑 (根据 2026 年的时间线)
        # 大唐杯通常 12月-次年3月报名，4月省赛，6月国赛
        now = datetime.date.today()
        month = now.month
        
        if 1 <= month <= 3:
            status_text = "报名进行中"
            status_color = "green"
        elif 4 <= month <= 5:
            status_text = "省赛进行中"
            status_color = "blue"
        elif month == 6:
            status_text = "全国总决赛"
            status_color = "blue"
        else:
            status_text = "非赛季时期"
            status_color = "gray"

        # 3. 详细赛程（基于往届规律的预估，方便生成详情页）
        detailed_schedule = [
            {
                "day": "2026 赛季关键节点",
                "events": [
                    {"time": "1月 - 3月", "desc": "在线报名与校内选拔", "loc": "官网/各高校"},
                    {"time": "4月中下旬", "desc": "省赛/区域赛", "loc": "各省赛点"},
                    {"time": "5月 - 6月", "desc": "全国总决赛", "loc": "北京/北方工大"}
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
