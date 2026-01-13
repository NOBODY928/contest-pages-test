import requests
from bs4 import BeautifulSoup
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os
import time
import datetime
import yaml
from jinja2 import Environment, FileSystemLoader

# 1. 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 2. 定义请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive"
}

# 3. 创建 Session
def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

# 4. 爬取核心逻辑
def get_data(comp_id, comp_name, homepage):
    # 如果是 ICPC 这种不需要爬的，直接返回固定数据(示例)
    if "icpc" in str(comp_id).lower():
         return {
            "status": {"text": "赛程已公布", "color": "blue"},
            "info_grid": [
                {"label": "赛事名称", "value": "ICPC World Finals"},
                {"label": "最新动态", "value": "2025-09-20 开赛"},
            ]
        }

    # 正常的研创网爬取
    comp_id = str(comp_id).strip()
    # 优先使用 yaml 里配置的 homepage，如果没有则拼接默认 id
    url = homepage if homepage else f"https://cpipc.acge.org.cn/cw/hp/{comp_id}"
    
    try:
        session = get_session()
        r = session.get(url, headers=HEADERS, timeout=30, verify=False)
        r.raise_for_status()
        r.encoding = "utf-8"
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        # 获取状态
        status_tag = soup.select_one(".state") or soup.select_one(".status-tag")
        if status_tag:
            raw_text = status_tag.get_text(strip=True)
            status_color = "green" if "报名" in raw_text or "进行" in raw_text else "blue"
            status_text = raw_text
        else:
            status_text = "查看官网"
            status_color = "blue"

        # 获取动态
        notice_tag = soup.select_one(".news-list-item a") or soup.select_one(".notice-list a")
        latest_notice = notice_tag.get_text(strip=True) if notice_tag else "点击官网查看详情..."

        return {
            "status": {"text": status_text, "color": status_color},
            "info_grid": [
                {"label": "赛事名称", "value": comp_name},
                {"label": "最新动态", "value": latest_notice[:30] + "..." if len(latest_notice)>30 else latest_notice},
            ]
        }

    except Exception as e:
        print(f"Error fetching {comp_name}: {e}")
        return {
            "status": {"text": "待更新", "color": "yellow"},
            "info_grid": [
                {"label": "赛事名称", "value": comp_name},
                {"label": "状态", "value": "数据同步中"},
            ]
        }

# 5. 主程序
def main():
    print(">>> 读取配置文件 contests.yaml ...")
    with open("contests.yaml", "r", encoding="utf-8") as f:
        contests_config = yaml.safe_load(f)

    final_data = []

    for item in contests_config:
        print(f"正在处理: {item['name']} ...")
        
        # 1. 爬取动态数据
        crawled_data = get_data(item.get('id'), item['name'], item.get('homepage'))
        
        # 2. 合并数据：将 YAML 里的 logo, tags, url 和爬取到的 status, info 合并
        merged_item = {
            "name": item['name'],
            "url": item.get('homepage', '#'),
            "logo": item.get('logo', ''), # 这里读取 YAML 里的 logo 路径
            "tags": item.get('tags', []),
            "status": crawled_data['status'],
            "info_grid": crawled_data['info_grid']
        }
        final_data.append(merged_item)

    # 3. 保存 data.json (备份用)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(">>> data.json 生成成功")

    # 4. 【关键步骤】使用 Jinja2 渲染 HTML 模板
    print(">>> 正在渲染 index.html 模板...")
    
    # 加载 templates 目录
    env = Environment(loader=FileSystemLoader('templates'))
    # 获取 index.html.j2 模板
    template = env.get_template('index.html.j2')
    
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 渲染！把数据传给模板
    html_output = template.render(contests=final_data, updated_at=current_time)
    
    # 写入根目录的 index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_output)
        
    print(">>> index.html 生成成功！(Apple 风格样式已应用)")

if __name__ == "__main__":
    main()
