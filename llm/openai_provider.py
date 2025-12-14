import os
from typing import List, Dict, Optional
from .base import BaseLLM

class OpenAILLM(BaseLLM):
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Please install openai package: pip install openai")
            
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate(self, messages: List[Dict[str, str]], stop: Optional[List[str]] = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stop=stop,
            temperature=0.7
        )
        return response.choices[0].message.content
