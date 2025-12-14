from datetime import datetime, timedelta
import pytz
from .base import BaseTool

class DateTimeTool(BaseTool):
    """
    日期时间工具 - 获取当前时间、日期，进行时间计算
    """
    
    def __init__(self):
        super().__init__(
            name="DateTime",
            description="获取当前日期时间或进行时间计算。命令: 'now'(当前时间), 'today'(今天日期), 'timezone:Asia/Shanghai'(指定时区时间)"
        )
    
    def run(self, query: str) -> str:
        """
        执行时间相关操作
        
        参数:
            query: 时间查询命令
        
        返回:
            时间信息字符串
        """
        try:
            query = query.strip().lower()
            
            if query == "now":
                # 当前时间
                now = datetime.now()
                return f"当前时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')}"
            
            elif query == "today":
                # 今天日期
                today = datetime.now()
                weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
                weekday = weekdays[today.weekday()]
                return f"今天是: {today.strftime('%Y年%m月%d日')} {weekday}"
            
            elif query.startswith("timezone:"):
                # 指定时区的时间
                tz_name = query.split(":", 1)[1].strip()
                try:
                    tz = pytz.timezone(tz_name)
                    now = datetime.now(tz)
                    return f"{tz_name} 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
                except pytz.exceptions.UnknownTimeZoneError:
                    return f"错误: 未知时区 '{tz_name}'"
            
            elif query.startswith("add:") or query.startswith("subtract:"):
                # 时间计算 (未来功能)
                return "时间计算功能开发中..."
            
            else:
                # 默认返回完整信息
                now = datetime.now()
                weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
                weekday = weekdays[now.weekday()]
                
                info = f"""
当前日期时间信息
━━━━━━━━━━━━━━━━━
📅 日期: {now.strftime('%Y年%m月%d日')} {weekday}
⏰ 时间: {now.strftime('%H:%M:%S')}
🌍 时区: {datetime.now().astimezone().tzinfo}

支持的命令:
- now: 当前时间
- today: 今天日期
- timezone:时区名: 指定时区时间
""".strip()
                return info
                
        except Exception as e:
            return f"时间查询出错: {str(e)}"

