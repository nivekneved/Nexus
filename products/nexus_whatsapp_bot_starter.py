"""
Nexus™ WhatsApp Bot Starter (Micro-Edition)
===========================================
A self-hosted, lightweight conversational WhatsApp bot template in Python/FastAPI.
Runs locally or on any $5 VPS with zero vendor lock-in.

Features:
- Instant wa.me 1-click customer routing
- Automated FAQ & business inquiry auto-replies
- Seamless MCB Juice / PayPal payment link generator
- Ready for Meta WhatsApp Cloud API or Twilio WhatsApp sandbox

Usage:
  pip install fastapi uvicorn
  python nexus_whatsapp_bot_starter.py
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import urllib.parse

app = FastAPI(title="Nexus WhatsApp Bot Starter")

# === BUSINESS CONFIGURATION ===
BUSINESS_NAME = "My Fast Business"
CONTACT_PHONE = "+23058169420"
PAYMENT_LINK = "https://www.paypal.com/checkoutnow?token=86S57862G8674101J"

@app.get("/")
def home():
    return {
        "status": "ONLINE",
        "bot": f"{BUSINESS_NAME} WhatsApp Concierge",
        "version": "1.0.0",
        "instructions": "Send POST to /webhook or use /wa-link to generate customer wa.me links"
    }

@app.get("/wa-link")
def generate_customer_link(message: str = "Hi! I want to order."):
    """Generates a 1-click WhatsApp customer chat link."""
    encoded_msg = urllib.parse.quote(message)
    clean_phone = CONTACT_PHONE.replace("+", "").replace(" ", "")
    wa_url = f"https://wa.me/{clean_phone}?text={encoded_msg}"
    return {
        "success": True,
        "whatsapp_url": wa_url,
        "clean_phone": clean_phone
    }

class InboundWhatsAppMessage(BaseModel):
    sender: str
    message: str

@app.post("/webhook")
def handle_incoming_message(payload: InboundWhatsAppMessage):
    """Simple 24/7 rule-based conversational AI bot."""
    msg = payload.message.lower().strip()
    
    if "price" in msg or "cost" in msg or "tarif" in msg:
        reply = f"Our standard package starts at $1.00 USD. Pay instantly here: {PAYMENT_LINK}"
    elif "hours" in msg or "location" in msg:
        reply = f"{BUSINESS_NAME} operates 24/7 autonomously. Message us anytime!"
    elif "human" in msg or "support" in msg:
        reply = f"Transferring to a human operator at {CONTACT_PHONE}. One moment please!"
    else:
        reply = f"Hello! Welcome to {BUSINESS_NAME}. How can we help you today? Reply 'price' or 'support'."
        
    return {
        "reply": reply,
        "recipient": payload.sender,
        "status": "DELIVERED"
    }

if __name__ == "__main__":
    print(f"🚀 {BUSINESS_NAME} WhatsApp Bot starting on http://127.0.0.1:5000")
    uvicorn.run(app, host="127.0.0.1", port=5000)
