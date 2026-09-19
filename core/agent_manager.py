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

class AgentManager:
    """
    Central Backbone Orchestrator:
    1. Dynamic Discovery & Plugin Registry (loads all agents in agents/ folder)
    2. Multi-Agent Lifecycle Management (Enable/Disable, Trigger Manual Run)
    3. Universal Addon Integration & 25-Safeguard Defense Shield
    4. Unified Background Scheduler for each agent's custom interval
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentManager, cls).__new__(cls)
            cls._instance.agents: Dict[str, BaseAgent] = {}
            cls._instance.scheduler_thread = None
            cls._instance.stop_event = threading.Event()
            cls._instance.is_scheduler_running = False
            cls._instance._register_security_shield_addons()
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

    def register_agent(self, agent: BaseAgent):
        """Registers an instantiated agent into the central hub and addon registry."""
        self.agents[agent.agent_id] = agent
        addon_registry.register_addon(
            addon_id=agent.agent_id,
            name=agent.name,
            category="primary_agent",
            description=agent.description,
            default_active=agent.is_enabled
        )
        print(f"[AgentManager] Registered employee: {agent.name} (ID: {agent.agent_id})")

    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        return self.agents.get(agent_id)

    def list_agents(self) -> List[Dict]:
        return [agent.get_info() for agent in self.agents.values()]

    def run_agent(self, agent_id: str) -> Dict:
        """Manually triggers a single execution cycle for a specific agent if active."""
        if not addon_registry.is_active(agent_id):
            return {
                "success": False,
                "agent_id": agent_id,
                "error": f"Agent '{agent_id}' is deactivated in Addon Registry."
            }

        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent '{agent_id}' not found.")
        
        agent.last_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        agent.last_run_status = "Running..."
        
        try:
            result = agent.run_cycle()
            agent.run_count += 1
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

        while not self.stop_event.is_set():
            now = time.time()
            for agent_id, agent in list(self.agents.items()):
                if not agent.is_enabled or not addon_registry.is_active(agent_id):
                    continue

                interval_sec = agent.schedule_minutes * 60
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

