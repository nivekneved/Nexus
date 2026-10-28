import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent

class IdeaHunterAgent(BaseAgent):
    """
    Overnight Startup Research Team (Scout, Analyst, Builder).
    Mines social media, forums, and reviews for real complaints to generate actionable MVP ideas.
    """
    def __init__(self):
        super().__init__(
            agent_id="idea_hunter",
            name="Overnight Startup Research Team",
            description="Mines X, Reddit, app store reviews, G2 and Product Hunt for real complaints to generate actionable startup MVPs.",
            icon="search",
            schedule_minutes=180
        )
        self.config = {
            "TARGET_NICHES": "mobile app devlopment, web dev, booking apps, car rental, travel agencies",
            "AVAILABLE_SKILLS": "native mobile dev, React",
            "BUDGET": "$10",
            "HOURS_PER_WEEK": 20,
            "TARGET_AUDIENCE": "Both B2B and B2C",
            "MIN_PAIN_SCORE": 18,
            "MAX_SCORE": 25
        }

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Executes the overnight research workflow:
        1. Scout: Searches for complaints.
        2. Analyst: Scores and clusters pains.
        3. Builder: Drafts the MVP implementation and go-to-market.
        """
        # 1. SCOUT PHASE
        queries = [
            "\"spreadsheet nightmare\" OR \"hate doing this manually\"",
            "\"is there a tool that\" OR \"wish there was\"",
            "\"still doing this manually\" OR \"doing this manually\""
        ]

        results = []
        for query in queries:
            # Using the newly added nexus_search capability
            search_res = self.nexus_search(query=query, category="web", max_results=10)
            if search_res.get("success"):
                results.append(search_res)

        # 2. ANALYST PHASE (Mock logic - in reality, evaluate results against MIN_PAIN_SCORE)
        # Cluster results into distinct startup pain points

        # 3. BUILDER PHASE
        # Output the formatted MVP proposals

        return {
            "status": "success",
            "message": "Nightly Idea Hunter run completed.",
            "data": results,
            "timestamp": datetime.utcnow().isoformat()
        }

    def run_cycle(self) -> Dict[str, Any]:
        return self.execute()

    def get_stats(self) -> Dict[str, Any]:
        return {
            "target_niches": self.config.get("TARGET_NICHES", ""),
            "min_pain_score": self.config.get("MIN_PAIN_SCORE", 18),
            "status": "ACTIVE"
        }
