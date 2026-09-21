# ⚡ Nexus™ Complete Capability Catalog (CAN_DO.md)
*Official Capabilities, Features, and Operations of the Nexus Sovereign Autonomous AI Workforce*

---

## 🏛️ 1. Core Revenue & Commercial Operations

| Capability | What It Does | Primary Service |
| :--- | :--- | :--- |
| **$1 Digital Vending Machine** | Runs a cyberpunk software storefront ([`/store`](https://nexusbots-nu.vercel.app/store)) selling self-hosted developer tools. | `core/digital_store_service.py` |
| **Instant PayPal 1-Click Checkout** | Creates live PayPal order tokens ($1.00 USD), captures funds, and delivers download links in under 1 second. | `core/payment_service.py` |
| **MCB Juice Domestic Routing** | Enables Mauritian clients to pay Rs 45 MUR to `+230 58169420` with duplicate and fraud verification. | `security/financial_shield.py` |
| **Instant Digital Fulfillment** | Delivers zero-dependency Python scripts and zip bundles via secure one-time download tokens ([`/download/{id}`](https://nexusbots-nu.vercel.app/download/nexus-email-guardian)). | `core/digital_store_service.py` |
| **Automated HTML Invoices & Receipts** | Generates branded, printable tax invoices and receipts with business details, VAT exemptions, and timestamps. | `core/receipt_generator.py` |
| **CSR & NGO Donation Portal** | Live donation gateway for *Enn Rev Enn Sourir* ([`/donations`](https://nexusbots-nu.vercel.app/donations)) to support underprivileged children in Mauritius. | `core/payment_service.py` |

---

## 🏭 2. Autonomous Product Manufacturing (5-Stage Factory)

You provide the factory a single keyword (e.g. `"invoice parser"` or `"crypto tracker"`), and it runs the entire pipeline with **zero human intervention**:

```
[1. Scout Demand] ──► [2. Spec Metadata] ──► [3. Synthesize Code] ──► [4. Sandbox QA] ──► [5. Live Store Deploy]
  YouTube Views         Price & Features        Standard Library        py_compile & Exec      PayPal & Discord Drop
```

1. **Scout Demand**: Scrapes YouTube viewer counts and search results to verify that at least 50,000+ people are actively searching for a solution.
2. **Spec Metadata**: Generates the product name, marketing tagline, bullet-point feature list, and $1 / Rs 45 price tag.
3. **Synthesize Code**: Writes a single-file, production-ready Python utility using only standard libraries (zero `pip install` required for buyers).
4. **Sandbox QA**: Tests the code in an isolated execution sandbox for syntax flaws and runtime crashes within a strict 6-second timeout.
5. **Live Store Deploy**: Registers the product in the live store catalog, packages the developer zip bundle, generates the live PayPal checkout link, and pushes announcement cards to social channels.

---

## 🤖 3. The 18 Autonomous Primary Agents

### 💼 Executive & Management
1. **Executive AI Managing Partner (`executive_partner`)**: Your trusted AI co-director. Logs strategic executive decisions, tracks monthly revenue targets (Rs 150,000 MUR), and enforces operational guardrails.
2. **Context Chronicler & Morning Chief of Staff (`chief_of_staff`)**: Summarizes what happened overnight and drafts your morning executive wake-up briefing.
3. **Zero-Regression & Safe Backup Sentinel (`regression_sentinel`)**: Runs periodic health checks on your database and codebase, creating snapshot backups before any major changes.

### 💰 Sales, Marketing & Growth
4. **B2B Lead Scout & Researcher (`lead_finder`)**: Searches for businesses in targeted verticals (clinics, tour operators, SMEs) and drafts bilingual French/English sales pitches.
5. **Autonomous Revenue Scout & Fund Harvester (`growth_hacker`)**: Identifies developer grant programs, open bounties, and unmonetized niches.
6. **Marketing & Social Media Influencer Usher (`influencer_usher`)**: Generates tailored outreach pitches for tech influencers and Twitter/LinkedIn audiences.
7. **Social & Webhook Broadcaster (`social_broadcaster`)**: Posts rich embed announcement cards to Discord channels, Slack workspaces, and Telegram channels whenever a new tool is published.

### 🛡️ Security, Email & Infrastructure
8. **Email Hygiene & Anti-Spam Agent (`email_hygiene`)**: Scans your IMAP accounts (Gmail/Outlook), classifies emails using Gemini AI, and safely trashes spam while keeping 2FA codes immune from deletion.
9. **Zombie Subscription Purger (`ghost_unsubscriber`)**: Detects unwanted recurring SaaS newsletters and extracts 1-click unsubscribe headers.
10. **Cloud Bills & Domain Expirations Sentinel (`infra_finance_sentinel`)**: Tracks cloud infrastructure spending and alerts you if burn approaches your $180 monthly cap.
11. **GitHub Sentinel & Breaking-Change Watchdog (`repo_radar`)**: Monitors GitHub repositories for dependency CVE vulnerabilities and upstream breaking changes.
12. **Spec-to-Code & Quality Inspector (`spec_auditor`)**: Audits synthesized code against security guidelines and coding standards.

### 📱 Client Concierge & Mobile
13. **Customer Support & VIP Concierge (`customer_support`)**: Resolves customer inquiries, tracks tickets, and provides download assistance.
14. **Bilingual French/English Localization Concierge (`bilingual_concierge`)**: Translates pitches, store descriptions, and customer replies between English and French.
15. **Mobile Release & App Store Sentinel (`appstore_sentinel`)**: Tracks mobile app store review guidelines and submission readiness.
16. **Meeting & Calendar Coordinator (`meeting_assistant`)**: Proposes meeting slots and coordinates availability for client discovery calls.
17. **Mobile Executive Dispatcher (`mobile_dispatcher`)**: Prepares high-priority notifications and WhatsApp links formatted for mobile screens.
18. **Night Shift Flight Recorder (`overnight_chronicle`)**: Conducts automated 30-minute sweeps 24 hours a day and signs all activity with SHA-256 hashes.

---

## 🛠️ 4. The 9 Universal Agent Superpowers (Tool Registry)

Any of the 18 agents can dynamically execute these tools via `self.call_tool(tool_name, **kwargs)` or via REST at `POST /api/tools/execute`:

1. `niche_scout`: Crawls online developer forums for high-intent pain points.
2. `scout_video_trends`: Scrapes live YouTube video view counts to validate market demand.
3. `verify_email_domain`: Conducts DNS socket MX record resolution to prevent email bounce bans.
4. `generate_whatsapp_link`: Builds dynamic `wa.me` links with URL-encoded bilingual sales pitches.
5. `create_paypal_link`: Generates live PayPal checkout tokens on the fly.
6. `check_paypal_balance`: Directly queries official PayPal balances via OAuth2 REST API.
7. `run_safe_diagnostic`: Verifies localhost ports, network latency, and memory usage.
8. `run_python_sandbox`: Validates and executes Python code in an isolated sub-process.
9. `broadcast_product_announcement`: Dispatches rich product announcement cards to Discord/Slack webhooks.

---

## 🧠 5. MemGPT-Style 3-Tiered Memory Engine

- **Tier 1 (Working Memory)**: Instant RAM state for the active task.
- **Tier 2 (Recall Memory)**: A sliding cache of the last 100 scouted niches, tool executions, and client responses (`memory/recall_memory.json`).
- **Tier 3 (Archival Memory)**: Permanent business ground truth (owner credentials, MCB Juice phone numbers, and approved product blueprints) stored in `memory/archival_memory.json`.

---

## 🔒 6. Security, Safety & Financial Defense (25 Safeguards)

- **Immunity Shield**: Protected keywords (`verification code`, `OTP`, `security alert`, `receipt`, `invoice`) make it physically impossible for the AI to trash banking emails or login credentials.
- **Cryptographic Audit Ledger**: Every email action and financial transaction is logged with timestamps and irreversible SHA-256 hash signatures.
- **Replay Protection**: Prevents duplicate or fraudulent MCB Juice reference numbers from claiming products twice.
- **Subagent Circuit Breakers**: If a subagent encounters 3 consecutive errors, its circuit trips and stops execution automatically to protect the system.
- **Enterprise Disaster Recovery**: Full JSON and SQL backup exporter (`core/backup_service.py`) and 1-click restore (`restore.py`).

---

## 🌐 7. Multi-Channel Deployment & Cloud Resilience

- **Local Executive Cockpit (`http://127.0.0.1:8000`)**: Full local control dashboard, real-time telemetry, and persistent IMAP background workers.
- **Live Vercel Cloud Gateway (`https://nexusbots-nu.vercel.app`)**: High-speed, globally distributed serverless edge with zero cold-start crashes (read-only filesystem protected).
- **Public Tunnel Starter (`scripts/start_public_tunnel.py`)**: 1-click Cloudflare Quick Tunnel / Localtunnel to expose localhost for testing without port forwarding.
- **Executive PDF Manual Generator (`scripts/generate_manual_pdf.py`)**: Produces printable A4 PDF documentation on demand ([`https://nexusbots-nu.vercel.app/manual`](https://nexusbots-nu.vercel.app/manual)).
