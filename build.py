import yaml
import json
import importlib
import datetime
import os
import sys

# 这一步是为了让 python 能找到 parsers 文件夹里的代码
sys.path.append(os.getcwd())

def main():
    print(">>> 开始构建 data.json ...")
    
    final_data = {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": []
    }

    # 1. 读取 contests.yaml
    try:
        with open("contests.yaml", "r", encoding="utf-8") as f:
            contest_list = yaml.safe_load(f)
    except FileNotFoundError:
        print("错误: 找不到 contests.yaml 文件")
        return

    # 2. 循环处理每一个竞赛
    for contest in contest_list:
        print(f"正在处理: {contest['name']} ({contest['id']})...")
        
        # 基础静态数据
        item = {
            "id": contest["id"],
            "title": contest["name"],
            "tags": contest.get("tags", []),
            "link_homepage": contest.get("homepage", ""),
            "link_detail": f"/details/{contest['id']}.html",
            # 默认兜底数据
            "status": {"text": "待更新", "color": "gray"},
            "info_grid": [{"label": "数据源", "value": "等待同步"}],
            "last_updated": ""
        }

        # 3. 如果配置了 parser，尝试运行它
        if contest.get("parser"):
            try:
                # 动态加载 parser 模块 (例如 parsers.icpc)
                module = importlib.import_module(contest["parser"])
                
                # 重新加载模块，防止缓存（调试时很有用）
                importlib.reload(module)
                
                # 执行 parse() 函数
                dynamic_data = module.parse() 
                
                # 合并数据
                item.update(dynamic_data)
                item["last_updated"] = datetime.datetime.now().strftime("%H:%M")
                print(f"  -> 抓取成功: {dynamic_data['status']['text']}")
                
            except Exception as e:
                print(f"  -> [错误] 抓取失败: {e}")
                item["status"] = {"text": "抓取异常", "color": "red"}
                item["info_grid"] = [{"label": "错误信息", "value": str(e)}]

        final_data["items"].append(item)

    # 4. 保存结果
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print("\n>>> 构建完成！已写入 data.json")

if __name__ == "__main__":
    main()
