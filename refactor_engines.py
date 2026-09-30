import os
import re

# 1. Create the Executive Reporting Engine (Master Clock Facade)
reporting_engine_code = """
import threading
import time
from datetime import datetime
from typing import Dict, Any, Optional

from core.daily_brief_service import daily_brief_service
from core.overnight_chronicle import overnight_chronicle

class ExecutiveReportingEngine:
    \"\"\"
    Unified Executive Reporting & Telemetry Engine.
    Provides a single Master Clock thread for both the 4 PM Daily Brief
    and the 24/7 Overnight Autopilot sweeps.
    \"\"\"
    def __init__(self):
        self.daily = daily_brief_service
        self.night = overnight_chronicle

        # We will keep track of the master clock state
        self.is_running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Inherit settings
        self.target_time_str = self.daily.target_time_str
        self.last_sent_date = self.daily.last_sent_date
        self.interval_minutes = self.night.interval_minutes

    def start_master_clock(self):
        if self.is_running:
            return
        self.is_running = True

        # Stop any standalone threads to prevent duplication
        try:
            self.daily.is_running = False
            if hasattr(self.daily, '_stop_event'): self.daily._stop_event.set()
        except Exception: pass

        try:
            if hasattr(self.night, 'stop'): self.night.stop()
        except Exception: pass

        self.night.is_running = True # Mark active for logic
        self.night.started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._master_clock_loop, daemon=True)
        self._thread.start()
        print("[ExecutiveReportingEngine] Master Clock started. Controlling Daily Brief & Night Shift.")

    def stop_master_clock(self):
        self.is_running = False
        self.night.is_running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)
        print("[ExecutiveReportingEngine] Master Clock stopped.")

    def _master_clock_loop(self):
        while not self._stop_event.is_set():
            now = datetime.now()

            # --- 1. DAILY BRIEF (4 PM) LOGIC ---
            try:
                target_hour, target_min = map(int, self.daily.target_time_str.split(":"))
                if now.hour == target_hour and now.minute == target_min:
                    today_str = now.strftime("%Y-%m-%d")
                    if self.daily.last_sent_date != today_str:
                        self.daily.dispatch_daily_brief()
                        self.daily.last_sent_date = today_str
                        self.daily._save_state()
            except Exception as e:
                print(f"[MasterClock] Daily Brief Error: {e}")

            # --- 2. OVERNIGHT CHRONICLE LOGIC ---
            try:
                if self.night.is_running:
                    # Execute night shift cycle directly
                    self.night.run_full_night_shift_cycle()
            except Exception as e:
                print(f"[MasterClock] Night Shift Error: {e}")

            # Sleep for the night interval (converted to seconds)
            # Default to 30 mins if not set
            sleep_time = (self.night.interval_minutes * 60) if self.night.interval_minutes else 1800

            # We sleep in small chunks so we can intercept the stop event quickly
            chunks = int(sleep_time / 5)
            for _ in range(chunks):
                if self._stop_event.is_set():
                    break
                time.sleep(5)

    # Facade Methods for server.py routing
    def compile_daily_brief(self): return self.daily.compile_daily_brief()
    def dispatch_daily_brief(self): return self.daily.dispatch_daily_brief()
    def load_events(self): return self.night.load_events()
    def generate_morning_dossier(self): return self.night.generate_morning_dossier()
    def run_full_night_shift_cycle(self): return self.night.run_full_night_shift_cycle()
    def toggle_night_shift(self):
        if self.is_running:
            self.stop_master_clock()
        else:
            self.start_master_clock()
        return {"is_active": self.is_running}

    @property
    def cycles_completed(self): return self.night.cycles_completed
    @property
    def started_at(self): return self.night.started_at
    @property
    def last_cycle_at(self): return self.night.last_cycle_at
    @property
    def next_cycle_at(self): return self.night.next_cycle_at

reporting_engine = ExecutiveReportingEngine()
"""

with open("core/executive_reporting_engine.py", "w", encoding="utf-8") as f:
    f.write(reporting_engine_code)


# 2. Create the Treasury Engine (Unified Commerce Facade)
treasury_engine_code = """
from typing import Dict, Any, Optional
from core.crypto_treasury import crypto_treasury
from core.payment_service import payment_service
from core.crypto_verifier import crypto_verifier
from core.receipt_generator import receipt_generator

class TreasuryEngine:
    \"\"\"
    Unified Treasury & Commerce Engine.
    Provides a single interface for FIAT (PayPal/MCB Juice), Crypto (USDC/Base),
    Verification, and Receipt Generation.
    \"\"\"
    def __init__(self):
        self.crypto = crypto_treasury
        self.fiat = payment_service
        self.verifier = crypto_verifier
        self.receipts = receipt_generator

    # --- Unified Payment Gateway ---
    def process_fiat_payment(self, amount: float, currency: str, source: str) -> Dict[str, Any]:
        return self.fiat.process_payment(amount, currency, source)

    def process_crypto_payment(self, tx_hash: str, expected_amount: float) -> Dict[str, Any]:
        # 1. Verify on-chain
        verification = self.verifier.verify_transaction(tx_hash)
        if not verification.get("valid"):
            return {"success": False, "error": "Invalid transaction"}

        # 2. Add to treasury
        return self.crypto.record_deposit(tx_hash, expected_amount)

    # --- Unified Receipt Generation ---
    def generate_and_dispatch_receipt(self, payment_data: Dict[str, Any], send_whatsapp: bool = True) -> Dict[str, Any]:
        receipt = self.receipts.generate_receipt(payment_data)
        if send_whatsapp:
            pass # Hook into whatsapp gateway if needed
        return receipt

    # --- Treasury Balances ---
    def get_consolidated_balances(self) -> Dict[str, Any]:
        fiat_balance = self.fiat.get_balance() if hasattr(self.fiat, 'get_balance') else 0.0
        crypto_balance = self.crypto.get_treasury_balance() if hasattr(self.crypto, 'get_treasury_balance') else 0.0
        return {
            "success": True,
            "fiat_mur": fiat_balance,
            "crypto_usdc": crypto_balance,
            "total_estimated_usd": (fiat_balance / 45.0) + crypto_balance
        }

treasury_engine = TreasuryEngine()
"""

with open("core/treasury_engine.py", "w", encoding="utf-8") as f:
    f.write(treasury_engine_code)


# 3. Refactor server.py to use the Reporting Engine Facade
# We will do a safe regex replacement for the endpoints
try:
    with open("server.py", "r", encoding="utf-8") as f:
        server_code = f.read()

    # Imports replacements
    server_code = server_code.replace(
        "from core.daily_brief_service import daily_brief_service",
        "from core.executive_reporting_engine import reporting_engine"
    )
    server_code = server_code.replace(
        "from core.overnight_chronicle import overnight_chronicle",
        "from core.executive_reporting_engine import reporting_engine"
    )

    # Startup call replacement
    server_code = server_code.replace(
        "daily_brief_service.start_scheduler()",
        "reporting_engine.start_master_clock()"
    )

    # Replace references to overnight_chronicle toggle explicitly first because its method changed
    server_code = server_code.replace(
        "overnight_chronicle.toggle()",
        "reporting_engine.toggle_night_shift()"
    )

    # Endpoint logic replacements
    server_code = server_code.replace("daily_brief_service.", "reporting_engine.")
    server_code = server_code.replace("overnight_chronicle.", "reporting_engine.")

    with open("server.py", "w", encoding="utf-8") as f:
        f.write(server_code)
    print("Successfully refactored server.py to use Unified Engines!")
except Exception as e:
    print(f"Error patching server.py: {e}")
