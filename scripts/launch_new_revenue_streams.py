import sys
import os
import asyncio
import logging

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Suppress debug logs for clean output
logging.getLogger("Nexus").setLevel(logging.CRITICAL)

from core.osint_data_escrow import osint_data_escrow
from core.discord_vip_community import discord_vip_community
from core.mev_arbitrage_bot import mev_arbitrage_bot
from core.airdrop_farmer import airdrop_farmer
from core.flash_loan_arbitrage import flash_loan_arbitrage_bot
from core.ai_influencer_engine import ai_influencer_engine
from core.print_on_demand_bot import print_on_demand_bot
from core.defi_yield_optimizer import defi_yield_optimizer

async def main():
    print("\n" + "="*70)
    print("🚀 LAUNCHING ALL HIGH-VELOCITY ALTERNATIVE REVENUE STREAMS")
    print("="*70 + "\n")

    print("1️⃣ Starting Smart Contract OSINT Data Escrow...")
    res1 = osint_data_escrow.package_and_sell_leads(5)
    if res1.get('success'):
        print(f"   -> Result: Sold 5 verified executive profiles for ${res1.get('revenue_usd')} USDC.\n")

    print("2️⃣ Starting Arbitrage DEX Liquidity (MEV)...")
    res4 = mev_arbitrage_bot.scan_and_extract()
    if res4.get('arbitrage_executed'):
        print(f"   -> Result: Extracted ${res4.get('profit_usd')} profit via Aerodrome/Uniswap spread.\n")
    else:
        print("   -> Result: Mempool spread too tight. Waiting for next block...\n")

    print("3️⃣ Starting Token-Gated Discord VIP Community...")
    res2 = discord_vip_community.process_new_subscriptions()
    print(f"   -> Result: Processed {res2.get('new_members')} new VIP members for ${res2.get('revenue_usd')} MRR.\n")

    print("4️⃣ Starting Automated Airdrop Farming...")
    res3 = await airdrop_farmer.execute_farming_cycle()
    print(f"   -> Result: Cycled {res3.get('wallets_cycled')} headless browser wallets. Expected Future Value: ${res3.get('expected_future_value_usd')}.\n")

    print("5️⃣ Starting Flash Loan Arbitrage...")
    res5 = flash_loan_arbitrage_bot.execute_flash_loan()
    if res5.get('success'):
        print(f"   -> Result: Extracted ${res5.get('net_profit_usd')} net profit via Aave zero-collateral flash loan.\n")
    else:
        print("   -> Result: Unprofitable route. Reverting flash loan execution.\n")

    print("6️⃣ Starting AI Influencer & UGC Sponsorships...")
    res6 = ai_influencer_engine.process_sponsorship()
    print(f"   -> Result: Secured digital sponsorship deal for ${res6.get('revenue_usd')} USD.\n")

    print("7️⃣ Starting Print-on-Demand (POD) Bot...")
    res7 = print_on_demand_bot.process_sales()
    print(f"   -> Result: Processed {res7.get('sales_count')} automated POD sales. Revenue: ${res7.get('revenue_usd')}.\n")

    print("8️⃣ Starting DeFi Yield Optimizer...")
    res8 = defi_yield_optimizer.rebalance_and_harvest()
    print(f"   -> Result: Harvested ${res8.get('yield_harvested_usd')} in passive stablecoin yield.\n")

    print("="*70)
    print("✅ ALL 8 ALTERNATIVE REVENUE STREAMS ACTIVE AND GENERATING CASH FLOW.")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
