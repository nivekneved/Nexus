import os
import shutil
import json
import re
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.subagent import BaseSubAgent

BACKUPS_DIR = "backups"
BACKUP_MANIFEST_FILE = "backups/manifest.json"

class WorkspaceSnapshotSubAgent(BaseSubAgent):
    """
    Subagent 1: Creates an isolated, instant rollback snapshot of git state and critical databases.
    """
    def __init__(self):
        super().__init__(
            subagent_id="sentinel_workspace_snapshot",
            name="Workspace Snapshot SubAgent",
            parent_agent_id="regression_sentinel",
            description="Captures Git branch, HEAD commit, uncommitted diffs, and backs up critical database and config files."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        reason = payload.get("reason", "Routine Safety Snapshot")
        backup_dir = payload.get("backup_dir", BACKUPS_DIR)
        critical_files_str = payload.get("critical_files", "email_accounts.json,support_tickets.json,.env,trash_ledger.json")
        max_retained = int(payload.get("max_retained", 10))

        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_id = f"snap_{timestamp}"
        target_dir = os.path.join(backup_dir, snapshot_id)
        os.makedirs(target_dir, exist_ok=True)

        copied_files = []
        critical_files = [f.strip() for f in critical_files_str.split(",") if f.strip()]
        for cf in critical_files:
            if os.path.exists(cf):
                dest = os.path.join(target_dir, cf)
                shutil.copy2(cf, dest)
                copied_files.append(cf)

        # Capture Git branch & diff
        git_summary = {"branch": "unknown", "head_commit": "unknown"}
        try:
            res_b = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, timeout=5)
            if res_b.returncode == 0:
                git_summary["branch"] = res_b.stdout.strip()

            res_c = subprocess.run(["git", "log", "-1", "--oneline"], capture_output=True, text=True, timeout=5)
            if res_c.returncode == 0:
                git_summary["head_commit"] = res_c.stdout.strip()

            diff_res = subprocess.run(["git", "diff"], capture_output=True, text=True, timeout=5)
            if diff_res.returncode == 0 and diff_res.stdout:
                with open(os.path.join(target_dir, "uncommitted.diff"), "w", encoding="utf-8") as df:
                    df.write(diff_res.stdout)
        except Exception:
            pass

        record = {
            "id": snapshot_id,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": reason,
            "files_saved": copied_files,
            "git": git_summary,
            "snapshot_path": target_dir
        }

        # Update manifest
        manifest = []
        if os.path.exists(BACKUP_MANIFEST_FILE):
            try:
                with open(BACKUP_MANIFEST_FILE, "r", encoding="utf-8") as mf:
                    manifest = json.load(mf)
            except Exception:
                manifest = []
        manifest.insert(0, record)

        # Prune old backups
        if len(manifest) > max_retained:
            prune_candidates = manifest[max_retained:]
            manifest = manifest[:max_retained]
            for p in prune_candidates:
                p_path = p.get("snapshot_path")
                if p_path and os.path.exists(p_path):
                    shutil.rmtree(p_path, ignore_errors=True)

        with open(BACKUP_MANIFEST_FILE, "w", encoding="utf-8") as mf:
            json.dump(manifest, mf, indent=2, ensure_ascii=False)

        return record


class RunawayPollAuditorSubAgent(BaseSubAgent):
    """
    Subagent 2: Scans client and frontend code for aggressive polling or unthrottled request loops.
    """
    def __init__(self):
        super().__init__(
            subagent_id="sentinel_runaway_poll_auditor",
            name="Runaway Poll Auditor SubAgent",
            parent_agent_id="regression_sentinel",
            description="Audits JavaScript files for aggressive setInterval/setTimeout loops that cause API overusage."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        min_poll_ms = int(payload.get("min_poll_ms", 3000))
        static_dir = payload.get("static_dir", "static")

        alerts = []
        if os.path.exists(static_dir):
            for file in os.listdir(static_dir):
                if file.endswith(".js"):
                    fpath = os.path.join(static_dir, file)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        for m in re.finditer(r"setInterval\s*\(\s*([^,]+),\s*(\d+)\s*\)", content):
                            ms = int(m.group(2))
                            if ms < min_poll_ms:
                                alerts.append({
                                    "file": file,
                                    "type": "AGGRESSIVE_POLL",
                                    "interval_ms": ms,
                                    "recommendation": f"Increase {ms}ms interval to at least {min_poll_ms}ms to conserve bandwidth."
                                })
                    except Exception:
                        pass

        return {
            "alerts": alerts,
            "alerts_count": len(alerts),
            "is_optimized": len(alerts) == 0
        }


class SnapshotRestoreSubAgent(BaseSubAgent):
    """
    Subagent 3: Executes verified 1-click restoration from snapshot archives.
    """
    def __init__(self):
        super().__init__(
            subagent_id="sentinel_snapshot_restore",
            name="Snapshot Restore SubAgent",
            parent_agent_id="regression_sentinel",
            description="Restores database and configuration files safely from manifest-registered snapshots."
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        snapshot_id = payload.get("snapshot_id", "")
        manifest_file = payload.get("manifest_file", BACKUP_MANIFEST_FILE)

        manifest = []
        if os.path.exists(manifest_file):
            try:
                with open(manifest_file, "r", encoding="utf-8") as mf:
                    manifest = json.load(mf)
            except Exception:
                manifest = []

        target = next((s for s in manifest if s["id"] == snapshot_id), None)
        if not target:
            return {"success": False, "error": f"Snapshot '{snapshot_id}' not found."}

        snap_path = target.get("snapshot_path")
        if not snap_path or not os.path.exists(snap_path):
            return {"success": False, "error": f"Snapshot directory missing: {snap_path}"}

        restored_files = []
        for root, _, files in os.walk(snap_path):
            for file in files:
                if file == "uncommitted.diff":
                    continue
                src = os.path.join(root, file)
                rel = os.path.relpath(src, snap_path)
                shutil.copy2(src, rel)
                restored_files.append(rel)

        return {
            "success": True,
            "snapshot_id": snapshot_id,
            "restored_files": restored_files,
            "restored_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
