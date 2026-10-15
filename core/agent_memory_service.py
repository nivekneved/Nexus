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
        """Searches memories within a category with Kronos-style temporal recency and keyword scoring."""
        try:
            store = safe_load_json(MEMORY_STORE_FILE, default={})
            mems = store.get(category, [])
            q_lower = query.lower()

            scored_mems = []
            for idx, m in enumerate(mems):
                doc = m.get("document", "").lower()
                meta = str(m.get("metadata", "")).lower()
                score = 0
                if q_lower in doc or q_lower in meta:
                    score += 10
                # Kronos Temporal Recency Bonus: newer memories get higher temporal rank
                recency_bonus = max(0, 1.0 - (idx * 0.05))
                score += recency_bonus

                scored_mems.append((score, m))

            scored_mems.sort(key=lambda x: x[0], reverse=True)
            return [m for score, m in scored_mems[:n_results]]
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
