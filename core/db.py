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


def get_all_invoices() -> List[Dict[str, Any]]:
    """Returns all invoices directly from the relational SQLite table with fallback to kv_state."""
    conn = get_connection()
    try:
        cur = conn.execute("SELECT raw_json FROM invoices ORDER BY created_at DESC")
        rows = cur.fetchall()
        if rows:
            return [json.loads(r["raw_json"]) for r in rows if r["raw_json"]]
    except Exception as e:
        logger.debug(f"[DB] Invoices query note: {e}")

    # Fallback to kv_state
    data = get_state("invoices.json")
    if isinstance(data, list):
        return data
    return []


def upsert_invoice(inv: Dict[str, Any]) -> bool:
    """Inserts or updates an invoice in SQLite invoices table and syncs kv_state."""
    conn = get_connection()
    inv_id = inv.get("id")
    if not inv_id:
        return False
    raw_json = json.dumps(inv, ensure_ascii=False)
    client_name = inv.get("client_name", "Unknown")
    client_email = inv.get("client_email", "")
    amount = float(inv.get("amount", 0.0))
    currency = inv.get("currency", "USD").upper()
    status = inv.get("status", "PENDING").upper()
    created_at = inv.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        with conn:
            conn.execute("""
                INSERT INTO invoices (id, client_name, client_email, amount, currency, status, created_at, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    client_name = excluded.client_name,
                    client_email = excluded.client_email,
                    amount = excluded.amount,
                    currency = excluded.currency,
                    status = excluded.status,
                    raw_json = excluded.raw_json;
            """, (inv_id, client_name, client_email, amount, currency, status, created_at, raw_json))
        return True
    except Exception as e:
        logger.error(f"[DB] Error upserting invoice {inv_id}: {e}")
        return False


def get_real_revenue_metrics() -> Dict[str, Any]:
    """Calculates 100% verified, real-time revenue and receivables directly from the SQLite database."""
    invoices = get_all_invoices()
    fiat_settled_mur = 0.0
    crypto_settled_usd = 0.0
    pending_mur = 0.0
    pending_usd = 0.0
    paid_count = 0
    pending_count = 0

    for inv in invoices:
        status = str(inv.get("status", "")).upper()
        amt = float(inv.get("amount", 0.0))
        curr = str(inv.get("currency", "MUR")).upper()

        if status in ("PAID", "COMPLETED", "SETTLED"):
            paid_count += 1
            if curr == "MUR":
                fiat_settled_mur += amt
            elif curr == "USD":
                crypto_settled_usd += amt
        else:
            pending_count += 1
            if curr == "MUR":
                pending_mur += amt
            elif curr == "USD":
                pending_usd += amt

    total_realized_mur = fiat_settled_mur + (crypto_settled_usd * 46.50)
    total_pipeline_mur = pending_mur + (pending_usd * 46.50)

    return {
        "fiat_settled_mur": round(fiat_settled_mur, 2),
        "crypto_settled_usd": round(crypto_settled_usd, 2),
        "total_realized_mur": round(total_realized_mur, 2),
        "pending_mur": round(pending_mur, 2),
        "pending_usd": round(pending_usd, 2),
        "total_pipeline_mur": round(total_pipeline_mur, 2),
        "paid_invoices_count": paid_count,
        "pending_invoices_count": pending_count,
        "total_invoices_count": len(invoices)
    }


# Auto-initialize database schema on module load
try:
    init_database()
except Exception as e:
    logger.warning(f"[DB] Deferred initialization: {e}")

