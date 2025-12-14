from .base import BaseTool

class WebSearchTool(BaseTool):
    """
    网络搜索工具 - 在互联网上搜索信息
    
    注意: 这是一个模拟工具，实际应用中应该调用真实的搜索 API
    如 Google Search API, Bing Search API, SerpAPI 等
    """
    
    def __init__(self, api_key: str = None):
        super().__init__(
            name="WebSearch",
            description="在互联网上搜索信息。输入搜索关键词，返回相关结果。"
        )
        self.api_key = api_key
    
    def run(self, query: str) -> str:
        """
        执行网络搜索
        
        参数:
            query: 搜索关键词
        
        返回:
            搜索结果
        """
        if not query.strip():
            return "错误: 请提供搜索关键词"
        
        # 模拟搜索结果
        results = f"""
网络搜索结果: "{query}"
━━━━━━━━━━━━━━━━━━━━━━

提示: 这是一个模拟工具。

实际应用中可以集成以下搜索 API:

1. Google Custom Search API
   - https://developers.google.com/custom-search

2. Bing Web Search API
   - https://www.microsoft.com/en-us/bing/apis/bing-web-search-api

3. SerpAPI (多搜索引擎聚合)
   - https://serpapi.com/

4. DuckDuckGo API (免费)
   - https://duckduckgo.com/api

要启用真实搜索，请:
1. 注册获取 API Key
2. 安装对应的 Python SDK
3. 在工具初始化时传入 API Key
""".strip()
        
        return results


class DuckDuckGoSearchTool(BaseTool):
    """
    DuckDuckGo 搜索工具 - 使用 DuckDuckGo 的免费搜索
    
    优势: 无需 API Key，尊重隐私
    """
    
    def __init__(self):
        super().__init__(
            name="DuckDuckGoSearch",
            description="使用 DuckDuckGo 搜索互联网信息（免费，无需 API Key）"
        )
    
    def run(self, query: str) -> str:
        """
        使用 DuckDuckGo 进行搜索
        
        需要安装: pip install duckduckgo-search
        """
        try:
            # 尝试导入 duckduckgo_search
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=5))
                
                for i, result in enumerate(search_results, 1):
                    title = result.get('title', 'No title')
                    link = result.get('link', '')
                    snippet = result.get('body', 'No description')
                    
                    results.append(f"{i}. {title}")
                    results.append(f"   链接: {link}")
                    results.append(f"   摘要: {snippet}")
                    results.append("")
            
            if results:
                return f"搜索结果: \"{query}\"\n\n" + "\n".join(results)
            else:
                return f"未找到关于 '{query}' 的搜索结果"
                
        except ImportError:
            return """
错误: 未安装 duckduckgo-search 库

请运行以下命令安装:
pip install duckduckgo-search

然后重启应用程序。
""".strip()
        except Exception as e:
            return f"搜索出错: {str(e)}"

