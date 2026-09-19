import os
import json
import time
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.repo_radar.subagents import (
    DependabotSecuritySubAgent,
    BreakingReleaseSubAgent,
    PRReviewWatchdogSubAgent,
    REPO_ALERTS_FILE
)

class RepoRadarAgent(BaseAgent):
    """
    Employee #12: GitHub Sentinel & Dependency Breaking-Change Watchdog
    - Audits agency repos for critical Dependabot CVE alerts
    - Monitors Next.js, Flutter, FastAPI, and Firebase breaking releases
    - Tracks pending PRs, unmerged branches, and client reviews
    """
    def __init__(self):
        super().__init__(
            agent_id="repo_radar",
            name="GitHub Sentinel & Breaking-Change Watchdog",
            description="Audits production codebases for critical Dependabot CVE vulnerabilities, tracks major framework updates (Next.js, Flutter), and monitors pending PR reviews.",
            icon="target",
            schedule_minutes=180
        )
        self.config = {
            "TRACKED_FRAMEWORKS": "Next.js, React, Tailwind CSS, Python, FastAPI",
            "MONITORED_PROJECTS": "Agents (Nexus Autonomous Workforce Engine), eco-travellounge.mu",
            "ALERT_ON_CRITICAL_CVE": True,
            "MOBILE_NUMBER": "+230 58169420",
            "CHECK_STALE_BRANCHES": True
        }
        self.stats = {
            "critical_cves": 1,
            "major_releases": 2,
            "pending_prs": 2,
            "scans_completed": 8
        }
        self._register_subagents()

    def _register_subagents(self):
        self.register_subagent(DependabotSecuritySubAgent())
        self.register_subagent(BreakingReleaseSubAgent())
        self.register_subagent(PRReviewWatchdogSubAgent())

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "TRACKED_FRAMEWORKS",
                "label": "Monitored Tech Stack Frameworks",
                "type": "text",
                "default": "next.js,flutter,fastapi,firebase,tailwind",
                "description": "Comma-separated list of frameworks to track for breaking changes"
            },
            {
                "key": "ALERT_ON_CRITICAL_CVE",
                "label": "Instant Mobile Alert on Critical CVE",
                "type": "boolean",
                "default": True,
                "description": "Dispatch high-urgency WhatsApp notification when critical zero-day is found"
            },
            {
                "key": "CHECK_STALE_BRANCHES",
                "label": "Audit Stale Branches & Open PRs",
                "type": "boolean",
                "default": True,
                "description": "Flag pull requests awaiting code review longer than 48 hours"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Saved", file_used="repo_radar/agent.py", message="Repo Radar tracking parameters updated", level="SUCCESS")
        return True

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Critical CVEs Found", "value": self.stats["critical_cves"], "color": "red" if self.stats["critical_cves"] > 0 else "green"},
            {"title": "Major Framework Updates", "value": self.stats["major_releases"], "color": "blue"},
            {"title": "Pending PR Reviews", "value": self.stats["pending_prs"], "color": "amber"},
            {"title": "Audits Run", "value": self.stats["scans_completed"], "color": "blue"}
        ]

    def get_alerts(self) -> Dict[str, Any]:
        if os.path.exists(REPO_ALERTS_FILE):
            try:
                with open(REPO_ALERTS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def run_cycle(self) -> Dict[str, Any]:
        self.log(step="Audit Repos", file_used="repo_radar/agent.py", message="Auditing codebases for CVE security alerts & framework deprecations...", level="INFO")

        # 1. Check Dependabot Security
        sec_res = self.run_subagent("dependabot_security")
        critical_cves = sec_res.get("data", {}).get("critical_high_count", 0)
        self.stats["critical_cves"] = critical_cves

        # 2. Check Breaking Releases
        frameworks = [f.strip() for f in self.config.get("TRACKED_FRAMEWORKS", "").split(",") if f.strip()]
        rel_res = self.run_subagent("breaking_release_watcher", {"frameworks": frameworks})
        releases = rel_res.get("data", {}).get("releases", [])
        self.stats["major_releases"] = len(releases)

        # 3. Check Pending PRs
        pr_res = self.run_subagent("pr_review_watchdog")
        pending_prs = pr_res.get("data", {}).get("pending_count", 0)
        self.stats["pending_prs"] = pending_prs

        # Compile and save alerts
        combined_report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "critical_cves": sec_res.get("data", {}).get("alerts", []),
            "framework_updates": releases,
            "pending_prs": pr_res.get("data", {}).get("items", [])
        }

        with open(REPO_ALERTS_FILE, "w", encoding="utf-8") as f:
            json.dump(combined_report, f, indent=2, ensure_ascii=False)

        self.stats["scans_completed"] += 1
        self.log(step="Radar Report Ready", file_used="repo_radar_alerts.json", message=f"Audit complete: {critical_cves} CVEs, {len(releases)} framework updates, {pending_prs} PRs awaiting review", level="ACTION")

        # Immediate WhatsApp P1 Alert on Critical CVE
        if critical_cves > 0 and self.config.get("ALERT_ON_CRITICAL_CVE"):
            try:
                from core.agent_manager import AgentManager
                dispatcher = AgentManager().get_agent("mobile_dispatcher")
                if dispatcher and hasattr(dispatcher, "send_notification"):
                    first_cve = sec_res.get("data", {}).get("alerts", [{}])[0]
                    cve_desc = first_cve.get("description", "Vulnerability detected")
                    pkg = first_cve.get("package", "dependency")
                    dispatcher.send_notification(
                        title="🚨 P1 Security Alert: Critical CVE Found",
                        message=f"Critical CVE detected in '{pkg}' on production branch. {cve_desc}. Fix recommendation available in Web Command Center.",
                        urgency="P1"
                    )
            except Exception:
                pass

        return {
            "status": "Success",
            "critical_cves": critical_cves,
            "framework_updates": len(releases),
            "pending_prs": pending_prs
        }
