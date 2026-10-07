"""
Nexus™ Agent Memory Service
===========================
Integrates the `agentmemory` package (Chromadb-backed vector memory) to provide
persistent, queryable long-term memory for autonomous agents.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger("Nexus.AgentMemory")

class AgentMemoryService:
    def __init__(self):
        self.is_initialized = False

    def initialize(self):
        if not self.is_initialized:
            try:
                import agentmemory
                self.agentmemory = agentmemory
                self.is_initialized = True
                logger.info("[AgentMemory] ChromaDB-backed agent memory initialized.")
            except ImportError:
                logger.warning("[AgentMemory] 'agentmemory' package not found. Running in fallback mode.")

    def save_memory(self, category: str, text: str, metadata: Dict[str, Any] = None) -> bool:
        """Saves a new memory into the specified category."""
        self.initialize()
        if not self.is_initialized:
            return False

        try:
            self.agentmemory.create_memory(category, text, metadata=metadata)
            logger.info(f"[AgentMemory] Saved to category '{category}': {text[:30]}...")
            return True
        except Exception as e:
            logger.error(f"[AgentMemory] Error saving memory: {e}")
            return False

    def search_memory(self, category: str, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Searches memories within a category based on semantic similarity."""
        self.initialize()
        if not self.is_initialized:
            return []

        try:
            results = self.agentmemory.search_memory(category, query, n_results=n_results)
            logger.info(f"[AgentMemory] Found {len(results)} matches in '{category}' for query '{query}'.")
            # results is typically a list of dictionaries with 'document' and 'metadata'
            return results
        except Exception as e:
            logger.error(f"[AgentMemory] Error searching memory: {e}")
            return []

    def get_memory_stats(self, category: str) -> Dict[str, Any]:
        """Returns statistics about a specific memory category."""
        self.initialize()
        if not self.is_initialized:
            return {"count": 0}

        try:
            memories = self.agentmemory.get_memories(category)
            return {"count": len(memories)}
        except Exception as e:
            logger.error(f"[AgentMemory] Error getting stats: {e}")
            return {"count": 0}

agent_memory_service = AgentMemoryService()
