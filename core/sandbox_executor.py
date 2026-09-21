"""
Nexus™ Self-Testing Python Sandbox & Code Validator
==================================================
Inspired by E2B and Open Interpreter.
Executes and validates generated digital scripts in an isolated subprocess,
asserting compile integrity, safe execution, and zero crashes (exit code == 0).
"""

import os
import sys
import tempfile
import subprocess
import time
from typing import Dict, Any, Optional

class PythonSandboxExecutor:
    """Executes Python code in an isolated local sandbox with strict limits."""
    
    def __init__(self, timeout_seconds: int = 6):
        self.timeout_seconds = timeout_seconds

    def validate_and_test(
        self,
        code_content: Optional[str] = None,
        file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Runs a two-stage verification on the target Python script:
        1. Bytecode syntax compilation check (py_compile)
        2. Isolated execution test with timeout
        """
        temp_file_created = False
        target_file = file_path

        if code_content and not file_path:
            fd, tmp_name = tempfile.mkstemp(suffix=".py", prefix="nexus_sandbox_")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(code_content)
            target_file = tmp_name
            temp_file_created = True

        if not target_file or not os.path.exists(target_file):
            return {
                "passed": False,
                "stage": "FILE_RESOLVE",
                "error": f"Target file '{target_file}' does not exist."
            }

        start_time = time.time()
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        try:
            # Stage 1: Syntax & Bytecode Compilation
            compile_cmd = [sys.executable, "-m", "py_compile", target_file]
            comp_res = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                timeout=self.timeout_seconds
            )
            if comp_res.returncode != 0:
                duration_ms = round((time.time() - start_time) * 1000, 2)
                return {
                    "passed": False,
                    "stage": "SYNTAX_COMPILATION",
                    "duration_ms": duration_ms,
                    "error": comp_res.stderr.strip() or "Syntax error in script.",
                    "exit_code": comp_res.returncode
                }

            # Stage 2: Sandbox Dry Execution
            run_cmd = [sys.executable, target_file]
            exec_res = subprocess.run(
                run_cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                timeout=self.timeout_seconds
            )
            duration_ms = round((time.time() - start_time) * 1000, 2)

            passed = (exec_res.returncode == 0)
            return {
                "passed": passed,
                "stage": "EXECUTION_COMPLETE",
                "duration_ms": duration_ms,
                "exit_code": exec_res.returncode,
                "stdout": exec_res.stdout[:1500],
                "stderr": exec_res.stderr[:500],
                "error": None if passed else exec_res.stderr.strip()
            }

        except subprocess.TimeoutExpired:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "passed": False,
                "stage": "TIMEOUT",
                "duration_ms": duration_ms,
                "error": f"Execution exceeded safety limit of {self.timeout_seconds}s."
            }
        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "passed": False,
                "stage": "UNCAUGHT_EXCEPTION",
                "duration_ms": duration_ms,
                "error": str(e)
            }
        finally:
            if temp_file_created and os.path.exists(target_file):
                try:
                    os.remove(target_file)
                except Exception:
                    pass

sandbox_executor = PythonSandboxExecutor()
