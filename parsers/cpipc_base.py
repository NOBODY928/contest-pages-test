import requests
from bs4 import BeautifulSoup  # <--- 就是缺了这一行！
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os
import time

# 1. 禁用 SSL 警告（防止控制台输出一大堆红色警告）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 2. 【核心修复】这里就是你缺失的 HEADERS 定义
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
# 创建一个带有重试功能的 session
def get_session():
    session = requests.Session()
    retry = Retry(
        total=3,  # 最多重试3次
        backoff_factor=1,  # 每次重试间隔 1秒, 2秒, 4秒...
        status_forcelist=[500, 502, 503, 504],  # 遇到这些服务器错误码就重试
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def get_data(comp_id, comp_name):
    comp_id = str(comp_id).strip()
    url = f"https://cpipc.acge.org.cn/cw/hp/{comp_id}"
    
    try:
        session = get_session() # 获取带重试功能的 session
        
        # 使用 session.get 而不是 requests.get
        r = session.get(url, headers=HEADERS, timeout=60, verify=False)
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

    except Exception as e:
        # 【新增】打印出具体是哪个比赛出错了，以及错误信息是什么
        print(f"Error fetching {comp_name} (ID: {comp_id}): {e}")
        
        return {
            "status": {"text": "待更新", "color": "yellow"},
            "info_grid": [
                {"label": "赛事名称", "value": comp_name},
                {"label": "状态", "value": "数据同步中"},
            ],
        }
