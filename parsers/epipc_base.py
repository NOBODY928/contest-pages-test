import requests
from bs4 import BeautifulSoup

def get_data(comp_id, comp_name):
    url = f"https://cpipc.acge.org.cn/cw/hp/{comp_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # 设置合理的超时时间，防止单个失败拖慢整个 build
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. 抓取状态文本 (针对系列赛官网的多种可能类名)
        status_tag = soup.select_one('.state') or soup.select_one('.status-tag') or soup.select_one('.competition-state')
        raw_status = status_tag.get_text(strip=True) if status_tag else "查看官网"
        
        # 2. 统一颜色逻辑映射
        status_text = raw_status
        status_color = "blue"  # 默认为蓝色 (查看官网)

        # 优先级判断：报名中 > 进行中 > 待更新
        if any(word in raw_status for word in ["报名", "火热", "开启"]):
            status_color = "green"
            status_text = "报名中"
        elif any(word in raw_status for word in ["同步", "更新", "数据"]):
            status_color = "yellow"
        elif any(word in raw_status for word in ["结束", "闭幕", "公示"]):
            status_color = "gray"
        else:
            # 只要成功抓取到具体文字且不是“待更新”，就显示为蓝色“查看官网”
            status_color = "blue"
            if raw_status == "查看官网":
                status_text = "查看官网"

        # 3. 抓取最新公告
        notice_tag = soup.select_one('.news-list-item a') or soup.select_one('.notice-list a')
        latest_notice = notice_tag.get_text(strip=True) if notice_tag else "点击官网查看详情"
        
        return {
            "status": {"text": status_text, "color": status_color},
            "info_grid": [
                {"label": "赛事全称", "value": comp_name},
                {"label": "最新动态", "value": latest_notice[:25] + "..."}
            ],
            "detailed_schedule": [
                {"day": "官方动态", "events": [{"time": "最新", "desc": latest_notice, "loc": "官网"}]}
            ]
        }
    except Exception as e:
        print(f"Error fetching {comp_name}: {e}")
        # 抓取彻底失败时才显示黄色
        return {
            "status": {"text": "待更新", "color": "yellow"},
            "info_grid": [
                {"label": "赛事名称", "value": comp_name},
                {"label": "数据状态", "value": "同步异常，请检查网络"}
            ]
        }
