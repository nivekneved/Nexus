"""
Nexus Workforce -- Data Access Layer (DAL)
==========================================
Unified interface for all runtime data I/O.
Backbone powered by SQLite WAL (Write-Ahead Logging) with atomic JSON synchronization.
"""

import json
import logging
from pathlib import Path
from typing import Any
from core.paths import DATA_DIR, LOGS_DIR
from core.db import get_state, set_state

logger = logging.getLogger("Nexus.DAL")

_REGISTRY: dict[str, Path] = {
    "invoices":             DATA_DIR / "invoices.json",
    "leads":                DATA_DIR / "leads_pipeline.json",
    "trash_ledger":         DATA_DIR / "trash_ledger.json",
    "partner_decisions":    DATA_DIR / "partner_decisions.json",
    "addons_state":         DATA_DIR / "addons_state.json",
    "autopilot_state":      DATA_DIR / "autopilot_state.json",
    "subscriptions":        DATA_DIR / "subscriptions_catalog.json",
    "revenue_blueprints":   DATA_DIR / "revenue_blueprints.json",
    "mobile_notifications": DATA_DIR / "mobile_notifications.json",
    "overnight_activity":   DATA_DIR / "overnight_activity.json",
    "spec_audit_reports":   DATA_DIR / "spec_audit_reports.json",
    "repo_radar_alerts":    DATA_DIR / "repo_radar_alerts.json",
    "infra_finance":        DATA_DIR / "infra_finance_audit.json",
    "localization":         DATA_DIR / "localization_audit.json",
    "standup_brief":        DATA_DIR / "latest_standup_brief.json",
    "tech_dossier":         DATA_DIR / "latest_tech_dossier.json",
    "newsletter_digest":    DATA_DIR / "daily_newsletter_digest.json",
    "crypto_wallet":        DATA_DIR / "crypto_wallet.json",
    "crypto_transactions":  DATA_DIR / "crypto_transactions.json",
    "crypto_spend_history": DATA_DIR / "crypto_spend_history.json",
}


def path(key: str) -> Path:
    """Return the filesystem path for a given DAL key."""
    p = _REGISTRY.get(key)
    if p is None:
        # Fallback to key filename in DATA_DIR
        return DATA_DIR / (key if key.endswith(".json") else f"{key}.json")
    return p


def exists(key: str) -> bool:
    """Return True if the backing record exists in SQLite or on disk."""
    p = path(key)
    if get_state(p.name) is not None:
        return True
    return p.exists()


def load(key: str, default: Any = None) -> Any:
    """
    Load data for key. Queries high-concurrency SQLite WAL first, falling back to disk.
    default=None auto-returns [] for safety.
    """
    p = path(key)
    # 1. Primary: High-speed SQLite state
    db_val = get_state(p.name)
    if db_val is not None:
        return db_val

    # 2. Fallback: Disk load and cache into SQLite
    if not p.exists():
        return default if default is not None else []
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        set_state(p.name, data, sync_json=False)
        return data
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("DAL load failed for %r: %s", key, e)
        return default if default is not None else []


def save(key: str, data: Any) -> None:
    """
    Persist data via SQLite WAL engine and sync atomically to disk.
    Guarantees ACID transactions across multiple processes.
    """
    p = path(key)
    success = set_state(p.name, data, sync_json=True)
    if not success:
        logger.error(f"DAL save failed for {key}")
        raise IOError(f"Failed to persist state for {key}")


def append(key: str, entry: Any, max_items: int = 500) -> None:
    """Prepend entry to a list, capped at max_items. For event logs and decision feeds."""
    items = load(key, default=[])
    if not isinstance(items, list):
        items = []
    items.insert(0, entry)
    save(key, items[:max_items])
