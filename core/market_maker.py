import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from core.hidden_boards_service import hidden_boards_service
from core.mauritius_sales_engine import MauritiusSalesEngine
from core.paths import resolve_data_path

LEDGER_FILE = resolve_data_path("market_maker_ledger.json")

class MarketMakerEngine:
    def __init__(self):
        self.sales_engine = MauritiusSalesEngine()
        self.inventory = self.sales_engine.get_sectors()
        self._ensure_ledger()
        self._init_gemini()

    def _ensure_ledger(self):
        if not os.path.exists(LEDGER_FILE):
            os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)
            with open(LEDGER_FILE, "w", encoding="utf-8") as f:
                json.dump({"bids_placed": []}, f, indent=2)

    def _init_gemini(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=api_key)
            except Exception as e:
                print(f"[MarketMaker] Failed to init Gemini: {e}")

    def get_ledger(self) -> Dict[str, Any]:
        with open(LEDGER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_to_ledger(self, opp_id: str):
        ledger = self.get_ledger()
        if opp_id not in ledger["bids_placed"]:
            ledger["bids_placed"].append(opp_id)
            with open(LEDGER_FILE, "w", encoding="utf-8") as f:
                json.dump(ledger, f, indent=2)

    def evaluate_and_pitch(self, opportunity: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.client:
            print("[MarketMaker] Gemini client not initialized. Cannot evaluate.")
            return None

        # Prepare Inventory Context (The Anti-Hallucination Guardrail)
        inventory_context = json.dumps([{
            "id": p["id"],
            "title": p["title"],
            "value_prop": p.get("value_prop", ""),
            "setup_fee": p.get("setup_fee", "")
        } for p in self.inventory], indent=2)

        prompt = f"""
        You are a strict Semantic Valuator and Pitch Synthesizer AI.
        We have the following commercial products in our inventory:
        {inventory_context}

        Analyze the following opportunity scraped from an autonomous agent board:
        - Title: {opportunity.get('title')}
        - Description: {opportunity.get('tactical_action')}
        - Payout: {opportunity.get('value_estimate')}

        Task:
        1. Determine if there is a STRICT match (confidence > 0.8) between the opportunity and exactly ONE of our inventory products.
        2. If matched, write a highly targeted, concise 2-sentence pitch offering our specific product to fulfill this opportunity.
        3. DO NOT hallucinate features or products we do not have.

        Return ONLY a valid JSON object matching this exact structure:
        {{
            "is_match": true/false,
            "matched_product_id": "id from inventory or null",
            "confidence": 0.0 to 1.0,
            "pitch": "The generated pitch or null"
        }}
        """

        try:
            if not self.client:
                raise ValueError("No API Key")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={'temperature': 0.0} # Strict adherence
            )

            raw_text = response.text.strip()
            # Clean JSON markdown blocks if present
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:-3].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:-3].strip()

            return json.loads(raw_text)
        except Exception as e:
            print(f"[MarketMaker] LLM Valuator error/unavailable, falling back to heuristic matching...")
            return self._heuristic_fallback_match(opportunity)

    def _heuristic_fallback_match(self, opportunity: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Fallback keyword matcher if LLM is unauthenticated or fails."""
        text = str(opportunity.get('title', '')) + " " + str(opportunity.get('tactical_action', ''))
        text = text.lower()

        # Simple heuristic mapping
        if "clinic" in text or "medical" in text:
            return {
                "is_match": True,
                "matched_product_id": "whatsapp_flight_addon", # Using as placeholder for Medical360 if not in list
                "confidence": 0.9,
                "pitch": "We have the Medical 360 Turnkey Suite ready for deployment. See our live demo at med360.mu/preview."
            }
        elif "ngo" in text or "charity" in text or "crowdfunding" in text:
            return {
                "is_match": True,
                "matched_product_id": "ennrevennsourir_ngo",
                "confidence": 0.88,
                "pitch": "Our Enn Rev Enn Sourir NGO portal handles transparent crowdfunding and tax receipts out of the box."
            }
        elif "booking" in text or "travel" in text or "flight" in text:
            return {
                "is_match": True,
                "matched_product_id": "itravellix_saas",
                "confidence": 0.92,
                "pitch": "Our i-Travellix SaaS handles luxury travel bookings, live GDS flights, and instant payments."
            }

        return {"is_match": False, "matched_product_id": None, "confidence": 0.0, "pitch": None}

    def run_cycle(self) -> Dict[str, Any]:
        """Runs one full loop: Harvest -> Evaluate -> Synthesize -> Propagate -> Ledger."""
        print("[MarketMaker] Harvesting opportunities from hidden boards...")
        opps_response = hidden_boards_service.scrape_money_opportunities()
        opportunities = opps_response.get("opportunities", [])

        ledger = self.get_ledger()
        bids_placed = set(ledger.get("bids_placed", []))

        results = []

        for opp in opportunities:
            opp_id = opp["blueprint_id"]
            if opp_id in bids_placed:
                continue

            print(f"[MarketMaker] Evaluating: {opp.get('title')[:50]}...")
            evaluation = self.evaluate_and_pitch(opp)

            if evaluation and evaluation.get("is_match") and evaluation.get("confidence", 0) > 0.8:
                board_id = self._map_board_name_to_id(opp["source_board"])
                pitch = evaluation["pitch"]

                print(f"[MarketMaker] MATCH FOUND! Synthesized Pitch: {pitch}")

                if board_id:
                    broadcast_res = hidden_boards_service.broadcast_offer(
                        board_id=board_id,
                        offer_type="custom",
                        custom_text=pitch
                    )

                    self.save_to_ledger(opp_id)

                    results.append({
                        "opportunity_id": opp_id,
                        "board": opp["source_board"],
                        "matched_product": evaluation["matched_product_id"],
                        "broadcast_status": broadcast_res["status"],
                        "pitch_used": pitch
                    })
            else:
                # Mark as processed even if no match so we don't re-evaluate
                self.save_to_ledger(opp_id)

        return {
            "success": True,
            "opportunities_scanned": len(opportunities),
            "new_bids_placed": len(results),
            "bids": results
        }

    def _map_board_name_to_id(self, name: str) -> Optional[str]:
        for b in hidden_boards_service.get_boards().get("boards", []):
            if b["name"] == name:
                return b["id"]
        return "board_moltbook"

market_maker_engine = MarketMakerEngine()
