import requests
from bs4 import BeautifulSoup
import datetime

def parse():
    # 这里模拟爬虫逻辑
    # 实际部署时，你可以把下面的变量替换为 soup.find(...) 的结果
    
    event_name = "The 2025 ICPC World Finals"
    start_date_str = "2025-09-20"
    end_date_str = "2025-09-25"
    location = "中国 (China)"
    
    # 简单的状态判断逻辑
    today = datetime.date.today().isoformat()
    
    # 默认状态
    status_text = "未知"
    status_color = "gray"

    if today < start_date_str:
        status_text = "筹备中"
        status_color = "blue"
    elif start_date_str <= today <= end_date_str:
        status_text = "进行中"
        status_color = "green"
    else:
        status_text = "已结束"
        status_color = "gray"

    # 返回标准化的数据结构
    return {
        "status": {
            "text": status_text,
            "color": status_color
        },
        "info_grid": [
            {"label": "当前阶段", "value": event_name},
            {"label": "比赛时间", "value": f"{start_date_str} 至 {end_date_str}"},
            {"label": "地点", "value": location}
        ]
    }
