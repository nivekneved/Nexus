
import logging
from typing import Dict, Any, List

from core.jarvis_skills import jarvis_skills
from core.tool_registry import tool_registry
from core.addon_registry import addon_registry
from core.scenario_library import DAILY_SCENARIOS

class CoreSkillsEngine:
    """
    Unified Subagent and Skill Library Orchestrator.
    Consolidates the standalone Jarvis Skills, Global Tool Registry,
    Addon Marketplace, and the massive 125 Scenario Library into a single interface.
    """
    def __init__(self):
        self.skills = jarvis_skills
        self.tools = tool_registry
        self.addons = addon_registry
        self.scenarios = DAILY_SCENARIOS

    def get_all_scenarios(self) -> Dict[str, Any]:
        return self.scenarios

    def get_available_tools(self) -> Dict[str, Any]:
        return self.tools.get_available_tools()

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        return self.tools.call_tool(tool_name, **kwargs)

    def get_addons(self) -> List[Dict[str, Any]]:
        if hasattr(self.addons, 'get_addons'):
            return self.addons.get_addons()
        return []

skills_engine = CoreSkillsEngine()
