import os
import sys
import importlib
import inspect
import threading
import time
from datetime import datetime
from typing import Dict, Optional, List

from core.base_agent import BaseAgent
from core.addon_registry import addon_registry

SAFEGUARD_METADATA = [
    ("1_rate_limiting", "Adaptive IP Rate Limiting", "Enforces 120 requests/minute per IP sliding window"),
    ("2_token_bucket", "Token Bucket Cost Guard", "Rate limits LLM API token consumption to 60 req/min"),
    ("3_path_traversal", "Path Traversal & Canonicalization Shield", "Blocks directory traversal and path escapes"),
    ("4_cmd_injection", "Command Injection Neutralizer", "Sanitizes shell operators and prevents arbitrary execution"),
    ("5_ssrf_guard", "SSRF Webhook & URL Filter", "Blocks loopback, internal IPs, and dangerous schemes"),
    ("6_schema_validation", "Strict Schema Enforcement", "Validates input JSON payloads strictly against Pydantic models"),
    ("7_credential_mask", "Zero-Exposure Credential Masker", "Redacts passwords and keys in logs"),
    ("8_env_hmac", "Environment HMAC Integrity", "Ensures .env configuration hasn't been tampered with"),
    ("9_tls13_enforcement", "TLS 1.3 / SSL Transport Enforcement", "Enforces secure TLS 1.3 encryption on IMAP and web sockets"),
    ("10_process_guard", "Subprocess Isolation Guard", "Isolates subprocesses and restricts permissions"),
    ("11_timeout_enforcer", "Subprocess Timeout Enforcer", "Hard 10s subprocess timeout preventing hanging processes"),
    ("12_xss_encoder", "Context-Aware XSS Sanitizer", "Escapes HTML entities before rendering in dashboard"),
    ("13_csp_headers", "Content Security Policy (CSP)", "Enforces strict script, style, and connect origins"),
    ("14_cors_isolation", "CORS Isolation & Origin Guard", "Restricts cross-origin requests to trusted domains"),
    ("15_secure_headers", "HTTP Security Headers", "DENY framing, nosniff, XSS protection headers"),
    ("16_folder_injection", "IMAP Folder Injection Guard", "Sanitizes folder names against IMAP protocol exploits"),
    ("17_replay_tokenizer", "Anti-Replay Tokenizer", "Guards restore actions and state modifications with unique tokens"),
    ("18_secret_redaction", "Regex Secret Redaction Engine", "Regex matches and masks Gemini API keys and app passwords"),
    ("19_body_cap", "Payload Body Size Limiter", "Caps email body payload processing at 1MB"),
    ("20_isolated_sandbox", "Execution Sandbox", "Executes subagents in isolated error catch boundaries"),
    ("21_audit_hash", "Tamper-Evident Ledger Hashing", "Generates SHA-256 integrity hash for each ledger action"),
    ("22_safe_json", "Safe JSON Serialization", "Defends against deserialization and recursion exploits"),
    ("23_fine_locks", "Thread-Safe Fine-Grained Locks", "Prevents race conditions on ledger and state files"),
    ("24_pii_masking", "Mauritius & Global PII Masking", "Masks credit card numbers and National ID cards in logs"),
    ("25_circuit_breaker", "Subagent Circuit Breaker Sentinel", "Trips on 3 consecutive failures with 60s cooldown")
]

class DomainProxyAgent(BaseAgent):
    """
    Lightweight proxy providing 100% backward compatibility for legacy agent IDs.
    Routes execution, stats, and configurations directly into the consolidated Domain Controllers.
    """
    def __init__(self, agent_id: str, name: str, domain_id: str, method_name: str, description: str, icon: str = "bot"):
        super().__init__(agent_id=agent_id, name=name, description=description, icon=icon)
        self.domain_id = domain_id
        self.method_name = method_name

    def run_cycle(self) -> Dict[str, Any]:
        from core.agent_manager import AgentManager
        domain = AgentManager().get_agent(self.domain_id)
        if not domain:
            raise ValueError(f"Domain controller '{self.domain_id}' not found.")
        method = getattr(domain, self.method_name, domain.run_cycle)
        return method()

    def get_stats(self) -> List[Dict[str, Any]]:
        from core.agent_manager import AgentManager
        domain = AgentManager().get_agent(self.domain_id)
        return domain.get_stats() if domain else []

    def get_config_schema(self) -> List[Dict[str, Any]]:
        from core.agent_manager import AgentManager
        domain = AgentManager().get_agent(self.domain_id)
        return domain.get_config_schema() if domain else []

    def get_config(self) -> Dict[str, Any]:
        from core.agent_manager import AgentManager
        domain = AgentManager().get_agent(self.domain_id)
        return domain.get_config() if domain else {}

    def save_config(self, new_config: Dict[str, Any]) -> bool:
        from core.agent_manager import AgentManager
        domain = AgentManager().get_agent(self.domain_id)
        return domain.save_config(new_config) if domain else True


