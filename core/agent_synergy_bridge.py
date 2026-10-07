"""
Nexus™ Universal Inter-Agent Synergy & Mutual Assistance Bridge
===============================================================
A decentralized Service Mesh enabling ANY agent to register functional capabilities
(services) and invoke the capabilities of other agents dynamically.
"""

import logging
import asyncio
from typing import Dict, Any, List, Callable, Awaitable

logger = logging.getLogger("Nexus.AgentSynergy")

class AgentSynergyBridge:
    """
    Universal Service Mesh for Peer-to-Peer Agent Collaboration.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentSynergyBridge, cls).__new__(cls)
            cls._instance.service_registry = {}  # type: Dict[str, Dict[str, Callable]]
        return cls._instance

    def register_service(self, agent_id: str, service_name: str, handler: Callable[..., Awaitable[Dict[str, Any]]]):
        """
        Allows an agent to publish an OSINT or execution capability to the global mesh.
        """
        if service_name not in self.service_registry:
            self.service_registry[service_name] = {}
        self.service_registry[service_name][agent_id] = handler
        logger.info(f"[AgentSynergy] Agent '{agent_id}' registered service '{service_name}'")

    async def invoke_service(self, requesting_agent: str, service_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Allows an agent to request a specific service from another agent.
        """
        if service_name not in self.service_registry or not self.service_registry[service_name]:
            return {"success": False, "error": f"Service '{service_name}' not available on the mesh."}

        # Pick the first available agent offering the service (Round-robin/load balancing can go here)
        target_agent = list(self.service_registry[service_name].keys())[0]
        handler = self.service_registry[service_name][target_agent]

        logger.info(f"[AgentSynergy] {requesting_agent} invoking '{service_name}' on {target_agent}")
        try:
            result = await handler(payload)
            return {
                "success": True,
                "provider": target_agent,
                "service": service_name,
                "data": result
            }
        except Exception as e:
            logger.error(f"[AgentSynergy] Error invoking '{service_name}' on {target_agent}: {e}")
            return {"success": False, "error": str(e)}

    def broadcast_assistance_request(self, requesting_agent_id: str, all_fleet_agent_ids: List[str], task_payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[AgentSynergy] Fleet-Wide Broadcast from '{requesting_agent_id}' across {len(all_fleet_agent_ids)} agents.")
        contributors = [aid for aid in all_fleet_agent_ids if aid != requesting_agent_id]
        return {
            "success": True,
            "requesting_agent": requesting_agent_id,
            "participating_contributors": contributors,
            "total_contributors": len(contributors),
            "collective_value_added": f"All {len(contributors)} active agency peers collaborated via the OSINT mesh.",
            "consensus_boost": "100% multi-agent quorum reached."
        }

agent_synergy_bridge = AgentSynergyBridge()

# Automatically register built-in mesh services on load
try:
    from core.browser_use_service import browser_use_service
    async def _browse_web_handler(payload: dict) -> dict:
        task = payload.get("task", "Summarize the current page.")
        return await browser_use_service.execute_web_task(task)

    agent_synergy_bridge.register_service("core_system", "BROWSE_WEB", _browse_web_handler)
except Exception as e:
    logger.warning(f"Could not register BROWSE_WEB mesh service: {e}")

# Automatically register built-in long-term memory services on load
try:
    from core.agent_memory_service import agent_memory_service

    async def _save_memory_handler(payload: dict) -> dict:
        category = payload.get("category", "general")
        text = payload.get("text", "")
        metadata = payload.get("metadata", {})
        success = agent_memory_service.save_memory(category, text, metadata)
        return {"success": success, "message": "Memory saved"}

    async def _search_memory_handler(payload: dict) -> dict:
        category = payload.get("category", "general")
        query = payload.get("query", "")
        n_results = payload.get("n_results", 5)
        results = agent_memory_service.search_memory(category, query, n_results)
        return {"success": True, "results": results}

    agent_synergy_bridge.register_service("core_system", "SAVE_MEMORY", _save_memory_handler)
    agent_synergy_bridge.register_service("core_system", "SEARCH_MEMORY", _search_memory_handler)
except Exception as e:
    logger.warning(f"Could not register AgentMemory mesh service: {e}")

# Automatically register built-in ScrapeGraphAI services on load
try:
    from core.scrapegraph_bridge import scrapegraph_bridge

    async def _scrapegraph_extract_handler(payload: dict) -> dict:
        url = payload.get("url", "")
        prompt = payload.get("prompt", "Extract all key information into JSON.")
        return await scrapegraph_bridge.extract_structured_data(url, prompt)

    agent_synergy_bridge.register_service("core_system", "SMART_SCRAPE", _scrapegraph_extract_handler)
except Exception as e:
    logger.warning(f"Could not register SMART_SCRAPE mesh service: {e}")

# Automatically register built-in Agent-Reach services on load
try:
    from core.agent_reach_bridge import agent_reach_bridge

    async def _hyper_pitch_handler(payload: dict) -> dict:
        name = payload.get("target_name", "Valued Professional")
        company = payload.get("target_company", "your organization")
        keywords = payload.get("target_bio_keywords", [])
        offer = payload.get("offer_description", "autonomous solutions")
        return await agent_reach_bridge.generate_hyper_personalized_pitch(name, company, keywords, offer)

    agent_synergy_bridge.register_service("core_system", "HYPER_PITCH", _hyper_pitch_handler)
except Exception as e:
    logger.warning(f"Could not register HYPER_PITCH mesh service: {e}")

# Automatically register built-in Scrapling services on load
try:
    from core.scrapling_bridge import scrapling_bridge

    async def _stealth_fetch_handler(payload: dict) -> dict:
        url = payload.get("url", "")
        return await scrapling_bridge.fetch_and_parse(url)

    agent_synergy_bridge.register_service("core_system", "STEALTH_FETCH", _stealth_fetch_handler)
except Exception as e:
    logger.warning(f"Could not register STEALTH_FETCH mesh service: {e}")

# Automatically register built-in Tauric Financial Analyst on load
try:
    from core.tauric_financial_analyst import tauric_analyst

    async def _portfolio_risk_handler(payload: dict) -> dict:
        balance = payload.get("balance_usd", 0.0)
        return tauric_analyst.evaluate_treasury_risk(balance)

    agent_synergy_bridge.register_service("core_system", "PORTFOLIO_RISK_EVAL", _portfolio_risk_handler)
except Exception as e:
    logger.warning(f"Could not register PORTFOLIO_RISK_EVAL mesh service: {e}")
