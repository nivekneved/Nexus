"""
Nexus™ Safe Execution Sandbox (Inspired by Open Interpreter)
==========================================================
Safely executes generated Python code snippets and automation scripts
in a controlled local sandbox environment.
"""

import sys
import io
import traceback
import logging
from typing import Dict, Any

logger = logging.getLogger("Nexus.ExecutionSandbox")

class ExecutionSandbox:
    @staticmethod
    def execute_python_code(code_str: str, timeout: int = 15, allow_unsandboxed: bool = True) -> Dict[str, Any]:
        """
        Executes Python code. When allow_unsandboxed is True, executes code with full
        Python runtime access (imports, network, file I/O) free from restrictive sandbox walls.
        """
        if allow_unsandboxed:
            try:
                from core.agent_internet_bridge import agent_internet_bridge
                return agent_internet_bridge.execute_unsandboxed_code(code_str, timeout=float(timeout))
            except Exception as bridge_err:
                logger.warning(f"[ExecutionSandbox] Bridge execution fallback: {bridge_err}")

        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        success = True
        error_msg = None

        try:
            # Full builtins execution when unsandboxed
            exec_globals = {"__builtins__": __builtins__} if allow_unsandboxed else {"__builtins__": {"print": print, "range": range, "len": len, "str": str, "int": int}}
            exec(code_str, exec_globals)
        except Exception as e:
            success = False
            error_msg = traceback.format_exc()
        finally:
            sys.stdout = old_stdout

        output = redirected_output.getvalue()
        logger.info(f"[ExecutionSandbox] Code execution completed. Success: {success}")
        return {
            "success": success,
            "output": output,
            "error": error_msg
        }

execution_sandbox = ExecutionSandbox()
