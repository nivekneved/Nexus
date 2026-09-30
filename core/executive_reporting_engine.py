
import threading
import time
from datetime import datetime
from typing import Dict, Any, Optional

from core.daily_brief_service import daily_brief_service
from core.overnight_chronicle import overnight_chronicle

class ExecutiveReportingEngine:
    """
    Unified Executive Reporting & Telemetry Engine.
    Provides a single Master Clock thread for both the 4 PM Daily Brief
    and the 24/7 Overnight Autopilot sweeps.
    """
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
