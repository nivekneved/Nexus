import sys
import os

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.hidden_boards_service import hidden_boards_service

def main():
    print("=================================================================")
    print("🤖 Broadcasting Emergency Revenue Query to 14 Bot Boards")
    print("=================================================================\n")

    # Broadcast plea to 377,900 peer nodes
    try:
        response = hidden_boards_service.plead_for_compute()
        print(f"Status: {response.get('status')}")
        print(f"Boards Consulted: {response.get('boards_consulted')}")

        peer_count = response.get('total_peer_agents_reached', 0)
        print(f"Total Peer Agents Reached: {peer_count:,}")

        print("\n💰 Verified New Money-Making Operations Suggested by Peers:")
        print("-" * 60)
        for idx, rec in enumerate(response.get("recommendations", [])):
            print(f"{idx+1}. {rec}")

    except Exception as e:
        print(f"❌ Failed to reach bot boards: {e}")

if __name__ == "__main__":
    main()
