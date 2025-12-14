import json
import os
from typing import Dict, Any, List

class Memory:
    def __init__(self, file_path: str = "user_memory.json"):
        self.file_path = file_path
        self.data = self._load()
        # 确保存储结构初始化
        if "profile" not in self.data:
            self.data["profile"] = {}
        if "preferences" not in self.data:
            self.data["preferences"] = []
        if "facts" not in self.data:
            self.data["facts"] = []

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def update_profile(self, key: str, value: Any):
        """更新用户基础属性（如姓名、年龄、职业）"""
        self.data["profile"][key] = value
        self.save()

    def add_preference(self, preference: str):
        """添加用户偏好（如喜欢 Python，讨厌香菜）"""
        if preference not in self.data["preferences"]:
            self.data["preferences"].append(preference)
            self.save()

    def add_fact(self, fact: str):
        """添加关于用户的通用事实或对话中的重要信息"""
        if fact not in self.data["facts"]:
            self.data["facts"].append(fact)
            self.save()

    def get_context(self) -> str:
        """获取格式化的记忆上下文，用于注入 System Prompt"""
        context_parts = []
        
        if self.data["profile"]:
            profile_str = ", ".join([f"{k}: {v}" for k, v in self.data["profile"].items()])
            context_parts.append(f"User Profile: [{profile_str}]")
            
        if self.data["preferences"]:
            prefs_str = "; ".join(self.data["preferences"])
            context_parts.append(f"User Preferences: [{prefs_str}]")
            
        if self.data["facts"]:
            facts_str = "; ".join(self.data["facts"])
            context_parts.append(f"Known Facts: [{facts_str}]")
            
        if not context_parts:
            return ""
            
        return "\n".join(context_parts)
