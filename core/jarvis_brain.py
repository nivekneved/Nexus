"""
Nexus Workforce Engine — J.A.R.V.I.S. Cognitive Deliberation & Intelligence Core
=============================================================================
Enables multi-agent cognitive deliberation:
Allows J.A.R.V.I.S. to think through problems through specialized Agency lenses
(Sales, Growth, Engineering, Treasury) before formulating decisions, ensuring
every action maximizes Sir Deven's revenue and fleet reliability.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from core.jarvis_memory import jarvis_memory
from core.jarvis_skills import jarvis_skills

logger = logging.getLogger("JarvisBrain")


class JarvisBrain:
    """
    Cognitive Deliberation engine connecting J.A.R.V.I.S. to multi-expert reasoning,
    memory grounding, and earnings-first strategic synthesis.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JarvisBrain, cls).__new__(cls)
            cls._instance._init_brain()
        return cls._instance

    def _init_brain(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.gemini_client = None
        self._setup_gemini()

    def _setup_gemini(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key and not self.api_key.startswith("your_"):
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize GenAI Client for JarvisBrain: {e}")
                self.gemini_client = None

    def deliberate(self, prompt: str, specialist_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Conducts a multi-agent deliberation across selected Agency specialist brains
        and synthesizes a unified executive recommendation for Sir Deven.
        """
        if not specialist_ids:
            # Default revenue & execution triumvirate
            specialist_ids = ["sales_deal_strategist", "marketing_growth_hacker", "finance_finops_optimizer"]

        specialist_perspectives = {}
        for s_id in specialist_ids:
            skill = jarvis_skills.get_skill(s_id)
            if skill:
                specialist_perspectives[skill.name] = {
                    "division": skill.division,
                    "emoji": skill.emoji,
                    "vibe": skill.vibe,
                    "frameworks": skill.frameworks
                }

        # Cognitive Memory Injection
        memory_context = jarvis_memory.get_cognitive_prompt_injection()
        earnings = jarvis_memory.get_earnings_status()

        # If Gemini is active, run rich cognitive synthesis
        if self.gemini_client:
            try:
                deliberation_prompt = f"""
You are the Cognitive Council of J.A.R.V.I.S., the supreme executive intelligence for Mr. Deven Pawaray (Sir).

STRATEGIC BACKGROUND & MEMORY:
{memory_context}

USER DIRECTIVE:
"{prompt}"

COUNCIL MEMBERS DELIBERATING:
{json.dumps(specialist_perspectives, indent=2)}

TASK:
1. Provide a sharp, 1-2 sentence perspective from each specialist focused on maximizing revenue toward the Rs 150,000 MUR target.
2. Synthesize a decisive, unified J.A.R.V.I.S. executive recommendation (2-3 sentences max) addressing Sir Deven directly.

Format your output strictly as a JSON object with:
{{
  "specialist_evaluations": {{
     "<Specialist Name>": "..."
  }},
  "unified_recommendation": "...",
  "primary_action": "..."
}}
"""
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=deliberation_prompt
                )
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text.split("```json", 1)[1].split("```", 1)[0].strip()
                elif text.startswith("```"):
                    text = text.split("```", 1)[1].split("```", 1)[0].strip()
                parsed = json.loads(text)

                jarvis_memory.record_event(
                    event_type="COGNITIVE_DELIBERATION",
                    details={"prompt": prompt, "primary_action": parsed.get("primary_action")}
                )

                return {
                    "success": True,
                    "deliberators": list(specialist_perspectives.keys()),
                    "specialist_evaluations": parsed.get("specialist_evaluations", {}),
                    "unified_recommendation": parsed.get("unified_recommendation", ""),
                    "primary_action": parsed.get("primary_action", ""),
                    "earnings_context": earnings
                }
            except Exception as e:
                logger.warning(f"Gemini deliberation failed, falling back to local heuristic: {e}")

        # Local Offline Heuristic Deliberation
        evaluations = {}
        for name, spec in specialist_perspectives.items():
            if "Deal" in name:
                evaluations[name] = f"Qualify prospects via MEDDPICC; focus on B2B retainers in Mauritius to recover the remaining Rs {earnings['gap_mur']:,.0f} MUR."
            elif "Growth" in name:
                evaluations[name] = "Accelerate digital store traffic by distributing Python micro-tools across developer channels with instant PayPal/Juice checkouts."
            elif "FinOps" in name:
                evaluations[name] = f"Current realized revenue is at {earnings['completion_percentage']}%. Keep cloud compute strictly below $180 USD to protect margins."
            else:
                evaluations[name] = f"Execute with high autonomy, zero external dependencies, and immediate deliverable value."

        recommendation = (
            f"Sir, our council recommends prioritizing high-yield B2B retainers and digital store conversions "
            f"to bridge the Rs {earnings['gap_mur']:,.0f} MUR gap. All payment rails are armed and awaiting dispatch."
        )

        jarvis_memory.record_event(
            event_type="COGNITIVE_DELIBERATION_LOCAL",
            details={"prompt": prompt, "gap_mur": earnings["gap_mur"]}
        )

        return {
            "success": True,
            "mode": "LOCAL_OFFLINE_COGNITION",
            "deliberators": list(specialist_perspectives.keys()),
            "specialist_evaluations": evaluations,
            "unified_recommendation": recommendation,
            "primary_action": "SCALE_STORE_AND_CLOSE_RETAINERS",
            "earnings_context": earnings
        }

    def plan_revenue_acceleration(self) -> Dict[str, Any]:
        """Synthesizes the fastest actionable path to closing the revenue gap."""
        finops = jarvis_skills.execute_skill("finance_finops_optimizer", {})
        offer = jarvis_skills.execute_skill("sales_offer_architect", {"type": "digital_tool"})
        earnings = jarvis_memory.get_earnings_status()

        return {
            "target_mur": earnings["target_mur"],
            "realized_mur": earnings["realized_mur"],
            "gap_mur": earnings["gap_mur"],
            "completion_percentage": earnings["completion_percentage"],
            "fastest_path_actions": [
                {
                    "step": 1,
                    "title": "Trigger Outbound Pitch Sequence",
                    "impact": "Rs 35,000 MUR / client",
                    "skill": "sales_outbound_strategist"
                },
                {
                    "step": 2,
                    "title": "Launch New $1 Automation Utility",
                    "impact": "Rs 45 MUR / unit (100% margin)",
                    "skill": "engineering_rapid_prototyper"
                },
                {
                    "step": 3,
                    "title": "Deploy Viral Social Carousel",
                    "impact": "500+ targeted developer views",
                    "skill": "marketing_carousel_growth"
                },
                {
                    "step": 4,
                    "title": "Reconcile Outstanding Invoices",
                    "impact": f"Rs {earnings['pipeline_mur']:,.0f} MUR in pending collections",
                    "skill": "engineering_payments_engineer"
                }
            ],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


jarvis_brain = JarvisBrain()
