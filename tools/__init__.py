"""
Tools Package - 所有可用工具的集合

包含:
- 基础工具类 (BaseTool)
- 工具注册器 (ToolRegistry)
- 各种具体工具实现
"""

from .base import BaseTool
from .registry import ToolRegistry, global_registry, register_tool

# 导入所有工具
from .search import SearchTool
from .remember import RememberTool
from .image_gen import ImageGenTool
from .deep_research import DeepResearchTool
from .calculator import CalculatorTool
from .weather import WeatherTool, WeatherAPITool
from .translator import TranslatorTool, LLMTranslatorTool
from .datetime_tool import DateTimeTool
from .web_search import WebSearchTool, DuckDuckGoSearchTool

__all__ = [
    # 基础类
    'BaseTool',
    'ToolRegistry',
    'global_registry',
    'register_tool',
    
    # 具体工具
    'SearchTool',
    'RememberTool',
    'ImageGenTool',
    'DeepResearchTool',
    'CalculatorTool',
    'WeatherTool',
    'WeatherAPITool',
    'TranslatorTool',
    'LLMTranslatorTool',
    'DateTimeTool',
    'WebSearchTool',
    'DuckDuckGoSearchTool',
]

