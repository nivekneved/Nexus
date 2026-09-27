"""
Nexus™ Durable Heartbeat Daemon & Tick Context Engine
=====================================================
Inspired by Conway Automaton's DurableScheduler and Heartbeat Daemon:
"Between turns, a heartbeat daemon runs scheduled tasks — health checks, credit
monitoring, status pings — even while the agent loop sleeps."

Constructs a structured TickContext on every interval tick and triggers
autonomous wakes when external state changes (payments, overdue bills, inbox events).
"""

import os
import json
import time
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.telemetry import telemetry
from core.paths import resolve_data_path

HEARTBEAT_STATE_PATH = str(resolve_data_path("heartbeat_state.json"))
FINANCE_AUDIT_PATH = str(resolve_data_path("infra_finance_audit.json"))
INVOICES_PATH = str(resolve_data_path("invoices.json"))
LEADS_PATH = str(resolve_data_path("leads_pipeline.json"))


class HeartbeatDaemon:
    """
    Background daemon continuously evaluating operational environment
    and generating TickContext for the sovereign workforce.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(HeartbeatDaemon, cls).__new__(cls)
            cls._instance.is_running = False
            cls._instance.stop_event = threading.Event()
            cls._instance.thread = None
            cls._instance.tick_count = 0
            cls._instance.last_tick_context = {}
            cls._instance.tick_interval_seconds = 30
            cls._instance._load_state()
        return cls._instance

    def _load_state(self):
        if os.path.exists(HEARTBEAT_STATE_PATH):
            try:
                with open(HEARTBEAT_STATE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tick_count = data.get("total_ticks", 0)
                    self.last_tick_context = data.get("last_tick_context", {})
            except Exception:
                pass

    def _save_state(self):
        try:
            temp_path = f"{HEARTBEAT_STATE_PATH}.tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump({
                    "total_ticks": self.tick_count,
                    "last_tick_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "last_tick_context": self.last_tick_context
                }, f, indent=2, ensure_ascii=False)
            os.replace(temp_path, HEARTBEAT_STATE_PATH)
        except Exception:
            pass

    def build_tick_context(self) -> Dict[str, Any]:
        """
        Assembles real-time context across finance, leads, email, and survival tier.
        """
        from core.survival_engine import survival_engine
        tier_info = survival_engine.get_current_tier()

        overdue_invoices_count = 0
        if os.path.exists(INVOICES_PATH):
            try:
                with open(INVOICES_PATH, "r", encoding="utf-8") as f:
                    invoices = json.load(f)
                    overdue_invoices_count = sum(1 for inv in invoices if inv.get("status") == "OVERDUE")
            except Exception:
                pass

        leads_count = 0
        if os.path.exists(LEADS_PATH):
            try:
                with open(LEADS_PATH, "r", encoding="utf-8") as f:
                    leads_data = json.load(f)
                    leads_count = len(leads_data) if isinstance(leads_data, list) else len(leads_data.get("leads", []))
            except Exception:
                pass

        wake_events = []
        if overdue_invoices_count > 0:
            wake_events.append({
                "type": "OVERDUE_INVOICE",
                "severity": "HIGH",
                "target_agent": "infra_finance_sentinel",
                "description": f"{overdue_invoices_count} overdue invoice(s) need follow-up"
            })

        if tier_info["tier"] in ("critical", "dormant"):
            wake_events.append({
                "type": "SURVIVAL_ALERT",
                "severity": "CRITICAL",
                "target_agent": "executive_partner",
                "description": f"Compute budget alert: {tier_info['reason']}"
            })

        ctx = {
            "tick_id": self.tick_count + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "survival_tier": tier_info["tier"],
            "survival_reason": tier_info["reason"],
            "burn_rate_pct": tier_info["burn_rate_pct"],
            "cloud_spend_usd": tier_info["spend_usd"],
            "cloud_budget_usd": tier_info["budget_usd"],
            "overdue_invoices": overdue_invoices_count,
            "pipeline_leads": leads_count,
            "wake_events": wake_events,
            "should_wake_agent": len(wake_events) > 0
        }
        return ctx

    def tick(self) -> Dict[str, Any]:
        """Executes a single heartbeat evaluation tick."""
        self.tick_count += 1
        ctx = self.build_tick_context()
        self.last_tick_context = ctx
        self._save_state()

        # If wake events exist, selectively wake target agents
        if ctx.get("should_wake_agent"):
            for event in ctx.get("wake_events", []):
                target = event.get("target_agent")
                if target:
                    telemetry.emit(
                        agent_id="heartbeat_daemon",
                        agent_name="Heartbeat Daemon",
                        step="WAKE_EVENT_DISPATCH",
                        file_used="core/heartbeat_daemon.py",
                        message=f"Heartbeat woke agent '{target}' due to event: {event.get('description')}",
                        level="INFO"
                    )
        return ctx

    def start(self, interval_seconds: int = 30):
        """Starts the background heartbeat loop."""
        if self.is_running:
            return
        self.tick_interval_seconds = interval_seconds
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._loop, daemon=True, name="nexus-heartbeat-daemon")
        self.thread.start()
        self.is_running = True
        print(f"[HeartbeatDaemon] Started background heartbeat daemon (Tick interval: {interval_seconds}s).")

    def stop(self):
        """Stops the heartbeat loop."""
        if not self.is_running:
            return
        self.stop_event.set()
        self.is_running = False
        print("[HeartbeatDaemon] Stopped background heartbeat daemon.")

    def _loop(self):
        while not self.stop_event.is_set():
            try:
                self.tick()
            except Exception as e:
                print(f"[HeartbeatDaemon] Error in tick: {e}")
            self.stop_event.wait(self.tick_interval_seconds)

    def get_status(self) -> Dict[str, Any]:
        """Provides status of the heartbeat daemon and latest tick context."""
        return {
            "is_running": self.is_running,
            "tick_interval_seconds": self.tick_interval_seconds,
            "total_ticks": self.tick_count,
            "last_tick_context": self.last_tick_context
        }


heartbeat_daemon = HeartbeatDaemon()
