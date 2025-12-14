import os
from typing import List
from .base import BaseTool

class SearchTool(BaseTool):
    def __init__(self, docs_dir: str):
        super().__init__(
            name="Search",
            description="在本地文档中搜索关键字。当你需要回答有关特定主题（如 Python 或 Agent）的问题时很有用。"
        )
        self.docs_dir = docs_dir

    def run(self, query: str) -> str:
        results = []
        # 简单的关键字搜索
        # 1. 过滤停用词
        stopwords = {"what", "is", "a", "the", "an", "tell", "me", "about", "how", "to", "in", "of", "for", "with", "on"}
        raw_keywords = query.lower().replace("?", "").replace(".", "").split()
        keywords = [k for k in raw_keywords if k not in stopwords]
        
        if not keywords:
            keywords = raw_keywords # 如果所有内容都是停用词，则回退

        if not os.path.exists(self.docs_dir):
            return "Error: Knowledge base directory not found."

        for filename in os.listdir(self.docs_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.docs_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            # 检查行中是否包含任何有意义的关键字
                            if any(k in line.lower() for k in keywords):
                                results.append(f"[{filename}:{i+1}] {line.strip()}")
                except Exception as e:
                    results.append(f"Error reading {filename}: {str(e)}")
        
        if not results:
            return f"No relevant information found for keywords: {keywords}"
            
        # 限制结果以避免上下文溢出
        return "\n".join(results[:5])