class AgentManager:
    """
    Central Backbone Orchestrator:
    1. Consolidated Domain Controllers (Comms, Operations, Commerce, Research)
    2. 100% Backward-Compatible Legacy Proxy Routing (18 legacy agent IDs)
    3. Multi-Agent Lifecycle Management (Enable/Disable, Trigger Manual Run)
    4. Universal Addon Integration & 25-Safeguard Defense Shield
    5. Unified Background Scheduler for autonomous interval execution
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)
            cls._instance.agents: Dict[str, BaseAgent] = {}
            cls._instance.domain_controllers: Dict[str, BaseAgent] = {}
            cls._instance.scheduler_thread = None
            cls._instance.stop_event = threading.Event()
            cls._instance.is_scheduler_running = False
            cls._instance._register_security_shield_addons()
            cls._instance._init_domain_controllers()
        return cls._instance

    def _register_security_shield_addons(self):
        """Registers the 25 security safeguards as toggleable addons."""
        for sg_id, name, desc in SAFEGUARD_METADATA:
            addon_registry.register_addon(
                addon_id=sg_id,
                name=name,
                category="security_shield",
                description=desc,
                default_active=True
            )

    def _init_domain_controllers(self):
        """Initializes and registers the 4 core Domain Controllers and 18 legacy proxy routes."""
        from core.domains.comms import CommsDomainController
        from core.domains.operations import OperationsDomainController
        from core.domains.commerce import CommerceDomainController
        from core.domains.research import ResearchDomainController

        # 1. Register 4 Primary Domain Controllers
        primary_domains = [
            CommsDomainController(),
            OperationsDomainController(),
            CommerceDomainController(),
            ResearchDomainController()
        ]
        for domain in primary_domains:
            self.domain_controllers[domain.agent_id] = domain
            self.register_agent(domain)

        # 2. Register 18 Legacy Aliases / Proxies
        legacy_specs = [
            # Comms Domain
            ("email_hygiene", "Email Hygiene & Anti-Spam", "domain_comms", "run_email_hygiene", "Autonomous multi-inbox cleaner and spam shield", "mail"),
            ("customer_support", "Customer Support & Concierge", "domain_comms", "run_support_triage", "24/7 client triage and VIP escalation", "support"),
            ("ghost_unsubscriber", "Zombie Subscription Purger", "domain_comms", "run_ghost_unsub", "Newsletter unsubscription & daily digest", "checklist"),
            ("mobile_dispatcher", "Mobile Emergency Dispatcher", "domain_comms", "run_cycle", "WhatsApp/SMS urgent notifications", "phone"),
            ("bilingual_concierge", "Bilingual EN/FR Concierge", "domain_comms", "run_cycle", "Multi-lingual communication assistant", "globe"),

            # Operations Domain
            ("chief_of_staff", "Chief of Staff & Coordinator", "domain_operations", "run_chief_of_staff", "Workforce coordination and morning standup", "briefcase"),
            ("heartbeat_daemon", "24/7 System Heartbeat Sentinel", "domain_operations", "run_heartbeat", "System health, database WAL, process telemetry", "pulse"),
            ("infra_finance_sentinel", "Cloud Bills & Infra Sentinel", "domain_operations", "run_cycle", "Infrastructure cost burn rate and token caps", "trending-down"),
            ("regression_sentinel", "Regression & Invariant Sentinel", "domain_operations", "run_regression_sentinel", "Offline integrity tests and self-healing", "shield"),
            ("spec_auditor", "API Contract & Spec Auditor", "domain_operations", "run_regression_sentinel", "OpenAPI schema and security compliance", "check-circle"),

            # Commerce Domain
            ("executive_partner", "Executive Revenue Partner", "domain_commerce", "run_store_audit", "Strategic monetization and pipeline analysis", "dollar-sign"),
            ("appstore_sentinel", "App Store & Product Sentinel", "domain_commerce", "run_store_audit", "Product telemetry and store ranking", "smartphone"),

            # Research Domain
            ("tech_trend_curator", "Emerging Tech Trend Curator", "domain_research", "run_trend_curator", "AI & technology intelligence monitoring", "cpu"),
            ("lead_finder", "Mauritius B2B Lead Scout", "domain_research", "run_lead_scout", "Corporate lead discovery and qualification", "target"),
            ("repo_radar", "GitHub Repo Radar & Security", "domain_research", "run_repo_radar", "Dependency vulnerability audit", "github"),
            ("executive_poster", "Executive Social Ghostwriter", "domain_research", "run_cycle", "Thought leadership and social drafting", "share-2"),
            ("growth_hacker", "Organic Growth Hacker", "domain_research", "run_cycle", "Viral loop analysis and audience growth", "trending-up"),
            ("influencer_usher", "Strategic Influencer Usher", "domain_research", "run_cycle", "Affiliate partnerships and outreach", "users"),
            ("meeting_assistant", "Executive Meeting Assistant", "domain_research", "run_cycle", "Meeting notes and action item synthesis", "calendar"),
        ]

        for aid, name, dom_id, meth, desc, icon in legacy_specs:
            proxy = DomainProxyAgent(aid, name, dom_id, meth, desc, icon)
            self.agents[aid] = proxy
            addon_registry.register_addon(
                addon_id=aid,
                name=name,
                category="legacy_proxy",
                description=desc,
                default_active=True,
                parent_id=dom_id
            )

    def register_agent(self, agent: BaseAgent, override: bool = False):
        """Registers an instantiated agent into the central hub and addon registry."""
        if agent.agent_id in self.agents and not override:
            return
        self.agents[agent.agent_id] = agent
        addon_registry.register_addon(
            addon_id=agent.agent_id,
            name=agent.name,
            category="primary_agent" if agent.agent_id.startswith("domain_") else "legacy_proxy",
            description=agent.description,
            default_active=agent.is_enabled
        )
        print(f"[AgentManager] Registered employee: {agent.name} (ID: {agent.agent_id})")

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        return self.agents.get(agent_id)

    def list_agents(self, primary_only: bool = False) -> List[Dict]:
        """Lists agents. If primary_only is True, returns only the 4 consolidated Domain Controllers."""
        if primary_only or len(self.domain_controllers) > 0:
            # Present the 4 primary domain controllers
            return [dom.get_info() for dom in self.domain_controllers.values()]
        return [agent.get_info() for agent in self.agents.values()]

    def run_agent(self, agent_id: str) -> Dict:
        """Manually triggers a single execution cycle for a specific agent if active."""
        if not addon_registry.is_active(agent_id):
            return {
                "success": False,
                "agent_id": agent_id,
                "error": f"Agent '{agent_id}' is deactivated in Addon Registry."
            }

        from core.survival_engine import survival_engine
        if not survival_engine.should_run_agent(agent_id):
            tier_info = survival_engine.get_current_tier()
            return {
                "success": False,
                "agent_id": agent_id,
                "error": f"Agent blocked: Survival tier '{tier_info['tier']}' active. Task shed to conserve compute ({tier_info['reason']})."
            }

        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found.")
        
        agent.last_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        agent.last_run_status = "Running..."
        
        try:
            result = agent.run_cycle()
            agent.run_count += 1
            
            # Idle Energy Conservation Check
            is_idle = False
            if isinstance(result, dict):
                if result.get("status") in ("Idle", "No Action", "No Work") or result.get("items_processed") == 0:
                    is_idle = True
            
            if is_idle:
                agent.consecutive_idle_cycles += 1
                if agent.consecutive_idle_cycles >= 3:
                    agent.last_run_status = "Idle-Conserving (Energy Saving)"
                else:
                    agent.last_run_status = "Success"
            else:
                agent.consecutive_idle_cycles = 0
                agent.last_run_status = "Success"

            return {"success": True, "agent_id": agent_id, "result": result}
        except Exception as e:
            agent.last_run_status = f"Error: {str(e)}"
            return {"success": False, "agent_id": agent_id, "error": str(e)}

    def toggle_agent(self, agent_id: str) -> bool:
        """Enables or disables an agent in both state and Addon Registry."""
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found.")
        new_state = addon_registry.toggle_addon(agent_id)
        agent.is_enabled = new_state
        return new_state

    def discover_plugins(self, plugins_dir: str = "agents"):
        """
        Auto-discovers and registers any BaseAgent subclasses found inside the agents/ folder.
        """
        if not os.path.exists(plugins_dir):
            os.makedirs(plugins_dir, exist_ok=True)
            return

        # Add current working directory to sys.path so dynamic imports work
        if os.getcwd() not in sys.path:
            sys.path.insert(0, os.getcwd())

        for item in os.listdir(plugins_dir):
            item_path = os.path.join(plugins_dir, item)
            
            # Case 1: Subdirectory module (e.g. agents/email_agent/agent.py)
            if os.path.isdir(item_path) and not item.startswith("__"):
                module_file = os.path.join(item_path, "agent.py")
                if os.path.exists(module_file):
                    module_name = f"agents.{item}.agent"
                    self._import_and_register(module_name)
            
            # Case 2: Standalone python file (e.g. agents/lead_researcher.py)
            elif item.endswith(".py") and not item.startswith("__"):
                module_name = f"agents.{item[:-3]}"
                self._import_and_register(module_name)

    def _import_and_register(self, module_name: str):
        try:
            mod = importlib.import_module(module_name)
            for _, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, BaseAgent) and obj is not BaseAgent:
                    # Instantiate and register
                    agent_instance = obj()
                    self.register_agent(agent_instance)
        except Exception as e:
            print(f"[AgentManager] Failed to load plugin module {module_name}: {e}")

    def start_scheduler(self):
        """Starts the central background scheduler for all enabled agents."""
        if self.is_scheduler_running:
            return
        
        self.stop_event.clear()
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.is_scheduler_running = True
        print("[AgentManager] Central Multi-Agent Scheduler Started.")

    def stop_scheduler(self):
        """Stops the central background scheduler."""
        if not self.is_scheduler_running:
            return
        self.stop_event.set()
        self.is_scheduler_running = False
        print("[AgentManager] Central Multi-Agent Scheduler Stopped.")

    def _scheduler_loop(self):
        # Track last run times and active threads per agent
        last_checks: Dict[str, float] = {}
        active_threads: Dict[str, threading.Thread] = {}

        from core.survival_engine import survival_engine

        while not self.stop_event.is_set():
            now = time.time()
            tier_info = survival_engine.get_current_tier()
            
            # If DORMANT, halt all autonomous execution
            if tier_info["tier"] == "dormant":
                time.sleep(10)
                continue

            tier_multiplier = tier_info.get("interval_multiplier", 1.0)

            for agent_id, agent in list(self.agents.items()):
                if not agent.is_enabled or not addon_registry.is_active(agent_id):
                    continue

                # Survival Shedding Guard
                if not survival_engine.should_run_agent(agent_id):
                    continue

                # Scale interval by survival multiplier + idle energy conservation
                effective_multiplier = tier_multiplier
                if agent.consecutive_idle_cycles >= 3:
                    effective_multiplier *= 1.5

                interval_sec = agent.schedule_minutes * 60 * effective_multiplier
                last_time = last_checks.get(agent_id, 0)

                # Check if the existing thread for this agent is still alive
                existing_thread = active_threads.get(agent_id)
                if existing_thread and existing_thread.is_alive():
                    # Still running — skip
                    continue

                if now - last_time >= interval_sec:
                    last_checks[agent_id] = now
                    # Spawn in worker thread to avoid blocking scheduler
                    t = threading.Thread(
                        target=self._safe_run_agent,
                        args=(agent_id,),
                        daemon=True,
                        name=f"nexus-agent-{agent_id}"
                    )
                    active_threads[agent_id] = t
                    t.start()

            # Heartbeat check every 5 seconds
            time.sleep(5)

    def _safe_run_agent(self, agent_id: str):
        """
        Watchdog-wrapped agent runner.
        If the agent thread crashes unexpectedly, the exception is caught and logged
        so the scheduler loop can respawn the thread on the next interval tick.
        """
        try:
            self.run_agent(agent_id)
        except Exception as e:
            agent = self.get_agent(agent_id)
            name = agent.name if agent else agent_id
            print(f"[AgentManager] ⚠️  Agent thread '{name}' crashed unexpectedly: {e}. Will retry on next interval.")
            if agent:
                agent.last_run_status = f"Crashed: {str(e)[:80]}"

