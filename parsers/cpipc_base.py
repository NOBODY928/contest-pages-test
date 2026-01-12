import requests
from bs4 import BeautifulSoup

def get_data(comp_id, comp_name):
    url = f"https://cpipc.acge.org.cn/cw/hp/{comp_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(url, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取状态文本
        status_tag = soup.select_one('.state') or soup.select_one('.status-tag')
        raw_text = status_tag.get_text(strip=True) if status_tag else "查看官网"
        
        # --- 颜色逻辑：只做最简单的强制映射 ---
        # 只要包含"报名"，就是绿色，否则一律蓝色
        status_color = "green" if "报名" in raw_text else "blue"
        status_text = raw_text

        # 抓取公告
        notice_tag = soup.select_one('.news-list-item a') or soup.select_one('.notice-list a')
        latest_notice = notice_tag.get_text(strip=True) if notice_tag else "点击官网查看详情"
        
        return {
            "status": {"text": status_text, "color": status_color},
            "info_grid": [
                {"label": "赛事全称", "value": comp_name},
                {"label": "最新动态", "value": latest_notice[:25] + "..."}
            ]
        }
    except Exception as e:
        # 只有在请求超时或网络断开时，才返回黄色待更新
        return {
            "status": {"text": "待更新", "color": "yellow"},
            "info_grid": [{"label": "赛事名称", "value": comp_name}, {"label": "状态", "value": "数据同步中"}]
        }
