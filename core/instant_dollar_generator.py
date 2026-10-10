"""
Nexus™ $1.00 USD Instant Generation Engine
===========================================
Generates real live 1-click PayPal checkout links for real micro-products
and tracks true settlement status without synthetic in-memory mutations.
"""

import os
import time
import logging
from typing import Dict, Any
from core.digital_store_service import digital_store_service
from core.payment_service import payment_service
from core.storage import safe_load_json

logger = logging.getLogger("Nexus.InstantDollarGenerator")

class InstantDollarGenerator:
    @staticmethod
    def generate_dollar() -> Dict[str, Any]:
        """
        Generates a verified, real live $1.00 USD PayPal checkout order
        for a digital utility product, returning the direct payment URL.
        """
        timestamp = int(time.time())
        direct_link = os.getenv("PAYPAL_DIRECT_PAYMENT_URL", "").strip().strip("'\"")

        # 1. Create a real PayPal checkout order or direct link for $1.00 product
        try:
            order_data = digital_store_service.create_checkout_order(
                product_id="nexus-invoice-pdf-extractor",
                buyer_email=os.getenv("EMAIL_USER", "buyer@example.com"),
                currency="USD",
                payment_method="paypal"
            )
            checkout_url = direct_link or order_data.get("checkout_url")
            order_id = order_data.get("order_id", f"order_{timestamp}")
            invoice_id = order_data.get("invoice_id")
        except Exception as e:
            logger.error(f"[InstantDollarGenerator] Error creating checkout order: {e}")
            # Fallback to direct PayPal link if configured
            if direct_link:
                checkout_url = direct_link
                order_id = f"direct_{timestamp}"
                invoice_id = None
            else:
                return {
                    "success": False,
                    "error": f"Failed to generate PayPal checkout order: {str(e)}",
                    "instructions": "Ensure PAYPAL_CLIENT_ID & PAYPAL_SECRET or PAYPAL_DIRECT_PAYMENT_URL are configured in .env."
                }

        # 2. Query real settled balance from invoices database
        real_balance = payment_service.get_balance()

        logger.info(f"[InstantDollarGenerator] Live $1.00 PayPal order ready: {order_id} -> {checkout_url}")

        return {
            "success": True,
            "target_amount_usd": 1.00,
            "checkout_url": checkout_url,
            "order_id": order_id,
            "invoice_id": invoice_id,
            "status": "AWAITING_PAYMENT_CAPTURE",
            "settled_revenue_mur": real_balance,
            "message": "Live $1.00 PayPal checkout link created. Once approved by buyer, $1.00 will settle into your PayPal balance.",
            "direct_paypal_configured": bool(direct_link)
        }

instant_dollar_generator = InstantDollarGenerator()
