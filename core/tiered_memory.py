"""
Nexus™ 3-Tiered Memory Engine (Inspired by MemGPT / Letta)
=========================================================
Provides structured, persistent memory across 3 distinct tiers:
1. Working Memory (In-Memory RAM): Transient active task state and prompt context.
2. Recall Memory (Event Cache): Rolling window of the last 100 scouted niches, tool runs, and orders.
3. Archival Memory (Persistent Knowledge): Permanent verified templates, user preferences, and business rules.
"""

import os
import sys
import json
import time
from typing import Dict, Any, List, Optional

MEMORY_DIR = os.path.abspath("memory")
RECALL_FILE = os.path.join(MEMORY_DIR, "recall_memory.json")
ARCHIVAL_FILE = os.path.join(MEMORY_DIR, "archival_memory.json")

class TieredMemoryEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TieredMemoryEngine, cls).__new__(cls)
            cls._instance._init_storage()
        return cls._instance

    def _init_storage(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        self.working_memory: Dict[str, Any] = {
            "session_start": time.strftime("%Y-%m-%d %H:%M:%S"),
            "current_goal": "Autonomous $1 Digital Product Sales & Vending Machine",
            "active_tasks": []
        }
        if not os.path.exists(RECALL_FILE):
            self._save_json(RECALL_FILE, [])
        if not os.path.exists(ARCHIVAL_FILE):
            self._save_json(ARCHIVAL_FILE, {
                "owner": "Deven Pawaray",
                "brand": "Nexus AI Workforce",
                "default_currency": "USD",
                "mcb_juice": "+230 58169420",
                "verified_product_blueprints": [],
                "target_price_usd": 1.00
            })

    def _load_json(self, path: str, default: Any) -> Any:
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return default

    def _save_json(self, path: str, data: Any) -> bool:
        try:
            temp_path = f"{path}.tmp.{int(time.time()*1000)}"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(temp_path, path)
            return True
        except Exception as e:
            print(f"[TieredMemory] Save error for {path}: {e}")
            return False

    # Tier 1: Working Memory
    def set_working_context(self, key: str, value: Any):
        self.working_memory[key] = value

    def get_working_context(self, key: str, default: Any = None) -> Any:
        return self.working_memory.get(key, default)

    # Tier 2: Recall Memory (Rolling Cache of 100 items)
    def record_recall_event(self, event_type: str, details: Dict[str, Any]):
        events: List[Dict[str, Any]] = self._load_json(RECALL_FILE, [])
        record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "details": details
        }
        events.insert(0, record)
        events = events[:100]  # Keep most recent 100 items
        self._save_json(RECALL_FILE, events)

    def get_recent_recalls(self, event_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = self._load_json(RECALL_FILE, [])
        if event_type:
            events = [e for e in events if e.get("event_type") == event_type]
        return events[:limit]

    # Tier 3: Archival Memory (Permanent Long-Term Knowledge)
    def get_archival_knowledge(self) -> Dict[str, Any]:
        return self._load_json(ARCHIVAL_FILE, {})

    def update_archival_knowledge(self, key: str, value: Any) -> bool:
        data = self._load_json(ARCHIVAL_FILE, {})
        data[key] = value
        data["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        return self._save_json(ARCHIVAL_FILE, data)

    def archive_verified_product(self, product_meta: Dict[str, Any]):
        data = self._load_json(ARCHIVAL_FILE, {})
        blueprints = data.get("verified_product_blueprints", [])
        # Avoid duplicate entries
        if not any(b.get("id") == product_meta.get("id") for b in blueprints):
            blueprints.append(product_meta)
            data["verified_product_blueprints"] = blueprints
            data["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
            self._save_json(ARCHIVAL_FILE, data)

tiered_memory = TieredMemoryEngine()
