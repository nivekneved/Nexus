import unittest
from core.webhook_fulfillment_engine import webhook_fulfillment_engine

class TestWebhookFulfillmentEngine(unittest.TestCase):
    def test_download_token_generation(self):
        token = webhook_fulfillment_engine.generate_download_token("TEST-ORDER-123")
        self.assertTrue(token.startswith("NX-DL-"))
        self.assertGreater(len(token), 10)

    def test_social_seeding_broadcast(self):
        res = webhook_fulfillment_engine.broadcast_micro_asset_seed(
            asset_name="Test Utility",
            price_usd=1.00,
            checkout_url="https://www.paypal.com/ncp/payment/TEST"
        )
        self.assertTrue(res["success"])
        self.assertIn("Test Utility", res["syndicated_message"])

if __name__ == "__main__":
    unittest.main()
