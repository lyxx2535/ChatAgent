from typing import Dict, List, Optional, Type
from .base import BaseTool

class ToolRegistry:
    """
    工具注册器 - 用于动态管理和注册工具
    
    功能:
    - 注册工具实例或类
    - 通过装饰器自动注册工具
    - 获取所有可用工具
    - 按名称查找工具
    """
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._tool_classes: Dict[str, Type[BaseTool]] = {}
    
    def register(self, tool: BaseTool) -> None:
        """注册一个工具实例"""
        if tool.name in self._tools:
            print(f"Warning: Tool '{tool.name}' already exists. Overwriting.")
        self._tools[tool.name] = tool
        print(f"[Registry] Registered tool: {tool.name}")
    
    def register_class(self, tool_class: Type[BaseTool]) -> None:
        """注册一个工具类（用于延迟实例化）"""
        # 创建临时实例以获取名称
        temp_instance = tool_class()
        name = temp_instance.name
        self._tool_classes[name] = tool_class
        print(f"[Registry] Registered tool class: {name}")
    
    def register_multiple(self, tools: List[BaseTool]) -> None:
        """批量注册多个工具"""
        for tool in tools:
            self.register(tool)
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """根据名称获取工具"""
        return self._tools.get(name)
    
    def get_all_tools(self) -> List[BaseTool]:
        """获取所有已注册的工具"""
        return list(self._tools.values())
    
    def get_tool_names(self) -> List[str]:
        """获取所有工具名称"""
        return list(self._tools.keys())
    
    def unregister(self, name: str) -> bool:
        """注销一个工具"""
        if name in self._tools:
            del self._tools[name]
            print(f"[Registry] Unregistered tool: {name}")
            return True
        return False
    
    def clear(self) -> None:
        """清空所有工具"""
        self._tools.clear()
        self._tool_classes.clear()
        print("[Registry] Cleared all tools")
    
    def get_tools_description(self) -> str:
        """获取所有工具的描述信息（用于提示词）"""
        if not self._tools:
            return "No tools available."
        
        descriptions = []
        for tool in self._tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)


# 全局工具注册器实例
global_registry = ToolRegistry()


def register_tool(tool: BaseTool) -> BaseTool:
    """
    装饰器函数：自动注册工具到全局注册器
    
    用法:
    @register_tool
    class MyTool(BaseTool):
        ...
    """
    global_registry.register(tool)
    return tool

