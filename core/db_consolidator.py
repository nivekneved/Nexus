# -*- coding: utf-8 -*-
"""
Phase 1: Database & Storage Consolidator for Nexus Workforce.
Migrates loose state files into the primary SQLite database (`universal_records` table),
cleans up redundant `.bak` files, prunes historical snapshot archives, and executes VACUUM.
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
import sqlite3
import json
import glob
import shutil
from core.paths import SQLITE_DB_PATH, DATA_DIR

DB_PATH = str(SQLITE_DB_PATH)

def init_universal_table():
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("""
        CREATE TABLE IF NOT EXISTS universal_records (
            id TEXT PRIMARY KEY,
            domain TEXT NOT NULL,
            record_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            payload JSON NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_universal_domain ON universal_records(domain);")
    c.execute("CREATE INDEX IF NOT EXISTS idx_universal_type ON universal_records(record_type);")
    conn.commit()
    return conn

def migrate_json_stores(conn):
    c = conn.cursor()
    stores_to_migrate = [
        ("memory/archival_memory.json", "memory", "archival_memory"),
        ("memory/recall_memory.json", "memory", "recall_memory"),
        ("data/social_broadcast_queue.json", "comms", "broadcast_queue"),
        ("products/custom_catalog.json", "commerce", "product_catalog"),
        ("reports/fleet_run_summary.json", "operations", "fleet_run_summary")
    ]

    migrated_count = 0
    for path, domain, rtype in stores_to_migrate:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                record_id = f"{domain}_{rtype}"
                payload_str = json.dumps(data)
                c.execute("""
                    INSERT INTO universal_records (id, domain, record_type, status, payload, updated_at)
                    VALUES (?, ?, ?, 'active', ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(id) DO UPDATE SET
                        payload=excluded.payload,
                        updated_at=CURRENT_TIMESTAMP;
                """, (record_id, domain, rtype, payload_str))
                migrated_count += 1
                print(f"  ✓ Migrated {path} -> universal_records [id={record_id}]")
            except Exception as e:
                print(f"  ✗ Error migrating {path}: {e}")

    conn.commit()
    return migrated_count

def clean_bak_files():
    baks = glob.glob("**/*.bak", recursive=True)
    removed = 0
    for b in baks:
        try:
            os.remove(b)
            removed += 1
        except Exception as e:
            pass
    print(f"  ✓ Purged {removed} orphaned .bak files across workspace.")
    return removed

def prune_old_backups():
    # Keep the 3 newest snapshot folders, remove older ones to drastically cut disk footprint
    backups_dir = "backups"
    if not os.path.exists(backups_dir):
        return 0

    subdirs = []
    for entry in os.scandir(backups_dir):
        if entry.is_dir() and (entry.name.startswith("snapshot_") or entry.name.startswith("backup_")):
            subdirs.append(entry.path)

    # Sort descending (newest first)
    subdirs.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    retained = subdirs[:3]
    to_delete = subdirs[3:]

    deleted_count = 0
    for p in to_delete:
        try:
            shutil.rmtree(p)
            deleted_count += 1
        except Exception as e:
            pass

    print(f"  ✓ Retained {len(retained)} latest snapshots; pruned {deleted_count} historical snapshot folders.")
    return deleted_count

def vacuum_database(conn):
    try:
        conn.commit()
        conn.close()
        # Fresh connection for vacuum
        fresh_conn = sqlite3.connect(DB_PATH)
        fresh_conn.execute("VACUUM;")
        fresh_conn.execute("PRAGMA optimize;")
        fresh_conn.close()
        print(f"  ✓ Executed VACUUM & PRAGMA optimize on {DB_PATH}.")
    except Exception as e:
        print(f"  ✗ Vacuum warning: {e}")

def run_phase1():
    print("=" * 60)
    print("⚡ EXECUTING PHASE 1: DATABASE & STORAGE CONSOLIDATION")
    print("=" * 60)
    conn = init_universal_table()
    migrated = migrate_json_stores(conn)
    baks_cleaned = clean_bak_files()
    pruned_dirs = prune_old_backups()
    vacuum_database(conn)
    print("=" * 60)
    print("✅ PHASE 1 COMPLETE: Storage unified, bloat pruned.")
    print("=" * 60)

if __name__ == "__main__":
    run_phase1()
