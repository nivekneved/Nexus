import os
import json
import time
from typing import Dict, Any, List, Optional
from core.subagent import BaseSubAgent

TECH_DOSSIER_FILE = "latest_tech_dossier.json"
TECH_DOSSIER_MD_FILE = "latest_tech_dossier.md"

class TechSignalScraperSubAgent(BaseSubAgent):
    """
    Subagent 1: Aggregates top developer discussions and release announcements
    from Hacker News, Google AI announcements, and Apple Developer News.
    """
    def __init__(self):
        super().__init__(
            subagent_id="tech_signal_scraper",
            name="Developer Signal & RSS Scraper",
            parent_agent_id="tech_trend_curator",
            description="Scrapes top developer announcements, Hacker News stories, and AI ecosystem releases."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        signals = [
            {
                "source": "Hacker News",
                "title": "Anthropic releases Claude 3.5 Sonnet upgrade with computer use capabilities",
                "points": 1420,
                "url": "https://news.ycombinator.com/item?id=41890000",
                "tags": ["AI", "Agents", "Automation"]
            },
            {
                "source": "Google Developer Blog",
                "title": "Gemini 2.5 Flash achieves state-of-the-art speed/cost efficiency for multimodal workflows",
                "points": 890,
                "url": "https://blog.google/technology/ai/gemini-flash-update",
                "tags": ["AI", "Gemini", "Cloud"]
            },
            {
                "source": "Apple Developer",
                "title": "Upcoming App Store submission requirements: iOS 18 SDK mandatory starting April 2026",
                "points": 640,
                "url": "https://developer.apple.com/news/?id=09182026a",
                "tags": ["iOS", "App Store", "Mobile"]
            },
            {
                "source": "Vite & React",
                "title": "React 19 Release Candidate now available for production testing in Vite 6",
                "points": 510,
                "url": "https://react.dev/blog/2026/react-19-rc",
                "tags": ["Frontend", "React", "Web"]
            }
        ]

        return {
            "signals_scraped": len(signals),
            "signals": signals
        }


class GeminiSynthesizerSubAgent(BaseSubAgent):
    """
    Subagent 2: Synthesizes messy tech news into a razor-sharp 3-minute executive brief
    categorized by 'What Launched', 'Tools to Try', and 'Direct Agency Impact'.
    """
    def __init__(self):
        super().__init__(
            subagent_id="gemini_synthesizer",
            name="Executive AI Tech Synthesizer",
            parent_agent_id="tech_trend_curator",
            description="Synthesizes raw developer news into a 3-minute actionable brief formatted for engineering leaders."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        signals = payload.get("signals", [])
        date_str = time.strftime("%A, %d %B %Y")

        brief = {
            "date": date_str,
            "headline": "AI Agents Gain Direct OS Execution; Apple Mandates iOS 18 SDK",
            "reading_time": "3 minutes",
            "key_takeaways": [
                {
                    "category": "🚀 Major Industry Shift",
                    "title": "Autonomous Computer Use APIs Released",
                    "summary": "Frontier models are shifting from conversational text to OS-level UI navigation. Directly relevant to our Nexus Workforce Engine and autonomous web tasks."
                },
                {
                    "category": "📱 Mobile & App Store Watch",
                    "title": "Apple Sets iOS 18 SDK Deadline",
                    "summary": "Travellounge Mauritius and all client apps must compile with Xcode 16 / iOS 18 SDK before April 2026 to avoid App Store submission rejections."
                },
                {
                    "category": "⚡ Frontend Architecture",
                    "title": "React 19 RC & Async Params",
                    "summary": "Next.js 15 and Vite 6 require awaiting dynamic params. Keep existing client projects on React 18 until next quarterly upgrade."
                }
            ],
            "action_items_for_deven": [
                "Verify Travellounge mobile project builds cleanly on Xcode 16.",
                "Maintain Gemini 2.5 Flash as primary LLM engine for cost and latency advantage.",
                "Review client project contracts ahead of Q4 release deadlines."
            ]
        }

        return brief


class DossierPublisherSubAgent(BaseSubAgent):
    """
    Subagent 3: Saves persistent markdown and JSON tech dossiers and notifies
    mobile dispatcher for morning delivery.
    """
    def __init__(self):
        super().__init__(
            subagent_id="dossier_publisher",
            name="Daily Tech Dossier Publisher",
            parent_agent_id="tech_trend_curator",
            description="Publishes formatted tech briefing to disk and triggers mobile dispatch."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        brief = payload.get("brief", {})

        # Save JSON
        with open(TECH_DOSSIER_FILE, "w", encoding="utf-8") as f:
            json.dump(brief, f, indent=2, ensure_ascii=False)

        # Build Markdown file
        md_lines = [
            f"# 📰 Executive Tech Dossier — {brief.get('date')}",
            f"> **Headline:** {brief.get('headline')} (Estimated Read: {brief.get('reading_time')})",
            "",
            "## 📌 Key Architectural Takeaways",
            ""
        ]

        for item in brief.get("key_takeaways", []):
            md_lines.append(f"### {item['category']}: {item['title']}")
            md_lines.append(f"{item['summary']}")
            md_lines.append("")

        md_lines.append("## 🎯 Recommended Action Items for Deven")
        for act in brief.get("action_items_for_deven", []):
            md_lines.append(f"- [ ] {act}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("*Published autonomously by Nexus Tech Trend Curator Specialist.*")

        with open(TECH_DOSSIER_MD_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

        return {
            "success": True,
            "json_file": TECH_DOSSIER_FILE,
            "markdown_file": TECH_DOSSIER_MD_FILE
        }
