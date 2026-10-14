"""
Nexus™ Search, Dig & Locate Skills Module (v1.0)
=================================================
Provides explicit programmatic capabilities to every agent across the fleet:
1. Search Skill: Web searching, keyword extraction, vector memory lookup, lead indices.
2. Dig Skill: Deep reconnaissance, DOM/HTML scraping, HTTP inspection, DNS/MX record lookup, source text mining.
3. Locate Skill: Entity mapping, reverse phone enrichment, official company registry querying, and asset discovery.
"""

import os
import socket
import logging
import urllib.parse
from typing import Dict, Any, List, Optional
from core.agent_internet_bridge import agent_internet_bridge

logger = logging.getLogger("Nexus.SearchDigLocateSkills")

class AgentSearchDigLocateSkills:
    """
    Core skills engine providing Search, Dig, and Locate capabilities to all agents.
    """

    @staticmethod
    def agent_search(query: str, category: str = "web", max_results: int = 5) -> Dict[str, Any]:
        """
        [SEARCH SKILL] Searches the live public internet, vector memory, or lead indices.
        """
        logger.info(f"[SearchSkill] 🔍 Searching ({category}): '{query}'")
        try:
            if category == "web":
                return agent_internet_bridge.search_public_web(query=query, max_results=max_results)
            elif category == "memory":
                from core.agent_memory_service import agent_memory_service
                results = agent_memory_service.search_memory("general", query, n_results=max_results)
                return {"success": True, "category": "memory", "query": query, "results": results}
            else:
                return agent_internet_bridge.search_public_web(query=query, max_results=max_results)
        except Exception as e:
            logger.error(f"[SearchSkill] Error: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def agent_dig(target: str, dig_type: str = "web_dom", max_chars: int = 8000) -> Dict[str, Any]:
        """
        [DIG SKILL] Performs deep reconnaissance: DOM scraping, HTTP headers, DNS records, or text mining.
        """
        logger.info(f"[DigSkill] ⛏️ Digging ({dig_type}) into target: '{target}'")
        try:
            if dig_type == "web_dom":
                return agent_internet_bridge.scrape_webpage(url=target, max_chars=max_chars)
            elif dig_type == "dns":
                parsed_url = urllib.parse.urlparse(target)
                domain = parsed_url.netloc or parsed_url.path
                domain = domain.split("/")[0]
                try:
                    ip_address = socket.gethostbyname(domain)
                    return {"success": True, "dig_type": "dns", "domain": domain, "ip_address": ip_address}
                except Exception as dns_err:
                    return {"success": False, "dig_type": "dns", "domain": domain, "error": str(dns_err)}
            elif dig_type == "http_headers":
                return agent_internet_bridge.fetch_public_url(url=target, method="GET")
            else:
                return agent_internet_bridge.scrape_webpage(url=target, max_chars=max_chars)
        except Exception as e:
            logger.error(f"[DigSkill] Error: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def agent_locate(entity_query: str, locate_type: str = "registry") -> Dict[str, Any]:
        """
        [LOCATE SKILL] Maps precision entities: official registry lookups, reverse phone enrichment, or asset discovery.
        """
        logger.info(f"[LocateSkill] 📍 Locating ({locate_type}) for entity: '{entity_query}'")
        try:
            if locate_type == "registry":
                from core.official_registry_bridge import official_registry_bridge
                res = official_registry_bridge.query_official_registry("global", entity_query)
                return {"success": True, "locate_type": "registry", "query": entity_query, "result": res}
            elif locate_type == "phone":
                from core.reverse_phone_enrichment import reverse_phone_enrichment
                res = reverse_phone_enrichment.enrich_phone(entity_query)
                return {"success": True, "locate_type": "phone", "query": entity_query, "result": res}
            elif locate_type == "email_osint":
                from core.email_osint_service import email_osint_service
                res = email_osint_service.query_email(entity_query)
                return {"success": True, "locate_type": "email_osint", "query": entity_query, "result": res}
            else:
                from core.official_registry_bridge import official_registry_bridge
                res = official_registry_bridge.query_official_registry("global", entity_query)
                return {"success": True, "locate_type": "registry", "query": entity_query, "result": res}
        except Exception as e:
            logger.error(f"[LocateSkill] Error: {e}")
            return {"success": False, "error": str(e)}

agent_search_dig_locate = AgentSearchDigLocateSkills()
