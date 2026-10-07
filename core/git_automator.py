"""
Nexus™ Git Automation Service (Inspired by Aider)
==============================================
Automatically creates branches, commits code changes, and manages git logs
for autonomous agent modifications.
"""

import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger("Nexus.GitAutomator")

class GitAutomator:
    @staticmethod
    def commit_changes(file_path: str, commit_message: str) -> Dict[str, Any]:
        try:
            subprocess.run(["git", "add", file_path], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", f"[Nexus Agent] {commit_message}"], check=True, capture_output=True)
            logger.info(f"[GitAutomator] Successfully committed {file_path}: {commit_message}")
            return {"success": True, "message": f"Committed {file_path}"}
        except Exception as e:
            logger.warning(f"[GitAutomator] Git commit skipped or failed: {e}")
            return {"success": False, "error": str(e)}

git_automator = GitAutomator()
