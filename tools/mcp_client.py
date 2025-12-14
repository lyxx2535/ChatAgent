"""
MCP (Model Context Protocol) 客户端

MCP 是一个开放协议，允许 AI 应用连接到外部数据源和工具。

参考:
- MCP 官方文档: https://modelcontextprotocol.io/
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk

本实现提供了一个简化的 MCP 客户端包装器，用于连接外部 MCP 服务器。
"""

import json
from typing import Dict, List, Any, Optional
from .base import BaseTool


class MCPTool(BaseTool):
    """
    MCP 工具包装器 - 将 MCP 服务器的能力包装为 Agent 工具
    """
    
    def __init__(self, name: str, description: str, mcp_client, tool_name: str):
        """
        初始化 MCP 工具
        
        参数:
            name: 工具名称（在 Agent 中使用的名称）
            description: 工具描述
            mcp_client: MCP 客户端实例
            tool_name: MCP 服务器中的工具名称
        """
        super().__init__(name=name, description=description)
        self.mcp_client = mcp_client
        self.tool_name = tool_name
    
    def run(self, query: str) -> str:
        """调用 MCP 服务器的工具"""
        try:
            result = self.mcp_client.call_tool(self.tool_name, {"query": query})
            return result
        except Exception as e:
            return f"MCP 工具调用失败: {str(e)}"


