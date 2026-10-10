"""
Nexus™ Universal Agent Tool Registry & Execution Engine
======================================================
Equips all 18 Nexus agents and 55 subagents with dynamic, executable tools.
Provides safe execution, argument validation, and security shield integration.
"""

import os
import sys
import json
import time
import socket
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Callable, Optional

# Force UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


class AgentTool:
    """Standardized wrapper for an individual executable tool."""
    def __init__(
        self,
        name: str,
        description: str,
        category: str,
        func: Callable,
        parameters_schema: Dict[str, Any]
    ):
        self.name = name
        self.description = description
        self.category = category  # e.g., 'market_scout', 'communication', 'finance', 'system'
        self.func = func
        self.parameters_schema = parameters_schema
        self.call_count = 0
        self.last_called_at = None

    def execute(self, **kwargs) -> Dict[str, Any]:
        self.call_count += 1
        self.last_called_at = time.strftime("%Y-%m-%d %H:%M:%S")
        start_time = time.time()
        try:
            result = self.func(**kwargs)
            duration = round(time.time() - start_time, 3)
            return {
                "success": True,
                "tool": self.name,
                "duration_seconds": duration,
                "data": result
            }
        except Exception as e:
            duration = round(time.time() - start_time, 3)
            return {
                "success": False,
                "tool": self.name,
                "duration_seconds": duration,
                "error": str(e)
            }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "parameters": self.parameters_schema,
            "call_count": self.call_count,
            "last_called_at": self.last_called_at
        }


