import requests
from bs4 import BeautifulSoup

def get_data(comp_id, comp_name):
    url = f"https://cpipc.acge.org.cn/cw/hp/{comp_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(url, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取状态 (进行中/已结束)
        status_tag = soup.select_one('.state') or soup.select_one('.status-tag')
        status_text = status_tag.get_text(strip=True) if status_tag else "查看官网"
        
        # 抓取最新公告标题
        notice_tag = soup.select_one('.news-list-item a') or soup.select_one('.notice-list a')
        latest_notice = notice_tag.get_text(strip=True) if notice_tag else "暂无公告"
        
        return {
            "status": {"text": status_text, "color": "green" if "报名" in status_text else "blue"},
            "info_grid": [
                {"label": "赛事全称", "value": comp_name},
                {"label": "最新动态", "value": latest_notice[:25] + "..."}
            ]
        }
    except:
        return {
            "status": {"text": "同步中", "color": "yellow"},
            "info_grid": [{"label": "赛事名称", "value": comp_name}, {"label": "动态", "value": "点击官网查看"}]
        }
