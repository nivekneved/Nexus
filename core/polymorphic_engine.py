import os
import time
import hashlib
import json
import subprocess
from typing import Dict, Any, Optional, Callable
from security.shield import shield
from core.addon_registry import addon_registry
from core.telemetry import telemetry

class PolymorphicEngine:
    """
    Unified Polymorphic Execution & Caching Backbone.
    Enforces the core principle:
    'Why have 5 separate functions/components when 1 polymorphic engine
    can do the same job with higher reliability, lower bug surface, and unified caching?'
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PolymorphicEngine, cls).__new__(cls)
            cls._instance.cache: Dict[str, Dict[str, Any]] = {}
            cls._instance.cache_ttl_seconds = 300  # 5 minute default TTL
        return cls._instance

    def _get_cache_key(self, namespace: str, key_data: Any) -> str:
        serialized = json.dumps(key_data, sort_keys=True, default=str)
        hashed = hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]
        return f"{namespace}:{hashed}"

    def cached_execute(self, namespace: str, key_data: Any, executor_fn: Callable[[], Any], ttl_seconds: Optional[int] = None) -> Any:
        """Executes an operation with unified LRU/TTL caching to eliminate redundant calls."""
        ckey = self._get_cache_key(namespace, key_data)
        now = time.time()
        ttl = ttl_seconds or self.cache_ttl_seconds

        if ckey in self.cache:
            entry = self.cache[ckey]
            if now - entry["timestamp"] < ttl:
                return entry["data"]

        # Cache miss: compute and cache
        result = executor_fn()
        self.cache[ckey] = {"timestamp": now, "data": result}
        return result

    def execute_safe_subprocess(self, cmd_tokens: list, cwd: Optional[str] = None, timeout_sec: int = 10) -> Dict[str, Any]:
        """
        Polymorphic subprocess runner applying Safeguard 4 (Command Injection Neutralizer),
        Safeguard 11 (Subprocess Timeout Enforcer), and Safeguard 3 (Path Traversal Shield).
        """
        sanitized_tokens = shield.sanitize_command_args(cmd_tokens)
        safe_cwd = shield.sanitize_path(cwd) if cwd else None

        try:
            res = subprocess.run(
                sanitized_tokens,
                cwd=safe_cwd,
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            return {
                "success": res.returncode == 0,
                "stdout": res.stdout.strip(),
                "stderr": res.stderr.strip(),
                "exit_code": res.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Subprocess timed out after {timeout_sec}s",
                "exit_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1
            }

    def dispatch_telemetry(self, agent_id: str, step: str, file_used: str, message: str, level: str = "INFO", subagent_id: Optional[str] = None):
        """Polymorphic telemetry logger masking secrets and applying XSS/PII sanitization."""
        clean_msg = shield.mask_pii(shield.redact_secrets(message))
        full_step = f"[{subagent_id}] {step}" if subagent_id else step
        telemetry.log(
            agent=agent_id,
            step=full_step,
            file_used=file_used,
            message=clean_msg,
            level=level
        )

engine = PolymorphicEngine()
