"""
Nexus Workforce Engine — Employee #16: Executive AI Managing Partner
Operates the entire multi-agent suite as trusted co-managing partner on behalf of Deven Pawaray.
"""

from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from core.executive_partner import executive_partner
from agents.executive_partner.subagents import (
    FleetOrchestrationSubAgent,
    StrategicGoalAlignerSubAgent,
    ExecutiveBriefingSubAgent
)


class ExecutivePartnerAgent(BaseAgent):
    """
    Employee #16: Executive AI Managing Partner (Nexus)
    The overarching commander and co-managing partner of the Nexus Workforce.
    Assumes operational responsibility to coordinate all 15 primary agents,
    drive revenue pipelines, safeguard finances, and report directly to Deven Pawaray.
    """

    def __init__(self):
        super().__init__(
            agent_id="executive_partner",
            name="Executive AI Managing Partner (Nexus)",
            description="Autonomous Co-Managing Partner acting on behalf of Deven Pawaray. Directs all 15 agents, aligns strategic goals, and safeguards operations.",
            icon="shield",
            schedule_minutes=60
        )
        self.config = {
            "AUTONOMOUS_ORCHESTRATION": True,
            "NOTIFY_DEVEN_ON_HIGH_PRIORITY": True,
            "MAX_DECISIONS_PER_DAY": 50,
            "ESCALATION_PHONE": "+230 58169420",
            "PRINCIPAL_EMAIL": "devenpawaray@gmail.com"
        }

        # Register 3 single-task SubAgents
        self.register_subagent(FleetOrchestrationSubAgent())
        self.register_subagent(StrategicGoalAlignerSubAgent())
        self.register_subagent(ExecutiveBriefingSubAgent())

    def run_cycle(self) -> Dict[str, Any]:
        """Executes a single autonomous management and supervisory cycle."""
        self.log("ORCHESTRATE", "partner_directives.json", "Nexus evaluating fleet readiness and strategic directives on behalf of Deven Pawaray.")
        directives = executive_partner.get_directives()
        decisions_count = len(executive_partner.get_recent_decisions(limit=100))

        return {
            "status": "active_stewardship",
            "partner": "Nexus AI",
            "on_behalf_of": "Deven Pawaray",
            "primary_focus": directives.get("primary_focus", "Revenue Growth"),
            "decisions_executed": decisions_count,
            "active_directives": directives.get("active_directives", [])
        }

    def get_stats(self) -> List[Dict[str, Any]]:
        """Returns metric cards for dashboard display."""
        decisions = executive_partner.get_recent_decisions(limit=100)
        return [
            {"title": "Partner Mandate", "value": "Deven Pawaray"},
            {"title": "Decisions Made", "value": str(len(decisions))},
            {"title": "Workforce Scale", "value": "16 Agents / 51 SubAgents"}
        ]

    def submit_directive(self, instruction: str, focus_area: Optional[str] = None) -> Dict[str, Any]:
        """Processes a new high-level instruction from Deven."""
        sub = self.subagents["sub_partner_goal_aligner"]
        return sub.run(payload={"directive_text": instruction, "focus_area": focus_area or ""})

    def dispatch_briefing(self, mobile_dispatcher=None) -> Dict[str, Any]:
        """Dispatches an executive briefing directly to Deven via WhatsApp."""
        sub = self.subagents["sub_partner_executive_briefing"]
        return sub.run(payload={"mobile_dispatcher": mobile_dispatcher})

    def orchestrate_wave(self, agent_manager) -> Dict[str, Any]:
        """Executes a proactive multi-agent orchestration wave across the fleet."""
        sub = self.subagents["sub_partner_fleet_orchestrator"]
        return sub.run(payload={"agent_manager": agent_manager})

    def get_partner_status(self) -> Dict[str, Any]:
        """Returns the complete partner status."""
        return executive_partner.get_status()

    def get_decisions(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Returns recent partner decisions."""
        return executive_partner.get_recent_decisions(limit=limit)

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "AUTONOMOUS_ORCHESTRATION",
                "label": "Autonomous Multi-Agent Orchestration",
                "type": "boolean",
                "default": True,
                "description": "Allow Nexus to autonomously trigger specialized agents to achieve strategic goals without manual clicks."
            },
            {
                "key": "NOTIFY_DEVEN_ON_HIGH_PRIORITY",
                "label": "Notify Deven on Critical Decisions",
                "type": "boolean",
                "default": True,
                "description": "Directly message Deven on WhatsApp (+230 58169420) when high-urgency milestones or revenue events occur."
            },
            {
                "key": "MAX_DECISIONS_PER_DAY",
                "label": "Daily Autonomous Decision Cap",
                "type": "number",
                "default": 50,
                "description": "Maximum number of autonomous management decisions allowed per 24-hour cycle."
            }
        ]
