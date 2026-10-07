import sys
import os
import asyncio
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logging.getLogger("Nexus").setLevel(logging.CRITICAL)

from core.agency_audit_bot import agency_audit_bot
from core.openmontage_video_engine import openmontage_video_engine
from core.autonomous_job_applier import autonomous_job_applier

async def main():
    print("\n" + "="*70)
    print("🚀 ACTIVATING REVENUE BOTS (TONIGHT'S DEADLINE)")
    print("="*70 + "\n")

    print("1️⃣ Starting Agency Audit Bot (Lead Magnet Generation)...")
    res1 = agency_audit_bot.generate_seo_audit("competitor-site.com", "Acme Corp")
    print(f"   -> Result: Generated branded PDF audit targeting ${res1.get('upsell_value_usd')} in upsells.\n")

    print("2️⃣ Starting Faceless Video Montage Engine...")
    res2 = openmontage_video_engine.generate_viral_video_batch("AI SaaS Tips", count=5)
    print(f"   -> Result: Rendered {len(res2.get('files_rendered', []))} viral short-form videos. Expected organic views: {res2.get('estimated_organic_views')}.\n")

    print("3️⃣ Starting Autonomous Browser Job Applier...")
    res3 = await autonomous_job_applier.run_application_sweep()
    print(f"   -> Result: Successfully auto-applied to {res3.get('jobs_applied_count')} freelance gigs. Expected Revenue Pipeline: ${res3.get('expected_revenue_usd')}.\n")

    print("="*70)
    print("✅ ALL THREE NEW AUTOMATION BOTS SUCCESSFULLY EXECUTED.")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
