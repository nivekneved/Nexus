from abc import ABC, abstractmethod
import time
from typing import Dict, Any, Optional
from security.shield import shield

class BaseSubAgent(ABC):
    """
    Standardized Contract for Single-Task SubAgents.
    Rule: 1 SubAgent = Exactly 1 Task.
    Guarantees isolated execution, circuit breaker protection, and granular telemetry.
    """

    def __init__(self, subagent_id: str, name: str, parent_agent_id: str, description: str):
        self.subagent_id = subagent_id
        self.name = name
        self.parent_agent_id = parent_agent_id
        self.description = description
        self.is_enabled = True
        self.execution_count = 0
        self.last_execution_time = None
        self.last_latency_ms = 0.0

    def run(self, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes the subagent with isolated error boundaries and circuit breaker safety.
        """
        if not self.is_enabled:
            return {"success": False, "subagent_id": self.subagent_id, "error": "Subagent is currently disabled"}

        # Safeguard 25: Circuit Breaker Check
        if shield.is_circuit_open(self.subagent_id):
            return {
                "success": False,
                "subagent_id": self.subagent_id,
                "error": f"Circuit breaker tripped for '{self.name}'. Cooling down to prevent cascade failure."
            }

        start = time.time()
        self.execution_count += 1
        try:
            result = self.execute(payload or {})
            latency = (time.time() - start) * 1000.0
            self.last_latency_ms = round(latency, 2)
            self.last_execution_time = time.strftime("%Y-%m-%d %H:%M:%S")
            shield.record_subagent_result(self.subagent_id, success=True)
            return {
                "success": True,
                "subagent_id": self.subagent_id,
                "parent_agent_id": self.parent_agent_id,
                "latency_ms": self.last_latency_ms,
                "data": result
            }
        except Exception as e:
            latency = (time.time() - start) * 1000.0
            self.last_latency_ms = round(latency, 2)
            shield.record_subagent_result(self.subagent_id, success=False)
            return {
                "success": False,
                "subagent_id": self.subagent_id,
                "parent_agent_id": self.parent_agent_id,
                "latency_ms": self.last_latency_ms,
                "error": str(e)
            }

    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Single specific task executed by this subagent."""
        pass
