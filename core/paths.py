"""
Nexus Architecture — Unified Canonical Paths
============================================
Single-source deterministic paths for all runtime operations.
Eliminates ambiguity, multi-location fallback searches, and working directory drift.
"""

import os
from pathlib import Path

# Absolute Anchor to Workspace Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Core Operational Directories
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
DOCS_DIR = BASE_DIR / "docs"
REPORTS_DIR = BASE_DIR / "reports"
STATIC_DIR = BASE_DIR / "static"
SCRIPTS_DIR = BASE_DIR / "scripts"
BACKUPS_DIR = BASE_DIR / "backups"

# Ensure all essential runtime directories exist
for _directory in (DATA_DIR, LOGS_DIR, DOCS_DIR, REPORTS_DIR, STATIC_DIR, SCRIPTS_DIR, BACKUPS_DIR):
    _directory.mkdir(parents=True, exist_ok=True)

# Primary Local SQLite Database File
SQLITE_DB_PATH = DATA_DIR / "nexus_workforce.db"

def resolve_data_path(filename_or_path: str | Path) -> Path:
    """
    Deterministically resolves a data file to an absolute path within DATA_DIR.
    Prevents relative traversal attacks or split-brain directory drift.
    """
    p = Path(filename_or_path)
    if p.is_absolute():
        return p
    return DATA_DIR / p.name

def resolve_log_path(filename_or_path: str | Path) -> Path:
    """Deterministically resolves a log file within LOGS_DIR."""
    p = Path(filename_or_path)
    if p.is_absolute():
        return p
    return LOGS_DIR / p.name
