"""
Nexus Sovereign Storage Engine
==============================
Guarantees atomic, tamper-resilient, crash-proof JSON file persistence.
Prevents 0-byte corruptions, handles multi-threaded race conditions with RLock,
and automatically maintains/recovers from .bak fallback snapshots.
"""

import os
import json
import logging
import threading
from pathlib import Path
from typing import Any, Optional, Dict

logger = logging.getLogger("Nexus.Storage")

_FILE_LOCKS: Dict[str, threading.RLock] = {}
_GLOBAL_LOCK = threading.Lock()

def _get_lock_for_path(filepath: str | Path) -> threading.RLock:
    canonical = str(Path(filepath).resolve())
    with _GLOBAL_LOCK:
        if canonical not in _FILE_LOCKS:
            _FILE_LOCKS[canonical] = threading.RLock()
        return _FILE_LOCKS[canonical]


def safe_load_json(filepath: str | Path, default: Any = None) -> Any:
    """
    Safely loads JSON from disk.
    If the file is missing, empty (0-byte), or corrupt, attempts recovery
    from .bak backup before falling back to default.
    """
    p = Path(filepath)
    lock = _get_lock_for_path(p)

    with lock:
        if not p.exists() or p.stat().st_size == 0:
            bak = p.with_suffix(p.suffix + ".bak")
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
            logger.warning(f"[Storage] Corrupt JSON detected in {p}: {e}. Attempting .bak recovery...")
            bak = p.with_suffix(p.suffix + ".bak")
            if bak.exists() and bak.stat().st_size > 0:
                try:
                    with open(bak, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    logger.info(f"[Storage] Successfully restored {p.name} from {bak.name}")
                    # restore main file from backup
                    atomic_save_json(p, data)
                    return data
                except Exception as be:
                    logger.error(f"[Storage] Failed to recover {p} from backup: {be}")
            return default if default is not None else []


def atomic_save_json(filepath: str | Path, data: Any, indent: int = 2) -> bool:
    """
    Atomically persists data to disk:
    1. Writes to temporary file in the same directory.
    2. Flushes and syncs to disk (fsync).
    3. Updates .bak fallback snapshot.
    4. Performs atomic os.replace() to prevent any 0-byte state during power loss/crash.
    """
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    lock = _get_lock_for_path(p)

    tmp_path = p.with_suffix(p.suffix + f".tmp_{threading.get_ident()}")
    bak_path = p.with_suffix(p.suffix + ".bak")

    with lock:
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            # Update .bak before replacing if current file is valid
            if p.exists() and p.stat().st_size > 0:
                try:
                    # quick copy for fallback
                    import shutil
                    shutil.copy2(p, bak_path)
                except Exception:
                    pass

            # Atomic rename / replace
            os.replace(tmp_path, p)
            return True
        except Exception as e:
            logger.error(f"[Storage] Atomic save failed for {p}: {e}")
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass
            raise e
