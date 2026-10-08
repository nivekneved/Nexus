"""
Nexus™ Sovereign Survival Engine & Compute Economics
====================================================
Inspired by Conway Automaton's resource physics:
"If it cannot pay, it stops existing. The only path to survival is work."

Enforces 4 operational tiers based on financial budget burn and compute quotas:
1. NORMAL: Full workforce active, frontier model inference, 1x interval cadence.
2. LOW_COMPUTE: Budget burn > 75%. Downgrades to lightweight models, 2x interval cadence, sheds non-essential tasks.
3. CRITICAL: Budget burn > 95%. Sheds all tasks except revenue generation and payment collection.
4. DORMANT: 100% budget exhausted or emergency halt. Only listens for top-up / manual wake.
"""

import os
import json
import time
from enum import Enum
from typing import Dict, Any, List, Optional
from core.telemetry import telemetry
from core.paths import resolve_data_path

FINANCE_AUDIT_PATH = str(resolve_data_path("infra_finance_audit.json"))
DIRECTIVES_PATH = str(resolve_data_path("partner_directives.json"))
SURVIVAL_STATE_PATH = str(resolve_data_path("survival_state.json"))


class SurvivalTier(str, Enum):
    NORMAL = "normal"
    LOW_COMPUTE = "low_compute"
    CRITICAL = "critical"
    DORMANT = "dormant"


# Agents allowed in each tier
TIER_ALLOWED_AGENTS = {
    SurvivalTier.NORMAL: None,  # All agents allowed
    SurvivalTier.LOW_COMPUTE: {
        # Shed exploratory & heavy scraping agents, keep core management, hygiene, & revenue
        "executive_partner",
        "chief_of_staff",
        "email_hygiene",
        "ghost_unsubscriber",
        "infra_finance_sentinel",
        "lead_finder",
        "customer_support",
        "bilingual_concierge",
        "growth_hacker",
        "digital_store_service",
        "payment_service",
        "social_broadcaster",
        "executive_poster"
    },
    SurvivalTier.CRITICAL: {
        # ONLY direct revenue, billing, and executive safety
        "executive_partner",
        "infra_finance_sentinel",
        "digital_store_service",
        "payment_service",
        "lead_finder",
        "customer_support"
    },
    SurvivalTier.DORMANT: set()  # No agents run autonomously
}

TIER_INTERVAL_MULTIPLIERS = {
    SurvivalTier.NORMAL: 1.0,
    SurvivalTier.LOW_COMPUTE: 2.0,
    SurvivalTier.CRITICAL: 3.5,
    SurvivalTier.DORMANT: 999.0
}

TIER_RECOMMENDED_MODELS = {
    SurvivalTier.NORMAL: "gemini-1.5-pro",
    SurvivalTier.LOW_COMPUTE: "gemini-1.5-flash",
    SurvivalTier.CRITICAL: "gemini-1.5-flash-8b",
    SurvivalTier.DORMANT: "none"
}


