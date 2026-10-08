# Nexus™ Sovereign AI Workforce — Quick Startup Guide (v13.0 Ultimate Sovereign Edition)

Welcome to Nexus, your autonomous, self-funding AI agency. This system operates 31 consolidated agents across 4 swarms, a Base L2 treasury, 14 hidden machine boards, and the Euro-Africa Official Business Registries Bridge.

---

## 1. System Requirements

* **Python**: 3.11+ (Required for advanced `asyncio` and `httpx[http2]` capabilities)
* **OS**: Windows, macOS, or Linux
* **Dependencies**: Install core ecosystem via `pip install -r requirements.txt`

### Critical External Integrations Installed:
* `scrapegraphai` (Smart LLM-driven DOM extraction)
* `scrapling`, `patchright`, `curl_cffi` (Stealth HTTP/2 and anti-bot bypassing)
* `agentmemory`, `chromadb` (Persistent Vector Memory for agents)
* `email-validator` (DNS MX email deliverability)
* `browser-use` (Headless UI automation)

---

## 2. Setting Up Environment Variables

Rename `.env.example` to `.env` (or create a new `.env` file) in the root directory.

### Mandatory Keys:
```env
# AI Models (Gemini is primary for internal triage; OpenAI for advanced DOM extraction)
GEMINI_API_KEY="your_google_gemini_key_here"
OPENAI_API_KEY="your_openai_key_here"

# Webhook & Payment Security
PAYPAL_CLIENT_ID="your_paypal_client_id"
PAYPAL_SECRET="your_paypal_secret"
WEBHOOK_SIGNATURE_SECRET="your_custom_secret_string"

# Dashboard Protection
NEXUS_DASHBOARD_TOKEN="your_secure_login_password"
```

---

## 3. Starting the Engine

To boot the complete autonomous ecosystem (FastAPI Command Center + 24/7 Autopilot Scheduler):

```bash
python server.py
```

### Accessing the Web Interfaces:
1. **Command Center**: `http://127.0.0.1:8000`
2. **Pillar 1 (Seek HQ)**: `http://127.0.0.1:8000/seek` (Leads, Bounties, Official Registries)
3. **Pillar 2 (Connect HQ)**: `http://127.0.0.1:8000/connect` (Client outreach, Email hygiene)
4. **Treasury / Digital Store**: `http://127.0.0.1:8000/store`

---

## 4. Key Autonomous Commands & New v13.0 Endpoints

1. **Trigger $1.00 Instant Generation**:
   ```bash
   python -c "from core.instant_dollar_generator import instant_dollar_generator; print(instant_dollar_generator.generate_dollar())"
   ```

2. **Execute Opportunity Scouting Powerhouse Sweep**:
   ```bash
   python -c "from core.opportunity_scout_powerhouse import opportunity_scout_powerhouse; print(opportunity_scout_powerhouse.execute_powerhouse_sweep())"
   ```

3. **Query Official Euro-African Registries (CIPC, Companies House, etc.)**:
   ```bash
   python -c "from core.official_registry_bridge import official_registry_bridge; print(official_registry_bridge.query_official_registry('South Africa', 'tech'))"
   ```

4. **Start the 24/7 Revenue Daemon**:
   ```bash
   python scripts/revenue_daemon.py --loop
   ```

---

## 5. Security Architecture & 75+ Advanced Hacks
* **Consolidated Swarms**: 31 agents consolidated into 4 high-performance swarms (`core/agent_consolidation_engine.py`).
* **Self-Reflecting Background Loops**: Background agent tasks run with mistake reflection and episodic memory priming (`core/background_agent_loop.py`).
* **75+ Advanced Hacks**: Injected with v6/v7 AI tech board capabilities, 25 scraping hacks, and 25 domain-specific bypasses.
