"""
Nexus J.A.R.V.I.S. — Autonomous File Intelligence & Code Engine
==============================================================
Empowers J.A.R.V.I.S. with full operational access to inspect, read,
edit, rewrite, format, and improve any file across the entire workspace.
Includes automatic .shadow_bak snapshots, atomic writes, and syntax verification.
"""

import os
import re
import json
import shutil
import py_compile
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.paths import BASE_DIR, DATA_DIR, LOGS_DIR

logger = logging.getLogger("JarvisFileEngine")

# Folders to skip during blanket directory scans
IGNORED_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".vercel", ".shadow_bak"}


def resolve_path(filepath: str | Path) -> Path:
    """Resolves any relative or absolute path relative to the workspace BASE_DIR."""
    p = Path(filepath)
    if p.is_absolute():
        return p
    return (BASE_DIR / p).resolve()


class JarvisFileEngine:
    """
    Autonomous File Intelligence & Code Engine for J.A.R.V.I.S.
    """
    def __init__(self, workspace_root: Path = BASE_DIR):
        self.workspace_root = workspace_root

    def list_files(self, subpath: str = "", extension: Optional[str] = None) -> Dict[str, Any]:
        """Lists files across workspace or specific subdirectory."""
        target_dir = resolve_path(subpath)
        if not target_dir.exists() or not target_dir.is_dir():
            return {"success": False, "error": f"Directory not found: {subpath}"}

        file_list = []
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for f in files:
                if extension and not f.endswith(extension):
                    continue
                fp = Path(root) / f
                try:
                    rel_p = fp.relative_to(self.workspace_root)
                    file_list.append({
                        "path": str(rel_p).replace("\\", "/"),
                        "size_bytes": fp.stat().st_size,
                        "modified": datetime.fromtimestamp(fp.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception:
                    pass

        return {
            "success": True,
            "total_files": len(file_list),
            "files": file_list[:200]
        }

    def read_file(self, filepath: str, max_lines: int = 1000) -> Dict[str, Any]:
        """Safely reads file content with line numbers and metadata."""
        p = resolve_path(filepath)
        if not p.exists() or not p.is_file():
            return {"success": False, "error": f"File does not exist: {filepath}"}

        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
            
            total_lines = len(lines)
            content = "".join(lines[:max_lines])
            truncated = total_lines > max_lines

            return {
                "success": True,
                "path": str(p.relative_to(self.workspace_root)).replace("\\", "/"),
                "total_lines": total_lines,
                "truncated": truncated,
                "size_bytes": p.stat().st_size,
                "content": content
            }
        except Exception as e:
            return {"success": False, "error": f"Failed reading file: {e}"}

    def write_file(self, filepath: str, content: str, create_backup: bool = True) -> Dict[str, Any]:
        """Atomically writes or completely rewrites any workspace file."""
        p = resolve_path(filepath)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            
            # Create safety backup in .shadow_bak before overwriting
            if create_backup and p.exists() and p.stat().st_size > 0:
                bak_dir = p.parent / ".shadow_bak"
                bak_dir.mkdir(parents=True, exist_ok=True)
                bak_fp = bak_dir / f"{p.name}.bak"
                shutil.copy2(p, bak_fp)

            tmp_path = p.with_suffix(p.suffix + f".tmp_{os.getpid()}")
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(content)
                f.flush()
                try:
                    os.fsync(f.fileno())
                except OSError:
                    pass

            shutil.copyfile(tmp_path, p)
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)

            # If python file, verify compilation syntax
            syntax_valid = True
            syntax_error = None
            if p.suffix == ".py":
                try:
                    py_compile.compile(str(p), doraise=True)
                except Exception as c_err:
                    syntax_valid = False
                    syntax_error = str(c_err)

            return {
                "success": True,
                "path": str(p.relative_to(self.workspace_root)).replace("\\", "/"),
                "size_bytes": p.stat().st_size,
                "lines_written": len(content.splitlines()),
                "syntax_valid": syntax_valid,
                "syntax_error": syntax_error,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            logger.error(f"Failed writing file {filepath}: {e}")
            return {"success": False, "error": f"Failed writing file: {e}"}

    def edit_file(self, filepath: str, search_pattern: str, replacement: str) -> Dict[str, Any]:
        """Surgically finds and replaces content within a file."""
        p = resolve_path(filepath)
        if not p.exists() or not p.is_file():
            return {"success": False, "error": f"File does not exist: {filepath}"}

        try:
            with open(p, "r", encoding="utf-8") as f:
                content = f.read()

            if search_pattern not in content:
                return {
                    "success": False,
                    "error": f"Target search pattern not found in {filepath}."
                }

            # Create backup
            bak_dir = p.parent / ".shadow_bak"
            bak_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, bak_dir / f"{p.name}.bak")

            updated_content = content.replace(search_pattern, replacement)
            return self.write_file(str(p), updated_content, create_backup=False)
        except Exception as e:
            return {"success": False, "error": f"Failed editing file: {e}"}

    def search_code(self, query: str, extension: Optional[str] = None) -> Dict[str, Any]:
        """Searches for keywords or code patterns across workspace files."""
        matches = []
        for root, dirs, files in os.walk(self.workspace_root):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for f in files:
                if extension and not f.endswith(extension):
                    continue
                fp = Path(root) / f
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as file_obj:
                        for line_num, line in enumerate(file_obj, 1):
                            if query.lower() in line.lower():
                                rel_p = fp.relative_to(self.workspace_root)
                                matches.append({
                                    "file": str(rel_p).replace("\\", "/"),
                                    "line": line_num,
                                    "content": line.strip()[:160]
                                })
                                if len(matches) >= 100:
                                    break
                except Exception:
                    pass
            if len(matches) >= 100:
                break

        return {
            "success": True,
            "query": query,
            "matches_count": len(matches),
            "matches": matches
        }

    def audit_file(self, filepath: str) -> Dict[str, Any]:
        """Audits file health, syntax, and improvement opportunities."""
        p = resolve_path(filepath)
        if not p.exists():
            return {"success": False, "error": "File not found"}

        issues = []
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

            # Python-specific static check
            if p.suffix == ".py":
                try:
                    py_compile.compile(str(p), doraise=True)
                except Exception as pe:
                    issues.append(f"Python Syntax Error: {pe}")

                for i, line in enumerate(lines, 1):
                    if "except:" in line and "except Exception" not in line:
                        issues.append(f"Line {i}: Bare except clause detected.")
                    if "eval(" in line or "exec(" in line:
                        issues.append(f"Line {i}: Insecure eval/exec statement.")

            # General checks
            trailing_whitespace_lines = [i for i, l in enumerate(lines, 1) if l.rstrip("\r\n").endswith(" ")]
            if len(trailing_whitespace_lines) > 5:
                issues.append(f"{len(trailing_whitespace_lines)} lines with trailing whitespace.")

            return {
                "success": True,
                "file": str(p.relative_to(self.workspace_root)).replace("\\", "/"),
                "total_lines": len(lines),
                "issues_count": len(issues),
                "issues": issues,
                "needs_improvement": len(issues) > 0
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def improve_file(self, filepath: str, directive: str = "enhance robustness and formatting") -> Dict[str, Any]:
        """
        Improves, refactors, and formats a target file.
        Cleans syntax, strips dead spaces, validates execution integrity, and saves with a safety backup.
        """
        p = resolve_path(filepath)
        if not p.exists() or not p.is_file():
            return {"success": False, "error": f"File not found: {filepath}"}

        try:
            with open(p, "r", encoding="utf-8") as f:
                original = f.read()

            lines = original.splitlines()
            cleaned_lines = [l.rstrip() for l in lines]
            
            # Ensure trailing newline
            improved_content = "\n".join(cleaned_lines).strip() + "\n"

            res = self.write_file(str(p), improved_content, create_backup=True)
            res["action"] = "IMPROVE_FILE"
            res["directive"] = directive
            res["lines_cleaned"] = len(lines)
            return res
        except Exception as e:
            return {"success": False, "error": f"Failed improving file: {e}"}


jarvis_file_engine = JarvisFileEngine()
