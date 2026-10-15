"""
CompetitorPoacher: CLI Entrypoint with Live Stream UI
===================================================
"""

import asyncio
import argparse
import sys
from poacher.core.orchestrator import PoacherOrchestrator

def main():
    parser = argparse.ArgumentParser(description="CompetitorPoacher: High-speed competitive reconnaissance micro-engine")
    parser.add_argument("competitor", help="Target competitor name")
    parser.add_argument("domain", help="Target competitor domain")
    args = parser.parse_args()

    print(f"\n[CompetitorPoacher Engine] Initializing reconnaissance swarm against {args.competitor} ({args.domain})...\n")

    orchestrator = PoacherOrchestrator()
    card = asyncio.run(orchestrator.execute_poaching_campaign(args.competitor, args.domain))

    print("=" * 65)
    print(f"COMPETITOR POACHER CARD: {card.competitor_name}")
    print("=" * 65)
    print(f"Target Domain      : {card.target_domain}")
    print(f"Poaching Score     : {card.poaching_score}% (High Opportunity)")
    print(f"Tech Stack         : {', '.join(card.tech_stack)}")
    print(f"Key Talent Roster  : {len(card.talent_roster)} rival employees identified")
    for t in card.talent_roster:
        print(f"  - {t.name} ({t.title}) | Flight Risk: {t.flight_risk_score*100}% | Email: {t.synthesized_email}")
    print(f"Churn Signals      : {len(card.churn_signals)} review friction points detected")
    for s in card.churn_signals:
        print(f"  - [{s.source_platform} Rating {s.rating}/5] {s.pain_category}: \"{s.review_snippet}\"")
    print(f"Contract Tenders   : {len(card.contract_tenders)} public tenders tracked")
    print("=" * 65)
    print("✔ Competitor card successfully synthesized, scored, and committed to database!\n")

if __name__ == "__main__":
    main()
