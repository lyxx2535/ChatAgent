from typing import List, Dict, Optional
from .base import BaseLLM
import random

class MockLLM(BaseLLM):
    def generate(self, messages: List[Dict[str, str]], stop: Optional[List[str]] = None) -> str:
        last_message = messages[-1]["content"].lower()
        
        # 模拟工具使用决策
        # 如果用户询问 "python" 或 "agent" 且我们尚未搜索，则假装搜索。
        # 我们假设如果最后一条消息来自用户，我们可能需要搜索。
        # 如果最后一条消息是观察结果（工具输出），我们进行回答。
        
        # 检查上一条消息是否为工具输出（观察结果）
        # 在这个简单的 mock 中，我们查看消息历史。 
        # 但通常由调用者管理循环。
        
        # Mock 的简单启发式方法：
        if "search" in last_message or "find" in last_message or "what is" in last_message:
            # 如果我们在历史记录中看到此查询的 "Observation"，我们进行回答。
            # 但在这里，如果看起来我们尚未采取行动，我们只返回 Action。
            # 为简单起见，如果存在关键字且不是后续跟进，我们就触发搜索。
            pass

        # 为了使 ReAct 循环稳健，我们需要查看是否刚刚获得了 Observation。
        # 假设系统提示 agent。
        
        # 如果最后一条消息包含 "Observation:"，这意味着我们刚刚获得了搜索结果。
        # 所以我们应该生成最终答案。
        if "Observation:" in messages[-1]["content"]:
            observation = messages[-1]["content"].replace("Observation:", "").strip()
            return "Based on my research, " + observation[:100] + "... I hope that answers your question."

        # 模拟记忆触发
        if "my name is" in last_message:
            name = last_message.split("my name is")[-1].strip()
            return f"ACTION: Remember [profile: name is {name}]"
        
        if "i like" in last_message:
            pref = last_message.split("i like")[-1].strip()
            return f"ACTION: Remember [preference: likes {pref}]"

        # 模拟深度研究触发
        # 如果包含 "research" 或 "study" 或 "deeply"
        if "research" in last_message or "study" in last_message or "deeply" in last_message:
            topic = last_message.replace("research", "").replace("deeply", "").replace("study", "").strip()
            return f"ACTION: DeepResearch [{topic}]"

        # 模拟生图触发
        if "draw" in last_message or "generate image" in last_message or "create an image" in last_message:
            # 提取描述，简单处理
            prompt = last_message.replace("draw", "").replace("generate image", "").replace("create an image", "").strip()
            if not prompt: prompt = "something amazing"
            return f"ACTION: ImageGen [{prompt}]"
            
        # 如果用户询问我们有文档的特定主题：
        if "python" in last_message or "agent" in last_message:
            return f"ACTION: Search [{last_message}]"
             
        return "I am a Mock Agent. I can chat with you, but I don't know much without my tools. Try asking 'What is Python?'"
