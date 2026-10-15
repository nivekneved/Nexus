"""
Nexus 3-Cycle Agent Journey Tracker & Demonstration
===================================================
Executes 3 consecutive autonomous run cycles for a pillar agent,
tracking tasks completed, synergy handoffs, and self-evolution upgrades.
"""

import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.agent_manager import AgentManager

def simulate_agent_3_cycles(agent_id: str = "lead_finder"):
    manager = AgentManager()
    agent = manager.get_agent(agent_id)
    if not agent:
        print(f"❌ Agent {agent_id} not found.")
        return

    print("=========================================================")
    print(f"🚀 INITIATING 3-CYCLE JOURNEY FOR: {agent.name} (ID: {agent_id})")
    print("=========================================================")

    journey_log = []

    for cycle in range(1, 4):
        print(f"\n--- [Cycle {cycle} / 3] Starting execution for {agent.name} ---")
        try:
            # Execute agent cycle via AgentManager
            result = manager.run_agent(agent_id)
            journey_log.append({
                "cycle": cycle,
                "status": "SUCCESS",
                "result": result
            })
            print(f"   ✅ Cycle {cycle} completed successfully.")
            print(f"   🧬 Self-Evolution Protocol: Upgraded parameters & recorded memory.")
        except Exception as e:
            journey_log.append({
                "cycle": cycle,
                "status": "FAILED",
                "error": str(e)
            })
            print(f"   ❌ Cycle {cycle} failed: {e}")

    print("\n=========================================================")
    print(f"📊 FINAL 3-CYCLE JOURNEY REPORT FOR: {agent.name}")
    print("=========================================================")
    for entry in journey_log:
        print(f"Cycle {entry['cycle']}: Status = {entry['status']}")
        if entry['status'] == 'SUCCESS':
            res = entry['result']
            print(f"   ➔ Result Data: {str(res)[:150]}...")
    print("=========================================================\n")

if __name__ == "__main__":
    target_agent = sys.argv[1] if len(sys.argv) > 1 else "lead_finder"
    simulate_agent_3_cycles(target_agent)
