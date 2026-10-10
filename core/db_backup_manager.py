# -*- coding: utf-8 -*-
"""
Nexus™ Database Backup & Easy Restore Manager (v35.0)
=====================================================
Manages timestamped SQLite database and JSON ledger backups with 1-click restore capabilities.
"""

import os
import shutil
import time
import logging
from pathlib import Path
from typing import Dict, Any, List
from core.telemetry import telemetry

logger = logging.getLogger("Nexus.DBBackupManager")

BACKUP_DIR = Path("data/backups")
DB_PATH = Path("nexus_workforce.db")

class DBBackupManager:
    def __init__(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    def create_db_backup(self) -> Dict[str, Any]:
        """
        Creates a timestamped backup of SQLite DB and critical JSON ledgers.
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_name = f"nexus_db_backup_{timestamp}"
        target_subfolder = BACKUP_DIR / backup_name
        target_subfolder.mkdir(parents=True, exist_ok=True)

        backed_up_files = []

        # 1. Backup SQLite DB if exists
        if DB_PATH.exists():
            dest_db = target_subfolder / DB_PATH.name
            shutil.copy2(DB_PATH, dest_db)
            backed_up_files.append(str(dest_db))

        # 2. Backup JSON ledgers
        ledger_files = ["treasury_ledger.json", "leads_pipeline.json", "data/invoices.json"]
        for lf in ledger_files:
            p = Path(lf)
            if p.exists():
                dest_lf = target_subfolder / p.name
                shutil.copy2(p, dest_lf)
                backed_up_files.append(str(dest_lf))

        telemetry.emit(
            agent_id="domain_operations",
            agent_name="Operations & System Integrity Domain Controller",
            step="DB_BACKUP_CREATED",
            file_used="core/db_backup_manager.py",
            message=f"Successfully created database backup snapshot at '{target_subfolder}'.",
            level="SUCCESS"
        )

        return {
            "success": True,
            "version": "35.0 DB Backup Manager",
            "backup_id": backup_name,
            "backup_path": str(target_subfolder),
            "backed_up_files": backed_up_files,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "message": f"Database successfully backed up as '{backup_name}'!"
        }

    def list_backups(self) -> List[Dict[str, Any]]:
        """
        Lists all available database backup snapshots.
        """
        backups = []
        if BACKUP_DIR.exists():
            for entry in sorted(BACKUP_DIR.iterdir(), reverse=True):
                if entry.is_dir():
                    files = [f.name for f in entry.iterdir()]
                    backups.append({
                        "backup_id": entry.name,
                        "path": str(entry),
                        "files": files,
                        "created_at": time.ctime(entry.stat().st_mtime)
                    })
        return backups

    def restore_db_backup(self, backup_id: str) -> Dict[str, Any]:
        """
        Restores SQLite DB and JSON ledgers from a specific backup snapshot.
        """
        target_subfolder = BACKUP_DIR / backup_id
        if not target_subfolder.exists() or not target_subfolder.is_dir():
            return {
                "success": False,
                "error": f"Backup snapshot '{backup_id}' not found."
            }

        restored_files = []

        # 1. Restore SQLite DB
        src_db = target_subfolder / DB_PATH.name
        if src_db.exists():
            shutil.copy2(src_db, DB_PATH)
            restored_files.append(str(DB_PATH))

        # 2. Restore JSON ledgers
        for p_name in ["treasury_ledger.json", "leads_pipeline.json", "invoices.json"]:
            src_lf = target_subfolder / p_name
            if src_lf.exists():
                dest_lf = Path("data") / p_name if p_name == "invoices.json" else Path(p_name)
                dest_lf.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_lf, dest_lf)
                restored_files.append(str(dest_lf))

        telemetry.emit(
            agent_id="domain_operations",
            agent_name="Operations & System Integrity Domain Controller",
            step="DB_BACKUP_RESTORED",
            file_used="core/db_backup_manager.py",
            message=f"Successfully restored database snapshot from '{backup_id}'.",
            level="SUCCESS"
        )

        return {
            "success": True,
            "version": "35.0 DB Backup Manager",
            "restored_backup_id": backup_id,
            "restored_files": restored_files,
            "message": f"Database successfully restored from backup '{backup_id}'!"
        }

db_backup_manager = DBBackupManager()
