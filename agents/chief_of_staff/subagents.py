import os
import re
import json
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.subagent import BaseSubAgent
from core.agent_manager import AgentManager

class GitPulseHarvesterSubAgent(BaseSubAgent):
    """
    Subagent 1: Harvester of multi-project Git status, uncommitted files, branches, and TODOs.
    """
    def __init__(self):
        super().__init__(
            subagent_id="chief_git_pulse_harvester",
            name="Git Pulse Harvester SubAgent",
            parent_agent_id="chief_of_staff",
            description="Audits git branches, dirty status, uncommitted changes, recent commits, and open TODO items across workspaces."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        project_path = payload.get("project_path", "")
        max_commits = payload.get("max_commits", 3)

        if not os.path.exists(project_path):
            return {
                "exists": False,
                "path": project_path,
                "name": os.path.basename(project_path) or project_path,
                "status": "Directory not found on current filesystem"
            }

        status_info = {
            "exists": True,
            "path": project_path,
            "name": os.path.basename(project_path) or project_path,
            "branch": "unknown",
            "is_dirty": False,
            "uncommitted_files_count": 0,
            "recent_commits": [],
            "open_todos_count": 0
        }

        # Query Git Branch
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if res.returncode == 0:
                status_info["branch"] = res.stdout.strip()
        except Exception:
            pass

        # Query Git Status (Dirty state)
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if res.returncode == 0:
                dirty_lines = [l for l in res.stdout.split("\n") if l.strip()]
                status_info["is_dirty"] = len(dirty_lines) > 0
                status_info["uncommitted_files_count"] = len(dirty_lines)
        except Exception:
            pass

        # Query Recent Commits
        try:
            res = subprocess.run(
                ["git", "log", f"-n{max_commits}", "--pretty=format:%h - %s (%cr)"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if res.returncode == 0:
                status_info["recent_commits"] = [c.strip() for c in res.stdout.split("\n") if c.strip()]
        except Exception:
            pass

        # Scan for TODOs in root files
        todo_count = 0
        try:
            for item in os.listdir(project_path)[:30]:
                ipath = os.path.join(project_path, item)
                if os.path.isfile(ipath) and not item.startswith("."):
                    try:
                        with open(ipath, "r", encoding="utf-8", errors="ignore") as f:
                            text = f.read(50000)
                            todo_count += len(re.findall(r"\b(TODO|FIXME)\b", text, re.IGNORECASE))
                    except Exception:
                        pass
        except Exception:
            pass
        status_info["open_todos_count"] = todo_count

        return status_info


class StandupDossierSynthesizerSubAgent(BaseSubAgent):
    """
    Subagent 2: Synthesizes harvested multi-project telemetry into an executive standup briefing.
    """
    def __init__(self):
        super().__init__(
            subagent_id="chief_standup_synthesizer",
            name="Standup Dossier Synthesizer SubAgent",
            parent_agent_id="chief_of_staff",
            description="Compiles multi-workspace git telemetry into formatted executive morning standup briefings with priority action items."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        harvested = payload.get("harvested_projects", [])
        user_phone = payload.get("user_phone", "+230 58169420")
        total_projects = len(harvested)

        summary_lines = [
            f"☀️ *NEXUS EXECUTIVE STANDUP BRIEF* ({datetime.now().strftime('%d %b %Y, %H:%M')})",
            f"Active Projects Monitored: {total_projects} | WhatsApp Mobile: {user_phone}\n"
        ]

        active_branches = set()
        dirty_projects = 0
        total_todos = 0

        for item in harvested:
            if not item.get("exists"):
                continue
            name = item.get("name", "Project")
            branch = item.get("branch", "main")
            active_branches.add(branch)
            is_dirty = item.get("is_dirty", False)
            if is_dirty:
                dirty_projects += 1
            dirty_msg = "⚠️ Uncommitted work pending" if is_dirty else "✅ Clean working tree"
            files_count = item.get("uncommitted_files_count", 0)
            todos = item.get("open_todos_count", 0)
            total_todos += todos
            
            summary_lines.append(f"📌 *{name}* (Branch: `{branch}`)")
            summary_lines.append(f"  • Status: {dirty_msg} ({files_count} file(s) changed)")
            if item.get("recent_commits"):
                summary_lines.append(f"  • Last Commit: {item['recent_commits'][0]}")
            if todos > 0:
                summary_lines.append(f"  • Action items: {todos} open TODOs found")
            summary_lines.append("")

        summary_lines.append("🎯 *Recommended Focus Today:*")
        summary_lines.append("1. Verify App Store Sentinel pre-flight audit for live event readiness.")
        if dirty_projects > 0:
            summary_lines.append(f"2. Commit or stash pending changes across {dirty_projects} dirty repositories.")
        else:
            summary_lines.append("2. All active working trees clean. Safe to proceed with feature branches.")
        summary_lines.append("3. Review priority client inquiries in Customer Support queue.")

        brief_text = "\n".join(summary_lines)

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "projects_count": total_projects,
            "active_branches_count": len(active_branches),
            "dirty_projects_count": dirty_projects,
            "total_todos_count": total_todos,
            "brief_text": brief_text
        }


class MorningStandupDispatcherSubAgent(BaseSubAgent):
    """
    Subagent 3: Persists standup briefs to disk and dispatches to mobile channels.
    """
    def __init__(self):
        super().__init__(
            subagent_id="chief_standup_dispatcher",
            name="Morning Standup Dispatcher SubAgent",
            parent_agent_id="chief_of_staff",
            description="Persists latest standup briefs to JSON and dispatches mobile alerts to Deven's WhatsApp."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        brief_data = payload.get("brief_data", {})
        file_path = payload.get("file_path", "latest_standup_brief.json")
        auto_dispatch = payload.get("auto_dispatch", True)

        # Write to disk
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(brief_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            return {"success": False, "error": str(e)}

        dispatched_to_mobile = False
        if auto_dispatch:
            manager = AgentManager()
            dispatcher = manager.get_agent("mobile_dispatcher")
            if dispatcher and hasattr(dispatcher, "send_notification"):
                dispatcher.send_notification(
                    title="☀️ Nexus Morning Standup Brief",
                    message=brief_data.get("brief_text", "Morning brief ready."),
                    urgency="Daily Brief"
                )
                dispatched_to_mobile = True

        return {
            "success": True,
            "file_written": file_path,
            "dispatched_to_mobile": dispatched_to_mobile
        }
