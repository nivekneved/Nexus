"""
Nexus Workforce — High-Concurrency SQLite Database Engine
==========================================================
Eliminates flat JSON file locks and multi-process corruption risks.
Utilizes SQLite with Write-Ahead Logging (WAL) for safe, concurrent multi-process access.
"""

import os
import json
import sqlite3
import threading
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from core.paths import SQLITE_DB_PATH, DATA_DIR

logger = logging.getLogger("Nexus.DB")

_local = threading.local()

def get_connection() -> sqlite3.Connection:
    """Returns a thread-local SQLite connection configured with WAL and busy timeouts."""
    conn = getattr(_local, "conn", None)
    if conn is None:
        conn = sqlite3.connect(
            str(SQLITE_DB_PATH),
            timeout=30.0,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        # Configure WAL mode for concurrent reads and writes across processes
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        _local.conn = conn
    return conn


def init_database():
    """Initializes tables, indexes, and schema definitions."""
    conn = get_connection()
    with conn:
        # 1. Universal Document / Key-Value Store for all agent states
        conn.execute("""
            CREATE TABLE IF NOT EXISTS kv_state (
                key TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)

        # 2. Relational Invoices Table for high-integrity financial operations
        conn.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id TEXT PRIMARY KEY,
                client_name TEXT,
                client_email TEXT,
                amount REAL,
                currency TEXT,
                status TEXT,
                created_at TEXT,
                raw_json TEXT NOT NULL
            );
        """)

        # 3. High-Integrity Recovery Ledger (Trash & Quarantines)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trash_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT,
                timestamp TEXT,
                sender TEXT,
                subject TEXT,
                category TEXT,
                reason TEXT,
                action TEXT,
                original_folder TEXT
            );
        """)

        # 4. Activity Logs & Telemetry
        conn.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                source TEXT NOT NULL,
                details TEXT NOT NULL
            );
        """)

        conn.execute("CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_activity_time ON activity_logs(timestamp);")


def get_state(key: str, default: Any = None) -> Any:
    """Fetches arbitrary state from SQLite kv_state table."""
    conn = get_connection()
    try:
        cur = conn.execute("SELECT data FROM kv_state WHERE key = ?", (key,))
        row = cur.fetchone()
        if row:
            return json.loads(row["data"])
    except Exception as e:
        logger.error(f"[DB] Error fetching state for key {key}: {e}")
    return default


def set_state(key: str, data: Any, sync_json: bool = True) -> bool:
    """
    Persists arbitrary state atomically into SQLite kv_state.
    Optionally mirrors to data/<key>.json to maintain 100% backward compatibility.
    """
    conn = get_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_str = json.dumps(data, indent=2, ensure_ascii=False)

    try:
        with conn:
            conn.execute("""
                INSERT INTO kv_state (key, data, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    data = excluded.data,
                    updated_at = excluded.updated_at;
            """, (key, json_str, now_str))

        if sync_json:
            # Sync to data/ folder atomically with retry to handle Windows file locking
            try:
                target_json = DATA_DIR / (key if key.endswith(".json") else f"{key}.json")
                tmp_json = target_json.with_suffix(f".tmp_{os.getpid()}_{threading.get_ident()}")
                with open(tmp_json, "w", encoding="utf-8") as f:
                    f.write(json_str)
                    f.flush()
                    try:
                        os.fsync(f.fileno())
                    except OSError:
                        pass
                for _ in range(5):
                    try:
                        os.replace(tmp_json, target_json)
                        break
                    except (PermissionError, OSError):
                        import time
                        time.sleep(0.02)
                else:
                    try:
                        import shutil
                        shutil.copy2(tmp_json, target_json)
                        tmp_json.unlink(missing_ok=True)
                    except Exception:
                        pass
            except Exception as e:
                logger.debug(f"[DB] Non-critical mirror sync note for {key}: {e}")
        return True
    except Exception as e:
        logger.error(f"[DB] Error persisting state for key {key}: {e}")
        return False


def seed_from_json_files():
    """Seeds the SQLite database from any existing JSON files in DATA_DIR on startup."""
    init_database()
    conn = get_connection()
    count = 0
    for jf in DATA_DIR.glob("*.json"):
        key = jf.name
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
            json_str = json.dumps(data, ensure_ascii=False)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with conn:
                conn.execute("""
                    INSERT OR IGNORE INTO kv_state (key, data, updated_at)
                    VALUES (?, ?, ?);
                """, (key, json_str, now_str))
            count += 1
        except Exception as e:
            logger.warning(f"[DB] Could not seed {jf.name} into SQLite: {e}")
    logger.info(f"[DB] Seeded {count} stores into SQLite WAL database.")

# Auto-initialize database schema on module load
try:
    init_database()
except Exception as e:
    logger.warning(f"[DB] Deferred initialization: {e}")
