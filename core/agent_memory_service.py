"""
Nexus™ Agent Memory Service
===========================
Provides robust persistent long-term memory for autonomous agents (with JSON storage fallback).
"""

import logging
import time
from typing import Dict, Any, List
from core.storage import atomic_save_json, safe_load_json

logger = logging.getLogger("Nexus.AgentMemory")

MEMORY_STORE_FILE = "agent_memory_store.json"

class AgentMemoryService:
    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        if not safe_load_json(MEMORY_STORE_FILE):
            atomic_save_json(MEMORY_STORE_FILE, {})

    def save_memory(self, category: str, text: str, metadata: Dict[str, Any] = None) -> bool:
        """Saves a new memory into the specified category."""
        try:
            store = safe_load_json(MEMORY_STORE_FILE, default={})
            store.setdefault(category, [])
            store[category].insert(0, {
                "document": text,
                "metadata": metadata or {},
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            atomic_save_json(MEMORY_STORE_FILE, store)
            logger.info(f"[AgentMemory] Saved memory to '{category}': {text[:30]}...")
            return True
        except Exception as e:
            logger.error(f"[AgentMemory] Error saving memory: {e}")
            return False

    def search_memory(self, category: str, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Searches memories within a category based on keyword matching."""
        try:
            store = safe_load_json(MEMORY_STORE_FILE, default={})
            mems = store.get(category, [])
            q_lower = query.lower()
            matches = [m for m in mems if q_lower in m.get("document", "").lower() or q_lower in str(m.get("metadata", "")).lower()]
            return matches[:n_results]
        except Exception as e:
            logger.error(f"[AgentMemory] Error searching memory: {e}")
            return []

    def get_memory_stats(self, category: str) -> Dict[str, Any]:
        """Returns statistics about a specific memory category."""
        try:
            store = safe_load_json(MEMORY_STORE_FILE, default={})
            mems = store.get(category, [])
            return {"count": len(mems)}
        except Exception as e:
            logger.error(f"[AgentMemory] Error getting stats: {e}")
            return {"count": 0}

agent_memory_service = AgentMemoryService()
