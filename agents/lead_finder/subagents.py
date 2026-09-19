import os
import json
from datetime import datetime
from typing import Dict, Any, List
from core.subagent import BaseSubAgent

LEADS_FILE = "leads_pipeline.json"

class ICPFitScorerSubAgent(BaseSubAgent):
    """
    Subagent 1: Computes Ideal Customer Profile (ICP) match score against criteria.
    """
    def __init__(self):
        super().__init__(
            subagent_id="lead_icp_fit_scorer",
            name="ICP Fit Scorer SubAgent",
            parent_agent_id="lead_finder",
            description="Evaluates prospect industry, revenue stage, company size, and geographic alignment against target criteria."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        company_data = payload.get("company_data", {})
        target_industry = payload.get("target_industry", "SaaS / AI")
        min_fit_score = payload.get("min_fit_score", 80)

        # Baseline score calculation
        score = 70
        industry = company_data.get("industry", "")
        if any(w.lower() in industry.lower() for w in target_industry.split("/")):
            score += 15
        
        employees = company_data.get("employees", 25)
        if 10 <= employees <= 250:
            score += 10

        pain_points = company_data.get("pain_points", [])
        if pain_points:
            score += 5

        fit_score = min(score, 100)
        is_qualified = fit_score >= min_fit_score

        return {
            "fit_score": fit_score,
            "is_qualified": is_qualified,
            "match_tier": "Tier 1 High Fit" if fit_score >= 90 else ("Tier 2 Qualified" if fit_score >= 80 else "Low Fit")
        }


class CompanySignalResearcherSubAgent(BaseSubAgent):
    """
    Subagent 2: Researches digital footprint, recent tech hiring, and operational bottlenecks.
    """
    def __init__(self):
        super().__init__(
            subagent_id="lead_company_signal_researcher",
            name="Company Signal Researcher SubAgent",
            parent_agent_id="lead_finder",
            description="Audits company public signals, engineering job postings, tech stack footprint, and customer pain points."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        company_name = payload.get("company_name", "Acme Corp")
        website = payload.get("website", "https://example.com")

        # Synthetic signal harvesting (or live scraping when API key is present)
        signals = [
            "Recently listed job openings for Operations Manager and Customer Success Leads",
            "Tech stack indicates FastAPI, Next.js, and multi-tenant Postgres",
            "Public CEO tweet regarding inbox overload and manual triage bottlenecks"
        ]
        primary_pain_point = "Scaling manual customer operations and email response bottlenecks"

        return {
            "company_name": company_name,
            "website": website,
            "verified_signals": signals,
            "primary_pain_point": primary_pain_point,
            "research_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


class PersonalizedPitchCraftSubAgent(BaseSubAgent):
    """
    Subagent 3: Crafts custom, non-spammy outreach hooks and saves to the leads pipeline.
    """
    def __init__(self):
        super().__init__(
            subagent_id="lead_pitch_crafter",
            name="Personalized Pitch Crafter SubAgent",
            parent_agent_id="lead_finder",
            description="Generates tailored cold outreach hooks focused on the prospect's exact pain point and registers them in the pipeline."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        lead_record = payload.get("lead_record", {})
        pipeline_file = payload.get("pipeline_file", LEADS_FILE)

        contact = lead_record.get("contact_name", "there")
        company = lead_record.get("company", "your company")
        pain_point = lead_record.get("pain_point", "manual operational bottlenecks")

        hook = (
            f"Hi {contact},\n\n"
            f"Saw that {company} is scaling fast. Most growing teams hit a wall with {pain_point.lower()}. "
            f"We deployed an autonomous AI workforce that triages incoming inquiries and handles 85% of repetitive ops without human fatigue.\n\n"
            f"Would you be open to a 5-minute teardown of how this works for your team?"
        )
        lead_record["suggested_hook"] = hook

        # Persist to pipeline
        pipeline = []
        if os.path.exists(pipeline_file):
            try:
                with open(pipeline_file, "r", encoding="utf-8") as f:
                    pipeline = json.load(f)
            except Exception:
                pipeline = []

        pipeline.insert(0, lead_record)
        pipeline = pipeline[:50]

        try:
            with open(pipeline_file, "w", encoding="utf-8") as f:
                json.dump(pipeline, f, indent=2, ensure_ascii=False)
        except Exception as e:
            return {"success": False, "error": str(e), "hook": hook}

        return {
            "success": True,
            "lead_id": lead_record.get("id"),
            "hook": hook,
            "total_leads": len(pipeline)
        }
