"""
Nexus™ Sovereign Crypto Verifier & Spending Guardrails
=====================================================
Directly inspired by nxs-agents/nexus-protocol's on-chain verifier & policy runtime.
Protects Nexus's wallet from runaway spending, unauthorized drains, or malicious calls.
Enforces per-transaction limits, daily rolling budget caps, and address validation.
"""

import os
import json
import time
from typing import Dict, Any, Tuple
from core.telemetry import telemetry

from core.paths import resolve_data_path

VERIFIER_STATE_PATH = str(resolve_data_path("crypto_spend_history.json"))

# Defaults (can be overridden via .env)
DEFAULT_MAX_SINGLE_TX_USD = 15.00
DEFAULT_DAILY_LIMIT_USD = 50.00
ONE_DAY_SECONDS = 86400


class CryptoVerifier:
    """
    Autonomous Policy Verifier.
    Acts as the on-chain pre-flight gatekeeper before any cryptographic signature is issued.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CryptoVerifier, cls).__new__(cls)
            cls._instance.state_path = VERIFIER_STATE_PATH
            cls._instance._ensure_state()
        return cls._instance

    def _ensure_state(self):
        if not os.path.exists(self.state_path):
            initial_data = {
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_historical_spend_usd": 0.0,
                "history": []
            }
            try:
                with open(self.state_path, "w", encoding="utf-8") as f:
                    json.dump(initial_data, f, indent=2)
            except Exception:
                pass

    def get_limits(self) -> Dict[str, float]:
        """Reads spending limits configured in environment."""
        try:
            max_single = float(os.getenv("NEXUS_WALLET_MAX_SINGLE_TX_USD", str(DEFAULT_MAX_SINGLE_TX_USD)))
        except ValueError:
            max_single = DEFAULT_MAX_SINGLE_TX_USD

        try:
            daily_limit = float(os.getenv("NEXUS_WALLET_DAILY_LIMIT_USD", str(DEFAULT_DAILY_LIMIT_USD)))
        except ValueError:
            daily_limit = DEFAULT_DAILY_LIMIT_USD

        return {
            "max_single_tx_usd": max_single,
            "daily_limit_usd": daily_limit
        }

    def _load_history(self) -> Dict[str, Any]:
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"created_at": time.strftime("%Y-%m-%d %H:%M:%S"), "total_historical_spend_usd": 0.0, "history": []}

    def _save_history(self, data: Dict[str, Any]):
        try:
            temp_path = f"{self.state_path}.tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_path, self.state_path)
        except Exception:
            pass

    def get_rolling_24h_spend(self) -> float:
        """Calculates total USD/USDC spent in the last 24 hours."""
        data = self._load_history()
        now = time.time()
        rolling_total = 0.0
        for entry in data.get("history", []):
            if now - entry.get("timestamp", 0) <= ONE_DAY_SECONDS:
                rolling_total += entry.get("amount_usd", 0.0)
        return round(rolling_total, 2)

    def verify_spend(self, amount_usd: float, recipient: str, reason: str = "") -> Tuple[bool, str]:
        """
        Evaluates policy constraints against an autonomous spend request.
        Returns:
            (is_allowed: bool, justification: str)
        """
        # 1. Amount validation
        if amount_usd <= 0:
            return False, "Amount must be strictly positive."

        # 2. Address validation
        recipient_clean = recipient.strip()
        if not recipient_clean.startswith("0x") or len(recipient_clean) != 42:
            return False, f"Invalid EVM recipient address '{recipient}'. Must be 42 characters starting with 0x."
        if recipient_clean.lower() == "0x" + "0" * 40:
            return False, "Transactions to the zero address (burn address) are blocked by guardrails."

        # 3. Single-transaction ceiling check
        limits = self.get_limits()
        if amount_usd > limits["max_single_tx_usd"]:
            msg = (
                f"Policy Violation: Spend of ${amount_usd:.2f} USDC exceeds single-transaction ceiling "
                f"of ${limits['max_single_tx_usd']:.2f}. Requires explicit Partner Sign-off."
            )
            telemetry.emit(
                agent_id="crypto_verifier",
                agent_name="Policy Verifier",
                step="SPEND_REJECTED",
                file_used="core/crypto_verifier.py",
                message=msg,
                level="WARNING"
            )
            return False, msg

        # 4. 24-Hour rolling budget check
        current_24h = self.get_rolling_24h_spend()
        projected_24h = current_24h + amount_usd
        if projected_24h > limits["daily_limit_usd"]:
            msg = (
                f"Policy Violation: Spend of ${amount_usd:.2f} USDC would push 24h spend to ${projected_24h:.2f}, "
                f"exceeding daily limit of ${limits['daily_limit_usd']:.2f} (current: ${current_24h:.2f})."
            )
            telemetry.emit(
                agent_id="crypto_verifier",
                agent_name="Policy Verifier",
                step="SPEND_REJECTED",
                file_used="core/crypto_verifier.py",
                message=msg,
                level="WARNING"
            )
            return False, msg

        # Verification Passed
        return True, "Verified: within per-tx ceiling and rolling 24h quota."

    def record_spend(self, tx_hash: str, amount_usd: float, recipient: str, reason: str = ""):
        """Records an authorized spend into the historical verifier ledger."""
        data = self._load_history()
        now = time.time()
        entry = {
            "timestamp": now,
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)),
            "tx_hash": tx_hash,
            "amount_usd": round(amount_usd, 2),
            "recipient": recipient,
            "reason": reason
        }
        data.setdefault("history", []).append(entry)
        data["total_historical_spend_usd"] = round(data.get("total_historical_spend_usd", 0.0) + amount_usd, 2)
        self._save_history(data)

        telemetry.emit(
            agent_id="crypto_verifier",
            agent_name="Policy Verifier",
            step="SPEND_COMMITTED",
            file_used="core/crypto_verifier.py",
            message=f"Recorded spend of ${amount_usd:.2f} USDC to {recipient[:10]}... Reason: {reason or 'None'}",
            level="INFO"
        )

    def get_summary(self) -> Dict[str, Any]:
        """Returns full policy and budget telemetry."""
        limits = self.get_limits()
        spent_24h = self.get_rolling_24h_spend()
        remaining_24h = max(0.0, round(limits["daily_limit_usd"] - spent_24h, 2))
        data = self._load_history()

        return {
            "status": "ARMED_AND_ENFORCING",
            "limits": limits,
            "spent_last_24h_usd": spent_24h,
            "remaining_daily_budget_usd": remaining_24h,
            "total_historical_spend_usd": data.get("total_historical_spend_usd", 0.0),
            "total_authorized_transactions": len(data.get("history", []))
        }


crypto_verifier = CryptoVerifier()
