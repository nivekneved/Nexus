# -*- coding: utf-8 -*-
"""
Nexus™ Agent Inner Monologue & Thought Stream Inspector (v22.0)
==============================================================
Provides real-time visibility into the cognitive trace, inner monologues, thoughts,
and active execution states of all 41 agents in the background.
"""

import logging
from typing import Dict, Any, List
from core.agent_manager import AgentManager
from core.telemetry import telemetry

logger = logging.getLogger("Nexus.AgentThoughtInspector")
agent_manager = AgentManager()

class AgentThoughtInspector:
    @staticmethod
    def get_all_agent_thoughts() -> Dict[str, Any]:
        """
        Inspects the live telemetry history and agent states to return the current
        inner monologues, thoughts, and execution steps for every agent.
        """
        recent_events = telemetry.get_recent_history()
        agents_info = agent_manager.list_agents()

        # Map recent telemetry events by agent_id
        agent_thoughts_map: Dict[str, List[Dict[str, Any]]] = {}
        for ev in recent_events:
            aid = ev.get("agent_id")
            if aid not in agent_thoughts_map:
                agent_thoughts_map[aid] = []
            agent_thoughts_map[aid].append(ev)

        comprehensive_stream = []
        for ag in agents_info:
            aid = ag.get("id")
            name = ag.get("name")
            status = ag.get("last_run_status", "Idle")
            last_run = ag.get("last_run_time", "Never")

            # Get latest thought / telemetry for this agent
            agent_evs = agent_thoughts_map.get(aid, [])
            latest_thought = agent_evs[-1] if agent_evs else {
                "timestamp": "Just now",
                "step": "STANDBY",
                "file_used": "core/base_agent.py",
                "message": f"Agent '{name}' is standing by on the Universal Synergy Mesh, monitoring background loops.",
                "level": "INFO"
            }

            comprehensive_stream.append({
                "agent_id": aid,
                "agent_name": name,
                "status": status,
                "last_run_time": last_run,
                "current_thought": {
                    "timestamp": latest_thought.get("timestamp"),
                    "step": latest_thought.get("step"),
                    "action_file": latest_thought.get("file_used"),
                    "inner_monologue": latest_thought.get("message"),
                    "log_level": latest_thought.get("level")
                },
                "recent_cognitive_trace": agent_evs[-5:] # Last 5 thoughts
            })

        return {
            "success": True,
            "version": "22.0 Agent Thought Inspector",
            "total_agents_reporting": len(comprehensive_stream),
            "fleet_thought_streams": comprehensive_stream
        }

agent_thought_inspector = AgentThoughtInspector()
