"""
增强版 Agent 主程序

展示新的工具系统特性:
1. 工具注册器 (ToolRegistry)
2. 更多实用工具 (计算器、天气、日期时间、翻译、网络搜索)
3. MCP 客户端支持 (可选)
4. 动态工具管理
"""

import os
import sys
from dotenv import load_dotenv

# 将当前目录添加到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.core_enhanced import EnhancedChatAgent
from agent.memory import Memory
from tools.registry import ToolRegistry
from tools.search import SearchTool
from tools.remember import RememberTool
from tools.image_gen import ImageGenTool
from tools.deep_research import DeepResearchTool
from tools.calculator import CalculatorTool
from tools.weather import WeatherTool
from tools.translator import TranslatorTool
from tools.datetime_tool import DateTimeTool
from tools.web_search import WebSearchTool, DuckDuckGoSearchTool
from llm.mock_provider import MockLLM
from llm.openai_provider import OpenAILLM


def setup_tools(docs_dir: str, memory: Memory) -> ToolRegistry:
    """设置并注册所有工具"""
    registry = ToolRegistry()
    
    # 核心工具
    search_tool = SearchTool(docs_dir)
    remember_tool = RememberTool(memory)
    
    # 实用工具
    calculator_tool = CalculatorTool()
    weather_tool = WeatherTool()
    datetime_tool = DateTimeTool()
    translator_tool = TranslatorTool()
    
    # 高级工具
    image_tool = ImageGenTool()
    research_tool = DeepResearchTool(search_tool)
    web_search_tool = WebSearchTool()
    
    # 尝试添加 DuckDuckGo 搜索（需要额外依赖）
    try:
        ddg_search_tool = DuckDuckGoSearchTool()
        registry.register(ddg_search_tool)
    except:
        print("[提示] DuckDuckGo 搜索工具不可用（需要安装 duckduckgo-search）")
    
    # 注册所有工具
    tools = [
        search_tool,
        remember_tool,
        calculator_tool,
        weather_tool,
        datetime_tool,
        translator_tool,
        image_tool,
        research_tool,
        web_search_tool,
    ]
    
    registry.register_multiple(tools)
    return registry


def setup_mcp_tools(registry: ToolRegistry):
    """
    设置 MCP 工具（可选）
    
    如果存在 mcp_config.json 文件，则尝试连接 MCP 服务器
    """
    from tools.mcp_client import create_mcp_manager_from_config
    
    config_file = "mcp_config.json"
    if os.path.exists(config_file):
        print(f"\n[MCP] 发现配置文件: {config_file}")
        print("[MCP] 正在尝试连接 MCP 服务器...")
        
        try:
            mcp_manager = create_mcp_manager_from_config(config_file)
            mcp_tools = mcp_manager.get_all_tools()
            
            if mcp_tools:
                registry.register_multiple(mcp_tools)
                print(f"[MCP] 成功添加 {len(mcp_tools)} 个 MCP 工具")
            else:
                print("[MCP] 未找到可用的 MCP 工具")
        except Exception as e:
            print(f"[MCP] 加载 MCP 工具失败: {str(e)}")
    else:
        print(f"\n[MCP] 未找到配置文件 {config_file}")
        print("[MCP] 如需使用 MCP 功能，请创建 mcp_config.json 配置文件")


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                  增强版 Chat Agent                         ║
║               Enhanced Tool System v2.0                   ║
╚═══════════════════════════════════════════════════════════╝

✨ 新特性:
  • 工具注册器 - 动态管理工具
  • 更多实用工具 - 计算器、天气、日期时间、翻译等
  • MCP 支持 - 连接外部服务器获取更多能力
  • 改进的错误处理和日志

📝 可用命令:
  • exit / quit - 退出程序
  • reset - 重置对话历史
  • tools - 查看所有可用工具
  • help - 显示帮助信息

💡 试试问我:
  • "2 + 2 等于多少？" (使用计算器)
  • "北京天气怎么样？" (查询天气)
  • "现在几点了？" (查询时间)
  • "What is Python?" (搜索知识库)
  • "画一个猫" (生成图片)
"""
    print(banner)


def print_help():
    """打印帮助信息"""
    help_text = """
═══════════════════════════════════════════════════════════
                        帮助信息
═══════════════════════════════════════════════════════════

🎯 如何使用:
  1. 直接输入问题，Agent 会自动选择合适的工具
  2. Agent 支持中文和英文
  3. 可以进行多轮对话

🛠️ 工具使用示例:
  • 计算: "计算 123 * 456"
  • 天气: "上海的天气"
  • 时间: "现在几点" 或 "今天星期几"
  • 翻译: "翻译 hello world"
  • 搜索: "什么是 Python"
  • 图片: "生成一个日落的图片"
  • 记忆: "记住我喜欢 Python"

📋 特殊命令:
  • exit/quit - 退出
  • reset - 重置历史
  • tools - 查看工具
  • help - 帮助信息

═══════════════════════════════════════════════════════════
"""
    print(help_text)


def main():
    load_dotenv()
    
    print_banner()
    
    # 1. 设置记忆系统
    memory = Memory()
    
    # 2. 设置工具注册器
    docs_dir = os.path.join(os.path.dirname(__file__), "data", "docs")
    tool_registry = setup_tools(docs_dir, memory)
    
    # 3. 尝试设置 MCP 工具（可选）
    setup_mcp_tools(tool_registry)
    
    print(f"\n✅ 已加载 {len(tool_registry.get_all_tools())} 个工具")
    
    # 4. 设置 LLM
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("🤖 使用 OpenAI LLM")
        llm = OpenAILLM(api_key=api_key)
    else:
        print("🤖 使用 Mock LLM (演示模式)")
        print("   提示: 设置 OPENAI_API_KEY 环境变量以使用真实模型")
        llm = MockLLM()
    
    # 5. 创建增强版 Agent
    agent = EnhancedChatAgent(
        llm=llm,
        tools=tool_registry,
        memory=memory,
        max_history=5,
        max_iterations=3
    )
    
    print("\n" + "="*60)
    print("Agent 已就绪！开始对话吧。")
    print("="*60)
    
    # 6. 交互循环
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
            
            # 处理特殊命令
            if user_input.lower() in ["exit", "quit"]:
                print("\n👋 再见！")
                break
            
            elif user_input.lower() == "reset":
                agent.reset()
                print("✅ 对话历史已重置")
                continue
            
            elif user_input.lower() == "tools":
                print("\n可用工具列表:")
                print("-" * 60)
                for tool in tool_registry.get_all_tools():
                    print(f"  • {tool.name}: {tool.description}")
                print("-" * 60)
                continue
            
            elif user_input.lower() == "help":
                print_help()
                continue
            
            # 处理正常对话
            print()  # 空行
            response = agent.chat(user_input, verbose=True)
            print(f"\n💬 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 收到中断信号，正在退出...")
            break
        
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()

