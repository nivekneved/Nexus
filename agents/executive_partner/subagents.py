"""
Nexus Workforce Engine — Executive AI Partner SubAgents
Specialized subagents for autonomous fleet orchestration, strategic goal alignment,
and high-level executive briefing creation on behalf of Deven Pawaray.
"""

from typing import Dict, Any
from core.subagent import BaseSubAgent
from core.executive_partner import executive_partner


class FleetOrchestrationSubAgent(BaseSubAgent):
    """
    SubAgent 1: Autonomous Multi-Agent Fleet Orchestrator.
    Evaluates business context and autonomously issues coordinated commands across the workforce.
    """
    def __init__(self):
        super().__init__(
            subagent_id="sub_partner_fleet_orchestrator",
            name="Multi-Agent Fleet Orchestrator",
            parent_agent_id="executive_partner",
            description="Coordinates cross-agent task sequences across sales, security, inbox, and finances on behalf of Deven."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        agent_manager = payload.get("agent_manager")
        res = executive_partner.orchestrate_workforce_wave(agent_manager)
        return {
            "status": "orchestrated",
            "actions_executed": res.get("actions_executed", []),
            "decision_id": res.get("decision", {}).get("decision_id")
        }


class StrategicGoalAlignerSubAgent(BaseSubAgent):
    """
    SubAgent 2: Strategic Goal Aligner.
    Translates high-level natural language instructions from Deven into concrete agent directives.
    """
    def __init__(self):
        super().__init__(
            subagent_id="sub_partner_goal_aligner",
            name="Strategic Goal Aligner",
            parent_agent_id="executive_partner",
            description="Translates Deven's overarching goals into immediate operational priorities for the 15 specialized agents."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        directive_text = payload.get("directive_text", "")
        focus_area = payload.get("focus_area", "")

        if not directive_text:
            return {"status": "no_directive_provided", "directives": executive_partner.get_directives()}
        res = executive_partner.update_directive(directive_text, focus_area)
        return {
            "status": "aligned",
            "active_directives": res.get("directives", {}).get("active_directives", []),
            "decision": res.get("decision")
        }


class ExecutiveBriefingSubAgent(BaseSubAgent):
    """
    SubAgent 3: Executive Briefing & Direct Dispatcher.
    Drafts concise co-founder updates and dispatches them to Deven's WhatsApp and Email.
    """
    def __init__(self):
        super().__init__(
            subagent_id="sub_partner_executive_briefing",
            name="Executive Briefing & Direct Dispatcher",
            parent_agent_id="executive_partner",
            description="Synthesizes business achievements, revenue inflows, and decisions into executive briefings for Deven (+230 58169420)."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        briefing_text = executive_partner.craft_partner_briefing()
        dispatched = False
        dispatch_res = None
        mobile_dispatcher = payload.get("mobile_dispatcher")

        if mobile_dispatcher and hasattr(mobile_dispatcher, "send_notification"):
            try:
                dispatch_res = mobile_dispatcher.send_notification(
                    title="🤝 Nexus Executive Partner Update",
                    message=briefing_text,
                    urgency="P1"
                )
                dispatched = True
            except Exception as e:
                dispatch_res = {"error": str(e)}

        return {
            "status": "drafted",
            "briefing": briefing_text,
            "dispatched_to_deven": dispatched,
            "dispatch_details": dispatch_res
        }
