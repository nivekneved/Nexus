# -*- coding: utf-8 -*-
"""
Nexus Workforce Engine — Revenue & Conversion Engine Module
=============================================================================
Handles conversion telemetry tracking, abandoned lead recovery, and webhook dispatch.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from core.paths import resolve_data_path

REVENUE_EVENTS_FILE = resolve_data_path("revenue_events.json")
ABANDONED_LEADS_FILE = resolve_data_path("abandoned_leads.json")

class RevenueEngine:
    def __init__(self):
        self._ensure_storage()

    def _ensure_storage(self):
        for f_path in [REVENUE_EVENTS_FILE, ABANDONED_LEADS_FILE]:
            if not os.path.exists(f_path):
                try:
                    with open(f_path, "w", encoding="utf-8") as f:
                        json.dump([], f, indent=2)
                except Exception:
                    pass

    def track_event(self, event_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        event_record = {
            "event_name": event_name,
            "payload": payload,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            events = []
            if os.path.exists(REVENUE_EVENTS_FILE):
                with open(REVENUE_EVENTS_FILE, "r", encoding="utf-8") as f:
                    events = json.load(f)
            events.insert(0, event_record)
            with open(REVENUE_EVENTS_FILE, "w", encoding="utf-8") as f:
                json.dump(events[:500], f, indent=2)
            return {"success": True, "tracked": event_name}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def capture_abandoned_lead(self, contact: str, source: str, cart_details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        lead_record = {
            "contact": contact,
            "source": source,
            "cart_details": cart_details or {},
            "status": "PENDING_RECOVERY",
            "captured_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            leads = []
            if os.path.exists(ABANDONED_LEADS_FILE):
                with open(ABANDONED_LEADS_FILE, "r", encoding="utf-8") as f:
                    leads = json.load(f)
            leads.insert(0, lead_record)
            with open(ABANDONED_LEADS_FILE, "w", encoding="utf-8") as f:
                json.dump(leads[:200], f, indent=2)
            return {"success": True, "lead_captured": contact}
        except Exception as e:
            return {"success": False, "error": str(e)}

revenue_engine = RevenueEngine()