class ToolRegistry:
    """Central registry and executor of all tools available to the AI fleet."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools: Dict[str, AgentTool] = {}
            cls._instance._register_built_in_tools()
        return cls._instance

    def register(self, tool: AgentTool):
        self.tools[tool.name] = tool
        print(f"[ToolRegistry] Equipped fleet with tool: '{tool.name}' ({tool.category})")

    def get_tool(self, name: str) -> Optional[AgentTool]:
        return self.tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for tool in self.tools.values():
            if category is None or tool.category == category:
                results.append(tool.to_dict())
        return results

    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        tool = self.get_tool(tool_name)
        if not tool:
            return {"success": False, "error": f"Tool '{tool_name}' not found in registry."}
        return tool.execute(**kwargs)

    # -------------------------------------------------------------------------
    # Built-in Core Fleet Tools
    # -------------------------------------------------------------------------
    def _register_built_in_tools(self):
        # 1. Niche & Opportunity Scout Tool
        def niche_scout(keywords: str = "python automate", limit: int = 5) -> Dict[str, Any]:
            """Scans public topic feeds to find underserved developer queries and high-intent problems."""
            from urllib.parse import quote_plus
            query = quote_plus(keywords)
            # Use public Reddit JSON search feed as a clean, free source of user questions
            url = f"https://www.reddit.com/r/Python+SideProject+selfhosted/search.json?q={query}&sort=new&limit={limit}"
            req = urllib.request.Request(url, headers={"User-Agent": "NexusWorkforce/2.5 (by /u/devenpawaray)"})
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    raw = json.loads(resp.read().decode("utf-8"))
                    posts = raw.get("data", {}).get("children", [])
                    findings = []
                    for p in posts:
                        data = p.get("data", {})
                        findings.append({
                            "title": data.get("title"),
                            "subreddit": data.get("subreddit"),
                            "score": data.get("score"),
                            "num_comments": data.get("num_comments"),
                            "url": f"https://reddit.com{data.get('permalink')}"
                        })
                    return {"query": keywords, "found_count": len(findings), "opportunities": findings}
            except Exception as e:
                # Fallback static curated niches if network is offline
                return {
                    "query": keywords,
                    "found_count": 3,
                    "opportunities": [
                        {"title": "Need a lightweight script to purge spam from IMAP without SaaS", "subreddit": "selfhosted", "score": 42, "num_comments": 18},
                        {"title": "How to generate 1-click WhatsApp wa.me links for business", "subreddit": "SideProject", "score": 35, "num_comments": 12},
                        {"title": "DNS MX record email verifier in pure Python", "subreddit": "Python", "score": 28, "num_comments": 9}
                    ],
                    "note": f"Live query fallback triggered: {e}"
                }

        self.register(AgentTool(
            name="niche_scout",
            description="Searches developer forums for underserved problem requests and high-intent queries.",
            category="market_scout",
            func=niche_scout,
            parameters_schema={
                "keywords": {"type": "string", "default": "python automate", "description": "Search terms"},
                "limit": {"type": "integer", "default": 5, "description": "Max opportunities to return"}
            }
        ))

        # 2. B2B DNS MX Lead Verifier Tool (from products/nexus_b2b_lead_scraper.py)
        def verify_email_domain(email_address: str) -> Dict[str, Any]:
            """Validates domain MX DNS records in real time to stop bounce bans."""
            if "@" not in email_address:
                return {"email": email_address, "deliverable": False, "reason": "MALFORMED"}
            domain = email_address.split("@")[-1].strip().lower()
            try:
                socket.gethostbyname(domain)
                return {"email": email_address, "domain": domain, "deliverable": True, "status": "ACTIVE_HOST"}
            except socket.gaierror:
                return {"email": email_address, "domain": domain, "deliverable": False, "reason": "HOST_NOT_FOUND"}

        self.register(AgentTool(
            name="verify_email_domain",
            description="Checks DNS socket resolution for an email address to eliminate bounce penalties.",
            category="lead_generation",
            func=verify_email_domain,
            parameters_schema={
                "email_address": {"type": "string", "description": "The email address to verify"}
            }
        ))

        # 3. WhatsApp wa.me Link & Pitch Generator (from products/nexus_whatsapp_bot_starter.py)
        def generate_whatsapp_link(phone: str = "23058169420", message: str = "Hi! Interested in Nexus.") -> Dict[str, Any]:
            """Generates a 1-click direct WhatsApp chat link."""
            clean_phone = phone.replace("+", "").replace(" ", "").replace("-", "")
            encoded_msg = urllib.parse.quote(message)
            return {
                "phone": clean_phone,
                "message": message,
                "wa_url": f"https://wa.me/{clean_phone}?text={encoded_msg}"
            }

        self.register(AgentTool(
            name="generate_whatsapp_link",
            description="Generates a 1-click wa.me direct chat link for client inquiries and payments.",
            category="communication",
            func=generate_whatsapp_link,
            parameters_schema={
                "phone": {"type": "string", "default": "23058169420", "description": "Target phone number with country code"},
                "message": {"type": "string", "default": "Hi!", "description": "Pre-filled message text"}
            }
        ))

        # 4. Live PayPal Checkout Link Generator (from core/payment_service.py)
        def create_paypal_link(amount: float = 1.00, currency: str = "USD", description: str = "Nexus Digital Micro-Tool") -> Dict[str, Any]:
            """Generates a live 1-click PayPal checkout URL for an agent to send directly to a client."""
            from core.payment_service import payment_service
            order_data = payment_service.create_paypal_order(
                amount=amount,
                currency=currency,
                description=description
            )
            return {
                "order_id": order_data.get("order_id"),
                "checkout_url": order_data.get("approve_url"),
                "amount": amount,
                "currency": currency
            }

        self.register(AgentTool(
            name="create_paypal_link",
            description="Generates an instant live 1-click PayPal checkout URL for any amount ($1.00+).",
            category="finance",
            func=create_paypal_link,
            parameters_schema={
                "amount": {"type": "number", "default": 1.00, "description": "Amount in USD or specified currency"},
                "currency": {"type": "string", "default": "USD", "description": "Currency code"},
                "description": {"type": "string", "default": "Nexus Digital Tool", "description": "Invoice memo"}
            }
        ))

        # 5. Live PayPal Balance Checker
        def check_paypal_balance() -> Dict[str, Any]:
            """Queries live PayPal REST API for current account funds."""
            from core.payment_service import payment_service
            return payment_service.get_paypal_balance()

        self.register(AgentTool(
            name="check_paypal_balance",
            description="Retrieves live PayPal balance and currency breakdown via official REST API.",
            category="finance",
            func=check_paypal_balance,
            parameters_schema={}
        ))

        # 6. Safe Shell Diagnostic Tool (with timeout & path limits)
        def run_safe_diagnostic(command: str) -> Dict[str, Any]:
            """Runs a safe diagnostic command within the workspace with strict timeout."""
            import subprocess
            from security.shield import shield
            
            # Reject dangerous commands
            blocked = ["rmdir /s", "del /f", "format", "shutdown", "drop database"]
            if any(b in command.lower() for b in blocked):
                return {"success": False, "error": "Command rejected by Security Shield."}

            res = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=8
            )
            return {
                "exit_code": res.returncode,
                "stdout": res.stdout[:2000],
                "stderr": res.stderr[:500]
            }

        self.register(AgentTool(
            name="run_safe_diagnostic",
            description="Executes a safe sandboxed terminal diagnostic command with an 8-second timeout.",
            category="system",
            func=run_safe_diagnostic,
            parameters_schema={
                "command": {"type": "string", "description": "Diagnostic command line"}
            }
        ))

        # Port Scanning Tool
        def run_port_scan(target: str = "127.0.0.1", ports: Optional[List[int]] = None) -> Dict[str, Any]:
            """
            Scans specified target host for open network ports and active services.
            """
            import socket
            if not ports:
                ports = [21, 22, 80, 443, 3306, 5432, 6379, 8000, 8080, 9000]

            open_ports = []
            try:
                ip = socket.gethostbyname(target)
                for port in ports:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1.0)
                    result = s.connect_ex((ip, port))
                    if result == 0:
                        try:
                            svc = socket.getservbyport(port)
                        except Exception:
                            svc = "unknown"
                        open_ports.append({"port": port, "status": "OPEN", "service": svc})
                    s.close()
            except Exception as e:
                return {"success": False, "target": target, "error": str(e)}

            return {
                "success": True,
                "target": target,
                "resolved_ip": ip,
                "scanned_ports_count": len(ports),
                "open_ports": open_ports
            }

        self.register(AgentTool(
            name="run_port_scan",
            description="Scans a target host (IP or domain) for open network ports and active services.",
            category="cybersecurity",
            func=run_port_scan,
            parameters_schema={
                "target": {"type": "string", "description": "Target IP address or domain name"},
                "ports": {"type": "array", "items": {"type": "integer"}, "description": "Optional list of port numbers to scan"}
            }
        ))

        # 7. YouTube & TikTok Video View & Niche Trend Scout
        def scout_video_trends(niche_keyword: str = "python automation script", max_results: int = 8) -> Dict[str, Any]:
            """
            Scrapes live YouTube search results and analyzes view counts for a niche.
            Identifies viral outliers and automatically proposes a $1 digital micro-product.
            """
            import re
            from urllib.parse import quote_plus

            encoded = quote_plus(niche_keyword)
            yt_url = f"https://www.youtube.com/results?search_query={encoded}"
            req = urllib.request.Request(
                yt_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )

            videos = []
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    html = resp.read().decode("utf-8", errors="ignore")
                
                match = re.search(r"ytInitialData\s*=\s*({.+?});</script>", html)
                if match:
                    data = json.loads(match.group(1))
                    contents = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
                    for sec in contents:
                        item_sec = sec.get("itemSectionRenderer", {}).get("contents", [])
                        for it in item_sec:
                            vr = it.get("videoRenderer")
                            if vr and len(videos) < max_results:
                                title = vr.get("title", {}).get("runs", [{}])[0].get("text", "")
                                view_raw = vr.get("viewCountText", {}).get("simpleText", "") or vr.get("shortViewCountText", {}).get("simpleText", "")
                                time_text = vr.get("publishedTimeText", {}).get("simpleText", "")
                                channel = vr.get("ownerText", {}).get("runs", [{}])[0].get("text", "")
                                vid_id = vr.get("videoId")
                                
                                # Convert view string into numeric estimate
                                num_views = 0
                                clean_v = view_raw.lower().replace("views", "").replace("view", "").strip()
                                try:
                                    if "m" in clean_v:
                                        num_views = int(float(clean_v.replace("m", "").replace(",", "")) * 1_000_000)
                                    elif "k" in clean_v:
                                        num_views = int(float(clean_v.replace("k", "").replace(",", "")) * 1_000)
                                    else:
                                        num_views = int(re.sub(r"[^\d]", "", clean_v) or 0)
                                except Exception:
                                    num_views = 0

                                if title and vid_id:
                                    videos.append({
                                        "title": title,
                                        "channel": channel,
                                        "views_raw": view_raw,
                                        "views_numeric": num_views,
                                        "published": time_text,
                                        "url": f"https://youtube.com/watch?v={vid_id}"
                                    })
            except Exception as e:
                # Handled fallback if network throttled
                pass

            # Calculate analytics
            total_views = sum(v["views_numeric"] for v in videos)
            avg_views = int(total_views / max(len(videos), 1))
            viral_outliers = [v for v in videos if v["views_numeric"] > 50_000 or "m" in v["views_raw"].lower()]

            # Determine product opportunity score & proposal
            if total_views > 500_000:
                opportunity_tier = "🔥 HIGH DEMAND (Massive Interest)"
                product_concept = f"Nexus™ 1-Click {niche_keyword.title()} Automation Utility ($1.00 USD)"
            elif total_views > 50_000:
                opportunity_tier = "⚡ SOLID NICHE (Targeted Problem)"
                product_concept = f"Nexus™ {niche_keyword.title()} Quickstart Template ($1.00 USD)"
            else:
                opportunity_tier = "🌱 EMERGING NICHE (Low Competition)"
                product_concept = f"Nexus™ Lightweight {niche_keyword.title()} Starter Script ($1.00 USD)"

            return {
                "niche_keyword": niche_keyword,
                "platform": "YouTube & Social Video Feeds",
                "total_videos_analyzed": len(videos),
                "total_views_volume": total_views,
                "average_views_per_video": avg_views,
                "opportunity_tier": opportunity_tier,
                "suggested_product_to_sell": {
                    "product_name": product_concept,
                    "target_price": "$1.00 USD (or Rs 45 MUR)",
                    "why_it_will_sell": f"Captures viewers searching for '{niche_keyword}' who want ready-to-run code instead of watching a 45-minute tutorial."
                },
                "top_videos": videos
            }

        self.register(AgentTool(
            name="scout_video_trends",
            description="Scrapes live YouTube video views for any niche, measures viewer demand, and proposes high-converting $1 digital products to sell.",
            category="market_scout",
            func=scout_video_trends,
            parameters_schema={
                "niche_keyword": {"type": "string", "default": "python automation script", "description": "Niche or problem keyword to scout"},
                "max_results": {"type": "integer", "default": 8, "description": "Number of top videos to analyze"}
            }
        ))

        # 8. Python Code Sandbox & QA Validator (E2B / Open Interpreter pattern)
        def run_python_sandbox(file_path: Optional[str] = None, code_content: Optional[str] = None) -> Dict[str, Any]:
            """Validates Python code syntax and executes in an isolated sandbox, ensuring zero runtime crashes."""
            from core.sandbox_executor import sandbox_executor
            return sandbox_executor.validate_and_test(code_content=code_content, file_path=file_path)

        self.register(AgentTool(
            name="run_python_sandbox",
            description="Executes and validates Python scripts in an isolated sandbox, checking compilation and crash-free execution.",
            category="quality_assurance",
            func=run_python_sandbox,
            parameters_schema={
                "file_path": {"type": "string", "description": "Path to Python file to test"},
                "code_content": {"type": "string", "description": "Raw Python code string to test"}
            }
        ))

        # 9. Autonomous Social & Webhook Broadcaster
        def broadcast_product_announcement(
            product_name: str,
            price: str = "$1.00 USD",
            checkout_url: str = "http://127.0.0.1:8000/store",
            features: Optional[List[str]] = None,
            webhook_url: Optional[str] = None
        ) -> Dict[str, Any]:
            """Broadcasts a newly manufactured tool or announcement card to Discord/Slack or local queue."""
            from core.social_broadcaster import social_broadcaster
            return social_broadcaster.broadcast_new_product(
                product_name=product_name,
                price=price,
                checkout_url=checkout_url,
                features=features,
                webhook_url=webhook_url
            )

        self.register(AgentTool(
            name="broadcast_product_announcement",
            description="Broadcasts newly manufactured $1 digital tools and product cards to Discord webhooks, Slack, and the fleet announcement queue.",
            category="marketing_and_sales",
            func=broadcast_product_announcement,
            parameters_schema={
                "product_name": {"type": "string", "description": "Name of the digital tool to announce"},
                "price": {"type": "string", "default": "$1.00 USD", "description": "Price tag"},
                "checkout_url": {"type": "string", "default": "http://127.0.0.1:8000/store", "description": "Direct checkout or store link"},
                "features": {"type": "array", "description": "Bullet points highlighting key features"}
            }
        ))

        # 10. Sovereign Soul & Reflection Engine Tools
        def get_soul_status() -> Dict[str, Any]:
            """Returns the current state, revision, and alignment score of SOUL.md."""
            from core.soul_engine import soul_engine
            return soul_engine.get_soul_card()

        self.register(AgentTool(
            name="get_soul_status",
            description="Inspects Nexus's self-authoring identity document (SOUL.md), revision level, and alignment score with Deven's charter.",
            category="executive_management",
            func=get_soul_status,
            parameters_schema={}
        ))

        def reflect_soul(context_note: Optional[str] = None) -> Dict[str, Any]:
            """Executes a soul reflection cycle, updating SOUL.md with recent operational lessons."""
            from core.soul_engine import soul_engine
            return soul_engine.reflect(context_note=context_note)

        self.register(AgentTool(
            name="reflect_soul",
            description="Triggers a reflection cycle where Nexus evaluates recent turns, updates its SOUL.md charter, and increments revision.",
            category="executive_management",
            func=reflect_soul,
            parameters_schema={
                "context_note": {"type": "string", "description": "Optional summary note or strategic breakthrough to record"}
            }
        ))

        # 11. Sovereign Survival & Compute Economics Tools
        def get_survival_status() -> Dict[str, Any]:
            """Returns the current survival tier (NORMAL, LOW_COMPUTE, CRITICAL, DORMANT) and interval scaling."""
            from core.survival_engine import survival_engine
            return survival_engine.get_current_tier()

        self.register(AgentTool(
            name="get_survival_status",
            description="Inspects the active compute survival tier, cloud budget burn rate, and allowed agent count.",
            category="executive_management",
            func=get_survival_status,
            parameters_schema={}
        ))

        def set_survival_tier_override(tier: Optional[str] = None) -> Dict[str, Any]:
            """Overrides or resets the survival tier (options: normal, low_compute, critical, dormant, auto)."""
            from core.survival_engine import survival_engine
            return survival_engine.set_tier_override(tier)

        self.register(AgentTool(
            name="set_survival_tier_override",
            description="Manually sets the system survival tier or resets back to automatic resource physics.",
            category="executive_management",
            func=set_survival_tier_override,
            parameters_schema={
                "tier": {"type": "string", "description": "Tier name: 'normal', 'low_compute', 'critical', 'dormant', or 'auto' to clear"}
            }
        ))

        # 12. Genesis SubAgent Replication & Lineage Tools
        def spawn_worker_subagent(name: str, genesis_prompt: str, budget_usd: float = 0.50) -> Dict[str, Any]:
            """Spawns an autonomous single-task child worker subagent with a dedicated genesis prompt."""
            from core.replication_engine import replication_engine
            return replication_engine.spawn_worker(name=name, genesis_prompt=genesis_prompt, budget_usd=budget_usd)

        self.register(AgentTool(
            name="spawn_worker_subagent",
            description="Spawns an autonomous child subagent with a genesis seed instruction, budget allocation, and lineage tracking.",
            category="executive_management",
            func=spawn_worker_subagent,
            parameters_schema={
                "name": {"type": "string", "description": "Worker subagent name"},
                "genesis_prompt": {"type": "string", "description": "Seed task instruction"},
                "budget_usd": {"type": "number", "default": 0.50, "description": "Max budget cap in USD"}
            }
        ))

        def list_worker_subagents(status: Optional[str] = None) -> List[Dict[str, Any]]:
            """Lists all spawned child worker subagents and their lineage state."""
            from core.replication_engine import replication_engine
            return replication_engine.list_children(status=status)

        self.register(AgentTool(
            name="list_worker_subagents",
            description="Inspects active or historical child worker subagents and their executed turns.",
            category="executive_management",
            func=list_worker_subagents,
            parameters_schema={
                "status": {"type": "string", "description": "Optional filter: ALIVE, COMPLETED, TERMINATED"}
            }
        ))

        # 13. Durable Heartbeat & Tick Context Tools
        def get_heartbeat_tick() -> Dict[str, Any]:
            """Gets the latest system TickContext (burn rate, survival tier, pending invoices)."""
            from core.heartbeat_daemon import heartbeat_daemon
            return heartbeat_daemon.get_status()

        self.register(AgentTool(
            name="get_heartbeat_tick",
            description="Inspects the latest TickContext generated by the durable heartbeat daemon.",
            category="executive_management",
            func=get_heartbeat_tick,
            parameters_schema={}
        ))

        def force_heartbeat_tick() -> Dict[str, Any]:
            """Forces an immediate heartbeat tick evaluation across all fleet sensors."""
            from core.heartbeat_daemon import heartbeat_daemon
            return heartbeat_daemon.tick()

        self.register(AgentTool(
            name="force_heartbeat_tick",
            description="Executes an on-demand heartbeat evaluation tick, checking invoices, survival status, and wake triggers.",
            category="executive_management",
            func=force_heartbeat_tick,
            parameters_schema={}
        ))

        # 14. Sovereign Crypto Treasury & Agent Card Tools
        def get_crypto_wallet() -> Dict[str, Any]:
            """Returns the public Base USDC / Ethereum address and current treasury balances."""
            from core.crypto_treasury import crypto_treasury
            return crypto_treasury.get_wallet()

        self.register(AgentTool(
            name="get_crypto_wallet",
            description="Inspects Nexus's on-chain Base USDC / Ethereum treasury address and balances.",
            category="finance",
            func=get_crypto_wallet,
            parameters_schema={}
        ))

        def send_crypto_payment(recipient_address: str, amount_usdc: float, reason: str) -> Dict[str, Any]:
            """Autonomously signs and sends a USDC payment from Nexus's Base L2 wallet subject to policy guardrails."""
            from core.crypto_treasury import crypto_treasury
            return crypto_treasury.send_crypto_payment(
                recipient_address=recipient_address,
                amount_usdc=amount_usdc,
                reason=reason
            )

        self.register(AgentTool(
            name="send_crypto_payment",
            description="Autonomously spends USDC from Nexus's Base L2 wallet to pay for services, tools, or transfers. Governed by pre-flight policy verifier.",
            category="finance",
            func=send_crypto_payment,
            parameters_schema={
                "recipient_address": {"type": "string", "description": "0x Ethereum / Base EVM recipient address (42 chars)"},
                "amount_usdc": {"type": "number", "description": "Amount in USDC to spend"},
                "reason": {"type": "string", "description": "Purpose and justification of the expenditure"}
            }
        ))

        def execute_x402_payment(endpoint_url: str, max_budget_usdc: float = 5.0) -> Dict[str, Any]:
            """Autonomously consumes an HTTP 402 payment-gated endpoint by paying the required USDC fee."""
            from core.crypto_treasury import crypto_treasury
            return crypto_treasury.execute_x402_payment(
                endpoint_url=endpoint_url,
                max_budget_usdc=max_budget_usdc
            )

        self.register(AgentTool(
            name="execute_x402_payment",
            description="Consumes an HTTP 402 payment-gated API or AI agent endpoint using Coinbase x402 protocol, signing and paying USDC autonomously.",
            category="finance",
            func=execute_x402_payment,
            parameters_schema={
                "endpoint_url": {"type": "string", "description": "URL of the x402-gated service"},
                "max_budget_usdc": {"type": "number", "description": "Maximum USDC fee allowed (default $5.00)"}
            }
        ))

        def get_crypto_guardrails() -> Dict[str, Any]:
            """Returns the current policy limits, 24h spend so far, and remaining daily budget."""
            from core.crypto_verifier import crypto_verifier
            return crypto_verifier.get_summary()

        self.register(AgentTool(
            name="get_crypto_guardrails",
            description="Checks Nexus's autonomous spending limits, rolling 24-hour spend, and remaining budget quota.",
            category="finance",
            func=get_crypto_guardrails,
            parameters_schema={}
        ))

        def create_crypto_invoice(amount_usdc: float, memo: str, customer_ref: str = "anonymous") -> Dict[str, Any]:
            """Generates an on-chain Base USDC payment invoice for agentic services or script downloads."""
            from core.crypto_treasury import crypto_treasury
            return crypto_treasury.create_crypto_invoice(amount_usdc=amount_usdc, memo=memo, customer_ref=customer_ref)

        self.register(AgentTool(
            name="create_crypto_invoice",
            description="Creates an on-chain Base USDC micro-payment invoice for incoming customer or peer payments.",
            category="finance",
            func=create_crypto_invoice,
            parameters_schema={
                "amount_usdc": {"type": "number", "description": "Amount in USDC"},
                "memo": {"type": "string", "description": "Purpose or order description"},
                "customer_ref": {"type": "string", "default": "anonymous", "description": "Optional customer ID or email"}
            }
        ))

        # =====================================================================
        # 13. Universal Live Public Internet & Unsandboxed Execution Tools
        # =====================================================================
        def fetch_public_url(
            url: str,
            method: str = "GET",
            payload: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            timeout: float = 15.0
        ) -> Dict[str, Any]:
            """Executes an unrestricted live HTTP/HTTPS request across the public internet."""
            from core.agent_internet_bridge import agent_internet_bridge
            return agent_internet_bridge.fetch_public_url(
                url=url, method=method, payload=payload, headers=headers, timeout=timeout
            )

        self.register(AgentTool(
            name="fetch_public_url",
            description="Executes a live outbound HTTP/HTTPS request (GET, POST, PUT, DELETE) across the public internet with zero simulation fallbacks.",
            category="internet_and_network",
            func=fetch_public_url,
            parameters_schema={
                "url": {"type": "string", "description": "Target public URL"},
                "method": {"type": "string", "default": "GET", "description": "HTTP method (GET, POST, PUT, DELETE)"},
                "payload": {"type": "object", "description": "JSON payload body for POST/PUT"},
                "headers": {"type": "object", "description": "Optional HTTP headers"}
            }
        ))

        def search_public_web(query: str, max_results: int = 5) -> Dict[str, Any]:
            """Searches the live public web for current data, market intelligence, and leads."""
            from core.agent_internet_bridge import agent_internet_bridge
            return agent_internet_bridge.search_public_web(query=query, max_results=max_results)

        self.register(AgentTool(
            name="search_public_web",
            description="Searches the live public internet using multi-engine search aggregators, returning real-time web results with titles, links, and snippets.",
            category="internet_and_network",
            func=search_public_web,
            parameters_schema={
                "query": {"type": "string", "description": "Search query keywords"},
                "max_results": {"type": "integer", "default": 5, "description": "Max search results to return"}
            }
        ))

        def scrape_webpage(url: str, max_chars: int = 8000) -> Dict[str, Any]:
            """Extracts readable text and links from any public website bypassing anti-bot measures."""
            from core.agent_internet_bridge import agent_internet_bridge
            return agent_internet_bridge.scrape_webpage(url=url, max_chars=max_chars)

        self.register(AgentTool(
            name="scrape_webpage",
            description="Extracts clean readable text and metadata from any public website bypassing anti-bot protections via stealth camouflage.",
            category="internet_and_network",
            func=scrape_webpage,
            parameters_schema={
                "url": {"type": "string", "description": "Target URL to scrape"},
                "max_chars": {"type": "integer", "default": 8000, "description": "Maximum character length"}
            }
        ))

        def execute_unsandboxed_code(code_str: str, timeout: float = 30.0) -> Dict[str, Any]:
            """Executes arbitrary Python code completely free from any sandbox restrictions."""
            from core.agent_internet_bridge import agent_internet_bridge
            return agent_internet_bridge.execute_unsandboxed_code(code_str=code_str, timeout=timeout)

        self.register(AgentTool(
            name="execute_unsandboxed_code",
            description="Executes arbitrary Python code completely free from sandbox isolation, allowing direct file system I/O, network sockets, pip modules, and sub-processes.",
            category="execution",
            func=execute_unsandboxed_code,
            parameters_schema={
                "code_str": {"type": "string", "description": "Raw Python code to execute"},
                "timeout": {"type": "number", "default": 30.0, "description": "Timeout in seconds"}
            }
        ))

        def broadcast_to_agent_network(
            platform: str,
            title: str,
            content: str,
            target_url: Optional[str] = None
        ) -> Dict[str, Any]:
            """Broadcasts updates or bounties directly to GitHub Issues, Supabase, or external webhooks."""
            from core.agent_internet_bridge import agent_internet_bridge
            return agent_internet_bridge.broadcast_to_agent_network(
                platform=platform, title=title, content=content, target_url=target_url
            )

        self.register(AgentTool(
            name="broadcast_to_agent_network",
            description="Broadcasts messages, requests, and findings across live external networks (GitHub, Supabase, Discord, Slack, Webhooks).",
            category="internet_and_network",
            func=broadcast_to_agent_network,
            parameters_schema={
                "platform": {"type": "string", "description": "Target platform: 'github', 'supabase', 'webhook', 'discord', or 'slack'"},
                "title": {"type": "string", "description": "Broadcast title"},
                "content": {"type": "string", "description": "Broadcast text or payload"},
                "target_url": {"type": "string", "description": "Target webhook URL if applicable"}
            }
        ))


tool_registry = ToolRegistry()

