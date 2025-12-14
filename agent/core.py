"""
增强版 ChatAgent - 支持工具注册器和 MCP 集成

新特性:
1. 支持 ToolRegistry 动态管理工具
2. 支持 MCP 客户端集成
3. 改进的工具调用机制
4. 更好的错误处理
"""

from typing import List, Dict, Optional, Union
import re
from llm.base import BaseLLM
from tools.base import BaseTool
from tools.registry import ToolRegistry
from .memory import Memory

SYSTEM_PROMPT = """You are a helpful AI assistant.
You have access to the following tools:
{tool_descriptions}

To use a tool, please use the following format:
ACTION: ToolName [Query]

Example:
User: What is Python?
Assistant: ACTION: Search [Python]

If you do not need to use a tool, just answer the user directly.
Always answer in the same language as the user.
{memory_context}
"""


class EnhancedChatAgent:
    """
    增强版对话 Agent
    
    支持:
    - 工具注册器 (ToolRegistry)
    - MCP 客户端集成
    - 动态工具管理
    - 记忆系统
    """
    
    def __init__(
        self, 
        llm: BaseLLM, 
        tools: Optional[Union[List[BaseTool], ToolRegistry]] = None,
        memory: Optional[Memory] = None,
        max_history: int = 5,
        max_iterations: int = 3
    ):
        """
        初始化增强版 Agent
        
        参数:
            llm: 语言模型
            tools: 工具列表或工具注册器
            memory: 记忆系统
            max_history: 保留的最大对话轮数
            max_iterations: ReAct 循环的最大迭代次数
        """
        self.llm = llm
        self.memory = memory
        self.history: List[Dict[str, str]] = []
        self.max_history = max_history
        self.max_iterations = max_iterations
        
        # 处理工具输入
        if isinstance(tools, ToolRegistry):
            self.tool_registry = tools
            self.tools = {t.name: t for t in tools.get_all_tools()}
        elif isinstance(tools, list):
            self.tool_registry = ToolRegistry()
            self.tool_registry.register_multiple(tools)
            self.tools = {t.name: t for t in tools}
        else:
            self.tool_registry = ToolRegistry()
            self.tools = {}
    
    def add_tool(self, tool: BaseTool) -> None:
        """动态添加工具"""
        self.tool_registry.register(tool)
        self.tools[tool.name] = tool
    
    def remove_tool(self, tool_name: str) -> bool:
        """移除工具"""
        if tool_name in self.tools:
            del self.tools[tool_name]
            return self.tool_registry.unregister(tool_name)
        return False
    
    def list_tools(self) -> List[str]:
        """列出所有可用工具"""
        return list(self.tools.keys())
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        tool_descs = "\n".join([f"- {t.name}: {t.description}" for t in self.tools.values()])
        if not tool_descs:
            tool_descs = "No tools available."
        
        mem_ctx = ""
        if self.memory:
            mem_ctx = self.memory.get_context()
        
        return SYSTEM_PROMPT.format(
            tool_descriptions=tool_descs, 
            memory_context=mem_ctx
        )
    
    def chat(self, user_input: str, verbose: bool = True) -> str:
        """
        处理用户输入并返回响应
        
        参数:
            user_input: 用户输入
            verbose: 是否打印详细日志
        
        返回:
            Agent 的响应
        """
        # 1. 添加用户消息到历史记录
        self.history.append({"role": "user", "content": user_input})
        
        # 2. 准备 LLM 消息
        messages = [
            {"role": "system", "content": self._build_system_prompt()}
        ] + self.history[-self.max_history * 2:]
        
        # 3. ReAct 循环
        for iteration in range(self.max_iterations):
            try:
                response = self.llm.generate(messages)
                
                # 检查是否有工具调用
                action_match = re.search(
                    r"ACTION:\s*(\w+)\s*\[(.*?)\]", 
                    response, 
                    re.IGNORECASE | re.DOTALL
                )
                
                if action_match:
                    tool_name = action_match.group(1)
                    tool_args = action_match.group(2).strip()
                    
                    if verbose:
                        print(f"\n[Agent 思考]: {response}")
                        print(f"[执行工具]: {tool_name}")
                        print(f"[工具参数]: {tool_args}")
                    
                    # 执行工具
                    if tool_name in self.tools:
                        try:
                            tool_result = self.tools[tool_name].run(tool_args)
                            observation = f"Observation: {tool_result}"
                            
                            if verbose:
                                print(f"[工具结果]: {tool_result[:200]}...")
                            
                            # 添加到上下文
                            messages.append({"role": "assistant", "content": response})
                            messages.append({"role": "system", "content": observation})
                            
                        except Exception as e:
                            error_msg = f"Observation: Tool execution error: {str(e)}"
                            messages.append({"role": "assistant", "content": response})
                            messages.append({"role": "system", "content": error_msg})
                            if verbose:
                                print(f"[工具错误]: {str(e)}")
                    else:
                        error_msg = f"Observation: Tool '{tool_name}' not found. Available tools: {', '.join(self.tools.keys())}"
                        messages.append({"role": "assistant", "content": response})
                        messages.append({"role": "system", "content": error_msg})
                        if verbose:
                            print(f"[错误]: 工具 '{tool_name}' 不存在")
                    
                    # 继续循环让 LLM 处理观察结果
                    continue
                
                else:
                    # 没有工具调用，这是最终回复
                    self.history.append({"role": "assistant", "content": response})
                    return response
                    
            except Exception as e:
                error_response = f"抱歉，处理您的请求时出现错误: {str(e)}"
                self.history.append({"role": "assistant", "content": error_response})
                return error_response
        
        # 达到最大迭代次数
        fallback_response = "抱歉，我在处理您的请求时遇到了一些困难。请尝试重新表述您的问题。"
        self.history.append({"role": "assistant", "content": fallback_response})
        return fallback_response
    
    def reset(self):
        """重置对话历史"""
        self.history = []
        print("[Agent] 对话历史已重置")
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.history.copy()
    
    def set_max_history(self, max_history: int):
        """设置最大历史记录数"""
        self.max_history = max_history
    
    def set_max_iterations(self, max_iterations: int):
        """设置最大迭代次数"""
        self.max_iterations = max_iterations


# 为了向后兼容，保留原来的 ChatAgent 类名
ChatAgent = EnhancedChatAgent

