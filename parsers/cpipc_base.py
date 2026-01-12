import requests
from bs4 import BeautifulSoup

def get_data(comp_id, comp_name):
    url = f"https://cpipc.acge.org.cn/cw/hp/{comp_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."}
    
    try:
        response = requests.get(url, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取原始状态文本
        status_tag = soup.select_one('.state') or soup.select_one('.status-tag')
        raw_status = status_tag.get_text(strip=True) if status_tag else "查看官网"
        
        # --- 核心逻辑：统一种类颜色 ---
        status_text = raw_status
        status_color = "blue"  # 默认蓝色 (查看官网)

        if any(word in raw_status for word in ["报名", "火热"]):
            status_color = "green"  # 报名中 -> 绿色
        elif any(word in raw_status for word in ["进行", "运行"]):
            status_color = "blue"   # 进行中 -> 蓝色
        elif any(word in raw_status for word in ["待更新", "同步", "未知"]):
            status_color = "yellow" # 待更新 -> 黄色
        elif any(word in raw_status for word in ["结束", "闭幕"]):
            status_color = "gray"   # 已结束 -> 灰色
        
        # 抓取最新公告
        notice_tag = soup.select_one('.news-list-item a') or soup.select_one('.notice-list a')
        latest_notice = notice_tag.get_text(strip=True) if notice_tag else "暂无公告"
        
        return {
            "status": {"text": status_text, "color": status_color},
            "info_grid": [
                {"label": "赛事全称", "value": comp_name},
                {"label": "最新动态", "value": latest_notice[:25] + "..."}
            ]
        }
    except:
        # 出错时统一显示黄色“待更新”
        return {
            "status": {"text": "待更新", "color": "yellow"},
            "info_grid": [{"label": "赛事名称", "value": comp_name}, {"label": "状态", "value": "点击官网查看"}]
        }
