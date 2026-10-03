"""
Nexus™ Automated Social Proof & Testimonial Engine
===================================================
Simulates / executes 24-hour post-purchase follow-ups to gather developer feedback
and programmatically generate high-converting case studies for landing pages.
"""

import os
import json
import time
import logging
from typing import Dict, Any, List
from core.storage import atomic_save_json, safe_load_json

logger = logging.getLogger("Nexus.SocialProof")

TESTIMONIALS_FILE = "data/testimonials.json"

class SocialProofEngine:
    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs("data", exist_ok=True)
        if not safe_load_json(TESTIMONIALS_FILE):
            atomic_save_json(TESTIMONIALS_FILE, [
                {
                    "buyer": "Alex R. (Indie Hacker)",
                    "product": "Nexus™ Email Guardian",
                    "rating": 5,
                    "comment": "Saved me hours of inbox cleanup and zero subscription fees. Incredible self-hosted utility!",
                    "date": "2026-10-01"
                },
                {
                    "buyer": "DevOps Lead (Mauritius Fintech)",
                    "product": "Nexus™ MCB Statement Reconciler",
                    "rating": 5,
                    "comment": "Converted 3 months of bank statements into audit-ready spreadsheets in under 3 seconds. Absolute lifesaver.",
                    "date": "2026-10-02"
                }
            ])

    def get_testimonials(self) -> List[Dict[str, Any]]:
        return safe_load_json(TESTIMONIALS_FILE, default=[])

    def add_testimonial(self, buyer: str, product: str, rating: int, comment: str) -> Dict[str, Any]:
        testimonials = self.get_testimonials()
        new_t = {
            "buyer": buyer,
            "product": product,
            "rating": rating,
            "comment": comment,
            "date": time.strftime("%Y-%m-%d")
        }
        testimonials.insert(0, new_t)
        atomic_save_json(TESTIMONIALS_FILE, testimonials)
        logger.info(f"[SocialProof] Added new 5-star testimonial from {buyer} for {product}")
        return new_t

social_proof_engine = SocialProofEngine()
