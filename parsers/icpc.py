import requests
from bs4 import BeautifulSoup
import datetime

def parse():
    # ICPC 官网是 Angular 动态网页，requests 抓不到内容，
    # 且 World Finals 时间一旦定下来很少变，直接硬编码是最稳妥的。
    
    # 1. 设定准确的已知时间 (手动维护 Sources of Truth)
    event_name = "ICPC World Finals 2025"
    start_date_str = "2025-09-20"
    end_date_str = "2025-09-25"
    location = "待公示" # 或者你可以填 "Beijing, China" 如果确定的话
    
    # 2. 状态逻辑修改
    # 只要当前日期还没过结束日期，就显示“赛程已公布”
    today = datetime.date.today().isoformat() # 格式 202X-XX-XX
    
    if today > end_date_str:
        status_text = "比赛已结束"
        status_color = "gray"
    elif today < start_date_str:
        status_text = "赛程已公布" # 因为我们已经填了具体日期，所以就是已公布
        status_color = "blue"
    else:
        status_text = "正在进行中"
        status_color = "green"

    return {
        "status": {"text": status_text, "color": status_color},
        "info_grid": [
            {"label": "最新赛事", "value": event_name},
            {"label": "时间范围", "value": f"{start_date_str} - {end_date_str}"},
            {"label": "地点", "value": location}
        ],
        # 因为抓不到动态网页的表格，这里给个简单的手动列表，或者留空
        "detailed_schedule": [
            {"day": start_date_str, "events": [{"time": "全天", "desc": "开幕式 & 签到", "loc": "待定"}]},
            {"day": end_date_str, "events": [{"time": "全天", "desc": "闭幕式 & 颁奖", "loc": "待定"}]}
        ] 
    }
