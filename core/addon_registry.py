import os
import json
import threading
from typing import Dict, Any, List, Optional

ADDONS_STATE_FILE = "addons_state.json"

class AddonRegistry:
    """
    Universal Addon Backbone
    Enforces the core principle:
    'Everything must come as an addon that can be activated and deactivated in the backend'
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AddonRegistry, cls).__new__(cls)
                cls._instance.addons: Dict[str, Dict[str, Any]] = {}
                cls._instance._load_saved_states()
        return cls._instance

    def _load_saved_states(self):
        self.saved_states = {}
        if os.path.exists(ADDONS_STATE_FILE):
            try:
                with open(ADDONS_STATE_FILE, "r", encoding="utf-8") as f:
                    self.saved_states = json.load(f)
            except Exception:
                self.saved_states = {}

    def _persist_states(self):
        states = {aid: a["is_active"] for aid, a in self.addons.items()}
        try:
            with open(ADDONS_STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(states, f, indent=2)
        except Exception:
            pass

    def register_addon(
        self,
        addon_id: str,
        name: str,
        category: str,
        description: str,
        default_active: bool = True,
        parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Registers any agent, subagent, or system feature as a modular toggleable Addon."""
        # If user previously saved a state, honor it; otherwise use default
        active_state = self.saved_states.get(addon_id, default_active)
        addon_record = {
            "id": addon_id,
            "name": name,
            "category": category,  # 'primary_agent', 'subagent', 'security_shield', 'engine_feature'
            "description": description,
            "is_active": active_state,
            "parent_id": parent_id
        }
        self.addons[addon_id] = addon_record
        return addon_record

    def is_active(self, addon_id: str) -> bool:
        addon = self.addons.get(addon_id)
        if not addon:
            return True  # fallback enabled if unregistered
        # If it's a subagent, verify parent is also active
        if addon.get("parent_id"):
            parent = self.addons.get(addon["parent_id"])
            if parent and not parent.get("is_active", True):
                return False
        return addon.get("is_active", True)

    def toggle_addon(self, addon_id: str) -> bool:
        if addon_id not in self.addons:
            raise ValueError(f"Addon '{addon_id}' not found in registry.")
        self.addons[addon_id]["is_active"] = not self.addons[addon_id]["is_active"]
        self._persist_states()
        return self.addons[addon_id]["is_active"]

    def set_addon_state(self, addon_id: str, is_active: bool) -> bool:
        if addon_id not in self.addons:
            raise ValueError(f"Addon '{addon_id}' not found in registry.")
        self.addons[addon_id]["is_active"] = bool(is_active)
        self._persist_states()
        return self.addons[addon_id]["is_active"]

    def list_addons(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        items = list(self.addons.values())
        if category:
            items = [it for it in items if it["category"] == category]
        return items

addon_registry = AddonRegistry()
