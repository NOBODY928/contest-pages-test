import requests
from bs4 import BeautifulSoup
import datetime

def parse():
    url = "https://dasai.lanqiao.cn/notices/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    # 1. 设定默认值，确保即便抓取失败也能显示正确的“蓝色/查看官网”
    status_text = "查看官网"
    status_color = "blue"
    latest_notice = "点击查看最新动态"
    
    # 2. 蓝桥杯 2026 赛季时间轴逻辑（根据当前日期自动切换颜色）
    now = datetime.date.today()
    if now.month <= 3:
        status_text = "报名/校赛阶段"
        status_color = "green"  # 3月前显示绿色
    elif now.month == 4:
        status_text = "省赛进行中"
        status_color = "blue"   # 4月显示蓝色
    else:
        status_text = "备赛/国赛期"
        status_color = "gray"   # 其他时间显示灰色

    try:
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            # 兼容多种可能的 HTML 结构
            notice = soup.select_one('.notice-list-item a') or soup.select_one('.news-title') or soup.select_one('article h2')
            if notice:
                latest_notice = notice.get_text(strip=True)
    except Exception as e:
        print(f"!!! Lanqiao Parser Error: {e}")

    # 3. 返回结构严谨的数据
    return {
        "status": {"text": status_text, "color": status_color},
        "info_grid": [
            {"label": "竞赛名称", "value": "第十七届蓝桥杯全国软件大赛"},
            {"label": "最新动态", "value": latest_notice[:25] + "..."}
        ],
        "detailed_schedule": [
            {"day": "2026 蓝桥杯官方里程碑", "events": [
                {"time": "即日起-3月", "desc": "各赛道省赛报名截止", "loc": "官网"},
                {"time": "4月中旬", "desc": "省赛阶段", "loc": "各校赛点"},
                {"time": "6月上旬", "desc": "全国总决赛", "loc": "待定"}
            ]}
        ]
    }
