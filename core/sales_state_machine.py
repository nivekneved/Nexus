"""
Nexus™ SalesGPT 7-Stage Conversational Sales State Machine
===========================================================
Drives visitors through an explicit 7-stage sales funnel:
1. Introduction -> 2. Qualification -> 3. Value Proposition -> 4. Needs Analysis
-> 5. Solution Presentation -> 6. Objection Handling -> 7. Closing & Checkout.
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("Nexus.SalesStateMachine")

STAGES = [
    "INTRODUCTION",
    "QUALIFICATION",
    "VALUE_PROPOSITION",
    "NEEDS_ANALYSIS",
    "SOLUTION_PRESENTATION",
    "OBJECTION_HANDLING",
    "CLOSING"
]

class SalesStateMachine:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def get_or_create_session(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "stage": "INTRODUCTION",
                "history": [],
                "user_intent": None,
                "selected_product": None
            }
        return self.sessions[session_id]

    def advance_stage(self, session_id: str, user_input: str) -> Dict[str, Any]:
        session = self.get_or_create_session(session_id)
        current_stage = session["stage"]
        session["history"].append({"role": "user", "content": user_input})

        # Simple stage transition logic
        if current_stage == "INTRODUCTION":
            session["stage"] = "QUALIFICATION"
            response = "Hello! Welcome to Nexus Sovereign Store. What specific automation or workflow problem are you looking to solve today?"
        elif current_stage == "QUALIFICATION":
            session["stage"] = "VALUE_PROPOSITION"
            session["user_intent"] = user_input
            response = "Got it. Nexus provides zero-subscription, self-hosted Python micro-utilities and B2B automation engines designed to save you time and protect your privacy."
        elif current_stage == "VALUE_PROPOSITION":
            session["stage"] = "NEEDS_ANALYSIS"
            response = "Are you looking for a quick $1.00 micro-utility (like a PDF invoice parser) or a complete B2B automated system?"
        elif current_stage == "NEEDS_ANALYSIS":
            session["stage"] = "SOLUTION_PRESENTATION"
            response = "Based on your needs, our catalog features production-ready scripts like the Email Guardian ($9) or MCB Statement Reconciler ($29). Would you like to view product details?"
        elif current_stage == "SOLUTION_PRESENTATION":
            session["stage"] = "OBJECTION_HANDLING"
            response = "All tools include full source code with perpetual commercial rights and zero monthly fees. Do you have any questions about setup or security?"
        elif current_stage == "OBJECTION_HANDLING":
            session["stage"] = "CLOSING"
            response = "Excellent. You can complete your secure checkout instantly via PayPal, MCB Juice, or Base L2 Crypto. Ready to deploy?"
        else:
            session["stage"] = "CLOSING"
            response = "Proceeding to secure checkout and instant download."

        session["history"].append({"role": "assistant", "content": response})
        return {
            "session_id": session_id,
            "stage": session["stage"],
            "response": response
        }

sales_state_machine = SalesStateMachine()
