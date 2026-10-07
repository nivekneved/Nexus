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
    def execute_python_code(code_str: str, timeout: int = 5) -> Dict[str, Any]:
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        success = True
        error_msg = None

        try:
            # Restricted globals execution
            restricted_globals = {"__builtins__": {"print": print, "range": range, "len": len, "str": str, "int": int}}
            exec(code_str, restricted_globals)
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
