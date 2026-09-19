"""
Nexus Workforce -- Data Access Layer (DAL)
==========================================
Single unified interface for all runtime data I/O.
Swap load()/save() internals for Supabase with zero agent/route refactoring.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("Nexus.DAL")

DATA_DIR = Path("data")
LOGS_DIR = Path("logs")
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

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
}


def path(key: str) -> Path:
    """Return the filesystem path for a given DAL key."""
    p = _REGISTRY.get(key)
    if p is None:
        raise KeyError(f"Unknown DAL key: {key!r}. Register it in core/dal.py")
    return p


def exists(key: str) -> bool:
    """Return True if the backing file exists."""
    return path(key).exists()


def load(key: str, default: Any = None) -> Any:
    """
    Load JSON for key. Returns default if missing or malformed.
    default=None auto-returns [] for safety.
    """
    p = path(key)
    if not p.exists():
        return default if default is not None else []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("DAL load failed for %r: %s", key, e)
        return default if default is not None else []


def save(key: str, data: Any) -> None:
    """
    Persist data as JSON. Uses atomic tmp+rename to prevent corruption on crash.
    """
    p = path(key)
    tmp = p.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp.replace(p)
    except OSError as e:
        logger.error("DAL save failed for %r: %s", key, e)
        if tmp.exists():
            tmp.unlink(missing_ok=True)
        raise


def append(key: str, entry: Any, max_items: int = 500) -> None:
    """Prepend entry to a list, capped at max_items. For event logs and decision feeds."""
    items = load(key, default=[])
    if not isinstance(items, list):
        items = []
    items.insert(0, entry)
    save(key, items[:max_items])


def migrate_root_files() -> dict:
    """
    One-shot migration: move legacy root-level JSON files into data/.
    Safe to call on every boot -- skips files already migrated.
    Returns {old_path: new_path} for all moved files.
    """
    moved = {}
    for key, dest in _REGISTRY.items():
        src = Path(dest.name)
        if src.exists() and not dest.exists():
            try:
                src.rename(dest)
                moved[str(src)] = str(dest)
                logger.info("Migrated %s to %s", src, dest)
            except OSError as e:
                logger.warning("Could not migrate %s: %s", src, e)
    return moved