class MCPClient:
    """
    MCP 客户端 - 连接到 MCP 服务器并获取其提供的工具
    
    MCP 允许通过标准协议连接到各种服务:
    - 文件系统访问
    - 数据库查询
    - API 调用
    - 浏览器自动化
    - 等等...
    """
    
    def __init__(self, server_config: Dict[str, Any]):
        """
        初始化 MCP 客户端
        
        参数:
            server_config: 服务器配置字典
                {
                    "name": "服务器名称",
                    "type": "stdio" | "http",  # 连接类型
                    "command": "服务器启动命令",  # stdio 类型时使用
                    "url": "服务器 URL",  # http 类型时使用
                    "env": {},  # 环境变量
                }
        """
        self.config = server_config
        self.server_name = server_config.get("name", "unknown")
        self.connection_type = server_config.get("type", "stdio")
        self.connected = False
        self.available_tools = []
        
        # 实际的 MCP 连接对象（需要 mcp SDK）
        self._mcp_connection = None
    
    def connect(self) -> bool:
        """
        连接到 MCP 服务器
        
        返回:
            是否连接成功
        """
        try:
            if self.connection_type == "stdio":
                return self._connect_stdio()
            elif self.connection_type == "http":
                return self._connect_http()
            else:
                print(f"不支持的连接类型: {self.connection_type}")
                return False
        except Exception as e:
            print(f"连接 MCP 服务器失败: {str(e)}")
            return False
    
    def _connect_stdio(self) -> bool:
        """通过 stdio 连接到服务器"""
        try:
            # 实际实现需要使用 mcp Python SDK
            # from mcp import ClientSession, StdioServerParameters
            # from mcp.client.stdio import stdio_client
            
            # server_params = StdioServerParameters(
            #     command=self.config.get("command"),
            #     args=self.config.get("args", []),
            #     env=self.config.get("env", {})
            # )
            # 
            # self._mcp_connection = await stdio_client(server_params)
            # self.connected = True
            
            # 目前返回模拟结果
            print(f"[MCP] 尝试连接到服务器: {self.server_name} (stdio)")
            print(f"[MCP] 提示: 完整的 MCP 实现需要安装 mcp SDK")
            print(f"[MCP] 命令: pip install mcp")
            self.connected = False
            return False
            
        except Exception as e:
            print(f"stdio 连接失败: {str(e)}")
            return False
    
    def _connect_http(self) -> bool:
        """通过 HTTP 连接到服务器"""
        try:
            url = self.config.get("url")
            if not url:
                raise ValueError("HTTP 连接需要提供 url")
            
            print(f"[MCP] 尝试连接到服务器: {self.server_name} (HTTP: {url})")
            print(f"[MCP] 提示: HTTP MCP 连接尚未实现")
            self.connected = False
            return False
            
        except Exception as e:
            print(f"HTTP 连接失败: {str(e)}")
            return False
    
    def list_tools(self) -> List[Dict[str, str]]:
        """
        列出服务器提供的所有工具
        
        返回:
            工具信息列表
        """
        if not self.connected:
            print("[MCP] 未连接到服务器")
            return []
        
        try:
            # 实际实现:
            # tools = await self._mcp_connection.list_tools()
            # return tools
            
            return self.available_tools
        except Exception as e:
            print(f"获取工具列表失败: {str(e)}")
            return []
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        调用服务器提供的工具
        
        参数:
            tool_name: 工具名称
            arguments: 工具参数
        
        返回:
            工具执行结果
        """
        if not self.connected:
            return "错误: 未连接到 MCP 服务器"
        
        try:
            # 实际实现:
            # result = await self._mcp_connection.call_tool(tool_name, arguments)
            # return result.content
            
            return f"模拟结果: 调用工具 {tool_name}，参数: {arguments}"
        except Exception as e:
            return f"调用工具失败: {str(e)}"
    
    def disconnect(self):
        """断开与服务器的连接"""
        if self._mcp_connection:
            try:
                # await self._mcp_connection.close()
                pass
            except:
                pass
        self.connected = False
        print(f"[MCP] 已断开与服务器 {self.server_name} 的连接")
    
    def get_tools_as_agent_tools(self) -> List[BaseTool]:
        """
        将 MCP 服务器的工具转换为 Agent 工具
        
        返回:
            BaseTool 列表
        """
        if not self.connected:
            print("[MCP] 未连接到服务器，无法获取工具")
            return []
        
        agent_tools = []
        for tool_info in self.list_tools():
            tool_name = tool_info.get("name")
            tool_desc = tool_info.get("description", "No description")
            
            # 创建包装工具
            mcp_tool = MCPTool(
                name=f"{self.server_name}_{tool_name}",
                description=tool_desc,
                mcp_client=self,
                tool_name=tool_name
            )
            agent_tools.append(mcp_tool)
        
        return agent_tools


class MCPManager:
    """
    MCP 管理器 - 管理多个 MCP 客户端连接
    """
    
    def __init__(self):
        self.clients: Dict[str, MCPClient] = {}
    
    def add_server(self, server_config: Dict[str, Any]) -> bool:
        """
        添加并连接到 MCP 服务器
        
        参数:
            server_config: 服务器配置
        
        返回:
            是否成功
        """
        server_name = server_config.get("name")
        if not server_name:
            print("错误: 服务器配置必须包含 name 字段")
            return False
        
        client = MCPClient(server_config)
        if client.connect():
            self.clients[server_name] = client
            print(f"[MCP Manager] 成功添加服务器: {server_name}")
            return True
        else:
            print(f"[MCP Manager] 添加服务器失败: {server_name}")
            return False
    
    def get_all_tools(self) -> List[BaseTool]:
        """
        获取所有已连接服务器提供的工具
        
        返回:
            所有工具的列表
        """
        all_tools = []
        for client in self.clients.values():
            all_tools.extend(client.get_tools_as_agent_tools())
        return all_tools
    
    def disconnect_all(self):
        """断开所有服务器连接"""
        for client in self.clients.values():
            client.disconnect()
        self.clients.clear()


# MCP 服务器配置示例
EXAMPLE_MCP_SERVERS = {
    "filesystem": {
        "name": "filesystem",
        "type": "stdio",
        "command": "mcp-server-filesystem",
        "args": ["/path/to/allowed/directory"],
        "description": "文件系统访问服务器"
    },
    "github": {
        "name": "github",
        "type": "stdio",
        "command": "mcp-server-github",
        "env": {
            "GITHUB_TOKEN": "your_token_here"
        },
        "description": "GitHub API 访问服务器"
    },
    "database": {
        "name": "database",
        "type": "stdio",
        "command": "mcp-server-sqlite",
        "args": ["path/to/database.db"],
        "description": "SQLite 数据库访问服务器"
    }
}


def create_mcp_manager_from_config(config_file: str) -> MCPManager:
    """
    从配置文件创建 MCP 管理器
    
    参数:
        config_file: JSON 配置文件路径
    
    返回:
        MCPManager 实例
    """
    manager = MCPManager()
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        servers = config.get("mcp_servers", [])
        for server_config in servers:
            manager.add_server(server_config)
        
        return manager
    except Exception as e:
        print(f"加载 MCP 配置文件失败: {str(e)}")
        return manager

