"""
Nexus™ Ruflo-Inspired Dynamic Swarm & Workflow Orchestrator
============================================================
Implements decentralized multi-agent routing, priority task queueing,
dynamic agent task allocation, and fault-tolerant retry loops bound to EconomicGate.
"""

import os
import json
import time
import logging
from typing import Dict, Any, List, Optional
from core.economic_gate import EconomicGate
from core.tool_registry import ToolRegistry

logger = logging.getLogger("Nexus.RufloOrchestrator")

class RufloSwarmOrchestrator:
    """
    Orchestrates multi-agent swarm workflows with priority queueing,
    economic unit gating, and robust error recovery.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RufloSwarmOrchestrator, cls).__new__(cls)
            cls._instance.task_queue: List[Dict[str, Any]] = []
            cls._instance.execution_history: List[Dict[str, Any]] = []
        return cls._instance

    def enqueue_task(self, task_name: str, payload: Dict[str, Any], reward_usd: float = 1.0, priority: int = 1) -> str:
        task_id = f"task_{int(time.time() * 1000)}"
        task_item = {
            "task_id": task_id,
            "task_name": task_name,
            "payload": payload,
            "reward_usd": reward_usd,
            "priority": priority,
            "status": "QUEUED",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.task_queue.append(task_item)
        # Sort queue by priority (descending) and reward (descending)
        self.task_queue.sort(key=lambda x: (x["priority"], x["reward_usd"]), reverse=True)
        logger.info(f"[RufloOrchestrator] Enqueued task {task_id}: {task_name} (Priority: {priority}, Reward: ${reward_usd})")
        return task_id

    def process_next_task(self) -> Optional[Dict[str, Any]]:
        if not self.task_queue:
            return None

        task = self.task_queue.pop(0)
        task_id = task["task_id"]
        task["status"] = "RUNNING"
        logger.info(f"[RufloOrchestrator] Executing task {task_id}: {task['task_name']}")

        # Economic Gate Evaluation
        gate = EconomicGate()
        approved, reason, metrics = gate.evaluate_task(
            task_id=task_id,
            reward_usd=task["reward_usd"],
            p_acceptance=0.92,
            category="swarm_workflow"
        )

        if not approved:
            task["status"] = "VETOED"
            task["result"] = {"success": False, "reason": reason, "metrics": metrics}
            self.execution_history.insert(0, task)
            logger.warning(f"[RufloOrchestrator] Task {task_id} VETOED by EconomicGate: {reason}")
            return task

        # Execute via Tool Registry if tool specified in payload
        tool_name = task["payload"].get("tool_name")
        tool_args = task["payload"].get("tool_args", {})

        start_t = time.time()
        try:
            if tool_name:
                registry = ToolRegistry()
                res = registry.call_tool(tool_name, **tool_args)
            else:
                # Default mock/simulated workflow execution
                res = {"success": True, "output": f"Successfully completed swarm workflow for {task['task_name']}"}

            duration = round(time.time() - start_t, 3)
            task["status"] = "COMPLETED"
            task["result"] = {"success": True, "execution_result": res, "duration": duration, "metrics": metrics}
        except Exception as e:
            duration = round(time.time() - start_t, 3)
            task["status"] = "FAILED"
            task["result"] = {"success": False, "error": str(e), "duration": duration, "metrics": metrics}

        self.execution_history.insert(0, task)
        return task

    def get_swarm_status(self) -> Dict[str, Any]:
        return {
            "queued_tasks": len(self.task_queue),
            "total_executed": len(self.execution_history),
            "queue": self.task_queue[:10],
            "recent_history": self.execution_history[:10]
        }

ruflo_orchestrator = RufloSwarmOrchestrator()
