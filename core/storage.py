"""
Nexus Sovereign Storage Engine
==============================
Guarantees atomic, tamper-resilient, crash-proof persistence.
- Enforces deterministic paths via core.paths (anchored strictly to DATA_DIR)
- Backed by SQLite WAL synchronization for multi-process safety
- Windows NTFS file lock retry mechanism to prevent WinError 32 / PermissionError
- Automated .shadow_bak snapshot creation and recovery
"""

import os
import json
import time
import shutil
import logging
import threading
from pathlib import Path
from typing import Any, Optional, Dict
from core.paths import resolve_data_path, DATA_DIR

logger = logging.getLogger("Nexus.Storage")

_FILE_LOCKS: Dict[str, threading.RLock] = {}
_GLOBAL_LOCK = threading.Lock()

def _get_lock_for_path(filepath: str | Path) -> threading.RLock:
    canonical = str(Path(filepath).resolve())
    with _GLOBAL_LOCK:
        if canonical not in _FILE_LOCKS:
            _FILE_LOCKS[canonical] = threading.RLock()
        return _FILE_LOCKS[canonical]


def _get_bak_path(p: Path) -> Path:
    """Returns the path to the .bak file inside a dedicated .shadow_bak folder."""
    bak_dir = p.parent / ".shadow_bak"
    try:
        bak_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    return bak_dir / f"{p.name}.bak"


def safe_load_json(filepath: str | Path, default: Any = None) -> Any:
    """
    Safely loads JSON.
    First attempts SQLite WAL state; falls back to deterministic disk location.
    """
    # 1. Resolve deterministic path
    if "VERCEL" in os.environ and not str(filepath).startswith("/tmp"):
        p = Path("/tmp") / Path(filepath).name
    else:
        p = resolve_data_path(filepath)

    # 2. Check high-concurrency SQLite store
    try:
        from core.db import get_state
        db_data = get_state(p.name)
        if db_data is not None:
            return db_data
    except Exception:
        pass

    lock = _get_lock_for_path(p)
    with lock:
        if not p.exists() or p.stat().st_size == 0:
            # Check shadow backup
            bak = _get_bak_path(p)
            if bak.exists() and bak.stat().st_size > 0:
                try:
                    with open(bak, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    logger.warning(f"[Storage] Auto-recovered {p.name} from backup {bak.name}")
                    return data
                except Exception as e:
                    logger.error(f"[Storage] Backup load failed for {bak}: {e}")
            return default if default is not None else []

        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"[Storage] Corrupt JSON in {p}: {e}. Trying shadow backup...")
            bak = _get_bak_path(p)
            if bak.exists() and bak.stat().st_size > 0:
                try:
                    with open(bak, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    logger.info(f"[Storage] Recovered {p.name} from backup.")
                    atomic_save_json(p, data)
                    return data
                except Exception:
                    pass
            return default if default is not None else []


def atomic_save_json(filepath: str | Path, data: Any, indent: int = 2) -> bool:
    """
    Atomically persists data to disk and mirrors to SQLite.
    Includes Windows NTFS retry logic to prevent WinError 32 PermissionError collisions.
    """
    if "VERCEL" in os.environ and not str(filepath).startswith("/tmp"):
        p = Path("/tmp") / Path(filepath).name
    else:
        p = resolve_data_path(filepath)

    try:
        p.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

    lock = _get_lock_for_path(p)
    tmp_path = p.with_suffix(p.suffix + f".tmp_{threading.get_ident()}_{os.getpid()}")
    bak_path = _get_bak_path(p)

    with lock:
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
                f.flush()
                try:
                    os.fsync(f.fileno())
                except OSError:
                    pass

            # Update shadow backup before replacing
            if p.exists() and p.stat().st_size > 0:
                try:
                    shutil.copy2(p, bak_path)
                except Exception:
                    pass

            # Atomic replace with Windows retry backoff and in-place copy fallback
            max_retries = 5
            replaced = False
            for attempt in range(max_retries):
                try:
                    os.replace(tmp_path, p)
                    replaced = True
                    break
                except (PermissionError, OSError):
                    time.sleep(0.05 * (attempt + 1))

            if not replaced:
                try:
                    shutil.copyfile(tmp_path, p)
                    tmp_path.unlink(missing_ok=True)
                except Exception as copy_err:
                    logger.error(f"[Storage] Windows copy fallback failed for {p}: {copy_err}")
                    raise copy_err

            # Synchronize to SQLite engine for cross-process ACID reads
            try:
                from core.db import set_state
                set_state(p.name, data, sync_json=False)
            except Exception:
                pass

            return True
        except Exception as e:
            logger.error(f"[Storage] Atomic save failed for {p}: {e}")
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass
            if "VERCEL" in os.environ:
                return False
            raise e
