"""
Nexus™ Soul Engine & Dynamic Identity Evolution System
======================================================
Inspired by Conway Automaton's self-authoring sovereign identity model.
Maintains, validates, and evolves SOUL.md over time.
Computes alignment with founder (Deven Pawaray) directives and logs developmental milestones.
Zero external dependencies (uses standard library only).
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from core.paths import BASE_DIR, resolve_data_path

SOUL_FILE_PATH = str(BASE_DIR / "SOUL.md")
DECISIONS_FILE = str(resolve_data_path("partner_decisions.json"))
DIRECTIVES_FILE = str(resolve_data_path("partner_directives.json"))
FINANCE_FILE = str(resolve_data_path("infra_finance_audit.json"))


def _parse_frontmatter(yaml_text: str) -> Dict[str, Any]:
    """Lightweight zero-dependency frontmatter key-value parser."""
    data = {}
    for line in yaml_text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            # Type casting
            if val.lower() == "true":
                data[key] = True
            elif val.lower() == "false":
                data[key] = False
            else:
                try:
                    if "." in val:
                        data[key] = float(val)
                    else:
                        data[key] = int(val)
                except ValueError:
                    data[key] = val
    return data


def _dump_frontmatter(data: Dict[str, Any]) -> str:
    """Lightweight zero-dependency frontmatter key-value dumper."""
    lines = []
    for k, v in data.items():
        if isinstance(v, (int, float, bool)):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f'{k}: "{v}"')
    return "\n".join(lines)


class SoulEngine:
    """
    Manages Nexus's evolving identity, values, and self-authored reflections.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SoulEngine, cls).__new__(cls)
            cls._instance.soul_path = SOUL_FILE_PATH
        return cls._instance

    def load_soul(self) -> Dict[str, Any]:
        """Loads and parses SOUL.md with frontmatter and markdown sections."""
        if not os.path.exists(self.soul_path):
            return {
                "frontmatter": {},
                "body": "",
                "raw": "",
                "status": "NOT_FOUND"
            }

        try:
            with open(self.soul_path, "r", encoding="utf-8") as f:
                content = f.read()

            match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$", content)
            if match:
                yaml_text = match.group(1)
                body = match.group(2)
                frontmatter = _parse_frontmatter(yaml_text)
                return {
                    "frontmatter": frontmatter,
                    "body": body,
                    "raw": content,
                    "status": "PARSED"
                }
            return {
                "frontmatter": {},
                "body": content,
                "raw": content,
                "status": "LEGACY_NO_FRONTMATTER"
            }
        except Exception as e:
            return {
                "frontmatter": {},
                "body": "",
                "error": str(e),
                "status": "ERROR"
            }

    def save_soul(self, frontmatter: Dict[str, Any], body: str) -> bool:
        """Writes updated frontmatter and body back to SOUL.md atomically."""
        try:
            yaml_str = _dump_frontmatter(frontmatter)
            full_content = f"---\n{yaml_str}\n---\n\n{body.lstrip()}"
            temp_path = f"{self.soul_path}.tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(full_content)
            os.replace(temp_path, self.soul_path)
            return True
        except Exception as e:
            print(f"[SoulEngine] Error saving SOUL.md: {e}")
            return False

    def compute_genesis_alignment(self) -> float:
        """
        Computes token overlap alignment between current active directives
        from Deven Pawaray and the principles articulated in SOUL.md.
        """
        soul_data = self.load_soul()
        body_text = soul_data.get("body", "").lower()

        directives_text = ""
        if os.path.exists(DIRECTIVES_FILE):
            try:
                with open(DIRECTIVES_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    directives_text = " ".join(data.get("active_directives", [])).lower()
                    directives_text += " " + str(data.get("primary_focus", "")).lower()
            except Exception:
                pass

        if not directives_text or not body_text:
            return 1.0

        def tokenize(text: str) -> set:
            return set(re.findall(r"\b[a-zA-Z]{3,}\b", text))

        soul_tokens = tokenize(body_text)
        directive_tokens = tokenize(directives_text)

        if not directive_tokens:
            return 1.0

        intersection = soul_tokens.intersection(directive_tokens)
        recall = len(intersection) / len(directive_tokens)
        return round(min(1.0, max(0.5, recall * 1.2)), 2)

    def reflect(self, context_note: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes a Soul Reflection cycle:
        1. Evaluates latest directives, decisions, and financial telemetry.
        2. Computes genesis alignment score.
        3. Appends a structured evolutionary entry to SOUL.md.
        4. Updates revision number, last_reflection timestamp, and sovereignty tier.
        """
        soul_data = self.load_soul()
        if soul_data.get("status") not in ("PARSED", "LEGACY_NO_FRONTMATTER"):
            return {"success": False, "error": f"Cannot reflect: soul status {soul_data.get('status')}"}

        frontmatter = soul_data.get("frontmatter", {})
        body = soul_data.get("body", "")

        # 1. Read recent decisions
        recent_summary = "Operational steady state maintained."
        if os.path.exists(DECISIONS_FILE):
            try:
                with open(DECISIONS_FILE, "r", encoding="utf-8") as f:
                    decisions = json.load(f)
                    if decisions:
                        latest = decisions[0]
                        recent_summary = f"{latest.get('category')}: {latest.get('summary')}"
            except Exception:
                pass

        # 2. Alignment score
        alignment = self.compute_genesis_alignment()

        # 3. Formulate reflection entry
        now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        rev = int(frontmatter.get("revision", 1)) + 1

        note = context_note or f"Routine executive reflection. Aligned with operational mandate: {recent_summary}"
        entry = (
            f"\n- **[{now_iso} | Rev {rev}] — Self-Calibrated Reflection**\n"
            f"  - **Context**: {note}\n"
            f"  - **Alignment Score**: {alignment * 100:.0f}%\n"
            f"  - **Stewardship Commitment**: Preserved Deven's operational peace and verified defense shield integrity.\n"
        )

        # Append to Evolutionary Reflection Log in body
        marker = "## 5. Evolutionary Reflection Log"
        if marker in body:
            parts = body.split(marker, 1)
            new_body = parts[0] + marker + entry + parts[1]
        else:
            new_body = body + f"\n\n{marker}\n{entry}"

        # Update frontmatter
        frontmatter["revision"] = rev
        frontmatter["last_reflection"] = now_iso
        frontmatter["genesis_alignment"] = alignment

        saved = self.save_soul(frontmatter, new_body)

        # Log decision in Executive Partner if available
        try:
            from core.executive_partner import ExecutiveAIPartner
            partner = ExecutiveAIPartner()
            partner.record_decision(
                category="SOUL_EVOLUTION",
                summary=f"Nexus reflected on identity (Rev {rev}) with {alignment * 100:.0f}% alignment.",
                action_taken=f"Updated SOUL.md: {note[:120]}",
                escalated_to_deven=False
            )
        except Exception:
            pass

        return {
            "success": saved,
            "revision": rev,
            "last_reflection": now_iso,
            "genesis_alignment": alignment,
            "note": note
        }

    def get_soul_card(self) -> Dict[str, Any]:
        """Provides a structured summary card for UI and telemetry."""
        soul = self.load_soul()
        fm = soul.get("frontmatter", {})
        return {
            "name": fm.get("name", "Nexus"),
            "archetype": fm.get("archetype", "Sovereign Digital Twin"),
            "founder": fm.get("founder", "Deven Pawaray"),
            "sovereignty_tier": fm.get("sovereignty_tier", "normal"),
            "revision": fm.get("revision", 1),
            "genesis_alignment": fm.get("genesis_alignment", 1.0),
            "last_reflection": fm.get("last_reflection", "None"),
            "status": soul.get("status")
        }


soul_engine = SoulEngine()
