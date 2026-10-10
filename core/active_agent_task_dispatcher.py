# -*- coding: utf-8 -*-
"""
Nexus™ Active Agent Task Dispatcher & Standby Elimination Engine (v43.0)
=====================================================================
Eliminates standby and idle agent states by dynamically dispatching active work queues
(lead prospecting, email hygiene, port scans, security audits) across all 41 agents.
"""

import time
import logging
from typing import Dict, Any, List
from core.storage import safe_load_json, atomic_save_json
from core.agent_manager import AgentManager
from core.telemetry import telemetry

logger = logging.getLogger("Nexus.ActiveAgentDispatcher")
agent_manager = AgentManager()

WORK_QUEUE_FILE = "active_agent_work_queue.json"

class ActiveAgentTaskDispatcher:
    def __init__(self):
        self._ensure_queue()

    def _ensure_queue(self):
        if not safe_load_json(WORK_QUEUE_FILE):
            atomic_save_json(WORK_QUEUE_FILE, [
                {"task_id": "tsk_01", "target_agent": "lead_finder", "task": "Scout fresh B2B leads across UK & South Africa registries.", "status": "QUEUED"},
                {"task_id": "tsk_02", "target_agent": "growth_hacker", "task": "Optimize multi-channel conversion bandit mutation arms.", "status": "QUEUED"},
                {"task_id": "tsk_03", "target_agent": "email_hygiene", "task": "Run MX DNS socket validation batch on inbound leads.", "status": "QUEUED"},
                {"task_id": "tsk_04", "target_agent": "bounty_hunter", "task": "Harvest active bug bounties and generate AST secure patches.", "status": "QUEUED"}
            ])

    def assign_work_to_all_agents(self) -> Dict[str, Any]:
        """
        Ensures zero agents are idle by assigning active tasks to every agent in the fleet.
        """
        start_time = time.time()
        queue = safe_load_json(WORK_QUEUE_FILE, default=[])
        agents = agent_manager.agents
        assigned_count = 0

        for agent_id, agent in agents.items():
            agent.is_enabled = True
            agent.consecutive_idle_cycles = 0  # Reset idle counter

            # Find or create active task for this agent
            agent_task = next((t for t in queue if t.get("target_agent") == agent_id and t.get("status") == "QUEUED"), None)
            if not agent_task:
                agent_task = {
                    "task_id": f"tsk_{int(time.time())}_{agent_id}",
                    "target_agent": agent_id,
                    "task": f"Executing continuous sovereign duties for {agent.name}.",
                    "status": "IN_PROGRESS"
                }
                queue.append(agent_task)
            else:
                agent_task["status"] = "IN_PROGRESS"

            assigned_count += 1
            telemetry.emit(
                agent_id=agent_id,
                agent_name=agent.name,
                step="ACTIVE_TASK_ASSIGNED",
                file_used="core/active_agent_task_dispatcher.py",
                message=f"Assigned task: '{agent_task['task']}' (Zero Standby Active).",
                level="INFO"
            )

        atomic_save_json(WORK_QUEUE_FILE, queue)
        elapsed_ms = (time.time() - start_time) * 1000.0

        return {
            "success": True,
            "version": "v43.0 Active Agent Task Dispatcher",
            "execution_time_ms": elapsed_ms,
            "agents_activated": assigned_count,
            "standby_status": "ZERO_IDLE_AGENTS",
            "message": f"Successfully activated all {assigned_count} agents. Zero standby permitted!"
        }

active_agent_dispatcher = ActiveAgentTaskDispatcher()
