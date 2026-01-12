import yaml
import json
import importlib
import datetime
import os
import sys

# 确保脚本能找到 parsers 目录
sys.path.append(os.getcwd())

def generate_detail_page(item, schedule):
    """ 
    生成二级详情页 - 静态渲染版
    直接将数据注入 HTML，无需在前端 fetch data.json，解决路径错误问题
    """
    days_html = ""
    if not schedule:
        days_html = '<p class="text-slate-400 italic text-center py-10">暂无详细日程数据同步</p>'
    else:
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
                <h3 class="text-lg font-bold text-blue-600 mb-4 pb-2 border-b-2 border-blue-50">📅 {day.get('day', '日期待定')}</h3>
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

    # 组合成完整的静态 HTML
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{item['title']} - 详细赛程</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        </style>
    </head>
    <body class="bg-slate-50 min-h-screen p-4 md:p-10">
        <div class="max-w-4xl mx-auto">
            <a href="/" class="inline-flex items-center text-blue-600 font-bold mb-8 hover:translate-x-1 transition-transform">
                ← 返回首页聚合
            </a>
            
            <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
                <div class="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 text-white">
                    <div class="flex flex-wrap items-center gap-3 mb-4">
                        {" ".join([f'<span class="px-3 py-1 bg-white/20 rounded-full text-xs">{t}</span>' for t in item.get('tags', [])])}
                    </div>
                    <h1 class="text-2xl md:text-4xl font-bold">{item['title']}</h1>
                    <p class="mt-4 opacity-90">
                        <a href="{item['link_homepage']}" target="_blank" class="inline-flex items-center underline decoration-2 underline-offset-4 hover:opacity-100">
                            访问官方网站官方链接
                            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        </a>
                    </p>
                </div>
                
                <div class="p-6 md:p-10">
                    <h2 class="text-xl font-bold text-slate-800 mb-8 flex items-center">
                        <span class="w-2 h-6 bg-blue-600 rounded-full mr-3"></span>
                        详细日程安排
                    </h2>
                    
                    <div class="space-y-4">
                        {days_html}
                    </div>
                </div>
            </div>
            
            <footer class="mt-12 text-center text-slate-400 text-sm">
                © {datetime.datetime.now().year} zihguo.me · 数据自动抓取于官网
            </footer>
        </div>
    </body>
    </html>
    """
    
    with open(f"details/{item['id']}.html", "w", encoding="utf-8") as f:
        f.write(html_template)

def main():
    print(">>> 启动构建程序...")
    
    # 1. 初始化数据结构
    final_data = {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": []
    }

    # 2. 检查并创建详情页目录
    if not os.path.exists("details"):
        os.makedirs("details")
        print("--- 已创建 details 目录")

    # 3. 读取配置文件
    try:
        with open("contests.yaml", "r", encoding="utf-8") as f:
            contest_list = yaml.safe_load(f)
    except Exception as e:
        print(f"!!! 错误：读取 contests.yaml 失败: {e}")
        return

    # 4. 遍历并处理每个竞赛
    for contest in contest_list:
        cid = contest.get("id", "unknown")
        name = contest.get("name", "未命名竞赛")
        print(f"正在处理 [{cid}] {name}...")
        
        # 初始卡片数据
        item = {
            "id": cid,
            "title": name,
            "tags": contest.get("tags", []),
            "link_homepage": contest.get("homepage", "#"),
            "link_detail": f"details/{cid}.html",
            "status": {"text": "待更新", "color": "gray"},
            "info_grid": [{"label": "数据状态", "value": "正在同步最新信息"}],
            "last_updated": datetime.datetime.now().strftime("%H:%M")
        }

        # 执行动态爬虫
        if contest.get("parser"):
            try:
                # 动态加载并重新运行 parser
                module = importlib.import_module(contest["parser"])
                importlib.reload(module)
                dynamic_data = module.parse() 
                
                # 合并爬虫抓取到的数据 (status, info_grid, detailed_schedule)
                item.update(dynamic_data)

                # 生成详情页
                schedule = dynamic_data.get("detailed_schedule", [])
                generate_detail_page(item, schedule)
                print(f"  -> 详情页生成成功")

            except Exception as e:
                print(f"  -> 解析失败: {e}")
        else:
            # 如果没有爬虫，也生成一个空的详情页
            generate_detail_page(item, [])

        final_data["items"].append(item)

    # 5. 写入 data.json 供主页使用
    try:
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        print(">>> 首页数据 data.json 更新成功")
    except Exception as e:
        print(f"!!! 错误：写入 data.json 失败: {e}")

    print(f">>> 构建完成！总计处理 {len(final_data['items'])} 个竞赛项目。")

if __name__ == "__main__":
    main()
