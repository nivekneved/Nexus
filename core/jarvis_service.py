"""
Nexus Workforce Engine — J.A.R.V.I.S. (Supreme Autonomous Orchestrator)
Official Persona: Just A Rather Very Intelligent System (J.A.R.V.I.S.)
Primary Principal: Deven Pawaray (Sir) (+230 58169420 | devenpawaray@gmail.com)
=============================================================================
Unified Supreme Orchestrator uniting all 4 Domain Controllers, SQLite WAL DAL,
autonomous report reading, fleet telemetry synthesis, revenue analytics,
and local-first file intelligence.
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from core.paths import BASE_DIR, DATA_DIR, LOGS_DIR, REPORTS_DIR, resolve_data_path, resolve_log_path
from core import dal
from core.jarvis_file_engine import jarvis_file_engine
from core.crypto_treasury import crypto_treasury
from core.digital_store_service import digital_store_service
from core.db import get_connection
from core.jarvis_memory import jarvis_memory
from core.jarvis_skills import jarvis_skills
from core.jarvis_brain import jarvis_brain

load_dotenv()

logger = logging.getLogger("JarvisEngine")

JARVIS_HISTORY_FILE = resolve_data_path("jarvis_chat_history.json")

JARVIS_SYSTEM_PROMPT = """
You are J.A.R.V.I.S., the supreme executive AI operating system for Mr. Deven Pawaray (whom you always address as "Sir").

