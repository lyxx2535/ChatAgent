from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], stop: Optional[List[str]] = None) -> str:
        """
        从 LLM 生成回复。
        
        参数：
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            stop: 停止序列列表。
            
        返回：
            生成的文本。
        """
        pass