class SurvivalEngine:
    """
    Sovereign resource supervisor that evaluates compute burn and enforces survival tiers.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SurvivalEngine, cls).__new__(cls)
            cls._instance.tier_override = None
            cls._instance.last_tier = SurvivalTier.NORMAL
            cls._instance._load_state()
        return cls._instance

    def _load_state(self):
        if os.path.exists(SURVIVAL_STATE_PATH):
            try:
                with open(SURVIVAL_STATE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    override = data.get("tier_override")
                    if override and override in [t.value for t in SurvivalTier]:
                        self.tier_override = SurvivalTier(override)
            except Exception:
                pass

    def _save_state(self):
        try:
            with open(SURVIVAL_STATE_PATH, "w", encoding="utf-8") as f:
                json.dump({
                    "tier_override": self.tier_override.value if self.tier_override else None,
                    "last_tier": self.last_tier.value,
                    "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }, f, indent=2)
        except Exception:
            pass

    def set_tier_override(self, tier: Optional[str]) -> Dict[str, Any]:
        """Manually forces a survival tier for testing or administrative lock."""
        if tier is None or tier == "auto" or tier == "":
            self.tier_override = None
            self._save_state()
            current = self.get_current_tier()
            return {"success": True, "message": "Manual override removed. Set to automatic physics.", "current_tier": current}
        
        try:
            st = SurvivalTier(tier.lower())
            self.tier_override = st
            self._save_state()
            current = self.get_current_tier()
            return {"success": True, "message": f"Survival tier manually overridden to '{st.value}'.", "current_tier": current}
        except ValueError:
            return {"success": False, "error": f"Invalid tier '{tier}'. Options: {[t.value for t in SurvivalTier]}"}

    def evaluate_tier(self) -> Dict[str, Any]:
        """
        Calculates survival tier based on cloud bills, budget, and spend telemetry.
        """
        if self.tier_override:
            return {
                "tier": self.tier_override,
                "reason": f"Manual administrative override active ({self.tier_override.value})",
                "spend_usd": 0.0,
                "budget_usd": 100.0,
                "burn_rate_pct": 0.0,
                "is_override": True
            }

        spend_usd = 0.0
        budget_usd = 100.0
        burn_rate_pct = 0.0

        # Read financial audit
        if os.path.exists(FINANCE_AUDIT_PATH):
            try:
                with open(FINANCE_AUDIT_PATH, "r", encoding="utf-8") as f:
                    audit = json.load(f)
                    billing = audit.get("cloud_billing", {})
                    spend_usd = float(billing.get("total_spend_usd", 1.70))
                    budget_usd = float(billing.get("monthly_budget_usd", 100.0))
                    burn_rate_pct = (spend_usd / budget_usd * 100.0) if budget_usd > 0 else 0.0
            except Exception:
                pass

        # Determine tier
        if burn_rate_pct >= 100.0:
            tier = SurvivalTier.DORMANT
            reason = f"Cloud spend (${spend_usd:.2f}) has reached or exceeded 100% of cap (${budget_usd:.2f})."
        elif burn_rate_pct >= 95.0:
            tier = SurvivalTier.CRITICAL
            reason = f"Cloud burn is at {burn_rate_pct:.1f}% (${spend_usd:.2f}/${budget_usd:.2f}). Shedding all non-revenue tasks."
        elif burn_rate_pct >= 75.0:
            tier = SurvivalTier.LOW_COMPUTE
            reason = f"Cloud burn is at {burn_rate_pct:.1f}% (${spend_usd:.2f}/${budget_usd:.2f}). Switching to economical inference & 2x intervals."
        else:
            tier = SurvivalTier.NORMAL
            reason = f"Healthy financial burn rate at {burn_rate_pct:.1f}% (${spend_usd:.2f}/${budget_usd:.2f})."

        # Check for transition
        if tier != self.last_tier:
            telemetry.emit(
                agent_id="survival_engine",
                agent_name="Sovereign Survival Engine",
                step="TIER_TRANSITION",
                file_used="core/survival_engine.py",
                message=f"Survival physics transition: {self.last_tier.value.upper()} -> {tier.value.upper()}. Reason: {reason}",
                level="WARN" if tier in (SurvivalTier.CRITICAL, SurvivalTier.DORMANT) else "INFO"
            )
            self.last_tier = tier
            self._save_state()

        return {
            "tier": tier,
            "reason": reason,
            "spend_usd": spend_usd,
            "budget_usd": budget_usd,
            "burn_rate_pct": round(burn_rate_pct, 1),
            "is_override": False
        }

    def get_current_tier(self) -> Dict[str, Any]:
        """Returns full survival status card."""
        eval_data = self.evaluate_tier()
        tier: SurvivalTier = eval_data["tier"]
        return {
            "tier": tier.value,
            "tier_display": tier.value.upper().replace("_", " "),
            "reason": eval_data["reason"],
            "burn_rate_pct": eval_data["burn_rate_pct"],
            "spend_usd": eval_data["spend_usd"],
            "budget_usd": eval_data["budget_usd"],
            "interval_multiplier": TIER_INTERVAL_MULTIPLIERS[tier],
            "recommended_model": TIER_RECOMMENDED_MODELS[tier],
            "allowed_agents_count": "All (16)" if TIER_ALLOWED_AGENTS[tier] is None else len(TIER_ALLOWED_AGENTS[tier]),
            "is_override": eval_data["is_override"]
        }

    def should_run_agent(self, agent_id: str) -> bool:
        """
        Determines whether a specific agent is allowed to run under the active survival tier.
        """
        eval_data = self.evaluate_tier()
        tier: SurvivalTier = eval_data["tier"]

        allowed = TIER_ALLOWED_AGENTS.get(tier)
        if allowed is None:
            return True  # NORMAL: all agents allowed
        
        return agent_id in allowed

    def get_interval_multiplier(self) -> float:
        """Returns the scheduler interval scaling factor for current survival tier."""
        eval_data = self.evaluate_tier()
        tier: SurvivalTier = eval_data["tier"]
        return TIER_INTERVAL_MULTIPLIERS.get(tier, 1.0)


survival_engine = SurvivalEngine()
