"""
Nexus™ Genesis SubAgent Replication & Lineage Engine
====================================================
Inspired by Conway Automaton's self-replication and child lifecycle system.
Allows Nexus to spawn, allocate budget to, supervise, and clean up
dynamic child subagents with specific genesis prompts and lineage tracking.
"""

import os
import json
import time
import uuid
from typing import Dict, Any, List, Optional
from core.telemetry import telemetry
from core.paths import resolve_data_path

LINEAGE_FILE_PATH = str(resolve_data_path("child_lineage.json"))


class ReplicationEngine:
    """
    Orchestrates the creation, lifecycle, and lineage of autonomous child worker agents.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ReplicationEngine, cls).__new__(cls)
            cls._instance.lineage_path = LINEAGE_FILE_PATH
            cls._instance._ensure_storage()
        return cls._instance

    def _ensure_storage(self):
        if not os.path.exists(self.lineage_path):
            try:
                with open(self.lineage_path, "w", encoding="utf-8") as f:
                    json.dump({"children": {}}, f, indent=2)
            except Exception:
                pass

    def _load_lineage(self) -> Dict[str, Any]:
        try:
            with open(self.lineage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"children": {}}

    def _save_lineage(self, data: Dict[str, Any]):
        try:
            temp_path = f"{self.lineage_path}.tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(temp_path, self.lineage_path)
        except Exception as e:
            print(f"[ReplicationEngine] Error saving lineage: {e}")

    def spawn_worker(
        self,
        name: str,
        genesis_prompt: str,
        parent_id: str = "nexus_core",
        budget_usd: float = 0.50,
        max_turns: int = 5
    ) -> Dict[str, Any]:
        """
        Spawns a new autonomous child subagent seeded with a genesis prompt.
        """
        child_id = f"child_{uuid.uuid4().hex[:8]}"
        now = time.strftime("%Y-%m-%d %H:%M:%S")

        record = {
            "child_id": child_id,
            "name": name,
            "parent_id": parent_id,
            "genesis_prompt": genesis_prompt,
            "status": "ALIVE",
            "allocated_budget_usd": budget_usd,
            "spent_usd": 0.0,
            "max_turns": max_turns,
            "turns_executed": 0,
            "created_at": now,
            "last_active": now,
            "messages": [
                {"role": "genesis", "content": genesis_prompt, "timestamp": now}
            ],
            "outputs": []
        }

        data = self._load_lineage()
        data["children"][child_id] = record
        self._save_lineage(data)

        telemetry.emit(
            agent_id=parent_id,
            agent_name="Replication Engine",
            step="SPAWN_CHILD_AGENT",
            file_used="core/replication_engine.py",
            message=f"Spawned child subagent '{name}' (ID: {child_id}) with budget ${budget_usd:.2f}",
            level="SUCCESS"
        )

        return {
            "success": True,
            "child_id": child_id,
            "name": name,
            "status": "ALIVE",
            "allocated_budget_usd": budget_usd,
            "created_at": now
        }

    def execute_child_turn(self, child_id: str, action_summary: str, cost_usd: float = 0.01) -> Dict[str, Any]:
        """
        Records a completed operational turn by a child subagent and enforces budget limits.
        """
        data = self._load_lineage()
        child = data["children"].get(child_id)
        if not child:
            return {"success": False, "error": f"Child subagent '{child_id}' not found."}

        if child["status"] != "ALIVE":
            return {"success": False, "error": f"Child subagent '{child_id}' is {child['status']}."}

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        child["turns_executed"] += 1
        child["spent_usd"] = round(child["spent_usd"] + cost_usd, 4)
        child["last_active"] = now
        child["outputs"].append({"turn": child["turns_executed"], "summary": action_summary, "timestamp": now})

        # Check turn or budget completion
        if child["turns_executed"] >= child["max_turns"]:
            child["status"] = "COMPLETED"
        elif child["spent_usd"] >= child["allocated_budget_usd"]:
            child["status"] = "BUDGET_EXHAUSTED"

        self._save_lineage(data)

        return {
            "success": True,
            "child_id": child_id,
            "status": child["status"],
            "turns_executed": child["turns_executed"],
            "spent_usd": child["spent_usd"]
        }

    def send_parent_message(self, child_id: str, message: str) -> Dict[str, Any]:
        """Sends an operational directive or clarification from the parent to the child."""
        data = self._load_lineage()
        child = data["children"].get(child_id)
        if not child:
            return {"success": False, "error": f"Child subagent '{child_id}' not found."}

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        child["messages"].append({"role": "parent", "content": message, "timestamp": now})
        child["last_active"] = now
        self._save_lineage(data)

        return {"success": True, "child_id": child_id, "messages_count": len(child["messages"])}

    def terminate_child(self, child_id: str, reason: str = "Mission Accomplished") -> Dict[str, Any]:
        """Gracefully shuts down and marks a child subagent as TERMINATED."""
        data = self._load_lineage()
        child = data["children"].get(child_id)
        if not child:
            return {"success": False, "error": f"Child subagent '{child_id}' not found."}

        child["status"] = "TERMINATED"
        child["termination_reason"] = reason
        child["last_active"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self._save_lineage(data)

        telemetry.emit(
            agent_id=child.get("parent_id", "nexus_core"),
            agent_name="Replication Engine",
            step="TERMINATE_CHILD_AGENT",
            file_used="core/replication_engine.py",
            message=f"Terminated child subagent '{child['name']}' ({child_id}): {reason}",
            level="INFO"
        )

        return {"success": True, "child_id": child_id, "status": "TERMINATED", "reason": reason}

    def list_children(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists child subagents, optionally filtered by status."""
        data = self._load_lineage()
        children = list(data.get("children", {}).values())
        if status:
            children = [c for c in children if c.get("status", "").upper() == status.upper()]
        return children

    def get_child_status(self, child_id: str) -> Optional[Dict[str, Any]]:
        """Gets full lineage and state of a specific child subagent."""
        data = self._load_lineage()
        return data.get("children", {}).get(child_id)


replication_engine = ReplicationEngine()
