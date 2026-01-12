import requests
from bs4 import BeautifulSoup
import datetime

def parse():
    url = "https://dasai.lanqiao.cn/notices/"
    # 强制预设，防止逻辑跑偏
    status_text = "报名进行中"
    status_color = "green"
    
    now = datetime.date.today()
    # 2026年3月前一律绿色报名中，之后切换为蓝色
    if now.month > 3:
        status_text = "查看官网"
        status_color = "blue"

    try:
        # 这里只负责抓动态，不改变颜色
        # ... 你的抓取逻辑 ...
        pass
    except:
        pass

    return {
        "status": {"text": status_text, "color": status_color},
        "info_grid": [
            {"label": "竞赛名称", "value": "第十七届蓝桥杯全国软件大赛"},
            {"label": "最新动态", "value": "点击查看官网公告..."}
        ]
    }
