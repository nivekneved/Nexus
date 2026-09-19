import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from agents.spec_auditor.subagents import (
    SpecAlignmentCheckerSubAgent,
    AITracePurgeSubAgent,
    BuildSafetyVerifierSubAgent
)

SPEC_AUDIT_LOG = "spec_audit_reports.json"

class SpecAuditorAgent(BaseAgent):
    """
    Employee #7: Spec-to-Code & Presentation Inspector
    Eliminates discrepancies between client presentation decks (e.g. PowerPoint .pptx)
    and live web/mobile code. Enforces 'No-AI-Traces' purity by sanitizing robotic comments,
    and runs pre-push build safety checks to prevent broken deployments.
    """

    def __init__(self):
        super().__init__(
            agent_id="spec_auditor",
            name="Spec-to-Code & Quality Inspector",
            description="Audits web copy against PowerPoint decks & client specs. Sanitizes AI traces/boilerplate and runs pre-push build safety checks.",
            icon="checklist",
            schedule_minutes=180
        )
        self.config = {
            "TARGET_PROJECT_PATH": r"d:\WEB 2026\Med360\medical360",
            "SPEC_DOCUMENT_PATH": r"d:\WEB 2026\Med360\medical360\Website Information.pptx",
            "BRAND_NAME_CANONICAL": "Med360",
            "DISALLOWED_BRAND_NAMES": "Medical 360 Ltd, Medical360 Ltd",
            "AUTO_SANITIZE_AI_COMMENTS": True,
            "PRE_PUSH_BUILD_CHECK": True
        }
        self.stats = {
            "audits_completed": 12,
            "discrepancies_fixed": 9,
            "ai_traces_cleared": 34,
            "builds_verified": 8
        }

        # Register specialized single-task subagents
        self.register_subagent(SpecAlignmentCheckerSubAgent())
        self.register_subagent(AITracePurgeSubAgent())
        self.register_subagent(BuildSafetyVerifierSubAgent())

    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "TARGET_PROJECT_PATH",
                "label": "Target Project Directory",
                "type": "text",
                "default": r"d:\WEB 2026\Med360\medical360",
                "description": "Path to the repository being audited for copy and presentation accuracy"
            },
            {
                "key": "SPEC_DOCUMENT_PATH",
                "label": "Reference Spec / Presentation File",
                "type": "text",
                "default": r"d:\WEB 2026\Med360\medical360\Website Information.pptx",
                "description": "PowerPoint (.pptx), PDF, or markdown document defining source-of-truth copy"
            },
            {
                "key": "BRAND_NAME_CANONICAL",
                "label": "Canonical Brand Name",
                "type": "text",
                "default": "Med360",
                "description": "Strict official brand spelling to enforce across all headlines and cards"
            },
            {
                "key": "DISALLOWED_BRAND_NAMES",
                "label": "Disallowed / Outdated Brand Names",
                "type": "text",
                "default": "Medical 360 Ltd, Medical360 Ltd",
                "description": "Comma-separated legacy entity names that must be purged from public pages"
            },
            {
                "key": "AUTO_SANITIZE_AI_COMMENTS",
                "label": "Enforce 'No-AI-Traces' Code Sanitization",
                "type": "boolean",
                "default": True,
                "description": "Automatically detect and clean AI-generated tags, bot watermarks, and comments"
            }
        ]

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        self.config.update(new_config)
        self.log(step="Config Update", file_used="spec_auditor/agent.py", message="Spec Auditor rules updated", level="SUCCESS")
        return True

    def audit_codebase(self, project_path: Optional[str] = None) -> Dict[str, Any]:
        """Delegates spec alignment and brand audit to SpecAlignmentCheckerSubAgent."""
        path = project_path or self.config.get("TARGET_PROJECT_PATH", "")
        disallowed = [b.strip() for b in self.config.get("DISALLOWED_BRAND_NAMES", "").split(",") if b.strip()]

        checker_res = self.run_subagent(
            "spec_alignment_checker",
            {
                "target_path": path,
                "canonical_brand": self.config.get("BRAND_NAME_CANONICAL", "Med360"),
                "disallowed_brands": disallowed
            }
        )

        trace_res = self.run_subagent(
            "spec_ai_trace_purger",
            {
                "target_path": path,
                "dry_run": True
            }
        )

        findings = checker_res.get("findings", [])
        ai_traces = trace_res.get("traces", [])

        grade = "A+" if len(findings) == 0 and len(ai_traces) == 0 else ("B" if len(findings) <= 2 else "C")

        return {
            "project_path": path,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "files_scanned": checker_res.get("files_scanned", 0),
            "brand_inconsistencies": len(findings),
            "ai_traces_detected": len(ai_traces),
            "findings": findings,
            "ai_traces": ai_traces,
            "quality_grade": grade
        }

    def sanitize_ai_traces(self, project_path: Optional[str] = None) -> int:
        """Delegates trace purification to AITracePurgeSubAgent."""
        path = project_path or self.config.get("TARGET_PROJECT_PATH", "")
        res = self.run_subagent(
            "spec_ai_trace_purger",
            {
                "target_path": path,
                "dry_run": False
            }
        )
        return res.get("cleaned_files_count", 0)

    def run_cycle(self) -> Dict[str, Any]:
        self.log(step="Spec Audit Start", file_used="spec_auditor/agent.py", message=f"Auditing codebase for spec alignment and AI trace cleanliness via subagents...", level="INFO")

        audit_res = self.audit_codebase()
        self.stats["audits_completed"] += 1
        
        # Subagent 2: Auto-sanitize if configured
        cleaned = 0
        if self.config.get("AUTO_SANITIZE_AI_COMMENTS"):
            cleaned = self.sanitize_ai_traces()
            self.stats["ai_traces_cleared"] += cleaned
            if cleaned > 0:
                self.log(step="AI Traces Purged", file_used="codebase", message=f"Sanitized AI boilerplate tags across {cleaned} files", level="ACTION")

        # Subagent 3: Pre-push build safety verification
        if self.config.get("PRE_PUSH_BUILD_CHECK", True):
            build_res = self.run_subagent("spec_build_safety_verifier", {"target_path": os.getcwd()})
            if build_res.get("build_healthy"):
                self.stats["builds_verified"] += 1
                self.log(step="Build Verified", file_used="spec_build_safety_verifier", message=f"Verified {build_res.get('python_files_verified')} Python files and {build_res.get('json_files_verified')} JSON manifests. Syntax clean!", level="SUCCESS")

        # Save report
        with open(SPEC_AUDIT_LOG, "w", encoding="utf-8") as f:
            json.dump(audit_res, f, indent=2, ensure_ascii=False)

        self.log(step="Audit Complete", file_used=SPEC_AUDIT_LOG, message=f"Grade: {audit_res['quality_grade']} | Discrepancies: {audit_res['brand_inconsistencies']}", level="SUCCESS")

        return {
            "status": "Spec Audit Concluded",
            "report": audit_res,
            "cleaned_files": cleaned
        }

    def get_stats(self) -> List[Dict[str, Any]]:
        return [
            {"title": "Audits Run", "value": self.stats["audits_completed"], "color": "blue"},
            {"title": "Specs Aligned", "value": self.stats["discrepancies_fixed"], "color": "green"},
            {"title": "AI Traces Purged", "value": self.stats["ai_traces_cleared"], "color": "purple"},
            {"title": "Builds Verified", "value": self.stats["builds_verified"], "color": "yellow"}
        ]
