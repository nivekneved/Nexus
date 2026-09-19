"""
Nexus Contact History & Outreach CRM Ledger
===========================================
Tracks every outbound message, channel, pitch text, delivery status,
and response metrics per contact. Persists to contact_history.json.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

HISTORY_FILE = "contact_history.json"

class ContactHistoryService:
    def __init__(self, file_path: str = HISTORY_FILE):
        self.file_path = file_path

    def _load(self) -> List[Dict[str, Any]]:
        from core.storage import safe_load_json
        return safe_load_json(self.file_path, default=[])

    def _save(self, records: List[Dict[str, Any]]):
        from core.storage import atomic_save_json
        try:
            atomic_save_json(self.file_path, records)
        except Exception as e:
            print(f"[ContactHistory] Error saving records: {e}")


    def record_outreach(
        self,
        recipient_email: str,
        company: str,
        contact_name: str,
        channel: str,
        subject: str,
        body: str,
        sender: str = "devenpawaray@gmail.com",
        status: str = "SENT",
        lead_id: Optional[str] = None,
        niche: Optional[str] = None,
        phone: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Records a new outbound message sent to a contact."""
        records = self._load()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        interaction_id = f"int_{int(time.time()*1000)}"

        # Find existing contact record or create new
        contact_record = next((r for r in records if r.get("email") == recipient_email), None)

        interaction_entry = {
            "interaction_id": interaction_id,
            "timestamp": now_str,
            "channel": channel,
            "sender": sender,
            "subject": subject,
            "body": body,
            "status": status,
            "metadata": metadata or {}
        }

        if contact_record:
            contact_record["company"] = company or contact_record.get("company")
            contact_record["contact_name"] = contact_name or contact_record.get("contact_name")
            contact_record["phone"] = phone or contact_record.get("phone")
            contact_record["niche"] = niche or contact_record.get("niche")
            contact_record["last_contacted"] = now_str
            contact_record["status"] = status
            contact_record["total_touches"] = contact_record.get("total_touches", 0) + 1
            if "interactions" not in contact_record:
                contact_record["interactions"] = []
            contact_record["interactions"].append(interaction_entry)
        else:
            contact_record = {
                "id": lead_id or f"ct_{int(time.time())}",
                "email": recipient_email,
                "company": company,
                "contact_name": contact_name,
                "phone": phone or "+230 58169420",
                "niche": niche or "general",
                "first_contacted": now_str,
                "last_contacted": now_str,
                "status": status,
                "total_touches": 1,
                "interactions": [interaction_entry]
            }
            records.append(contact_record)

        self._save(records)
        return contact_record

    def mark_bounced(self, email_address: str, reason: str = "Delivery failed / Address not found") -> bool:
        """Marks a contact and its latest outreach as BOUNCED."""
        clean_email = email_address.strip().lower()
        records = self._load()
        updated = False

        for r in records:
            r_email = (r.get("email") or "").strip().lower()
            if r_email == clean_email:
                r["status"] = "BOUNCED"
                r["bounce_reason"] = reason
                r["bounced_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Update latest interaction
                if r.get("interactions"):
                    r["interactions"][-1]["status"] = "BOUNCED"
                    r["interactions"][-1]["bounce_reason"] = reason
                updated = True

        if updated:
            self._save(records)
        return updated

    def get_all_contacts(self) -> List[Dict[str, Any]]:
        return self._load()

    def get_contact_by_email(self, email_address: str) -> Optional[Dict[str, Any]]:
        clean_email = (email_address or "").strip().lower()
        records = self._load()
        return next((r for r in records if (r.get("email") or "").strip().lower() == clean_email), None)

    def get_stats(self) -> Dict[str, Any]:
        """Calculates aggregated outreach delivery and response metrics."""
        records = self._load()
        total_contacts = len(records)
        total_interactions = sum(len(r.get("interactions", [])) for r in records)
        bounced_count = sum(1 for r in records if r.get("status") == "BOUNCED")
        sent_count = sum(1 for r in records if r.get("status") == "SENT")
        replied_count = sum(1 for r in records if r.get("status") == "REPLIED")

        deliverable_rate = (
            round(((total_contacts - bounced_count) / total_contacts) * 100, 1)
            if total_contacts > 0 else 100.0
        )

        return {
            "total_contacts": total_contacts,
            "total_interactions": total_interactions,
            "sent_count": sent_count,
            "bounced_count": bounced_count,
            "replied_count": replied_count,
            "deliverable_rate_pct": deliverable_rate
        }

contact_history_service = ContactHistoryService()
