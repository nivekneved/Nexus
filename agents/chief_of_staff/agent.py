import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.chief_of_staff.subagents import (
    GitPulseHarvesterSubAgent,
    StandupDossierSynthesizerSubAgent,
    MorningStandupDispatcherSubAgent
)

STANDUP_BRIEF_FILE = "latest_standup_brief.json"

DEFAULT_MONITORED_PROJECTS = [
    {"name": "Travellounge & Eco Platform", "path": r"d:\WEB 2026\Travellounge"},
    {"name": "Eco Travellounge Mobile/Web", "path": r"d:\WEB 2026\eco-travellounge.mu"},
    {"name": "Med360 Healthcare Portal", "path": r"d:\WEB 2026\Med360"},
    {"name": "Enn Rev Enn Sourir NGO", "path": r"d:\WEB 2026\ennrevennsourir"},
    {"name": "Nexus Autonomous Agents Suite", "path": r"c:\Users\deven\OneDrive\Desktop\Agents"}
]

class ChiefOfStaffAgent(BaseAgent):
    """
    Employee #6: Context Chronicler & Morning Chief of Staff
    Harvester of multi-project state, git history, uncommitted changes, and open tasks.
    Solves context-switching fatigue by answering 'Where did I leave off?'
    and dispatching an 08:00 AM executive standup briefing directly to WhatsApp.
    """

    def __init__(self):
        super().__init__(
            agent_id="chief_of_staff",
            name="Context Chronicler & Morning Chief of Staff",
            description="Autonomous cross-project Git tracker & standup coordinator. Answers 'Where did I leave off?' across Med360, Travellounge, and Agents, and dispatches morning WhatsApp briefs.",
            icon="briefcase",
            schedule_minutes=120
        )
        self.config = {
            "MONITORED_DIRECTORIES": "\n".join([p["path"] for p in DEFAULT_MONITORED_PROJECTS]),
            "MORNING_STANDUP_TIME": "08:00",
            "AUTO_DISPATCH_WHATSAPP": True,
            "MAX_RECENT_COMMITS": 3
        }
        self.stats = {
            "projects_tracked": len(DEFAULT_MONITORED_PROJECTS),
            "commits_monitored": 18,
            "active_branches": 5,
            "briefs_generated": 3
        }

        # Register specialized single-task subagents
        self.register_subagent(GitPulseHarvesterSubAgent())
        self.register_subagent(StandupDossierSynthesizerSubAgent())
        self.register_subagent(MorningStandupDispatcherSubAgent())

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "MONITORED_DIRECTORIES",
                "label": "Monitored Project Directories (One per line)",
                "type": "textarea",
                "default": "\n".join([p["path"] for p in DEFAULT_MONITORED_PROJECTS]),
                "description": "Paths to repositories tracked for commits, git status, and TODO audits"
            },
            {
                "key": "MORNING_STANDUP_TIME",
                "label": "Morning Standup Dispatch Time (24h)",
                "type": "text",
                "default": "08:00",
                "description": "Time to dispatch the executive brief to WhatsApp"
            },
            {
                "key": "AUTO_DISPATCH_WHATSAPP",
                "label": "Auto-Dispatch Brief to Mobile (WhatsApp)",
                "type": "boolean",
                "default": True,
                "description": "Forward the morning standup brief directly to Deven's WhatsApp (+230 58169420)"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Update", file_used="chief_of_staff/agent.py", message="Chief of Staff tracking preferences updated", level="SUCCESS")
        return True

    def _get_project_paths(self) -> List[Dict[str, str]]:
        raw = self.config.get("MONITORED_DIRECTORIES", "")
        lines = [line.strip() for line in raw.split("\n") if line.strip()]
        projects = []
        for p in lines:
            name = os.path.basename(p) or p
            projects.append({"name": name, "path": p})
        return projects

    def harvest_project_status(self, project_path: str) -> Dict[str, Any]:
        """Delegates git status harvesting to GitPulseHarvesterSubAgent."""
        return self.run_subagent(
            "chief_git_pulse_harvester",
            {
                "project_path": project_path,
                "max_commits": int(self.config.get("MAX_RECENT_COMMITS", 3))
            }
        )

    def generate_standup_brief(self) -> Dict[str, Any]:
        """Harvests projects and delegates brief synthesis & dispatch to subagents."""
        projects = self._get_project_paths()
        harvested = []
        total_commits = 0

        for p in projects:
            info = self.harvest_project_status(p["path"])
            harvested.append(info)
            if info.get("exists"):
                total_commits += len(info.get("recent_commits", []))

        # Delegate brief compilation to StandupDossierSynthesizerSubAgent
        synth_res = self.run_subagent(
            "chief_standup_synthesizer",
            {
                "harvested_projects": harvested,
                "user_phone": "+230 58169420"
            }
        )

        self.stats["projects_tracked"] = len(projects)
        self.stats["commits_monitored"] = total_commits
        self.stats["active_branches"] = synth_res.get("active_branches_count", 1)

        result = {
            "timestamp": synth_res.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "projects_count": len(projects),
            "projects": harvested,
            "brief_text": synth_res.get("brief_text", "")
        }

        # Delegate persistence and mobile dispatch to MorningStandupDispatcherSubAgent
        self.run_subagent(
            "chief_standup_dispatcher",
            {
                "brief_data": result,
                "file_path": STANDUP_BRIEF_FILE,
                "auto_dispatch": self.config.get("AUTO_DISPATCH_WHATSAPP", True)
            }
        )

        return result

    def run_cycle(self) -> Dict[str, Any]:
        self.log(step="Git Recon", file_used="chief_of_staff/agent.py", message="Scanning repository branches, commits, and diffs via subagents...", level="INFO")
        
        brief = self.generate_standup_brief()
        self.stats["briefs_generated"] += 1
        
        self.log(step="Context Synthesized", file_used=STANDUP_BRIEF_FILE, message=f"Generated executive digest across {brief['projects_count']} workspaces", level="ACTION")
        self.log(step="Standup Complete", file_used="chief_of_staff/agent.py", message="Chief of Staff executive cycle concluded successfully", level="SUCCESS")

        return {
            "status": "Chief of Staff Cycle Completed",
            "projects_scanned": brief["projects_count"],
            "brief": brief
        }

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Tracked Projects", "value": self.stats["projects_tracked"], "color": "blue"},
            {"title": "Commits Tracked", "value": self.stats["commits_monitored"], "color": "green"},
            {"title": "Active Branches", "value": self.stats["active_branches"], "color": "purple"},
            {"title": "Standups Dispatched", "value": self.stats["briefs_generated"], "color": "yellow"}
        ]
