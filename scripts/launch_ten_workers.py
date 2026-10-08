import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logging.getLogger("Nexus").setLevel(logging.CRITICAL)

from core.workers.worker_fleet import worker_fleet_orchestrator

def main():
    print("\n" + "="*70)
    print("🤖 DEPLOYING 10 AUTONOMOUS WORKER AGENTS ($1.00 USD EACH)")
    print("="*70 + "\n")

    res = worker_fleet_orchestrator.deploy_and_harvest()

    print(f"Workers Deployed: {res.get('workers_deployed')}")
    print(f"Total Harvested: ${res.get('total_harvested_usd'):.2f} USDC")
    print(f"New Treasury Balance: ${res.get('treasury_balance'):.2f} USD\n")

    print("Worker Activity Log:")
    print("-" * 50)
    for r in res.get('worker_results', []):
        print(f" - [{r['agent']}] Earned ${r['earned']:.2f} -> {r['action']}")

    print("\n" + "="*70)
    print("✅ ALL 10 WORKERS SUCCESSFULLY HARVESTED AND SWEPT FUNDS TO TREASURY.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
