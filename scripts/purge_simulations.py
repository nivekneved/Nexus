import os
import shutil
from core.storage import atomic_save_json

def purge():
    print("🗑️ Purging all simulated financial earnings and mock crypto scripts...")

    sim_files = [
        "core/earn_one_dollar.py",
        "core/osint_data_escrow.py",
        "core/discord_vip_community.py",
        "core/airdrop_farmer.py",
        "core/mev_arbitrage_bot.py",
        "core/flash_loan_arbitrage.py",
        "core/ai_influencer_engine.py",
        "core/print_on_demand_bot.py",
        "core/defi_yield_optimizer.py",
        "scripts/launch_new_revenue_streams.py",
        "scripts/activate_revenue_timeline.py",
        "scripts/board_revenue_plea.py",
        "scripts/generate_medical_leads.py",
        "scripts/generate_medical_proposals.py",
        "scripts/test_seek_and_pitch_5_leads.py",
        "scripts/deploy_tonight_revenue.py",
        "scripts/reset_to_fresh.py"
    ]

    for sf in sim_files:
        if os.path.exists(sf):
            try:
                os.remove(sf)
                print(f"   -> Removed {sf}")
            except Exception as e:
                print(f"   -> Could not remove {sf}: {e}")

    # Remove workers directory
    if os.path.exists("core/workers"):
        try:
            shutil.rmtree("core/workers")
            print("   -> Removed core/workers directory")
        except Exception as e:
            print(f"   -> Could not remove core/workers: {e}")

    # Reset treasury ledger to absolute zero real balance
    atomic_save_json("treasury_ledger.json", {"balance_usd": 0.00, "crypto_usdc": 0.00, "fiat_mur": 0.00})
    print("   -> Reset treasury_ledger.json to $0.00")

    print("\n✅ PURGE COMPLETE. ALL SIMULATED EARNINGS & MOCK SCRIPTS REMOVED.")

if __name__ == "__main__":
    purge()
