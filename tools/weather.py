import random
from .base import BaseTool

class WeatherTool(BaseTool):
    """
    天气查询工具 - 查询指定城市的天气信息
    
    注意: 这是一个模拟工具，实际应用中应该调用真实的天气 API
    如 OpenWeatherMap, 和风天气等
    """
    
    def __init__(self):
        super().__init__(
            name="Weather",
            description="查询指定城市的天气信息。输入城市名称，例如: '北京', 'Shanghai', 'New York'"
        )
        
        # 模拟天气数据
        self.weather_conditions = ["晴朗", "多云", "阴天", "小雨", "中雨", "大雨", "雷阵雨", "雪"]
        self.wind_directions = ["东风", "西风", "南风", "北风", "东南风", "西南风", "东北风", "西北风"]
    
    def run(self, query: str) -> str:
        """
        查询天气信息
        
        参数:
            query: 城市名称
        
        返回:
            天气信息字符串
        """
        city = query.strip()
        
        if not city:
            return "错误: 请提供城市名称"
        
        # 模拟天气数据（实际应用中应调用真实 API）
        temperature = random.randint(-10, 35)
        condition = random.choice(self.weather_conditions)
        humidity = random.randint(30, 90)
        wind = random.choice(self.wind_directions)
        wind_speed = random.randint(1, 8)
        
        weather_info = f"""
天气信息 - {city}
━━━━━━━━━━━━━━━━━
🌡️ 温度: {temperature}°C
☁️ 天气: {condition}
💧 湿度: {humidity}%
🌬️ 风向: {wind} {wind_speed}级

提示: 这是模拟数据。实际应用中请使用真实天气API。
""".strip()
        
        return weather_info


class WeatherAPITool(BaseTool):
    """
    真实天气 API 工具（需要配置 API Key）
    
    可以使用的免费 API:
    - OpenWeatherMap: https://openweathermap.org/api
    - 和风天气: https://dev.qweather.com/
    - WeatherAPI: https://www.weatherapi.com/
    """
    
    def __init__(self, api_key: str = None, provider: str = "openweathermap"):
        super().__init__(
            name="WeatherAPI",
            description="使用真实天气API查询天气信息。输入城市名称。"
        )
        self.api_key = api_key
        self.provider = provider
    
    def run(self, query: str) -> str:
        """
        调用真实天气 API
        
        注意: 需要先配置 API Key
        """
        if not self.api_key:
            return "错误: 未配置天气 API Key。请设置环境变量或在初始化时提供。"
        
        city = query.strip()
        
        try:
            # 这里应该实现真实的 API 调用
            # 示例伪代码:
            # import requests
            # if self.provider == "openweathermap":
            #     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang=zh_cn"
            #     response = requests.get(url)
            #     data = response.json()
            #     ...
            
            return f"天气 API 功能尚未实现。城市: {city}"
            
        except Exception as e:
            return f"查询天气失败: {str(e)}"

