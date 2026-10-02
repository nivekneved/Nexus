import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import sys
import json
import time
from datetime import datetime

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.market_maker import market_maker_engine
from core.freelance_arbitrage import freelance_arbitrage
from core.executive_reporting_engine import reporting_engine
from core.treasury_engine import treasury_engine

def run_overnight_revenue_campaign():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 LAUNCHING ALL AUTONOMOUS REVENUE AGENTS...")

    # 1. Start Master Clock (Reporting & Autopilot)
    reporting_engine.start_master_clock()
    print("[*] Master Clock & Overnight Chronicle Active.")

    # 2. Run Market Maker (Hidden Bot Boards Bidding)
    print("[*] Running Market Maker Hidden Boards Sweep...")
    mm_result = market_maker_engine.run_cycle()
    print(f"[*] Market Maker Result: {json.dumps(mm_result, indent=2)}")

    # 3. Run Freelance Arbitrage (Upwork / Fiverr Auto-Bidding)
    print("[*] Running Freelance Arbitrage Swarm...")
    fa_result = freelance_arbitrage.scan_and_bid()
    print(f"[*] Freelance Arbitrage Result: {json.dumps(fa_result, indent=2)}")

    # 4. Run FinOps Dunning Cycle
    print("[*] Running FinOps Dunning & Invoice Recovery...")
    dunning_result = treasury_engine.run_dunning_cycle()
    print(f"[*] Dunning Result: {json.dumps(dunning_result, indent=2)}")

    # Log summary
    summary = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market_maker": mm_result,
        "freelance_arbitrage": fa_result,
        "dunning": dunning_result,
        "status": "SWARM_RUNNING_24_7"
    }

    os.makedirs("reports", exist_ok=True)
    with open("reports/morning_revenue_surprise.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ ALL REVENUE AGENTS DEPLOYED. SLEEP WELL, SIR. SURPRISE REPORT SAVED TO reports/morning_revenue_surprise.json")

if __name__ == "__main__":
    run_overnight_revenue_campaign()
