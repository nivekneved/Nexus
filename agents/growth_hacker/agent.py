import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.growth_hacker.subagents import (
    AgentMonetizationScoutSubAgent,
    BountyOpportunityHarvesterSubAgent,
    RevenueExecutionClonerSubAgent,
    BLUEPRINTS_FILE,
    PROVEN_AI_AGENT_MONETIZATION_MODELS,
    ACTIVE_BOUNTIES_DATABASE
)

class GrowthHackerAgent(BaseAgent):
    """
    Employee #15: Autonomous Revenue Scout & Fund Harvester
    Continuously discovers what other AI agents are doing to generate funds,
    scans open-source bug bounties and client RFPs, and reverse-engineers their
    monetization tactics into ready-to-execute revenue streams for Nexus.
    """
    def __init__(self):
        super().__init__(
            agent_id="growth_hacker",
            name="Autonomous Revenue Scout & Fund Harvester",
            description="Searches for ways other AI agents generate funds, tracks high-payout bounties, and clones proven monetization blueprints into active Nexus cashflow pipelines.",
            icon="zap",
            schedule_minutes=180
        )
        self.config = {
            "SCAN_BOUNTY_PLATFORMS": True,
            "TRACK_COMPETITOR_MODELS": True,
            "AUTO_CLONE_TOP_TACTIC": True,
            "MIN_BOUNTY_REWARD_USD": 100,
            "PREFERRED_CURRENCY": "MUR"
        }
        self.stats = {
            "models_scouted": len(PROVEN_AI_AGENT_MONETIZATION_MODELS),
            "bounties_tracked": len(ACTIVE_BOUNTIES_DATABASE),
            "blueprints_active": self._count_blueprints(),
            "potential_inflow_mur": 95000
        }

        # Register specialized single-task subagents
        self.register_subagent(AgentMonetizationScoutSubAgent())
        self.register_subagent(BountyOpportunityHarvesterSubAgent())
        self.register_subagent(RevenueExecutionClonerSubAgent())

        # Seed initial blueprint if empty
        self._ensure_seed_blueprints()

    def _ensure_seed_blueprints(self):
        if not os.path.exists(BLUEPRINTS_FILE):
            seeds = [
                {
                    "blueprint_id": "BP-0001",
                    "source_model": "model_turnkey_whitelabel",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "READY_TO_EXECUTE",
                    "primary_offer": "Enn Rev Enn Sourir™ Turnkey NGO Portal (Rs 45,000) & Medical 360™ (Rs 45,000)",
                    "target_buyers": [
                        "Mauritian Corporate CSR Funds (MCB Forward Foundation, Rogers Capital, IBL)",
                        "Private Clinics & Diagnostic Labs (Clinique du Nord, Bon Pasteur, City Clinic)"
                    ],
                    "execution_channels": [
                        "1-Click WhatsApp Direct Pitch (+230 58169420)",
                        "MCB Juice Direct Reconciled Verification"
                    ],
                    "live_proof_assets": [
                        "https://ennrevennsourir.vercel.app",
                        "https://www.med360.mu/preview"
                    ],
                    "projected_inflow": "Rs 90,000 MUR (Clears Overdraft 180%)"
                },
                {
                    "blueprint_id": "BP-0002",
                    "source_model": "model_founder_license",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "READY_TO_EXECUTE",
                    "primary_offer": "Nexus 14-Agent Local Workforce Lifetime Commercial License ($249 USD)",
                    "target_buyers": [
                        "Indie Hackers on Twitter/X, Reddit r/indiehackers, and Product Hunt"
                    ],
                    "execution_channels": [
                        "Instant PayPal REST API Checkout ($249)",
                        "Automated Source Code + Docker Package Delivery"
                    ],
                    "live_proof_assets": [
                        "http://localhost:8000/license"
                    ],
                    "projected_inflow": "$1,245 USD (~Rs 57,000 MUR from 5 Sales)"
                }
            ]
            try:
                with open(BLUEPRINTS_FILE, "w", encoding="utf-8") as f:
                    json.dump(seeds, f, indent=2)
            except Exception:
                pass

    def get_blueprints(self) -> List[Dict[str, Any]]:
        self._ensure_seed_blueprints()
        try:
            with open(BLUEPRINTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _count_blueprints(self) -> int:
        return len(self.get_blueprints())

    def get_bounties(self) -> List[Dict[str, Any]]:
        return ACTIVE_BOUNTIES_DATABASE

    def get_competitor_models(self) -> List[Dict[str, Any]]:
        return PROVEN_AI_AGENT_MONETIZATION_MODELS

    def run_cycle(self) -> Dict[str, Any]:
        """Runs the complete growth hacking & monetization discovery cycle."""
        self.log(step="Monetization Scout", file_used="growth_hacker/agent.py", message="Scanning competitor agent frameworks for funding playbooks...", level="INFO")
        
        # Subagent 1: Scout Models
        scout_res = self.run_subagent("revenue_model_scout", {})
        
        # Subagent 2: Harvest Bounties
        bounty_res = self.run_subagent("bounty_grant_harvester", {})
        
        # Subagent 3: Clone top revenue model into executable blueprint
        clone_res = self.run_subagent("revenue_execution_cloner", {
            "model_id": "model_turnkey_whitelabel"
        })

        self.stats["blueprints_active"] = self._count_blueprints()
        self.log(
            step="Revenue Cloned",
            file_used=BLUEPRINTS_FILE,
            message=f"Synthesized active cashflow blueprint: {clone_res.get('blueprint', {}).get('blueprint_id', 'BP-NEW')}",
            level="SUCCESS"
        )

        return {
            "status": "Monetization Scout Cycle Finished",
            "competitor_models": scout_res,
            "bounties": bounty_res,
            "cloned_blueprint": clone_res
        }

    def clone_tactic(self, model_id: str) -> Dict[str, Any]:
        """Manually clones a specific monetization tactic chosen by the user."""
        res = self.run_subagent("revenue_execution_cloner", {"model_id": model_id})
        self.stats["blueprints_active"] = self._count_blueprints()
        return res

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "SCAN_BOUNTY_PLATFORMS",
                "label": "Scan Open Bounties (Algora / Gitcoin)",
                "type": "boolean",
                "default": True,
                "description": "Continuously scan open-source repositories for paid bounties"
            },
            {
                "key": "TRACK_COMPETITOR_MODELS",
                "label": "Audit Competitor AI Agent Monetization",
                "type": "boolean",
                "default": True,
                "description": "Reverse engineer pricing and monetization models of Devin, AutoGPT, and Lindy"
            },
            {
                "key": "AUTO_CLONE_TOP_TACTIC",
                "label": "Auto-Clone Top Tactics into Blueprints",
                "type": "boolean",
                "default": True,
                "description": "Generate immediate Nexus pitch funnels for the fastest-cash opportunities"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Update", file_used="growth_hacker/agent.py", message="Growth Hacker parameters updated", level="SUCCESS")
        return True

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Competitor Models Audited", "value": self.stats["models_scouted"], "color": "blue"},
            {"title": "Open Bounties Tracked", "value": self.stats["bounties_tracked"], "color": "green"},
            {"title": "Active Revenue Blueprints", "value": self.stats["blueprints_active"], "color": "yellow"}
        ]
