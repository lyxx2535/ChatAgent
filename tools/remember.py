from .base import BaseTool
from agent.memory import Memory

class RememberTool(BaseTool):
    def __init__(self, memory: Memory):
        super().__init__(
            name="Remember",
            description="Save important information about the user. Format: [category: content]. Categories: profile, preference, fact. Example: [preference: likes python]"
        )
        self.memory = memory

    def run(self, query: str) -> str:
        # Simple parsing logic
        # Expect query like "preference: likes python" or "profile: name is Bob"
        try:
            if ":" in query:
                category, content = query.split(":", 1)
                category = category.strip().lower()
                content = content.strip()
            else:
                # Default to fact if no category provided
                category = "fact"
                content = query.strip()

            if category == "profile":
                # Naive key-value extraction for profile
                # e.g. "name is Bob" -> key="name", value="Bob"
                # This is a simplification. Ideally LLM provides structured JSON.
                if " is " in content:
                    key, val = content.split(" is ", 1)
                    self.memory.update_profile(key.strip(), val.strip())
                    return f"Saved profile: {key.strip()} = {val.strip()}"
                else:
                    return f"Error: Profile updates need 'key is value' format. Got: {content}"
            
            elif category == "preference":
                self.memory.add_preference(content)
                return f"Saved preference: {content}"
                
            elif category == "fact":
                self.memory.add_fact(content)
                return f"Saved fact: {content}"
                
            else:
                return f"Error: Unknown memory category '{category}'. Use profile, preference, or fact."

        except Exception as e:
            return f"Error saving memory: {str(e)}"
