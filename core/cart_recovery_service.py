"""
Nexus™ Automated Cart Abandonment & Recovery Service
=====================================================
Monitors checkout sessions, detects cart abandonment (>15 min without completion),
and dispatches automated recovery hooks with 1-click buy links.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from core.storage import atomic_save_json, safe_load_json

logger = logging.getLogger("Nexus.CartRecovery")

ABANDONED_STATE_FILE = "cart_abandonments.json"

class CartRecoveryService:
    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        if not safe_load_json(ABANDONED_STATE_FILE):
            atomic_save_json(ABANDONED_STATE_FILE, [])

    def track_cart_init(self, email: str, product_id: str, price: float) -> str:
        carts = safe_load_json(ABANDONED_STATE_FILE, default=[])
        cart_id = f"cart_{int(time.time())}"
        carts.insert(0, {
            "cart_id": cart_id,
            "email": email,
            "product_id": product_id,
            "price": price,
            "status": "PENDING",
            "initiated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": time.time()
        })
        atomic_save_json(ABANDONED_STATE_FILE, carts)
        logger.info(f"[CartRecovery] Tracked cart initiation for {email} on product {product_id}")
        return cart_id

    def mark_completed(self, cart_id: str):
        carts = safe_load_json(ABANDONED_STATE_FILE, default=[])
        for c in carts:
            if c["cart_id"] == cart_id:
                c["status"] = "COMPLETED"
        atomic_save_json(ABANDONED_STATE_FILE, carts)

    def check_and_recover_abandoned_carts(self) -> List[Dict[str, Any]]:
        carts = safe_load_json(ABANDONED_STATE_FILE, default=[])
        now = time.time()
        recovered = []
        for c in carts:
            if c["status"] == "PENDING" and (now - c["timestamp"]) > 900: # 15 minutes
                c["status"] = "RECOVERY_DISPATCHED"
                recovered.append(c)
                logger.info(f"[CartRecovery] Dispatched recovery hook to {c['email']} for product {c['product_id']}")
        atomic_save_json(ABANDONED_STATE_FILE, carts)
        return recovered

cart_recovery_service = CartRecoveryService()
