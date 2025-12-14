from typing import List
from .base import BaseTool
from .search import SearchTool

class DeepResearchTool(BaseTool):
    def __init__(self, search_tool: SearchTool):
        super().__init__(
            name="DeepResearch",
            description="Perform a deep research on a complex topic. It automatically breaks down the topic into sub-questions, searches for each, and summarizes the findings. Use this for broad or complex queries."
        )
        self.search_tool = search_tool

    def _generate_sub_questions(self, topic: str) -> List[str]:
        # 在真实场景中，这里会调用 LLM 来分解问题
        # 模拟：针对不同 topic 生成固定的子问题
        topic = topic.lower()
        if "agent" in topic:
            return [
                "what is an intelligent agent",
                "characteristics of agents",
                "types of agents in ai"
            ]
        elif "python" in topic:
            return [
                "history of python programming language",
                "key features of python",
                "python use cases"
            ]
        else:
            return [
                f"what is {topic}",
                f"benefits of {topic}",
                f"examples of {topic}"
            ]

    def run(self, query: str) -> str:
        report = []
        report.append(f"=== Deep Research Report: {query} ===\n")
        
        # 1. 分解任务
        sub_questions = self._generate_sub_questions(query)
        report.append(f"Research Plan (Sub-tasks):")
        for q in sub_questions:
            report.append(f"- {q}")
        report.append("\n")
        
        # 2. 执行子任务（多次搜索）
        aggregated_info = []
        for i, question in enumerate(sub_questions):
            report.append(f"--- Step {i+1}: Researching '{question}' ---")
            search_result = self.search_tool.run(question)
            
            # 简化输出，避免报告过长
            # 提取搜索结果的前 100 个字符作为摘要
            summary = search_result.replace("\n", " ")[:150] + "..."
            report.append(f"Findings: {summary}\n")
            aggregated_info.append(search_result)
            
        # 3. 归纳结论 (Mock)
        # 真实场景会把 aggregated_info 发给 LLM 进行总结
        report.append("=== Final Conclusion ===")
        report.append(f"Based on {len(sub_questions)} research steps, we have gathered comprehensive information about '{query}'.")
        report.append("The documents cover definitions, characteristics, and use cases as detailed above.")
        
        return "\n".join(report)
