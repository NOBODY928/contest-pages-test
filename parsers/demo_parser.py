def parse(html: str, base_url: str, selectors: dict = None, limit: int = 20):
    # 先返回固定数据，确保流水线跑通；后续再替换为真实抓取解析
    return [
        {"title": "占位：后续这里显示抓取到的竞赛通知", "link": base_url, "date": ""}
    ]
