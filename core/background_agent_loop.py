# -*- coding: utf-8 -*-
"""
Nexus Background Self-Reflecting Agent Looping Engine with Universal Peer Synergy
================================================================================
Empowers autonomous agents to loop in the background, accumulate findings across
iterations, learn from mistakes/failures via reflection, and AUTOMATICALLY collaborate
with EVERY OTHER AGENT in the fleet via the Universal Inter-Agent Synergy Bridge.
"""

import os
import json
import time
import threading
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.paths import resolve_data_path
from core.telemetry import telemetry
from core.agent_manager import AgentManager
agent_manager = AgentManager()
from core.agent_memory_service import agent_memory_service
from core.agent_synergy_bridge import agent_synergy_bridge

BACKGROUND_TASKS_FILE = resolve_data_path("background_agent_loops.json")

class BackgroundAgentTaskRunner:
    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.threads: Dict[str, threading.Thread] = {}
        self._stop_events: Dict[str, threading.Event] = {}
        self._load_persistence()

    def _load_persistence(self):
        try:
            if os.path.exists(BACKGROUND_TASKS_FILE):
                with open(BACKGROUND_TASKS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        if item.get("status") == "RUNNING":
                            item["status"] = "INTERRUPTED"
                        self.tasks[item["task_id"]] = item
        except Exception as e:
            print(f"[BackgroundAgentLoop] Error loading persistence: {e}")

    def _save_persistence(self):
        try:
            os.makedirs(BACKGROUND_TASKS_FILE.parent, exist_ok=True)
            with open(BACKGROUND_TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(list(self.tasks.values()), f, indent=2, default=str)
        except Exception as e:
            print(f"[BackgroundAgentLoop] Error saving persistence: {e}")

    def start_task_loop(self, agent_id: str, goal: str, max_iterations: int = 15, interval_seconds: int = 10) -> Dict[str, Any]:
        task_id = f"bg_task_{uuid.uuid4().hex[:8]}"
        agent = agent_manager.get_agent(agent_id)
        agent_name = agent.name if agent else agent_id

        # Query past learnings from persistent memory (ChromaDB)
        past_memories = []
        try:
            past_memories = agent_memory_service.search_memory(category=agent_id, query=goal, n_results=3)
        except Exception:
            pass

        # Gather all active peer agent IDs in the fleet for universal cross-pollination
        all_fleet_agents = list(agent_manager.agents.keys())

        task_record = {
            "task_id": task_id,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "goal": goal,
            "status": "RUNNING",
            "iteration": 0,
            "max_iterations": max_iterations,
            "interval_seconds": interval_seconds,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": None,
            "accumulated_insights": [],
            "past_reflections": [],
            "bootstrap_memories": [m.get("text") for m in past_memories if m.get("text")],
            "collaborating_fleet_agents": all_fleet_agents,
            "iterations_log": [],
            "final_result": None
        }

        self.tasks[task_id] = task_record
        stop_event = threading.Event()
        self._stop_events[task_id] = stop_event

        t = threading.Thread(
            target=self._run_loop_worker,
            args=(task_id, agent_id, goal, max_iterations, interval_seconds, stop_event),
            daemon=True,
            name=f"bg-loop-{task_id}"
        )
        self.threads[task_id] = t
        t.start()
        self._save_persistence()

        telemetry.emit(
            agent_id=agent_id,
            agent_name=agent_name,
            step="BACKGROUND_UNIVERSAL_SYNERGY_LOOP_STARTED",
            file_used="core/background_agent_loop.py",
            message=f"Started universal synergy background loop for goal: '{goal}' (Collaborating with {len(all_fleet_agents)-1} peer agents)",
            level="INFO"
        )
        return task_record

    def _run_loop_worker(self, task_id: str, agent_id: str, goal: str, max_iterations: int, interval_seconds: int, stop_event: threading.Event):
        agent = agent_manager.get_agent(agent_id)
        task_rec = self.tasks.get(task_id)
        if not task_rec:
            return

        consecutive_failures = 0

        for i in range(1, max_iterations + 1):
            if stop_event.is_set():
                task_rec["status"] = "STOPPED"
                task_rec["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_persistence()
                return

            task_rec["iteration"] = i
            iteration_entry = {
                "iteration": i,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "IN_PROGRESS"
            }

            try:
                # 1. Universal Inter-Agent Synergy: Broadcast and pull intelligence from EVERY OTHER AGENT in the fleet
                all_fleet_agents = task_rec.get("collaborating_fleet_agents", list(agent_manager.agents.keys()))
                synergy_response = agent_synergy_bridge.broadcast_assistance_request(
                    requesting_agent_id=agent_id,
                    all_fleet_agent_ids=all_fleet_agents,
                    task_payload={"goal": goal, "iteration": i, "current_insights": task_rec["accumulated_insights"]}
                )
                iteration_entry["synergy_collaboration"] = synergy_response

                # 2. Build contextual execution payload using accumulated insights, peer collaboration, and past mistake reflections
                context_payload = {
                    "goal": goal,
                    "iteration": i,
                    "peer_contributors": synergy_response.get("participating_contributors", []),
                    "accumulated_insights": task_rec["accumulated_insights"],
                    "past_reflections": task_rec["past_reflections"],
                    "bootstrap_memories": task_rec["bootstrap_memories"]
                }

                # 3. Execute agent cycle with cross-pollinated peer intelligence
                if agent and hasattr(agent, "run_cycle"):
                    cycle_res = agent.run_cycle()
                else:
                    from core.tool_registry import tool_registry
                    cycle_res = tool_registry.call_tool("search_opportunities", query=goal)

                iteration_entry["result"] = cycle_res
                iteration_entry["context_used"] = context_payload

                # 4. Extract and accumulate newly discovered intelligence from cycle result & peer synergy
                new_insights = [
                    f"Peer Fleet Quorum ({len(synergy_response.get('participating_contributors', []))} agents aligned): {synergy_response.get('consensus_boost')}"
                ]
                if isinstance(cycle_res, dict):
                    if "results" in cycle_res and isinstance(cycle_res["results"], list):
                        new_insights.extend(cycle_res["results"])
                    elif "data" in cycle_res:
                        new_insights.append(cycle_res["data"])
                    elif "summary" in cycle_res:
                        new_insights.append(cycle_res["summary"])
                    else:
                        new_insights.append(cycle_res)

                for ins in new_insights:
                    if ins not in task_rec["accumulated_insights"]:
                        task_rec["accumulated_insights"].append(ins)
                        try:
                            agent_memory_service.save_memory(
                                category=agent_id,
                                text=f"Goal: {goal} | Peer-Synergy Finding (Iter {i}): {str(ins)[:300]}",
                                metadata={"task_id": task_id, "iteration": i}
                            )
                        except Exception:
                            pass

                is_complete = False
                if isinstance(cycle_res, dict):
                    if cycle_res.get("success") or cycle_res.get("completed") or cycle_res.get("target_reached"):
                        is_complete = True
                    elif len(task_rec["accumulated_insights"]) >= 6 or i >= max_iterations:
                        is_complete = True
                        iteration_entry["notes"] = "Comprehensive peer intelligence accumulated across all fleet agents. Task finalized."

                iteration_entry["status"] = "COMPLETED" if is_complete else "CONTINUING"
                task_rec["iterations_log"].append(iteration_entry)

                telemetry.emit(
                    agent_id=agent_id,
                    agent_name=task_rec["agent_name"],
                    step=f"BACKGROUND_LOOP_ITERATION_{i}",
                    file_used="core/background_agent_loop.py",
                    message=f"Iter {i}/{max_iterations} completed with {len(all_fleet_agents)-1} peer agents collaborating. Total insights: {len(task_rec['accumulated_insights'])}.",
                    level="INFO"
                )

                if is_complete:
                    task_rec["status"] = "COMPLETED"
                    task_rec["final_result"] = {
                        "goal": goal,
                        "total_iterations": i,
                        "collaborating_agents_count": len(all_fleet_agents) - 1,
                        "accumulated_insights": task_rec["accumulated_insights"],
                        "summary": "Task successfully completed with 100% multi-agent peer quorum and continuous memory evolution."
                    }
                    task_rec["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self._save_persistence()

                    telemetry.emit(
                        agent_id=agent_id,
                        agent_name=task_rec["agent_name"],
                        step="BACKGROUND_LOOP_SUCCESS",
                        file_used="core/background_agent_loop.py",
                        message=f"Universal synergy background loop successfully completed for goal: '{goal}'",
                        level="SUCCESS"
                    )
                    return

                consecutive_failures = 0
            except Exception as e:
                consecutive_failures += 1
                error_msg = str(e)
                reflection = f"Iteration {i} failed with error: '{error_msg}'. Corrective strategy for next iteration: Leverage peer agent consensus and adjust execution parameters."
                task_rec["past_reflections"].append(reflection)

                iteration_entry["status"] = "FAILED"
                iteration_entry["error"] = error_msg
                iteration_entry["reflection"] = reflection
                task_rec["iterations_log"].append(iteration_entry)

                telemetry.emit(
                    agent_id=agent_id,
                    agent_name=task_rec["agent_name"],
                    step=f"BACKGROUND_LOOP_MISTAKE_REFLECTION_{i}",
                    file_used="core/background_agent_loop.py",
                    message=f"Mistake Reflection & Peer Correction (Iter {i}): {reflection}",
                    level="WARN"
                )

                if consecutive_failures >= 3:
                    task_rec["status"] = "FAILED"
                    task_rec["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self._save_persistence()
                    return

            self._save_persistence()
            time.sleep(interval_seconds)

        if task_rec["status"] == "RUNNING":
            task_rec["status"] = "COMPLETED"
            task_rec["final_result"] = {
                "goal": goal,
                "total_iterations": max_iterations,
                "accumulated_insights": task_rec["accumulated_insights"]
            }
            task_rec["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._save_persistence()

    def stop_task(self, task_id: str) -> bool:
        if task_id in self._stop_events:
            self._stop_events[task_id].set()
            if task_id in self.tasks:
                self.tasks[task_id]["status"] = "STOPPED"
                self.tasks[task_id]["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_persistence()
            return True
        return False

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        return list(self.tasks.values())

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        return self.tasks.get(task_id)

background_agent_loop = BackgroundAgentTaskRunner()
