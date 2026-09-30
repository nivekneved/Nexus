"""
Nexus Architecture — Unified Canonical Paths
============================================
Single-source deterministic paths for all runtime operations.
Eliminates ambiguity, multi-location fallback searches, and working directory drift.
"""

import os
import shutil
import tempfile
from pathlib import Path

# Absolute Anchor to Workspace Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Detect serverless environment (Vercel / AWS Lambda)
IS_SERVERLESS = bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))

# Cross-platform safe temp root (/tmp on Linux/Lambda, %TEMP% on Windows)
TMP_ROOT = Path(tempfile.gettempdir()) / "nexus_runtime"

# Core Operational Directories
if IS_SERVERLESS:
    DATA_DIR = TMP_ROOT / "data"
    LOGS_DIR = TMP_ROOT / "logs"
    DOCS_DIR = BASE_DIR / "docs"
    REPORTS_DIR = TMP_ROOT / "reports"
    STATIC_DIR = BASE_DIR / "static"
    SCRIPTS_DIR = BASE_DIR / "scripts"
    BACKUPS_DIR = TMP_ROOT / "backups"
else:
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    DOCS_DIR = BASE_DIR / "docs"
    REPORTS_DIR = BASE_DIR / "reports"
    STATIC_DIR = BASE_DIR / "static"
    SCRIPTS_DIR = BASE_DIR / "scripts"
    BACKUPS_DIR = BASE_DIR / "backups"

# Ensure all essential runtime directories exist safely
for _directory in (DATA_DIR, LOGS_DIR, DOCS_DIR, REPORTS_DIR, STATIC_DIR, SCRIPTS_DIR, BACKUPS_DIR):
    try:
        _directory.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError):
        pass

# Primary Local SQLite Database File
SQLITE_DB_PATH = DATA_DIR / "nexus_workforce.db"

# Seed data from repository into /tmp on serverless environments
if IS_SERVERLESS:
    source_data_dir = BASE_DIR / "data"
    if source_data_dir.exists():
        try:
            for item in source_data_dir.iterdir():
                dest = DATA_DIR / item.name
                if not dest.exists() and item.is_file():
                    try:
                        shutil.copy2(item, dest)
                    except Exception:
                        pass
        except Exception:
            pass

def resolve_data_path(filename_or_path: str | Path) -> Path:
    """
    Deterministically resolves a data file to an absolute path within DATA_DIR.
    Prevents relative traversal attacks or split-brain directory drift.
    """
    p = Path(filename_or_path)
    if p.is_absolute():
        if IS_SERVERLESS and str(p).startswith(str(BASE_DIR / "data")):
            return DATA_DIR / p.name
        return p
    return DATA_DIR / p.name

def resolve_log_path(filename_or_path: str | Path) -> Path:
    """Deterministically resolves a log file within LOGS_DIR."""
    p = Path(filename_or_path)
    if p.is_absolute():
        if IS_SERVERLESS and str(p).startswith(str(BASE_DIR / "logs")):
            return LOGS_DIR / p.name
        return p
    return LOGS_DIR / p.name

