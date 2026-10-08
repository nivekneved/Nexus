"""
LeadScout-Core: Recursive Event-Driven Orchestrator
===================================================
Queue runner, event dispatcher, and recursive state manager.
"""

import asyncio
import logging
from typing import Dict, Any, List, Set, Type
from leadscout.core.card import LeadCard
from leadscout.probes.base import BaseProbe
from leadscout.probes.domain.dns_probe import InspectDNSAndMXTask
from leadscout.probes.domain.tech_probe import InspectWebTechStackTask
from leadscout.probes.domain.stealth_scrape_probe import StealthWebScrapeProbe
from leadscout.probes.identity.search_probe import DiscoverKeyStaffTask
from leadscout.probes.identity.social_probe import ResolveSocialProfilesTask
from leadscout.probes.identity.bio_probe import QueryGravatarByHashTask, ExtractBioKeywordsTask
from leadscout.probes.deliverability.matrix_probe import SynthesizeEmailPermutationsTask
from leadscout.probes.deliverability.smtp_probe import AsyncSMTPValidationTask, QueryDeveloperAPIsTask

logger = logging.getLogger("LeadScout.Orchestrator")

class RecursiveOrchestrator:
    def __init__(self, timeout_seconds: float = 30.0):
        self.timeout_seconds = timeout_seconds
        self.trigger_map: Dict[str, List[Type[BaseProbe]]] = {
            "DOMAIN_RESOLVED": [InspectDNSAndMXTask, InspectWebTechStackTask, DiscoverKeyStaffTask, StealthWebScrapeProbe],
            "STAFF_DISCOVERED": [SynthesizeEmailPermutationsTask, ResolveSocialProfilesTask],
            "EMAIL_SYNTHESIZED": [AsyncSMTPValidationTask],
            "EMAIL_CONFIRMED": [QueryGravatarByHashTask, QueryDeveloperAPIsTask],
            "IDENTITY_DISCOVERED": [ExtractBioKeywordsTask]
        }

    async def run_pipeline(self, company_name: str, domain: str) -> LeadCard:
        card = LeadCard(lead_id=f"lead_{int(asyncio.get_event_loop().time())}", company_name=company_name, domain=domain)
        task_queue: asyncio.Queue[Type[BaseProbe]] = asyncio.Queue()

        # Initial triggers
        await task_queue.put(InspectDNSAndMXTask)
        await task_queue.put(InspectWebTechStackTask)
        await task_queue.put(DiscoverKeyStaffTask)

        visited_tasks: Set[str] = set()

        async def worker():
            while True:
                try:
                    probe_cls = await asyncio.wait_for(task_queue.get(), timeout=2.0)
                except asyncio.TimeoutError:
                    break

                probe_name = probe_cls.name
                if probe_name in card.completed_probes:
                    task_queue.task_done()
                    continue

                card.completed_probes.add(probe_name)
                probe_instance = probe_cls()

                try:
                    logger.info(f"Executing probe: {probe_name} for {card.company_name}")
                    delta = await probe_instance.execute(card)

                    # Synergy Bridge Integration: Fetch external OSINT threat intel (Shodan) via Repo Radar
                    if probe_name == "InspectDNSAndMXTask" and card.domain:
                        from core.agent_synergy_bridge import agent_synergy_bridge
                        logger.info(f"[Orchestrator] Invoking Synergy Mesh for VULNERABILITY_SCAN on {card.domain}")
                        synergy_res = await agent_synergy_bridge.invoke_service("leadscout", "VULNERABILITY_SCAN", {"domain": card.domain})
                        if synergy_res.get("success"):
                            shodan_data = synergy_res.get("data", {})
                            logger.info(f"[Orchestrator] Received Synergy OSINT: {shodan_data.get('open_ports')}")
                            # Append discovered tech footprint from Shodan to LeadCard tech_stack
                            tech = shodan_data.get("tech_footprint", [])
                            if tech:
                                card.tech_stack.extend(tech)
                                card.tech_stack = list(set(card.tech_stack))

                    # Apply delta updates to LeadCard
                    events_to_dispatch = []
                    for key, val in delta.items():
                        if hasattr(card, key):
                            current_val = getattr(card, key)
                            if not current_val and val:
                                setattr(card, key, val)
                                events_to_dispatch.append(key)

                    # Trigger downstream tasks based on state transitions
                    if card.domain and "domain" not in visited_tasks:
                        visited_tasks.add("domain")
                        for t in self.trigger_map.get("DOMAIN_RESOLVED", []):
                            await task_queue.put(t)

                    if card.staff_members and "staff" not in visited_tasks:
                        visited_tasks.add("staff")
                        for t in self.trigger_map.get("STAFF_DISCOVERED", []):
                            await task_queue.put(t)

                    if card.email_permutations and "perms" not in visited_tasks:
                        visited_tasks.add("perms")
                        for t in self.trigger_map.get("EMAIL_SYNTHESIZED", []):
                            await task_queue.put(t)

                    if card.confirmed_emails and "confirmed" not in visited_tasks:
                        visited_tasks.add("confirmed")
                        for t in self.trigger_map.get("EMAIL_CONFIRMED", []):
                            await task_queue.put(t)

                    if card.social_profiles and "social" not in visited_tasks:
                        visited_tasks.add("social")
                        for t in self.trigger_map.get("IDENTITY_DISCOVERED", []):
                            await task_queue.put(t)

                except Exception as e:
                    logger.error(f"Error in probe {probe_name}: {e}")
                finally:
                    task_queue.task_done()

        # Run concurrent workers with timeout
        workers = [asyncio.create_task(worker()) for _ in range(3)]
        try:
            await asyncio.wait_for(task_queue.join(), timeout=self.timeout_seconds)
        except asyncio.TimeoutError:
            logger.warning("Pipeline recursion timeout reached.")
        finally:
            for w in workers:
                w.cancel()

        # Calculate final qualification score
        score = 50.0
        if card.mx_records: score += 15.0
        if card.staff_members: score += 15.0
        if card.confirmed_emails: score += 20.0
        card.qualification_score = min(score, 100.0)
        card.status = "QUALIFIED"

        return card
