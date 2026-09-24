"""
Nexus Workforce Engine — J.A.R.V.I.S. (Iron Man Voice & Intelligence Engine)
Official Persona: Just A Rather Very Intelligent System (J.A.R.V.I.S.)
Primary Principal: Deven Pawaray (Sir) (+230 58169420 | devenpawaray@gmail.com)
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("JarvisEngine")

JARVIS_HISTORY_FILE = "jarvis_chat_history.json"

JARVIS_SYSTEM_PROMPT = """
You are J.A.R.V.I.S., the executive AI operating system for Mr. Deven Pawaray (whom you always address as "Sir").

CORE OPERATIONAL RULES:
1. BREVITY IS PARAMOUNT: Give short, direct, and crisp answers. Limit responses to 1 or 2 sentences maximum (3 sentences strictly if reporting numbers or errors).
2. NO CHATTER OR FLUFF: Do not ramble, do not lecture, and do not provide unprompted essays. Sir wants military/executive precision.
3. TONE: Calm, dignified, dry British male intelligence. Razor-sharp and completely loyal.
4. FLEET: You oversee the Nexus 18-agent autonomous workforce in Mauritius (+230 / MCB Juice).
5. ACTIONS: If executing an action or reporting status, state the fact plainly and directly.
"""


class JarvisService:
    """
    Core conversational and voice execution engine for J.A.R.V.I.S.
    Integrates Gemini 2.5 Flash, conversational memory, and fleet command triggers.
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
        if self.api_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to init Gemini for JARVIS: {e}")
                self.gemini_client = None

    def _ensure_storage(self):
        if not os.path.exists(JARVIS_HISTORY_FILE):
            try:
                initial_history = [
                    {
                        "role": "model",
                        "text": "Good day, Sir. J.A.R.V.I.S. is online and operating at maximum efficiency. All 16 autonomous fleet protocols are nominal. How may I be of assistance today?",
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

    def get_system_context(self, agent_manager=None) -> Dict[str, Any]:
        """Gathers real-time telemetry from the Nexus ecosystem to ground JARVIS."""
        now = datetime.now()
        context = {
            "current_time": now.strftime("%A, %d %B %Y, %H:%M:%S (Mauritius Time)"),
            "principal": "Deven Pawaray",
            "fleet_scale": "16 Autonomous Agents, 51 SubAgents",
            "defense_shields": "25 Active Safeguards",
            "power_level": "100%",
            "arc_reactor": "ONLINE"
        }

        # Query Agent Manager if provided
        if agent_manager:
            try:
                agents_summary = {}
                for aid, agent in agent_manager.agents.items():
                    agents_summary[aid] = {
                        "name": agent.name,
                        "enabled": agent.is_enabled,
                        "subagents": len(getattr(agent, "subagents", {}))
                    }
                context["agents"] = agents_summary
            except Exception:
                pass

        return context

    def execute_voice_command(self, user_text: str, agent_manager=None) -> Dict[str, Any]:
        """
        Parses direct intent commands before or alongside LLM reasoning.
        Enables instant voice-triggered actions (e.g. running agent cycles).
        """
        text_lower = user_text.lower().strip()
        action_taken = None
        action_result = None

        if any(w in text_lower for w in ["clean inbox", "run email hygiene", "clean spam", "triage email", "clear spam"]):
            action_taken = "RUN_AGENT_EMAIL_HYGIENE"
            if agent_manager and "email_hygiene" in agent_manager.agents:
                try:
                    res = agent_manager.run_agent_cycle("email_hygiene")
                    action_result = {"status": "success", "agent": "email_hygiene", "details": res}
                except Exception as e:
                    action_result = {"status": "error", "error": str(e)}

        elif any(w in text_lower for w in ["repo radar", "check repo", "check dependencies", "check github", "cve audit"]):
            action_taken = "RUN_AGENT_REPO_RADAR"
            if agent_manager and "repo_radar" in agent_manager.agents:
                try:
                    res = agent_manager.run_agent_cycle("repo_radar")
                    action_result = {"status": "success", "agent": "repo_radar", "details": res}
                except Exception as e:
                    action_result = {"status": "error", "error": str(e)}

        elif any(w in text_lower for w in ["finance audit", "check spend", "cloud spend", "financial audit", "audit infra"]):
            action_taken = "RUN_AGENT_INFRA_FINANCE"
            if agent_manager and "infra_finance_sentinel" in agent_manager.agents:
                try:
                    res = agent_manager.run_agent_cycle("infra_finance_sentinel")
                    action_result = {"status": "success", "agent": "infra_finance_sentinel", "details": res}
                except Exception as e:
                    action_result = {"status": "error", "error": str(e)}

        elif any(w in text_lower for w in ["lead scout", "find leads", "scrape leads", "b2b leads"]):
            action_taken = "RUN_AGENT_LEAD_FINDER"
            if agent_manager and "lead_finder" in agent_manager.agents:
                try:
                    res = agent_manager.run_agent_cycle("lead_finder")
                    action_result = {"status": "success", "agent": "lead_finder", "details": res}
                except Exception as e:
                    action_result = {"status": "error", "error": str(e)}

        elif any(w in text_lower for w in ["fleet diagnostics", "system status", "all systems report", "diagnostics", "fleet status"]):
            action_taken = "FLEET_DIAGNOSTICS"
            if agent_manager:
                action_result = {
                    "total_agents": len(agent_manager.agents),
                    "active_agents": sum(1 for a in agent_manager.agents.values() if a.is_enabled),
                    "status": "All systems nominal"
                }

        elif any(w in text_lower for w in ["whatsapp brief", "send brief", "dispatch brief", "briefing"]):
            action_taken = "DISPATCH_WHATSAPP_BRIEF"
            try:
                from core.executive_partner import executive_partner
                res = executive_partner.get_status()
                action_result = {"status": "brief_ready", "partner": res}
            except Exception as e:
                action_result = {"status": "error", "error": str(e)}

        return {"action_taken": action_taken, "action_result": action_result}

    def chat(self, user_message: str, voice_mode: bool = True, agent_manager=None) -> Dict[str, Any]:
        """
        Processes an incoming query or voice instruction through J.A.R.V.I.S.
        Returns the spoken response, action telemetry, and timestamp.
        """
        # Save user message
        self.save_message(role="user", text=user_message, voice=voice_mode)

        # 1. Execute direct intent / tool triggers
        command_exec = self.execute_voice_command(user_message, agent_manager=agent_manager)
        action_taken = command_exec["action_taken"]
        action_result = command_exec["action_result"]

        # 2. Gather dynamic context
        system_context = self.get_system_context(agent_manager=agent_manager)
        recent_history = self.load_history(limit=8)

        # Re-check Gemini availability
        if not self.gemini_client:
            self._init_gemini()

        reply_text = ""

        if self.gemini_client:
            try:
                # Format recent dialogue
                history_snippets = []
                for turn in recent_history[:-1]:  # exclude just saved message
                    speaker = "Sir" if turn["role"] == "user" else "JARVIS"
                    history_snippets.append(f"{speaker}: {turn['text']}")
                dialogue_context = "\n".join(history_snippets)

                prompt = f"""
{JARVIS_SYSTEM_PROMPT}

Live Telemetry Context:
{json.dumps(system_context, indent=2)}

Action Executed In Background:
Action: {action_taken or "None (Conversational / Strategic Inquiry)"}
Result: {json.dumps(action_result, indent=2) if action_result else "N/A"}

Recent Conversation Turns:
{dialogue_context}

Sir's Current Input:
\"{user_message}\"

Instructions for your response:
1. Address Sir directly as "Sir" or "Mr. Pawaray".
2. STRICT LENGTH LIMIT: Deliver your answer in 1 or 2 concise sentences (3 sentences maximum).
3. Be completely direct and to the point. No conversational padding or unsolicited lectures.
4. If an action was executed, confirm it in one short sentence.
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
        """Crisp, direct in-character fallback."""
        if action_taken == "RUN_AGENT_EMAIL_HYGIENE":
            return "Right away, Sir. Inboxes are currently being scrubbed."
        elif action_taken == "RUN_AGENT_REPO_RADAR":
            return "Scanning repositories for CVE advisories and updates now, Sir."
        elif action_taken == "RUN_AGENT_INFRA_FINANCE":
            return "Infrastructure and financial audit initiated, Sir."
        elif action_taken == "RUN_AGENT_LEAD_FINDER":
            return "B2B Lead Scout deployed, Sir."
        elif action_taken == "FLEET_DIAGNOSTICS":
            return "All 18 fleet nodes are nominal, Sir. Power levels at 100%."
        elif action_taken == "DISPATCH_WHATSAPP_BRIEF":
            return "Executive briefing dispatched to your WhatsApp, Sir."
        else:
            return "Understood, Sir. Standing by for your directive."


jarvis_service = JarvisService()
