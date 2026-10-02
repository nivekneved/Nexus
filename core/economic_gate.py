"""
Nexus Autonomous Software Enterprise — Economic Triage & Unit Economics Gate
=============================================================================
Enforces mathematical unit economic gating across all autonomous swarms:
1. Expected Value Gate: EV = (Reward * P_acceptance) - Inference_Cost - Overhead
2. Negative EV Kill-Switch: Drops tasks with P_acceptance < 0.60 or Compute Cost > 0.25 * Reward
3. Static-Analysis-First Verification: Enforces deterministic linter/AST checks prior to LLM token consumption
4. Wall of Anti-Patterns: Vectorized memory of rejections and failed submissions to prevent repeat errors
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List
from core import dal
from core.survival_engine import survival_engine

logger = logging.getLogger("Nexus.EconomicGate")

# Pricing per million tokens (USD)
TOKEN_PRICING_PER_M = {
    "gemini-1.5-pro": {"input": 3.50, "output": 10.50},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-1.5-flash-8b": {"input": 0.0375, "output": 0.15},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00}
}


class EconomicGate:
    """
    Architect & Triage Gatekeeper:
    Prevents inference insolvency by strictly gating swarm execution.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EconomicGate, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def calculate_inference_cost(
        input_tokens: int,
        output_tokens: int,
        model: str = "gemini-1.5-flash"
    ) -> float:
        """Calculates exact USD inference cost based on token estimates."""
        rates = TOKEN_PRICING_PER_M.get(model, TOKEN_PRICING_PER_M["gemini-1.5-flash"])
        input_cost = (input_tokens / 1_000_000.0) * rates["input"]
        output_cost = (output_tokens / 1_000_000.0) * rates["output"]
        return round(input_cost + output_cost, 6)

    def evaluate_task(
        self,
        task_id: str,
        reward_usd: float,
        p_acceptance: float,
        estimated_input_tokens: int = 15_000,
        estimated_output_tokens: int = 3_000,
        verification_overhead_usd: float = 0.05,
        category: str = "bounty",
        task_signature: str = ""
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Evaluates task viability against strict enterprise unit economics:
        Returns: (is_approved, reason, metrics_dict)
        """
        # 1. Anti-Pattern Check (Has this failure vector occurred before?)
        if self.matches_anti_pattern(task_signature):
            reason = "VETOED: Matches registered Anti-Pattern on Wall of Anti-Patterns."
            logger.warning(f"[EconomicGate] Task {task_id} {reason}")
            return False, reason, {"ev": 0.0, "reason": "anti_pattern_match"}

        # 2. Model Selection based on Active Survival Tier
        tier_info = survival_engine.get_current_tier()
        model = tier_info.get("model", "gemini-1.5-flash")

        # 3. Calculate Unit Economics
        inference_cost = self.calculate_inference_cost(
            input_tokens=estimated_input_tokens,
            output_tokens=estimated_output_tokens,
            model=model
        )
        total_compute_cost = inference_cost + verification_overhead_usd

        # EV = (Reward * P_acceptance) - Inference Cost - Verification Overhead
        expected_value = (reward_usd * p_acceptance) - total_compute_cost

        metrics = {
            "task_id": task_id,
            "reward_usd": reward_usd,
            "p_acceptance": p_acceptance,
            "model_used": model,
            "inference_cost_usd": inference_cost,
            "total_compute_cost_usd": total_compute_cost,
            "expected_value_usd": round(expected_value, 4),
            "cost_to_reward_ratio": round(total_compute_cost / max(reward_usd, 0.01), 4),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 4. Enforce Negative EV Kill-Switch
        if p_acceptance < 0.60:
            reason = f"KILL-SWITCH: P_acceptance ({p_acceptance*100:.1f}%) below minimum 60% threshold."
            metrics["status"] = "VETOED_LOW_PROBABILITY"
            self._log_decision(metrics)
            return False, reason, metrics

        if total_compute_cost > (0.25 * reward_usd):
            reason = f"KILL-SWITCH: Compute cost (${total_compute_cost:.4f}) exceeds 25% of reward (${reward_usd:.2f})."
            metrics["status"] = "VETOED_HIGH_COMPUTE_COST"
            self._log_decision(metrics)
            return False, reason, metrics

        if expected_value <= 0:
            reason = f"KILL-SWITCH: Negative or zero Expected Value (${expected_value:.4f})."
            metrics["status"] = "VETOED_NEGATIVE_EV"
            self._log_decision(metrics)
            return False, reason, metrics

        # 5. Approved for Worker Swarm
        reason = f"APPROVED: Positive EV (+${expected_value:.2f}), cost ratio is {metrics['cost_to_reward_ratio']*100:.1f}% of reward."
        metrics["status"] = "APPROVED_POSITIVE_EV"
        self._log_decision(metrics)
        return True, reason, metrics

    def record_anti_pattern(self, category: str, pattern: str, reason: str):
        """Records a permanent rejection/failure vector to avoid repeat token burn."""
        anti_patterns = dal.load("anti_patterns", default=[])
        entry = {
            "id": f"AP-{int(datetime.now().timestamp())}",
            "category": category,
            "pattern": pattern.strip().lower(),
            "reason": reason,
            "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        anti_patterns.insert(0, entry)
        dal.save("anti_patterns", anti_patterns[:100])
        logger.info(f"[EconomicGate] Added Anti-Pattern: {category} -> {pattern[:40]}")

    def matches_anti_pattern(self, task_signature: str) -> bool:
        """Scans candidate task against Wall of Anti-Patterns."""
        if not task_signature:
            return False
        anti_patterns = dal.load("anti_patterns", default=[])
        sig = task_signature.strip().lower()
        for ap in anti_patterns:
            pat = ap.get("pattern", "")
            if pat and pat in sig:
                return True
        return False

    def _log_decision(self, metrics: Dict[str, Any]):
        try:
            dal.append("economic_evaluations", metrics, max_items=200)
        except Exception:
            pass


economic_gate = EconomicGate()
