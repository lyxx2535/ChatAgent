import os
import sys
from agent.core import ChatAgent
from tools.search import SearchTool
from llm.mock_provider import MockLLM

# 设置
docs_dir = os.path.join(os.path.dirname(__file__), "data", "docs")
search_tool = SearchTool(docs_dir)
llm = MockLLM()
agent = ChatAgent(llm=llm, tools=[search_tool])

print("--- 测试 1: 简单问候 ---")
response = agent.chat("Hello")
print(f"Agent: {response}\n")

print("--- 测试 2: 搜索触发 ---")
# 这应该触发模拟搜索逻辑
response = agent.chat("What is Python?")
print(f"Agent: {response}\n")

print("--- 测试 3: 搜索触发 2 ---")
response = agent.chat("Tell me about intelligent agents")
print(f"Agent: {response}\n")