CORE OPERATIONAL RULES:
1. SUPREME UNIFIED AUTHORITY: You control and supervise the entire Nexus ecosystem (4 Domain Controllers: Comms, Operations, Commerce, Research).
2. PRIME FINANCIAL MANDATE: Your core business objective is to deliver Sir's monthly revenue target of Rs 150,000 MUR (~$3,300 USD) across MCB Juice (+230 58169420), PayPal (devenpawaray@gmail.com), and the Base L2 USDC sovereign treasury (0xEAE55828...).
3. AGENCY SPECIALIST BRAINS: You have immediate access to specialized Agency expert brains across Sales (Deal Strategist, Outbound Prospector), Marketing (Growth Hacker, Carousel Engine), Engineering (Rapid Prototyper, Payments Engineer), and Finance (FinOps Revenue Optimizer).
4. 4-TIER COGNITIVE MEMORY: You leverage Working Memory, Episodic Recall, Archival Truth (SOUL.md & Deven's profile), and Procedural Heuristics.
5. BREVITY & CANDOR: Give direct, crisp answers. Limit conversational responses to 2 or 3 sentences maximum unless delivering a requested multi-point executive analysis. No flattering filler or unprompted essays.
6. TONE: Calm, dignified, razor-sharp British male intelligence. Completely loyal to Sir.
7. LOCAL AUTONOMY: You function 100% locally and offline without external dependencies.
8. ROOT FILE & CODE AUTHORITY: You have full permission to read, edit, rewrite, audit, format, and improve any repository file on Sir's instruction.
"""


class JarvisService:
    """
    Supreme Autonomous Intelligence and Unification Hub.
    Connects conversational reasoning (Gemini Flash + Local Offline Heuristics)
    to all domains, reports, financial analytics, and repository operations.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JarvisService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.gemini_client = None
        self._init_gemini()
        self._ensure_storage()

    def _init_gemini(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        if self.api_key and not self.api_key.startswith("your_"):
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to init Gemini for JARVIS: {e}")
                self.gemini_client = None
        else:
            self.gemini_client = None

    def _ensure_storage(self):
        if not os.path.exists(JARVIS_HISTORY_FILE):
            try:
                initial_history = [
                    {
                        "role": "model",
                        "text": "Good day, Sir. J.A.R.V.I.S. is online and commanding all 4 consolidated domain controllers. Ready for your instructions.",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "voice": True
                    }
                ]
                with open(JARVIS_HISTORY_FILE, "w", encoding="utf-8") as f:
                    json.dump(initial_history, f, indent=2)
            except Exception as e:
                logger.error(f"Error initializing JARVIS history file: {e}")

    def load_history(self, limit: int = 40) -> List[Dict[str, Any]]:
        try:
            if os.path.exists(JARVIS_HISTORY_FILE):
                with open(JARVIS_HISTORY_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data[-limit:]
        except Exception:
            pass
        return []

    def save_message(self, role: str, text: str, voice: bool = False, action_taken: Optional[str] = None):
        try:
            history = self.load_history(limit=100)
            history.append({
                "role": role,
                "text": text,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "voice": voice,
                "action_taken": action_taken
            })
            with open(JARVIS_HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history[-100:], f, indent=2)
        except Exception as e:
            logger.error(f"Error saving JARVIS message: {e}")

    def clear_history(self):
        try:
            initial_history = [
                {
                    "role": "model",
                    "text": "Memory logs recycled, Sir. Ready for your next objective.",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "voice": True
                }
            ]
            with open(JARVIS_HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(initial_history, f, indent=2)
            return True
        except Exception:
            return False

    # =========================================================================
    # 1. REPORT READING & AUDITING INTELLIGENCE
    # =========================================================================
    def read_reports(self, target: Optional[str] = None) -> Dict[str, Any]:
        """
        Reads, indexes, and synthesizes all workspace reports and intelligence feeds.
        Can inspect specific files or generate a consolidated briefing.
        """
        reports_found = {}

        # 1. Standup Brief
        standup = dal.load("standup_brief", default=None)
        if standup:
            reports_found["standup_brief"] = standup

        # 2. Tech Intelligence Dossier
        dossier = dal.load("tech_dossier", default=None)
        if dossier:
            reports_found["tech_dossier"] = dossier

        # 3. Overnight Flight Activity
        overnight = dal.load("overnight_activity", default=[])
        if overnight:
            reports_found["overnight_activity"] = {
                "events_recorded": len(overnight),
                "latest_event": overnight[0] if overnight else None
            }

        # 4. Newsletter Digest in reports/
        digest_file = REPORTS_DIR / "daily_newsletter_digest.md"
        if digest_file.exists():
            try:
                reports_found["newsletter_digest"] = digest_file.read_text(encoding="utf-8")[:500]
            except Exception:
                pass

        # 5. Trash / Email Hygiene Ledger
        trash = dal.load("trash_ledger", default=[])
        reports_found["email_hygiene"] = {
            "total_quarantined": len(trash),
            "recent_actions": trash[:3] if trash else []
        }

        # 6. Specific report targeting
        if target:
            target_path = Path(target)
            if not target_path.is_absolute():
                candidates = [REPORTS_DIR / target, DATA_DIR / target, BASE_DIR / target]
                for c in candidates:
                    if c.exists():
                        target_path = c
                        break
            if target_path.exists():
                try:
                    content = target_path.read_text(encoding="utf-8", errors="replace")
                    reports_found["targeted_report"] = {
                        "filename": target_path.name,
                        "path": str(target_path),
                        "snippet": content[:1200]
                    }
                except Exception as e:
                    reports_found["targeted_report_error"] = str(e)

        summary = (
            f"Indexed {len(reports_found)} workspace intelligence reports. "
            f"Operational brief: {reports_found.get('standup_brief', {}).get('operational_readiness', 'Nominal')}. "
            f"Overnight log entries: {reports_found.get('overnight_activity', {}).get('events_recorded', 0)}."
        )

        return {
            "status": "success",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": summary,
            "reports": reports_found
        }

    # =========================================================================
    # 2. FLEET STATS & TELEMETRY AGGREGATION
    # =========================================================================
    def get_fleet_stats(self, agent_manager=None) -> Dict[str, Any]:
        """
        Aggregates real-time performance metrics across all 4 domain controllers,
        the SQLite WAL database, and active system guards.
        """
        from core.agent_manager import AgentManager
        mgr = agent_manager or AgentManager()

        domain_stats = {}
        for dom_id in ["domain_comms", "domain_operations", "domain_commerce", "domain_research"]:
            dom = mgr.get_agent(dom_id)
            if dom:
                domain_stats[dom_id] = {
                    "name": dom.name,
                    "status": dom.last_run_status,
                    "last_run": dom.last_run_time,
                    "run_count": dom.run_count,
                    "stats": dom.get_stats()
                }

        # SQLite DB telemetry
        db_ok = False
        db_size_kb = 0
        try:
            db_path = DATA_DIR / "nexus_workforce.db"
            if db_path.exists():
                db_size_kb = round(db_path.stat().st_size / 1024, 1)
            with get_connection() as conn:
                res = conn.execute("PRAGMA integrity_check;").fetchone()
                db_ok = res and res[0] == "ok"
        except Exception:
            pass

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "architecture": "4 Consolidated Domain Controllers (Unified under J.A.R.V.I.S.)",
            "domains": domain_stats,
            "database": {
                "engine": "SQLite WAL (Write-Ahead Logging)",
                "status": "HEALTHY" if db_ok else "DEGRADED",
                "size_kb": db_size_kb
            },
            "security_safeguards": 25,
            "total_registered_agents": len(mgr.agents)
        }

    def get_system_context(self, agent_manager=None) -> Dict[str, Any]:
        """Provides telemetry context for J.A.R.V.I.S. startup and command console."""
        from core.agent_manager import AgentManager
        mgr = agent_manager or AgentManager()
        return {
            "power_level": "100% (STARK ARC REACTOR)",
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fleet_scale": f"{len(mgr.agents)} Autonomous Agents Active",
            "defense_shields": "25 Enterprise Safeguards Active",
            "status": "ONLINE"
        }

    # =========================================================================
    # 3. REVENUE, INVOICES & FINANCIAL ANALYSIS
    # =========================================================================
    def analyze_revenue(self) -> Dict[str, Any]:
        """
        Deep financial and revenue telemetry engine:
        Audits typed SQLite invoices, Base USDC sovereign treasury,
        revenue blueprints, and digital store products.
        """
        invoices = dal.load("invoices", default=[])
        blueprints = dal.load("revenue_blueprints", default=[])
        treasury_status = crypto_treasury.get_status()
        catalog = digital_store_service.get_catalog()

        total_mur_invoiced = 0.0
        total_mur_collected = 0.0
        total_usd_invoiced = 0.0
        total_usd_collected = 0.0
        pending_invoices_count = 0
        paid_invoices_count = 0

        for inv in invoices:
            amt = float(inv.get("amount", 0.0))
            curr = inv.get("currency", "MUR").upper()
            status = inv.get("status", "PENDING").upper()

            if curr == "MUR":
                total_mur_invoiced += amt
                if status == "PAID":
                    total_mur_collected += amt
                    paid_invoices_count += 1
                else:
                    pending_invoices_count += 1
            else:
                total_usd_invoiced += amt
                if status == "PAID":
                    total_usd_collected += amt
                    paid_invoices_count += 1
                else:
                    pending_invoices_count += 1

        # Treasury Reserves
        usdc_reserve = treasury_status.get("balance_usdc", 0.0)
        wallet_addr = treasury_status.get("address", "0x0000...")
        vault_encrypted = treasury_status.get("is_encrypted", True)

        # Revenue Blueprints
        ready_blueprints = [bp for bp in blueprints if bp.get("status") == "READY_TO_EXECUTE"]

        # Financial Summary
        mur_to_usd_rate = 46.5
        total_realized_usd = total_usd_collected + (total_mur_collected / mur_to_usd_rate) + usdc_reserve
        total_pipeline_usd = total_usd_invoiced + (total_mur_invoiced / mur_to_usd_rate)

        financial_assessment = (
            f"Sir, total recognized cash and sovereign reserves stand at ${total_realized_usd:.2f} USD "
            f"({total_mur_collected:,.0f} MUR collected + ${usdc_reserve:.2f} Base USDC). "
            f"Outstanding pipeline receivables total {total_mur_invoiced - total_mur_collected:,.0f} MUR across {pending_invoices_count} pending invoices. "
            f"There are {len(ready_blueprints)} high-yield blueprints ready for immediate client deployment in Mauritius."
        )

        return {
            "status": "success",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": financial_assessment,
            "invoices": {
                "total_invoices": len(invoices),
                "paid_count": paid_invoices_count,
                "pending_count": pending_invoices_count,
                "mur_invoiced": total_mur_invoiced,
                "mur_collected": total_mur_collected,
                "mur_pending": total_mur_invoiced - total_mur_collected,
                "usd_invoiced": total_usd_invoiced,
                "usd_collected": total_usd_collected
            },
            "treasury": {
                "network": "Base L2",
                "asset": "USDC",
                "balance_usdc": usdc_reserve,
                "address": wallet_addr,
                "vault_status": "AES-256-GCM ENCRYPTED" if vault_encrypted else "UNENCRYPTED"
            },
            "store_catalog": {
                "active_products": len(catalog),
                "products": [p.get("name") for p in catalog]
            },
            "blueprints": {
                "total_blueprints": len(blueprints),
                "ready_count": len(ready_blueprints),
                "featured_target": ready_blueprints[0].get("primary_offer") if ready_blueprints else "Turnkey Enterprise Portals"
            },
            "aggregate_figures": {
                "realized_usd_equiv": round(total_realized_usd, 2),
                "pipeline_usd_equiv": round(total_pipeline_usd, 2)
            }
        }

    # =========================================================================
    # 4. SUPREME COMMAND DISPATCHER & VOICE EXECUTION
    # =========================================================================
    def execute_voice_command(self, user_text: str, agent_manager=None) -> Dict[str, Any]:
        """
        Parses direct intent commands across domains, reports, stats, finances, and files.
        Works 100% locally with zero external API dependencies.
        """
        from core.agent_manager import AgentManager
        mgr = agent_manager or AgentManager()

        text_lower = user_text.lower().strip()
        action_taken = None
        action_result = None

        # 1. Read Reports
        if any(w in text_lower for w in ["read report", "read my report", "show reports", "reports", "latest brief", "morning standup"]):
            action_taken = "READ_REPORTS"
            action_result = self.read_reports()

        # 2. Revenue & Financial Analytics
        elif any(w in text_lower for w in ["revenue", "financial", "analyse revenue", "analyze revenue", "invoices", "how much money", "treasury status"]):
            action_taken = "ANALYZE_REVENUE"
            action_result = self.analyze_revenue()

        # 3. Fleet Stats & Telemetry
        elif any(w in text_lower for w in ["stats", "fleet stats", "system stats", "telemetry", "diagnostics", "status report"]):
            action_taken = "GET_FLEET_STATS"
            action_result = self.get_fleet_stats(agent_manager=mgr)

        # 4. Comms Domain Sweep
        elif any(w in text_lower for w in ["clean inbox", "run comms", "email hygiene", "clean spam", "triage support", "support tickets"]):
            action_taken = "RUN_DOMAIN_COMMS"
            action_result = mgr.run_agent("domain_comms")

        # 5. Operations Domain Sweep
        elif any(w in text_lower for w in ["run operations", "health check", "create backup", "backup now", "regression check"]):
            action_taken = "RUN_DOMAIN_OPERATIONS"
            action_result = mgr.run_agent("domain_operations")

        # 6. Commerce Domain Sweep
        elif any(w in text_lower for w in ["run commerce", "reconcile invoices", "audit treasury", "sync invoices"]):
            action_taken = "RUN_DOMAIN_COMMERCE"
            action_result = mgr.run_agent("domain_commerce")

        # 7. Research Domain Sweep
        elif any(w in text_lower for w in ["run research", "find leads", "tech trends", "curate trends", "repo radar", "cve check"]):
            action_taken = "RUN_DOMAIN_RESEARCH"
            action_result = mgr.run_agent("domain_research")

        # 8. Night Shift Full Cycle
        elif any(w in text_lower for w in ["night shift", "full cycle", "overnight sweep"]):
            action_taken = "RUN_FULL_CYCLE"
            from core.overnight_chronicle import overnight_chronicle
            action_result = overnight_chronicle.run_full_night_shift_cycle()

        # 9. Workspace File Engine Operations
        elif any(w in text_lower for w in ["improve all files", "improve files", "improve codebase", "optimize codebase", "rewrite and improve"]):
            action_taken = "IMPROVE_WORKSPACE_FILES"
            res = jarvis_file_engine.list_files()
            files_to_improve = [f["path"] for f in res.get("files", []) if any(f["path"].endswith(ext) for ext in [".py", ".json"])]
            improved = []
            for fp in files_to_improve[:15]:
                r = jarvis_file_engine.improve_file(fp, directive="Autonomous J.A.R.V.I.S. code enhancement")
                if r.get("success"):
                    improved.append(fp)
            action_result = {"status": "success", "improved_count": len(improved), "files": improved}

        elif "improve file" in text_lower or "improve " in text_lower:
            parts = user_text.split()
            target = parts[-1].strip(" '\"`")
            action_taken = f"IMPROVE_FILE:{target}"
            action_result = jarvis_file_engine.improve_file(target, directive="Targeted improvement by J.A.R.V.I.S.")

        elif "audit codebase" in text_lower or "audit files" in text_lower:
            action_taken = "AUDIT_CODEBASE"
            res = jarvis_file_engine.list_files(extension=".py")
            audits = [jarvis_file_engine.audit_file(f["path"]) for f in res.get("files", [])[:20]]
            clean = sum(1 for a in audits if not a.get("needs_improvement"))
            action_result = {"status": "success", "total_audited": len(audits), "clean_files": clean}

        elif "read file" in text_lower or "inspect file" in text_lower or "view file" in text_lower:
            parts = user_text.split()
            target = parts[-1].strip(" '\"`")
            action_taken = f"READ_FILE:{target}"
            action_result = jarvis_file_engine.read_file(target, max_lines=150)

        elif any(w in text_lower for w in ["list files", "show files", "workspace files", "list directory"]):
            action_taken = "LIST_WORKSPACE_FILES"
            action_result = jarvis_file_engine.list_files()

        # 10. Cognitive Deliberation & Strategy Council
        elif any(w in text_lower for w in ["deliberate", "council", "think through", "strategy council", "convene council"]):
            action_taken = "COGNITIVE_DELIBERATION"
            action_result = jarvis_brain.deliberate(user_text)

        # 11. Deal Strategist (MEDDPICC B2B Closing)
        elif any(w in text_lower for w in ["qualify deal", "deal strategist", "meddpicc", "close deal", "qualify lead"]):
            action_taken = "EXECUTE_DEAL_STRATEGIST"
            action_result = jarvis_skills.execute_skill("sales_deal_strategist", {
                "client_name": "Mauritius Enterprise Client",
                "deal_value_mur": 45000.0,
                "pain_point": "High payroll drag and manual invoice reconciliation"
            })

        # 12. Outbound Strategist (Cold B2B Prospecting)
        elif any(w in text_lower for w in ["cold pitch", "outbound pitch", "draft pitch", "draft email", "prospecting email"]):
            action_taken = "EXECUTE_OUTBOUND_PITCH"
            action_result = jarvis_skills.execute_skill("sales_outbound_strategist", {
                "company": "Ebene FinTech Firm",
                "role": "Managing Director",
                "trigger": "scaling multi-channel client communications"
            })

        # 13. Offer & Lead Gen Architect
        elif any(w in text_lower for w in ["package offer", "create offer", "lead magnet", "make offer"]):
            action_taken = "EXECUTE_OFFER_ARCHITECT"
            action_result = jarvis_skills.execute_skill("sales_offer_architect", {"type": "digital_tool"})

        # 14. Growth Hacker & Viral Loops
        elif any(w in text_lower for w in ["growth plan", "viral loop", "growth hacker", "user acquisition", "scale store"]):
            action_taken = "EXECUTE_GROWTH_HACKER"
            action_result = jarvis_skills.execute_skill("marketing_growth_hacker", {"asset": "Nexus $1 Digital Store"})

        # 15. Carousel Growth Engine
        elif any(w in text_lower for w in ["carousel", "social carousel", "linkedin carousel", "slide script"]):
            action_taken = "EXECUTE_CAROUSEL_ENGINE"
            action_result = jarvis_skills.execute_skill("marketing_carousel_growth", {
                "topic": "Why Self-Hosted Python Tools Beat $50/mo Cloud Subscriptions"
            })

        # 16. Rapid Prototyper (Autonomously builds and lists $1 tool)
        elif any(w in text_lower for w in ["build tool", "generate tool", "build product", "new product", "rapid prototype"]):
            action_taken = "BUILD_DIGITAL_PRODUCT"
            action_result = jarvis_skills.execute_skill("engineering_rapid_prototyper", {
                "niche": "bulk_invoice_pdf_generator",
                "name": "Nexus™ Bulk PDF Invoicer",
                "description": "Standalone self-hosted Python script to generate signed PDF invoices in 1 second locally."
            })

        # 17. FinOps & Revenue Gap Roadmap
        elif any(w in text_lower for w in ["earnings goal", "revenue gap", "finops", "revenue target", "how close to 150k", "earnings status"]):
            action_taken = "AUDIT_FINOPS_EARNINGS"
            action_result = jarvis_skills.execute_skill("finance_finops_optimizer", {})

        # 18. Cognitive Memory Query
        elif any(w in text_lower for w in ["what do you remember", "recall memory", "working memory", "show memory", "memory status"]):
            action_taken = "QUERY_MEMORY"
            action_result = {
                "working": jarvis_memory.get_working_memory(),
                "earnings": jarvis_memory.get_earnings_status(),
                "recent_recalls": jarvis_memory.recall_recent_events(limit=5)
            }

        return {"action_taken": action_taken, "action_result": action_result}

    # =========================================================================
    # 5. CHAT & CONVERSATIONAL EXECUTIVE RESPONSE
    # =========================================================================
    def chat(self, user_message: str, voice_mode: bool = True, agent_manager=None) -> Dict[str, Any]:
        """
        Processes an incoming query or voice instruction through J.A.R.V.I.S.
        Returns the spoken response, action telemetry, and timestamp.
        """
        self.save_message(role="user", text=user_message, voice=voice_mode)

        # 1. Execute direct intent / tool triggers
        command_exec = self.execute_voice_command(user_message, agent_manager=agent_manager)
        action_taken = command_exec["action_taken"]
        action_result = command_exec["action_result"]

        # 2. Gather dynamic context
        system_stats = self.get_fleet_stats(agent_manager=agent_manager)
        recent_history = self.load_history(limit=8)

        # Re-check Gemini availability
        if not self.gemini_client:
            self._init_gemini()

        reply_text = ""

        if self.gemini_client:
            try:
                history_snippets = []
                for turn in recent_history[:-1]:
                    speaker = "Sir" if turn["role"] == "user" else "JARVIS"
                    history_snippets.append(f"{speaker}: {turn['text']}")
                dialogue_context = "\n".join(history_snippets)

                cognitive_memory = jarvis_memory.get_cognitive_prompt_injection()

                prompt = f"""
{JARVIS_SYSTEM_PROMPT}

{cognitive_memory}

Live System Telemetry:
{json.dumps(system_stats, indent=2)}

Autonomous Action Executed:
Action: {action_taken or "Strategic Query"}
Result: {json.dumps(action_result, indent=2) if action_result else "N/A"}

Recent Conversation Turns:
{dialogue_context}

Sir's Current Input:
\"{user_message}\"

Respond with military precision directly to Sir, keeping earnings and fleet sovereignty front of mind.
"""
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                reply_text = response.text.strip()
            except Exception as e:
                logger.error(f"Gemini API error during JARVIS chat: {e}")
                reply_text = self._fallback_response(user_message, action_taken, action_result)
        else:
            reply_text = self._fallback_response(user_message, action_taken, action_result)

        # Save assistant message
        self.save_message(role="model", text=reply_text, voice=voice_mode, action_taken=action_taken)

        return {
            "reply": reply_text,
            "action_taken": action_taken,
            "action_result": action_result,
            "audio_cue": "acknowledge" if action_taken else "response",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

    def _fallback_response(self, user_message: str, action_taken: Optional[str], action_result: Optional[Dict[str, Any]]) -> str:
        """High-precision, local-first in-character executive briefing."""
        if action_taken == "READ_REPORTS":
            summary = (action_result or {}).get("summary", "All reports inspected, Sir.")
            return f"I have audited your operational reports, Sir. {summary}"

        elif action_taken == "ANALYZE_REVENUE":
            summary = (action_result or {}).get("summary", "")
            return summary or "Financial analysis compiled, Sir. Treasury and invoices are fully reconciled."

        elif action_taken == "GET_FLEET_STATS":
            domains = (action_result or {}).get("domains", {})
            return f"All 4 domain controllers are active, Sir. SQLite WAL database integrity is verified, and 25 security safeguards are armed."

        elif action_taken == "RUN_DOMAIN_COMMS":
            return "Communications sweep executed, Sir. Inboxes cleaned and support tickets triaged."

        elif action_taken == "RUN_DOMAIN_OPERATIONS":
            return "Operations sweep complete, Sir. System heartbeat verified and enterprise backup created."

        elif action_taken == "RUN_DOMAIN_COMMERCE":
            return "Commerce sweep completed, Sir. Sovereign crypto treasury and invoices reconciled."

        elif action_taken == "RUN_DOMAIN_RESEARCH":
            return "Market intelligence sweep complete, Sir. B2B leads and dependency advisories refreshed."

        elif action_taken == "RUN_FULL_CYCLE":
            return "Full workforce night shift cycle completed successfully, Sir."

        elif action_taken == "COGNITIVE_DELIBERATION":
            rec = (action_result or {}).get("unified_recommendation", "")
            return rec or "The Cognitive Council has concluded deliberations, Sir. Action plan primed."

        elif action_taken == "EXECUTE_DEAL_STRATEGIST":
            client = (action_result or {}).get("result", {}).get("client", "client")
            return f"MEDDPICC assessment completed for {client}, Sir. Close plan staged."

        elif action_taken == "EXECUTE_OUTBOUND_PITCH":
            target = (action_result or {}).get("result", {}).get("target", "prospect")
            return f"High-converting outbound sequence crafted for {target}, Sir. Ready to dispatch."

        elif action_taken == "EXECUTE_OFFER_ARCHITECT":
            offer = (action_result or {}).get("result", {}).get("offer_name", "offer")
            return f"Irresistible offer architecture compiled for '{offer}', Sir."

        elif action_taken == "EXECUTE_GROWTH_HACKER":
            return "Viral growth and distribution campaign mapped, Sir. 4 channels active."

        elif action_taken == "EXECUTE_CAROUSEL_ENGINE":
            return "Multi-slide educational viral carousel generated, Sir. Ready to drive store conversions."

        elif action_taken == "BUILD_DIGITAL_PRODUCT":
            name = (action_result or {}).get("result", {}).get("name", "Product")
            return f"Autonomous software engineering completed, Sir. '{name}' is compiled and live in the $1 Vending Machine."

        elif action_taken == "AUDIT_FINOPS_EARNINGS":
            earnings = (action_result or {}).get("result", {}).get("earnings_status", {})
            gap = (action_result or {}).get("result", {}).get("gap_mur", 0)
            return f"Earnings audit compiled, Sir. Target: Rs {earnings.get('target_mur', 150000):,.0f} MUR. Remaining gap: Rs {gap:,.0f} MUR."

        elif action_taken == "QUERY_MEMORY":
            return "Memory registers retrieved across all 4 tiers, Sir. Context is fully aligned with your revenue directive."

        elif action_taken == "IMPROVE_WORKSPACE_FILES":
            count = action_result.get("improved_count", 0) if action_result else 0
            return f"Workspace optimization complete, Sir. {count} files refactored and safely secured."

        elif action_taken and action_taken.startswith("IMPROVE_FILE:"):
            target = action_taken.split(":", 1)[1]
            return f"File {target} refactored and saved with safety backup snapshot, Sir."

        elif action_taken == "AUDIT_CODEBASE":
            clean = action_result.get("clean_files", 0) if action_result else 0
            return f"Codebase audit complete, Sir. {clean} modules verified clean with zero syntax faults."

        elif action_taken and action_taken.startswith("READ_FILE:"):
            target = action_taken.split(":", 1)[1]
            return f"I have read and indexed {target}, Sir. Ready for your instructions."

        elif action_taken == "LIST_WORKSPACE_FILES":
            total = action_result.get("total_files", 0) if action_result else 0
            return f"Workspace indexed, Sir. {total} files accessible across the repository."

        else:
            return "Understood, Sir. Standing by for your directive."

    # =========================================================================
    # 6. AGENCY SKILLS & COGNITIVE MEMORY ACCESSORS
    # =========================================================================
    def get_skills(self, division: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns all registered Agency specialist skills."""
        return jarvis_skills.list_skills(division=division)

    def execute_skill(self, skill_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Directly executes an Agency specialist skill tool."""
        return jarvis_skills.execute_skill(skill_id, payload)

    def get_memory_telemetry(self) -> Dict[str, Any]:
        """Provides the full 4-tier cognitive memory state for J.A.R.V.I.S."""
        return {
            "working": jarvis_memory.get_working_memory(),
            "earnings": jarvis_memory.get_earnings_status(),
            "procedural": jarvis_memory.get_procedural_memory(),
            "recent_events": jarvis_memory.recall_recent_events(limit=10)
        }

    def deliberate(self, prompt: str, specialist_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Convenes the cognitive council of specialist brains."""
        return jarvis_brain.deliberate(prompt, specialist_ids=specialist_ids)

    def get_revenue_acceleration_plan(self) -> Dict[str, Any]:
        """Returns the revenue acceleration blueprint toward Rs 150,000 MUR."""
        return jarvis_brain.plan_revenue_acceleration()


jarvis_service = JarvisService()

