import requests
from bs4 import BeautifulSoup
import datetime

def parse():
    url = "https://icpc.global/worldfinals/schedule"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    # 1. 默认兜底数据
    event_name = "ICPC World Finals"
    start_date_str = "2025-09-20" # 默认为截图日期
    end_date_str = "2025-09-25"
    location = "待公示"
    detailed_schedule = []

    try:
        # 2. 发起真实请求
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. 动态解析 (基于截图中的结构)
        # 提取标题，例如 "The 2025 ICPC World Finals"
        title_tag = soup.find('h1') or soup.find('div', class_='schedule-title')
        if title_tag:
            event_name = title_tag.get_text(strip=True)

        # 提取所有日期块
        # 截图显示日期作为小标题出现，后面紧跟表格
        days = []
        day_headers = soup.find_all(['h2', 'h3', 'div'], class_=lambda x: x and 'day' in x.lower())
        
        for day in day_headers:
            date_text = day.get_text(strip=True)
            days.append(date_text)
            
            # 提取该日期下的具体事件表格
            day_events = []
            table = day.find_next('table')
            if table:
                rows = table.find_all('tr')[1:] # 跳过表头
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        day_events.append({
                            "time": cols[0].get_text(strip=True),
                            "desc": cols[1].get_text(strip=True),
                            "loc": cols[2].get_text(strip=True) if len(cols) > 2 else ""
                        })
            detailed_schedule.append({"day": date_text, "events": day_events})

        if days:
            start_date_str = days[0]
            end_date_str = days[-1]

    except Exception as e:
        print(f"爬取解析失败: {e}")

    # 4. 状态逻辑判断 (保持原样)
    today = datetime.date.today().isoformat()
    status_text = "待更新"
    status_color = "yellow"

    # 注意：这里如果抓取到的是非标准日期格式，判断会失效，建议实战中转为 datetime 判断
    if "September" in start_date_str: # 针对截图日期格式的简单处理
        status_text = "赛程已公布"
        status_color = "blue"

    return {
        "status": {"text": status_text, "color": status_color},
        "info_grid": [
            {"label": "最新赛事", "value": event_name},
            {"label": "时间范围", "value": f"{start_date_str} - {end_date_str}"},
            {"label": "地点", "value": location}
        ],
        "detailed_schedule": detailed_schedule # 传给二级页面使用
    }
