"""
Nexus Departmental Personas Engine (Integrated from alacambra/one-man-company)
===========================================================================
Indexes and serves 40+ elite departmental agent persona specifications across
Design, Engineering, Marketing, Product, Project Management, Studio Operations, and Testing.
"""

import os
import glob
from typing import Dict, Any, List

OMC_DIR = r"C:/Users/deven/OneDrive/Desktop/Agents/.artifacts/scratch/alacambra_omc"

class DepartmentalPersonasEngine:
    def __init__(self):
        self.personas = self._load_personas()

    def _load_personas(self) -> List[Dict[str, Any]]:
        loaded = []
        if not os.path.exists(OMC_DIR):
            return loaded

        pattern = os.path.join(OMC_DIR, "**", "*.md")
        for path in glob.glob(pattern, recursive=True):
            if ".git" in path or "README.md" in path:
                continue
            rel_path = os.path.relpath(path, OMC_DIR)
            parts = rel_path.split(os.sep)
            department = parts[0] if len(parts) > 1 else "general"
            filename = parts[-1]
            persona_id = filename.replace(".md", "")

            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse description from frontmatter if possible
                desc = f"Specialized {department} agent persona."
                if content.startswith("---"):
                    lines = content.split("\n")
                    for line in lines[1:]:
                        if line.startswith("description:"):
                            desc = line.replace("description:", "").strip()
                            break

                loaded.append({
                    "id": persona_id,
                    "department": department,
                    "file_path": rel_path,
                    "description": desc,
                    "content_preview": content[:400] + "..."
                })
            except Exception:
                pass

        return loaded

    def get_personas(self, department: Optional[str] = None) -> List[Dict[str, Any]]:
        if department:
            return [p for p in self.personas if p["department"].lower() == department.lower()]
        return self.personas

    def get_persona_detail(self, persona_id: str) -> Optional[Dict[str, Any]]:
        for p in self.personas:
            if p["id"] == persona_id:
                path = os.path.join(OMC_DIR, p["file_path"])
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        full_content = f.read()
                    return {**p, "full_content": full_content}
        return None

departmental_personas = DepartmentalPersonasEngine()
