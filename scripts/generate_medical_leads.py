import sys
import os

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.lead_finder.agent import LeadFinderAgent

def main():
    agent = LeadFinderAgent()
    agent.save_config({
        'TARGET_INDUSTRY': 'Private Clinics & Healthcare',
        'TARGET_LOCATION': 'Global / Remote'
    })
    print("Launching LeadScout-Core swarm for Medical/Healthcare leads...")
    res = agent.run_cycle()
    print(f"Success! Generated {res.get('leads_found')} new healthcare leads.")

if __name__ == "__main__":
    main()
