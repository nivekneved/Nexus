# -*- coding: utf-8 -*-
"""
Nexus™ Mass Emailing & Campaign Dispatch Service (v36.0)
======================================================
Manages recipient lists imported from CSV/XLS, provides advanced filtering, sorting,
pagination, and dispatches high-deliverability cold/promotional email campaigns via SMTP.
"""

import os
import csv
import json
import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from core.storage import atomic_save_json, safe_load_json
from core.legal_guardrails import legal_guardrails
from core.inbox_feed_service import inbox_feed_service
from core.telemetry import telemetry

logger = logging.getLogger("Nexus.MassEmailService")

CONTACTS_LEDGER = "mass_email_contacts.json"
CAMPAIGNS_LEDGER = "mass_email_campaigns.json"

class MassEmailService:
    def __init__(self):
        self._ensure_files()

    def _ensure_files(self):
        if not safe_load_json(CONTACTS_LEDGER):
            atomic_save_json(CONTACTS_LEDGER, [])
        if not safe_load_json(CAMPAIGNS_LEDGER):
            atomic_save_json(CAMPAIGNS_LEDGER, [])

    def get_contacts(self, search: Optional[str] = None, page: int = 1, limit: int = 25) -> Dict[str, Any]:
        """
        Returns paginated, filtered, and sorted contact records.
        """
        contacts = safe_load_json(CONTACTS_LEDGER, default=[])

        if search:
            q = search.lower().strip()
            contacts = [c for c in contacts if q in c.get("email", "").lower() or q in c.get("name", "").lower() or q in c.get("company", "").lower()]

        total_records = len(contacts)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated = contacts[start_idx:end_idx]

        return {
            "success": True,
            "total_records": total_records,
            "page": page,
            "limit": limit,
            "total_pages": (total_records + limit - 1) // limit if limit > 0 else 1,
            "contacts": paginated
        }

    def import_contacts_from_csv(self, file_path: str) -> Dict[str, Any]:
        """
        Parses an uploaded CSV or Excel (XLS/XLSX) file and imports contacts into the mass emailing ledger.
        """
        import traceback
        contacts = safe_load_json(CONTACTS_LEDGER, default=[])
        imported_count = 0

        try:
            records = []
            lower_path = file_path.lower()
            if lower_path.endswith(('.xlsx', '.xls')):
                import pandas as pd
                try:
                    df = pd.read_excel(file_path)
                except Exception:
                    df = pd.read_excel(file_path, engine='openpyxl' if lower_path.endswith('.xlsx') else 'xlrd')
                records = df.to_dict(orient="records")
            else:
                import pandas as pd
                try:
                    df = pd.read_csv(file_path, encoding="utf-8")
                except Exception:
                    try:
                        df = pd.read_csv(file_path, encoding="latin-1")
                    except Exception:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            import csv
                            reader = csv.DictReader(f)
                            records = list(reader)
                if not records and 'df' in locals():
                    records = df.to_dict(orient="records")

            for row in records:
                row_lower = {str(k).strip().lower(): v for k, v in row.items() if k is not None}
                email = row_lower.get("email") or row_lower.get("mail") or row_lower.get("e-mail") or row_lower.get("electronic mail")
                if not email or not isinstance(email, str) or "@" not in email:
                    for val in row_lower.values():
                        if val and isinstance(val, str) and "@" in val and "." in val:
                            email = val.strip()
                            break
                if not email or "@" not in email:
                    continue

                name = row_lower.get("name") or row_lower.get("full name") or row_lower.get("contact name") or "Valued Partner"
                company = row_lower.get("company") or row_lower.get("organization") or row_lower.get("business") or "Enterprise"

                email = str(email).strip()
                name = str(name).strip() if name else "Valued Partner"
                company = str(company).strip() if company else "Enterprise"

                suppressed, _ = legal_guardrails.is_suppressed(email)
                if suppressed:
                    continue

                if not any(c.get("email", "").lower() == email.lower() for c in contacts):
                    contacts.append({
                        "id": f"cnt_{int(time.time() * 1000)}_{imported_count}",
                        "email": email,
                        "name": name,
                        "company": company,
                        "status": "SUBSCRIBED",
                        "imported_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    imported_count += 1

            atomic_save_json(CONTACTS_LEDGER, contacts)
            logger.info(f"[MassEmail] Successfully imported {imported_count} contacts.")
            return {
                "success": True,
                "imported_count": imported_count,
                "total_contacts": len(contacts),
                "message": f"Successfully imported {imported_count} contacts into Mass Emailing database."
            }
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"[MassEmail] Error parsing file: {e}\n{tb}")
            return {"success": False, "error": f"{str(e)}"}

    def dispatch_campaign(self, subject: str, body: str, target_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Dispatches mass email campaign to target subscribers via SMTP.
        """
        contacts = safe_load_json(CONTACTS_LEDGER, default=[])
        if target_ids:
            recipients = [c for c in contacts if c.get("id") in target_ids and c.get("status") == "SUBSCRIBED"]
        else:
            recipients = [c for c in contacts if c.get("status") == "SUBSCRIBED"]

        if not recipients:
            return {"success": False, "error": "No subscribed recipients selected for campaign."}

        sent_count = 0
        failed_count = 0

        for r in recipients:
            try:
                personalized_body = body.replace("{{name}}", r.get("name", "Partner")).replace("{{company}}", r.get("company", "Enterprise"))
                res = inbox_feed_service.send_outbound_email(
                    to_email=r["email"],
                    subject=subject,
                    body=personalized_body
                )
                if res.get("success"):
                    sent_count += 1
                else:
                    failed_count += 1
            except Exception:
                failed_count += 1

        campaign_record = {
            "campaign_id": f"cmp_{int(time.time())}",
            "subject": subject,
            "sent_count": sent_count,
            "failed_count": failed_count,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        campaigns = safe_load_json(CAMPAIGNS_LEDGER, default=[])
        campaigns.insert(0, campaign_record)
        atomic_save_json(CAMPAIGNS_LEDGER, campaigns)

        telemetry.emit(
            agent_id="domain_comms",
            agent_name="Communications Domain Controller",
            step="MASS_EMAIL_CAMPAIGN_DISPATCHED",
            file_used="core/mass_email_service.py",
            message=f"Mass email campaign dispatched: {sent_count} sent, {failed_count} failed.",
            level="SUCCESS"
        )

        return {
            "success": True,
            "campaign_id": campaign_record["campaign_id"],
            "sent_count": sent_count,
            "failed_count": failed_count,
            "message": f"Campaign successfully dispatched to {sent_count} recipients!"
        }

mass_email_service = MassEmailService()
