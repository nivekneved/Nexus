from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from core.telemetry import telemetry
from core.addon_registry import addon_registry
from core.subagent import BaseSubAgent

class BaseAgent(ABC):
    """
    Standardized Backbone Contract for all AI Agents / Digital Employees.
    Includes dynamic configuration schema, real-time telemetry logging,
    and single-task SubAgent integration.
    """

    def __init__(self, agent_id: str, name: str, description: str, icon: str = "bot", schedule_minutes: int = 60):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.icon = icon
        self.schedule_minutes = schedule_minutes
        self.is_enabled = True
        self.last_run_time = None
        self.last_run_status = "Idle"
        self.run_count = 0
        self.subagents: Dict[str, BaseSubAgent] = {}

    def register_subagent(self, subagent: BaseSubAgent):
        """Registers a dedicated single-task subagent under this agent."""
        self.subagents[subagent.subagent_id] = subagent
        addon_registry.register_addon(
            addon_id=subagent.subagent_id,
            name=subagent.name,
            category="subagent",
            description=subagent.description,
            default_active=True,
            parent_id=self.agent_id
        )

    def run_subagent(self, subagent_id: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes a single-task subagent if enabled in the Addon Registry.
        """
        if not addon_registry.is_active(subagent_id):
            return {
                "success": False,
                "subagent_id": subagent_id,
                "skipped": True,
                "reason": f"Subagent '{subagent_id}' is deactivated in Addon Registry."
            }
        subagent = self.subagents.get(subagent_id)
        if not subagent:
            return {
                "success": False,
                "subagent_id": subagent_id,
                "error": f"Subagent '{subagent_id}' not found on {self.name}."
            }
        return subagent.run(payload)

    @abstractmethod
    def run_cycle(self) -> Dict[str, Any]:
        """
        Executes a single autonomous cycle of this agent's core task.
        """
        pass

    @abstractmethod
    def get_stats(self) -> List[Dict[str, Any]]:
        """
        Returns metric cards to display on the dashboard for this agent.
        """
        pass

    def get_config_schema(self) -> List[Dict[str, Any]]:
        """
        Defines the configuration fields this agent needs.
        UI uses this schema to render a settings form automatically.
        """
        return []

    def get_config(self) -> Dict[str, Any]:
        """
        Returns the current saved values for this agent's configuration.
        """
        return {}

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        """
        Saves updated configuration values for this agent.
        """
        return True

    def log(self, step: str, file_used: str, message: str, level: str = "INFO"):
        """
        Emits a live telemetry event into the Mission Control streaming console.
        """
        telemetry.emit(
            agent_id=self.agent_id,
            agent_name=self.name,
            step=step,
            file_used=file_used,
            message=message,
            level=level
        )

    def get_info(self) -> Dict[str, Any]:
        """Returns standard metadata for UI rendering."""
        subagents_info = [
            {
                "id": s.subagent_id,
                "name": s.name,
                "description": s.description,
                "is_active": addon_registry.is_active(s.subagent_id),
                "execution_count": s.execution_count,
                "last_latency_ms": s.last_latency_ms
            }
            for s in self.subagents.values()
        ]
        return {
            "id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "schedule_minutes": self.schedule_minutes,
            "is_enabled": self.is_enabled and addon_registry.is_active(self.agent_id),
            "last_run_time": self.last_run_time,
            "last_run_status": self.last_run_status,
            "run_count": self.run_count,
            "stats": self.get_stats(),
            "config_schema": self.get_config_schema(),
            "current_config": self.get_config(),
            "subagents": subagents_info
        }

