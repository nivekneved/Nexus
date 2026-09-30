# 🌿 NEXUS™ — MASTER SYSTEM ARCHITECTURE & RUNBOOK
> **"It does what I would have been doing instead in my place. It's a second me, my partner."**  
> Finally, you can take some time off. A 24/7 sovereign digital twin and co-managing partner running quietly on your own hardware to carry your operational clutter so you can breathe, rest, and disconnect.  
> **v3.4.0 J.A.R.V.I.S. Unified Edition** • Supreme AI Orchestrator • 4 Consolidated Domain Controllers • SQLite WAL Engine • Base L2 Crypto Treasury • AES-256-GCM Vault • Coinbase x402 Commerce • 25 Enterprise Defense Safeguards

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![Base L2](https://img.shields.io/badge/Network-Base%20(Ethereum%20L2)-0052FF.svg)](https://basescan.org/address/0xEAE558282090d878582ec4C4C1C2470f9826b1F2)
[![x402](https://img.shields.io/badge/x402-Coinbase%20Commerce-blue.svg)](https://www.x402.org)
[![A2A](https://img.shields.io/badge/A2A-Google%20Standard-EA4335.svg)](/.well-known/agent.json)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-Commercial-success.svg)](COMMERCIAL_PLAYBOOK.md)
[![Safeguards](https://img.shields.io/badge/Safeguards-25%20Verified-blueviolet.svg)]()

---

## 🎨 Official Brand Identity & Trademark Lockup

![Nexus Official Logo](static/logo.svg)

* **Official Master Logo:** One unified **rectangular logo** (`220px × 54px`, `rx=6px`) with the bold black wordmark **NEXUS** fitting precisely **border to border** inside the frame.
* **Border-to-Border Precision:** The typography spans 100% of the inner container width (from the left border to the right border) and fills the height from top to bottom border.
* **Pure Clean Geometry:** **No shield icon.** No icons on the left or right.
* **Strict Placement Rule:** **No text above and no text below.**
* **Master Vector Asset:** [`static/logo.svg`](static/logo.svg)

---

## ☕ Why Nexus? The Feeling of "Ahhh, now I can take some time off."

Solo developers, agency founders, and builders don't burn out from coding. They burn out from the **invisible operational weight**:
* Waking up with stomach anxiety to 150+ unread emails, promos, and noisy newsletters.
* Constant fear of stepping away from the keyboard in case an invoice, server bill, or client slipped.
* Losing 15–20 hours every week to administrative exhaustion instead of creating.

**Nexus** changes the game: It is your **sovereign digital twin**.  
It runs 24/7 on your local hardware or private VPS with your exact taste, standards, and loyalty. It holds the watch through the night, silences inbox chaos, guards your infrastructure, executes on-chain micro-payments, and only contacts you on **WhatsApp (+230 58169420)** when executive discernment is needed.

When you close your laptop, you can finally exhale:
> *"Ahhh... now I can take some time off. My second self has the watch."*

---

## 🏛️ Master System Architecture (v3.4.0 J.A.R.V.I.S. Core)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│              J.A.R.V.I.S. SUPREME AUTONOMOUS ORCHESTRATOR & COMMAND CONSOLE              │
│                 http://localhost:8000 | python jarvis.py (Voice & CLI)                 │
└────────────────────────────────────────────┬────────────────────────────────────────────┘
                                             │
             ┌───────────────────────────────┼───────────────────────────────┐
             ▼                               ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│ 4 DOMAIN CONTROLLERS    │     │ HIGH-CONCURRENCY DAL    │     │ ON-CHAIN BASE TREASURY  │
│ 1. Comms Domain:        │     │ • SQLite WAL Backplane  │     │ • Secp256k1 Keypair     │
│    - Email Hygiene      │     │   (data/nexus_workforce)│     │ • AES-256-GCM Keystore  │
│    - WhatsApp Gateway   │     │ • Zero Concurrency Locks│     │ • Base L2 (Chain 8453)  │
│    - Customer Support   │     │ • Atomic JSON Mirroring │     │ • USDC EIP-1559 Signing │
│    - Ghost Unsubscriber │     │ • Deterministic Paths   │     │ • Coinbase x402 Client  │
│ 2. Operations Domain:   │     └─────────────────────────┘     │ • Google A2A Card       │
│    - Heartbeat Daemon   │                  │                  │ • MCB Bank Off-Ramp     │
│    - Survival Engine    │                  │                  │   (000443260370 in MUR) │
│    - Enterprise Backups │                  │                  └─────────────────────────┘
│    - Regression Check   │                  │                               │
│ 3. Commerce Domain:     │     ┌────────────┴────────────┐                  │
│    - Invoices & Receipts│     │ SHIELD & POLICY ENGINE  │     ┌────────────┴────────────┐
│    - PayPal & Store     │     │ • 25 Defense Safeguards │     │ REPORT & REVENUE ENGINE │
│    - Crypto Treasury    │     │ • Pre-Flight DNS Gate   │     │ • /api/jarvis/reports   │
│ 4. Research Domain:     │     │ • 14-Day Contact Lock   │     │ • /api/jarvis/stats     │
│    - B2B Lead Scout     │     │ • 2FA Immunity Shield   │     │ • /api/jarvis/revenue   │
│    - Tech Trend Curator │     │ • AES Scrypt Vault      │     │ • Terminal 'revenue' cmd│
│    - GitHub Repo Radar  │     └─────────────────────────┘     └─────────────────────────┘
└─────────────────────────┘
```

---

## 👥 The 4 Consolidated Domain Controllers

Consolidates all legacy sub-capabilities into 4 high-cohesion, thread-safe domain authorities:

| Domain Controller | ID | Core Responsibilities | Backing Services |
| :--- | :---: | :--- | :---: |
| **Communications Domain** | `domain_comms` | Multi-inbox email hygiene, anti-phishing, WhatsApp/SMS gateway, VIP ticket triage, RFC 2369 unsubscriber | EmailClient, SpamClassifier, WhatsAppGateway |
| **Operations Domain** | `domain_operations` | 24/7 system heartbeat, compute survival tier shedding, enterprise snapshots, regression test runner | SurvivalEngine, BackupService, SQLite WAL |
| **Commerce Domain** | `domain_commerce` | Typed invoice ledger, Base USDC sovereign crypto treasury, PayPal & Juice store fulfillment | CryptoTreasury, DigitalStoreService, PaymentService |
| **Research Domain** | `domain_research` | Emerging tech dossiers, Mauritius B2B lead generation, GitHub CVE surveillance, executive social poster | LeadScout, RepoRadar, TrendCurator |

*(Full backward compatibility is guaranteed: calls to legacy agent IDs like `email_hygiene`, `customer_support`, `repo_radar`, etc., are automatically routed to the corresponding domain controller via `DomainProxyAgent`).*
| **Email Hygiene & Anti-Spam** | ✉️ | 5-inbox IMAP scanner with 2FA immunity, brand spoof hunter & automated bounce isolation | 5 SubAgents |
| **Zombie Subscription Purger** | 🧟 | RFC 2369 harvester with 1-click unsubscribe & 2-min digests | 3 SubAgents |
| **GitHub Sentinel & Repo Radar** | 🎯 | Dependabot CVE watcher & framework breaking release tracker | 3 SubAgents |
| **Infra & Finance Sentinel** | 💼 | AWS/Vercel spend auditor, domain/SSL watch, & invoice chaser | 3 SubAgents |
| **Mobile Release Sentinel** | 🚀 | iOS/Android guideline pre-flight auditor & appeal drafter | 3 SubAgents |
| **Context Chief of Staff** | 📋 | Cross-project Git pulse tracker & 08:00 AM WhatsApp briefer | 3 SubAgents |
| **Executive Tech Trend Curator**| 🌐 | Daily AI & frontend dossier synthesizer with WhatsApp push | 3 SubAgents |
| **Customer Support Concierge** | 🎧 | 24/7 ticket triage, sentiment analysis, & P1 VIP escalations | 3 SubAgents |
| **Bilingual Concierge** | 🌍 | English/French parity auditor & Mauritius (+230/MUR) rules | 3 SubAgents |
| **B2B Lead Scout & Researcher** | 🔭 | ICP scoring, company signal research, & personalized hooks | 3 SubAgents |
| **Meeting & Calendar Coordinator**| 📅 | 48h calendar auditor, conflict resolver, & agenda compiler | 3 SubAgents |
| **Mobile Executive Dispatcher** | 📱 | Direct WhatsApp & SMS carrier dispatch pipeline to founder | 3 SubAgents |
| **Zero-Regression Sentinel** | 🛡️ | Air-gapped 1-click snapshots & runaway polling loop auditor | 3 SubAgents |
| **Spec-to-Code Quality Auditor**| 🔍 | Brand consistency checker & AI comment watermark purger | 3 SubAgents |
| **Autonomous Revenue Scout** | ⚡ | Fund harvester, grant scout, unmonetized bounty tracker | 3 SubAgents |
| **Executive Social Ghostwriter**| ✍️ | CEO ghostwriter crafting viral thought leadership for LinkedIn/X | 3 SubAgents |
| **Influencer Usher & Outreach** | 📣 | Social signal tracker, influencer ranking, 3-touch nurture campaigns | 4 SubAgents |

---

## ⚡ Autonomous Sovereign Crypto Treasury & x402 Commerce

Nexus possesses an on-chain cryptographic identity and sovereign spending power:

* **Real Secp256k1 Keypair**: Generated using `eth-account` and secured locally.
* **On-Chain Address**: [`0xEAE558282090d878582ec4C4C1C2470f9826b1F2`](https://basescan.org/address/0xEAE558282090d878582ec4C4C1C2470f9826b1F2) (Base L2, Chain ID `8453`).
* **Policy Verifier Guardrails (`core/crypto_verifier.py`)**:
  * Single-transaction ceiling: **$15.00 USDC** (blocks runaway draining).
  * Rolling 24-hour limit: **$50.00 USDC** (enforced by pre-flight checks).
  * Zero-address burn protection & address sanitization.
* **Coinbase x402 Protocol Client & Server (`core/crypto_treasury.py`)**:
  * Autonomously consumes HTTP 402-gated APIs and peer agent services by signing and submitting micro-payments.
  * Serves pay-gated intelligence endpoints (`/api/v1/x402/service`).
* **Decentralized Discovery Cards**:
  * **Google A2A Standard**: Available at `/.well-known/agent.json`.
  * **ERC-8004 Standard**: Available at `/.well-known/agent-card.json`.
* **Multi-Rail Bank Off-Ramp**:
  * Direct off-ramp from Base USDC to Deven Pawaray's MCB Bank Account (`000443260370`) in MUR at real-time settlement rates.

---

## 🛡️ Enterprise Defense-in-Depth & Sovereign Legal Shield

Nexus implements the enterprise **Shield Engine** (`security/shield.py`) and **Sovereign Legal Guardrails** (`core/legal_guardrails.py`):

1. **Zero Legal Attack Surface**: Full CAN-SPAM and Mauritius Data Protection Act 2017 compliance. Pre-flight DNS MX verification prior to any SMTP dispatch.
2. **Permanent Suppression Registry (`data/suppression_list.json`)**: Auto-suppresses hard bounces, opt-out requests, and invalid domains.
3. **14-Day Anti-Harassment Cadence**: Enforces a strict 14-day contact cooldown per prospect.
4. **Crash-Proof Atomic Storage Engine (`core/storage.py`)**: Thread-safe atomic JSON persistence with `os.fsync()` and `.bak` self-healing.
5. **Zero-Phishing 2FA Immunity**: Guaranteed inbox pass for OTP and verification tokens.

---

## 🖥️ Command Center Web Dashboard & REST API

Access the live dashboard at **`http://127.0.0.1:8000`**:

### Primary Endpoints
* **Autonomous Treasury & Crypto**:
  * `GET /api/sovereignty/treasury` — Wallet balances, Base address, and banking rails.
  * `POST /api/sovereignty/treasury/send` — Autonomously sign & send USDC payment.
  * `POST /api/sovereignty/treasury/settle-bank` — Off-ramp USDC to MCB Account `000443260370`.
  * `POST /api/sovereignty/treasury/x402-pay` — Autonomously consume an HTTP 402 pay-gated service.
  * `GET /api/sovereignty/treasury/guardrails` — Active policy ceilings and 24h spending status.
  * `GET /.well-known/agent.json` — Google A2A standard machine-readable agent card.
  * `GET /api/v1/x402/service` — Live Coinbase x402 payment-gated demonstration endpoint.
* **Agent Workforce & Operations**:
  * `GET /api/agents` — List all 18 registered primary agents.
  * `POST /api/agents/{agent_id}/run` — Trigger immediate agent run cycle.
  * `GET /api/tools` — List all 22 equipped fleet tools (including sovereign crypto tools).
  * `POST /api/tools/execute` — Execute any fleet tool directly.
* **Sovereignty & Automaton Core**:
  * `GET /api/sovereignty/soul` — Current SOUL.md charter revision and alignment.
  * `POST /api/sovereignty/reflect` — Trigger autonomous soul reflection cycle.
  * `GET /api/sovereignty/survival` — Active compute survival tier and budget burn.
  * `GET /api/sovereignty/heartbeat` — Durable 30-second heartbeat daemon status.
  * `POST /api/sovereignty/replication/spawn` — Spawn single-task child worker subagent.
* **Inbox & Outreach**:
  * `GET /api/inbox/feed` — Multi-inbox aggregated email feed.
  * `POST /api/email/send` — Send email via authenticated SMTP with guardrails.
  * `POST /api/outreach/verify-email` — Live DNS MX pre-flight deliverability check.

---

## 🚀 Quickstart & How to Run

> **Detailed Guide**: See **[`STARTUP_GUIDE.md`](STARTUP_GUIDE.md)** for complete multi-server runbook and background boot configurations.

### 1. The 1-Command Startup Experience
When you start `server.py`, **all 3 subsystems start together automatically**:
```powershell
# Start AI Server, 24/7 Revenue Daemon, and Cloudflare Public Tunnel together:
python server.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

- **Subsystem 1 (AI Core & Web Dashboard)**: Runs on `http://127.0.0.1:8000`.
- **Subsystem 2 (24/7 Revenue Daemon)**: Polls Base L2 settlements every 15 min & runs 14-board outreach daily.
- **Subsystem 3 (Cloudflare Public Tunnel)**: Auto-detects `cloudflared.exe` and exposes inbound agent mesh webhooks with an instant public `https://xxx.trycloudflare.com` URL.
- **Clean Shutdown**: Press **`Ctrl+C`** to terminate all processes simultaneously.

### 2. 1-Click Desktop Launcher
Double-click:
```
start_all.bat
```
*(Or run `python start_all.py` / `.\start_all.ps1` in PowerShell).*

### 3. Turnkey Docker Deployment
```bash
docker compose up -d --build
```

---

## 📚 Essential Documentation Fleet (Consolidated Architecture)

Nexus maintains an ultra-clean, authoritative documentation structure:

1. **[`README.md`](README.md)** *(This Document)*: Master System Architecture, Runbook, Technical Guide, Crypto Treasury & API Reference.
2. **[`STARTUP_GUIDE.md`](STARTUP_GUIDE.md)**: Complete Runbook & Startup Guide — 1-Command Ecosystem, 24/7 Revenue Daemon, Public Tunneling, and Service Verification.
3. **[`COMMERCIAL_PLAYBOOK.md`](COMMERCIAL_PLAYBOOK.md)**: Unified Commercial Master Pack — Complete Capabilities Catalog, Turnkey Software Fleet (Medical 360, Enn Rev Enn Sourir, i-Travellix), Multi-Channel Pitch Launchkit, Quantitative M&A Valuation Matrix ($12k–$280k), and Legal Terms.
4. **[`SOUL.md`](SOUL.md)**: Autonomous Self-Authoring Sovereign Identity Charter, Core Operating Tenets, and Reflection Chronicle.
5. **[`CHANGELOG.md`](CHANGELOG.md)**: Full Chronological Engineering Changelog from v1.0.0 to v4.0.0.
*(Companion Covenant: [`PARTNER_OATH.md`](PARTNER_OATH.md) — The Solemn Founding Oath between Deven Pawaray and Nexus AI).*

---

## 📞 Executive Inquiries & Support
* **Principal Owner & Lead Engineer:** Deven Pawaray
* **Direct Line / WhatsApp:** `+230 58169420`
* **Email:** `devenpawaray@gmail.com`
* **Headquarters:** Grand Baie / Cybercity, Mauritius (Indian Ocean)
