"""
Nexus™ MCP Tool Bundler & Exporter
===================================
Packs internal tools from ToolRegistry into Model Context Protocol (MCP)
compliant JSON schemas for $1.00 Digital Vending Machine distribution and external agent mesh.
"""

import json
from typing import Dict, Any, List
from core.tool_registry import ToolRegistry

class MCPToolBundler:
    """
    Exports registered tools into standard MCP schema format.
    """
    def __init__(self):
        self.registry = ToolRegistry()

    def export_mcp_manifest(self) -> Dict[str, Any]:
        tools = self.registry.list_tools()
        mcp_tools = []
        for t in tools:
            mcp_tools.append({
                "name": t["name"],
                "description": t["description"],
                "inputSchema": {
                    "type": "object",
                    "properties": t["parameters"],
                    "required": list(t["parameters"].keys())
                }
            })

        return {
            "mcpVersion": "1.0.0",
            "serverName": "Nexus-Sovereign-MCP-Server",
            "tools": mcp_tools
        }

    def export_as_json_string(self) -> str:
        return json.dumps(self.export_mcp_manifest(), indent=2)

mcp_bundler = MCPToolBundler()
