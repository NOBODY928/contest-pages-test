import datetime

def parse():
    # 逻辑：根据当前月份判断赛季阶段
    now = datetime.date.today()
    status_text = "查看官网"
    status_color = "blue"
    
    # 1-3月通常是报名确认和技术评审阶段
    if now.month <= 3:
        status_text = "赛季准备中"
        status_color = "blue"
    
    return {
        "status": {"text": status_text, "color": status_color},
        "info_grid": [
            {"label": "竞赛名称", "value": "全国大学生机器人大赛 RoboMaster"},
            {"label": "最新动态", "value": "点击查看 2026 赛季手册"}
        ],
        "detailed_schedule": [
            {"day": "2026 赛季预估表", "events": [
                {"time": "12-3月", "desc": "技术方案评审", "loc": "线上"},
                {"time": "5-6月", "desc": "分区赛阶段", "loc": "各赛区"},
                {"time": "8月", "desc": "全国总决赛", "loc": "深圳"}
            ]}
        ]
    }
