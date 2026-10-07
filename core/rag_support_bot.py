"""
Nexus™ RAG-Powered Customer Support Bot
=======================================
Uses agentmemory (ChromaDB) to answer technical product questions instantly.
"""
import logging
from typing import Dict, Any
from core.agent_memory_service import agent_memory_service

logger = logging.getLogger("Nexus.RAGSupportBot")

class RAGSupportBot:
    @staticmethod
    def answer_support_query(query: str) -> Dict[str, Any]:
        logger.info(f"[RAGSupportBot] Querying ChromaDB for: '{query}'")
        # Ensure memory is initialized
        agent_memory_service.initialize()
        results = agent_memory_service.search_memory("documentation", query, n_results=1)

        # Fallback if DB is empty
        answer = "To install the python script, run: pip install -r requirements.txt && python main.py"
        if results and hasattr(results, "documents") and results.documents:
             answer = results.documents[0][0]

        return {
            "success": True,
            "query": query,
            "instant_resolution": answer,
            "human_escalation_needed": False
        }

rag_support_bot = RAGSupportBot()
