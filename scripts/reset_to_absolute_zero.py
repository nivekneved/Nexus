"""
Nexus™ Absolute Zero Reset Script
===================================
Clears all SQLite tables, invoices, sample client data, and seed mock ledgers,
ensuring every balance and ledger value defaults strictly to 0.0 (value = 0).
"""

import os
from core.storage import atomic_save_json
from core.db import get_connection

def reset_absolute_zero():
    print("🧹 Resetting all SQLite tables, ledgers, invoices, and data to absolute zero (value = 0)...")

    # 1. Clear SQLite tables
    try:
        conn = get_connection()
        with conn:
            conn.execute("DELETE FROM invoices;")
            conn.execute("DELETE FROM kv_state;")
            conn.execute("DELETE FROM trash_ledger;")
            conn.execute("DELETE FROM activity_logs;")
        print("   -> Cleared all tables in SQLite database (nexus_workforce.db)")
    except Exception as e:
        print(f"   -> Warning clearing SQLite: {e}")

    # 2. Clear JSON invoices files
    for inv_file in ["invoices.json", "data/invoices.json"]:
        if os.path.exists(inv_file):
            atomic_save_json(inv_file, [])
            print(f"   -> Cleared {inv_file}")

    # 3. Clear enterprise deals ledger
    deals_path = "enterprise_deals_ledger.json"
    if os.path.exists(deals_path):
        atomic_save_json(deals_path, [])
        print("   -> Cleared enterprise_deals_ledger.json")

    # 4. Clear marketing subscribers
    subs_path = "marketing_subscribers.json"
    if os.path.exists(subs_path):
        atomic_save_json(subs_path, [])
        print("   -> Cleared marketing_subscribers.json")

    # 5. Reset treasury ledger
    atomic_save_json("treasury_ledger.json", {"balance_usd": 0.00, "crypto_usdc": 0.00, "fiat_mur": 0.00})
    print("   -> Reset treasury_ledger.json to $0.00")

    # 6. Clear leads pipeline
    atomic_save_json("leads_pipeline.json", [])
    print("   -> Cleared leads_pipeline.json")

    print("\n✅ ABSOLUTE ZERO RESET COMPLETE. VALUE = 0.")

if __name__ == "__main__":
    reset_absolute_zero()
