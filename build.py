import yaml
import json
import importlib
import datetime
import os
import sys

# 确保脚本能找到 parsers 目录
sys.path.append(os.getcwd())

def generate_detail_page(item, schedule):
    """ 生成二级详情页 """
    days_html = ""
    for day in schedule:
        events_rows = ""
        for e in day.get('events', []):
            events_rows += f"""
            <tr>
                <td class="py-3 font-mono font-bold text-slate-700">{e.get('time', '--')}</td>
                <td class="py-3 text-slate-800">{e.get('desc', '--')}</td>
                <td class="py-3 text-slate-500 italic">{e.get('loc', '--')}</td>
            </tr>
            """
        
        days_html += f"""
        <div class="mb-10">
            <h3 class="text-lg font-bold text-blue-600 mb-4 pb-2 border-b-2 border-blue-50">📅 {day.get('day', '未知日期')}</h3>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead class="text-slate-400 font-normal border-b border-slate-100">
                        <tr>
                            <th class="py-2 w-32">时间</th>
                            <th class="py-2">事项</th>
                            <th class="py-2">地点</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-50">
                        {events_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """

    # 组合成完整的 HTML
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{item['title']} - 详细赛程</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 min-h-screen p-4 md:p-10">
        <div class="max-w-4xl mx-auto">
            <a href="/" class="inline-flex items-center text-blue-600 font-bold mb-8 hover:underline">
                ← 返回首页聚合
            </a>
            <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
                <div class="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-white">
                    <h1 class="text-2xl md:text-3xl font-bold">{item['title']}</h1>
                    <p class="mt-2 opacity-80 underline"><a href="{item['link_homepage']}" target="_blank">访问官方网站 →</a></p>
                </div>
                <div class="p-6 md:p-10">
                    <h2 class="text-xl font-bold text-slate-800 mb-8 flex items-center">
                        <span class="w-2 h-6 bg-blue-600 rounded-full mr-3"></span>
                        详细日程安排
                    </h2>
                    <div class="space-y-4">
                        {days_html if days_html else '<p class="text-slate-400 italic">暂无详细日程数据同步</p>'}
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(f"details/{item['id']}.html", "w", encoding="utf-8") as f:
        f.write(html_template)

def main():
    print(">>> 开始构建竞赛数据与详情页...")
    
    # 修正点：不要在这里使用 f-string，直接定义字典
    final_data = {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": []
    }

    if not os.path.exists("details"):
        os.makedirs("details")

    try:
        with open("contests.yaml", "r", encoding="utf-8") as f:
            contest_list = yaml.safe_load(f)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return

    for contest in contest_list:
        print(f"正在处理: {contest['name']}...")
        
        # 修正点：直接定义 item 字典
        item = {
            "id": contest["id"],
            "title": contest["name"],
            "tags": contest.get("tags", []),
            "link_homepage": contest.get("homepage", ""),
            "link_detail": f"details/{contest['id']}.html",
            "status": {"text": "待更新", "color": "yellow"},
            "info_grid": [{"label": "官方链接", "value": "点击进入官网"}],
            "last_updated": datetime.datetime.now().strftime("%H:%M")
        }

        if contest.get("parser"):
            try:
                module = importlib.import_module(contest["parser"])
                importlib.reload(module)
                dynamic_data = module.parse() 
                
                # 合并爬虫数据
                item.update(dynamic_data)

                if "detailed_schedule" in dynamic_data:
                    generate_detail_page(item, dynamic_data["detailed_schedule"])
                    print(f"  -> 已成功生成详情页")

            except Exception as e:
                print(f"  -> 抓取或解析失败: {e}")

        final_data["items"].append(item)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    print(">>> 所有任务构建完成！")

if __name__ == "__main__":
    main()
