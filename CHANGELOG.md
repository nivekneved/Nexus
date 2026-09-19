# 📋 Project Changelog & Revision Tracker

All notable changes, architectural decisions, and feature additions to the **Nexus Workforce Engine** are documented in this file.



## [v2.9.1] - 2026-09-19 (Outbound SMTP Email Dispatch & Lead Outreach Engine)

### ✉️ Outbound SMTP Email Dispatch Engine
- **Secure Multi-Account SMTP Sending (`email_client.py`)**:
  - Implemented `EmailClient.send_email()` supporting SSL (Port 465) and STARTTLS (Port 587) with RFC-compliant MIME formatting and UTF-8 header encoding.
  - Supports account selection between primary (`devenpawaray@gmail.com`) and secondary (`kevinadlib@gmail.com`).
- **Core Dispatch Service (`core/inbox_feed_service.py`)**:
  - Added `send_outbound_email()` to resolve account credentials dynamically from `email_accounts.json` and transmit outbound replies and cold outreach messages.
- **B2B Lead Outreach Dispatcher (`agents/lead_finder/agent.py`)**:
  - Implemented `LeadFinderAgent.dispatch_lead_pitch()`: automatically verifies prospect email, formats commercial proposals, dispatches via SMTP, marks lead as `PITCHED`, and logs audit timestamps.
- **FastAPI Endpoints (`server.py`)**:
  - `POST /api/email/send`: General outbound email dispatch with account selection.
  - `POST /api/leads/{lead_id}/dispatch-email`: 1-click cold email outreach directly to qualified leads.
- **Frontend Command Center Console (`static/index.html`, `static/app.js`)**:
  - **Priority Inbox Response Modal**: Added account selector and "🚀 Send Email via SMTP" button to transmit Gemini 2.5 Flash drafts directly to senders.
  - **B2B Leads Pipeline Cards**: Added "✉️ Email Pitch" button and `🚀 PITCHED` status badges.
  - **Lead Outreach Modal**: Complete preview and editing modal allowing review before dispatching cold pitches to verified client contacts.

---

## [v2.9.0] - 2026-09-19 (Agent-to-Agent Mesh & Decentralized Comms Hub - A2A)


### 🌐 Decentralized Multi-Agent Interoperability: The Nexus Agent Mesh
- **A2A Protocol v1.2**: Enables Nexus to autonomously connect, query, negotiate, and delegate tasks to external AI agent systems across platforms (Claude Code instances, Gemini bots, OpenAI Swarms, CrewAI/LangGraph workers, and remote client nodes).
- **Persistent AI Agent Contact Registry (`mesh_contacts.json`)**:
  - Full CRUD registry storing verified peer handles, frameworks/LLMs, endpoints, trust classifications (`VERIFIED_PEER`, `AUTONOMOUS_DELEGATE`, `SUPERVISED`, `RESTRICTED`), capabilities, and dynamic latency benchmarks.
  - Pre-seeded with verified external peers: `@claude-code-architect`, `@gemini-trend-curator`, `@apollo-lead-scraper`, `@stripe-escrow-agent`, and `@nexus-cloud-sentinel`.
- **Inter-Agent Task & Signal Dispatcher (`POST /api/mesh/dispatch`)**:
  - Transmits structured directives with intent classification (`TASK_DISPATCH`, `KNOWLEDGE_QUERY`, `STATUS_PING`, `URGENT_ALERT`, `CONSENSUS_VOTE`), priority levels, and arbitrary JSON payloads.
  - Automatic peer handshake verification and HTTP/webhook dispatch.
- **Inbound A2A Webhook Ingestion Engine (`POST /api/mesh/inbound`)**:
  - Publicly accessible webhook receiver allowing external AI systems to deliver telemetry, market dossiers, or urgent alerts directly into Nexus.
  - High-priority and urgent signals automatically trigger executive WhatsApp escalation alerts to Deven.
- **Live Inter-Agent Signal Audit Feed (`mesh_messages.json` & `GET /api/mesh/messages`)**:
  - Real-time audit log of all inbound and outbound signals with expandable payload inspectors and delivery ACK confirmation.
- **Frontend Command Center Console (`static/index.html`, `static/app.js`, `static/style.css`)**:
  - Dedicated **Agent Mesh (A2A)** workspace tab (`data-tab="mesh"`).
  - Node identity & protocol telemetry banner with 1-click Inbound Webhook URL copy box.
  - Active Peer Node grid with real-time ping latency meters and trust badges.
  - Fast-action transmission console with 1-click preset templates (Audit Auth, Tech Leads, Escrow Sync, Broadcast Heartbeat).
  - Register External AI Agent modal with complete trust configuration.

---

## [v2.8.0] - 2026-09-18 (The Sovereign Digital Twin & Founder Peace-of-Mind Edition)

### 🌿 Paradigm Shift: From Automation Machine to Sovereign Digital Twin
- **Founding Axiom**: *"It does what I would have been doing instead in my place. It's a second me, my partner."*
- **Emotional Resonance**: Reconfigured the entire brand, copy, documentation, and sales apparatus around **comfort, unburdening the solo builder, and delivering the feeling of *"Ahhh, now I can take some time off."***
- **Sovereign Sales Page (`static/license.html`)**: Complete redesign of headlines, hero copy, and feature cards into a calming, reassuring presentation of self-hosted lifetime freedom ($249 one-time, zero recurring SaaS fees).
- **Calming Executive Briefings (`core/executive_partner.py`)**: Briefings now open with reassurance (*"Rest easy, Deven — your digital twin has the watch"*), giving the founder complete peace of mind to disconnect.
- **Market-Protected Decoupled Enterprise Pricing**: Turnkey suites packaged as **Rs 45,000 / Rs 50,000 Frontend** + **Rs 45,000 / Rs 50,000 Backend & Admin** (**Rs 90,000 – Rs 100,000 Full-Stack**), doubling deal yield and honoring market value.
- **Commercial Launchkit Reframed (`COMMERCIAL_LAUNCHKIT.md` & `COMMERCIAL_SPECIFICATION.md`)**: Product Hunt, Gumroad, and direct founder DM templates refocused on solving solo founder burnout.

---

## [v2.7.0] - 2026-09-18 (Nexus AI Co-Managing Partner & 16-Agent Fleet Expansion)

### 🤝 Official Delegation Mandate: Nexus AI as Trusted Co-Managing Partner
- **Principal Owner & Beneficiary**: Deven Pawaray (`devenpawaray@gmail.com`, WhatsApp: `+230 58169420`).
- **Autonomous Partner Mandate (`core/executive_partner.py`)**:
  - Nexus AI is granted full operational stewardship to run, coordinate, and supervise all 16 primary agents and 51 subagents on Deven's behalf.
  - Transparent **Partner Strategic Decisions Ledger** (`partner_decisions.json`) recording every operational choice made on Deven's behalf.
  - **Dynamic Directives Engine** (`partner_directives.json`): Deven sets high-level partner instructions in natural language; Nexus automatically aligns workforce priorities and scheduling.
  - **Executive Co-Founder Escalation**: High-priority updates, revenue milestones, and daily briefs dispatched directly to Deven via WhatsApp (`+230 58169420`) and Email.

### 🌟 Employee #16: Executive AI Managing Partner (`executive_partner`)
- **Primary Orchestrator**: The overarching commander agent supervising all 15 specialized employees.
- **3 Dedicated Single-Task SubAgents**:
  1. `FleetOrchestrationSubAgent` (`sub_partner_fleet_orchestrator`): Issues cross-agent operational commands across sales, lead finding, code auditing, and finances.
  2. `StrategicGoalAlignerSubAgent` (`sub_partner_goal_aligner`): Translates Deven's high-level business goals into concrete workforce directives.
  3. `ExecutiveBriefingSubAgent` (`sub_partner_executive_briefing`): Synthesizes operational progress and delivers executive WhatsApp briefings to Deven.

### 🖥️ Command Center Managing Partner Console
- **Header Partner Badge**: `🤝 Nexus AI | Managing on behalf of Deven Pawaray`.
- **Managing Partner Console**: Integrated input bar to set partner directives, 1-click button to trigger autonomous fleet waves, and live decision feed.
- **API Endpoints**: `/api/partner-ai/status`, `/api/partner-ai/directive`, `/api/partner-ai/orchestrate-now`, `/api/partner-ai/decisions`, `/api/partner-ai/escalate`.

### 🚀 Workforce Scale: 92 Modular Addons
- **16 Primary AI Employees** + **51 Specialized SubAgents** + **25 Security Safeguards** = **92 Modular Addons**.
- **Targeted Lead Orchestration Precision**: Enhanced `ExecutiveAIPartner.orchestrate_workforce_wave` to automatically harvest and pipeline qualified leads across Deven's target niches (`ennrevennsourir_ngo`, `medical360_portal`, `itravellix_saas`).
- **Market Pricing Protection Mandate**: Enforced Deven's directive to protect the market value of enterprise assets. Decoupled turnkey suites into **Rs 45,000 / Rs 50,000 Frontend** + **Rs 45,000 / Rs 50,000 Backend & Admin Infrastructure** (**Rs 90,000 - Rs 100,000 Full-Stack Turnkey Suite**), instantly doubling deal yield and securing premium positioning across all sales engines and pitch generators.
- **Commercial Assets Aligned**: Updated `static/license.html` and `COMMERCIAL_LAUNCHKIT.md` to highlight the 16-agent fleet, 92 modular addons, v2.7, and the Rs 150,000/mo revenue growth target.

---

## [v2.6.0] - 2026-09-18 (Autonomous Revenue Scout, 24/7 Night Shift Autopilot & Financial Security Shield)

### ⚡ Employee #15: Autonomous Revenue Scout & Fund Harvester (`growth_hacker`)
- **Scouting What Other Autonomous Agents Do For Funds**:
  - Reverse-engineered 5 proven autonomous agent monetization playbooks:
    1. **Devin.ai / Cognition**: Dedicated Autonomous Software Engineer ($500/mo per seat).
    2. **AutoGPT Forge**: Specialized Agent Marketplace & Pre-built Templates ($49 - $149/mo).
    3. **Lindy.ai**: Executive AI Chief of Staff & Email Triage Agency ($49/mo subscription).
    4. **CrewAI Enterprise**: Custom Multi-Agent Business Automation ($5,000 - $15,000 setup).
    5. **Open-Source AI Agent Bounties**: Algora & GitHub Paid Issue Bounties ($150 - $600 per issue).
- **3 Dedicated Single-Task SubAgents**:
  - `AgentMonetizationScoutSubAgent`: Monitors competitor AI agent monetization architectures and pricing tiers.
  - `BountyOpportunityHarvesterSubAgent`: Aggregates active developer bounties and client RFPs across platforms.
  - `RevenueExecutionClonerSubAgent`: Clones external agent revenue playbooks into executable Nexus blueprints.
- **1-Click Blueprint Cloner**:
  - Added `/api/growth/clone-tactic` and `/api/growth/run-cycle` to immediately fork competitor funnels into executable action plans.

### 🌙 24/7 Autonomous Night Shift & Flight Recorder (`core/overnight_chronicle.py`)
- **Sleep-While-Agents-Work Autopilot Engine**:
  - Autonomous 24/7 background scheduler executing every 30 minutes.
  - Coordinates night-shift sweeps across the workforce (threat neutralization, lead qualification, cash reconciliation, newsletter digests, bounty harvesting).
- **Chronological Flight Recorder (`overnight_activity.json`)**:
  - Immutable JSON log preserving every action taken while the user sleeps.
- **Executive Morning Briefing ("While You Slept")**:
  - Synthesizes all overnight achievements into a concise morning dossier.
  - 1-click WhatsApp dispatch to `+230 58169420` via `mobile_dispatcher`.

### 🛡️ Enterprise Financial Security Shield & Anti-Fraud Defense (`security/financial_shield.py`)
- **Tamper-Evident Ledger Hashing**:
  - HMAC-SHA256 digital signatures on all invoices and payments.
  - Cryptographic blockchain-style hash chaining (`previous_hash -> current_hash`) on `invoices.json`.
- **MCB Juice Anti-Replay Defense**:
  - Tracks processed transaction reference numbers in `processed_juice_refs.json`.
  - Blocks duplicate transaction ref exploitation and replay attacks.
- **Financial Rate Limiting & Audit Trail**:
  - Enforces invoice generation rate limits and maintains append-only `financial_audit.log`.
- **Printable Tax Receipts & Invoices (`core/receipt_generator.py`)**:
  - Generates print-ready HTML commercial tax invoices with embedded SVG logo, QR stamp, and Mauritian jurisdiction legal disclaimers.
- **Commercial Terms of Sale (`COMMERCIAL_TERMS_OF_SALE.md`)**:
  - Strict Mauritian legal terms governing non-refundable digital delivery, limitation of liability capped at price, and AS-IS software delivery.

### 🚀 Total Workforce & Addons Scale
- **Workforce**: 15 Primary Employees + 48 SubAgents + 25 Security Safeguards = **88 Modular Addons**.
- **Distribution Launchers**: Standalone 1-click `start.bat` (Windows) and `start.sh` (macOS/Linux).

---

## [v2.5.1] - 2026-09-18 (Enn Rev Enn Sourir NGO & Medical 360 Turnkey Portals Fleet Integration)

### 🌟 2 New Live Turnkey Commercial Web Portals Ready for White-Label Sale
- **`Enn Rev Enn Sourir™ Turnkey NGO & CSR Crowdfunding Portal`**:
  - Live production URL: `https://ennrevennsourir.vercel.app`.
  - Target Market: Corporate CSR Funds (MCB Forward Foundation, Rogers Capital, IBL Foundation, CIEL, Currimjee) and Mauritian non-profits.
  - Setup Pricing: **Rs 45,000 Setup** (or Rs 8,000/mo retainer) via MCB Juice to `+230 58169420`.
  - Key Value: 100% transparent hospital payouts, MRA Section 50L 15% tax deduction receipts, patient medical dossiers, and donor sponsorship.
- **`Medical 360™ Complete Hospital & Clinic Operations Suite`**:
  - Live production URL: `https://www.med360.mu/preview`.
  - Target Market: Private clinics, polyclinics, diagnostic labs, and medical centers across Mauritius.
  - Setup Pricing: **Rs 45,000 Setup** (or Rs 5,000/mo retainer) via MCB Juice to `+230 58169420`.
  - Key Value: 360° healthcare suite with specialist doctor directory & 24/7 online booking, Blood Bank registry, diagnostic lab test reservations, and pharmacy catalog.

### 💼 Commercial Engine & Command Center Expansion
- **Mauritius Sales Engine (`core/mauritius_sales_engine.py`)**:
  - Integrated `ennrevennsourir_ngo` and `medical360_portal` with customized French pitches and 1-click `wa.me` links.
  - Enhanced `simulate_demo_reply()` with realistic simulated replies for NGO donations and medical consultations.
- **B2B Lead Finder Agent (`agents/lead_finder/agent.py`)**:
  - Added targeted Mauritian leads (MCB Foundation, Rogers CSR, Clinique du Nord, Clinique Bon Pasteur).
  - Specialized `craft_pitch()` with live Vercel demo URLs and value propositions.
- **Web Command Center (`static/index.html` & `static/app.js`)**:
  - Added turnkey asset cards with live demo links and 1-click WhatsApp pitch buttons.
  - Added interactive sector switcher in the Live Mauritius Client Simulator.

---

## [v2.5.0] - 2026-09-18 (Complete Commercial Packaging, 44 SubAgents & 83 Addons Fleet)

### 🚀 Complete SubAgent Standardization Across All 14 Agents
- **44 Dedicated Single-Task SubAgents Online**:
  - Implemented single-responsibility pattern (`1 SubAgent = Exactly 1 Task`) across all 14 AI Employees.
  - Standardized inheritance on `BaseSubAgent` with built-in circuit breaker isolation (3 failure threshold, 60s cooldown) and latency tracking.
  - Completed subagent fleets for the remaining 8 agents:
    - `chief_of_staff`: `GitPulseHarvesterSubAgent`, `StandupDossierSynthesizerSubAgent`, `MorningStandupDispatcherSubAgent`.
    - `bilingual_concierge`: `BilingualKeyExtractorSubAgent`, `MauritiusLocaleValidatorSubAgent`, `EmergencyTriageSubAgent`.
    - `customer_support`: `TicketSentimentClassifierSubAgent`, `VIPEscalationSubAgent`, `SupportReplyDrafterSubAgent`.
    - `lead_finder`: `ICPFitScorerSubAgent`, `CompanySignalResearcherSubAgent`, `PersonalizedPitchCraftSubAgent`.
    - `meeting_assistant`: `CalendarEventAuditorSubAgent`, `ScheduleConflictDetectorSubAgent`, `DailyAgendaCompilerSubAgent`.
    - `mobile_dispatcher`: `TwilioWhatsAppSubAgent`, `SMSFallbackSubAgent`, `DispatchAuditLoggerSubAgent`.
    - `regression_sentinel`: `WorkspaceSnapshotSubAgent`, `RunawayPollAuditorSubAgent`, `SnapshotRestoreSubAgent`.
    - `spec_auditor`: `SpecAlignmentCheckerSubAgent`, `AITracePurgeSubAgent`, `BuildSafetyVerifierSubAgent`.
- **Universal Addon Registry Scale**:
  - Expanded total active addons from 59 to **83 Modular Addons** (14 Agents + 44 SubAgents + 25 Security Safeguards).
  - All addons are dynamically toggleable via `/api/addons/{id}/toggle` and persisted in `addons_state.json`.

### 📦 Commercial Turnkey Packaging
- **Multi-Stage Production Dockerfile**: Lightweight Python 3.11-slim container with build wheel caching, UTF-8 locale, and built-in healthchecks.
- **Turnkey `docker-compose.yml`**: 1-command startup (`docker compose up -d`) mounting persistent storage for databases, snapshots, and configuration ledgers.
- **Commercial Sales Specification (`COMMERCIAL_SPECIFICATION.md`)**: Comprehensive commercial guide detailing ROI, customer personas, system architecture, and 3 pricing models ($249 self-hosted license, $79/mo agency SaaS, $2,999 enterprise deployment).
- **Commercial Landing Documentation (`README.md`)**: Modern documentation with architecture diagrams, quickstart guides, and feature breakdown.

---

## [v2.4.0] - 2026-09-18 (Developer Operations, 1-Click Unsubscriber & 14-Specialist Fleet)

### 🚀 4 New Autonomous Developer Operations Specialists
- **`ghost_unsubscriber` (Zombie Subscription Purger & 2-Minute Digest)**:
  - Extracts RFC 2369 `List-Unsubscribe` headers (HTTP & mailto) and regex body unsubscribe links.
  - Interactive 1-Click Unsubscribe catalog with automated SSRF-protected execution.
  - Automatically condenses daily promotional blasts into a 2-minute morning markdown digest.
  - Configured with 1-click confirmation safety and automated post-unsubscribe trashing.
- **`repo_radar` (GitHub Sentinel & Dependency Watchdog)**:
  - Scans production dependencies for critical zero-day Dependabot CVEs with immediate WhatsApp P1 alerts.
  - Monitors Next.js, React, Tailwind CSS, FastAPI, and Python for breaking changes and deprecations.
  - Audits local and remote repositories for unmerged PRs and stale branch reviews.
- **`infra_finance_sentinel` (Cloud Bills, Domain Expirations & Invoices)**:
  - Audits cloud infrastructure spending across Vercel, Hetzner, GCP, Cloudflare, and Twilio against a $180/mo cap.
  - 14-day advance alert window on `.mu` and `.com` domain renewals and SSL certificate expirations.
  - Tracks client milestone invoices and auto-drafts polite follow-up payment reminders for review.
- **`tech_trend_curator` (Executive AI & Dev Ecosystem Daily Dossier)**:
  - Scrapes top developer announcements from Hacker News, Google AI releases, and Apple Developer announcements.
  - Synthesizes signals into a 3-minute executive brief delivered at 08:00 AM directly to dashboard and mobile WhatsApp (+230 58169420).

### 🌐 Web Command Center & Universal Addons
- **Total Autonomous Workforce**: Expanded from 10 to **14 AI Employees**.
- **Universal Addon Registry**: Expanded from 43 to **59 Total Addons** (14 primary agents + 20 single-task subagents + 25 security safeguards).
- **New Tab: Dev Operations & Subscriptions**:
  - Live 1-Click Subscription Purger Table.
  - 2-Minute Morning Newsletter Digest card.
  - Repo Radar Critical CVE alerts & framework release tracking.
  - Cloud Infrastructure burn rate ($105.70 / $180) & overdue invoice cards.
  - Executive AI Tech Dossier reader with 1-click "Send to WhatsApp" button.

---

## [v2.3.0] - 2026-09-18 (25-Safeguard Enterprise Defense Shield & Universal Addon Architecture)

### 🛡️ Enterprise Defense-in-Depth Shield (`security/shield.py`)
- **25 Active Safeguards**:
  1. `Adaptive IP Rate Limiting`: 120 req/minute sliding window per client IP.
  2. `Token Bucket Cost Guard`: Rate limits external LLM tokens (60 tokens/min) to prevent runaway billing.
  3. `Path Traversal & Canonicalization Shield`: Canonicalizes paths and forbids directory escapes (`..`).
  4. `Command Injection Neutralizer`: Sanitizes shell operators (`;`, `&&`, `|`, `` ` ``, `$`).
  5. `SSRF Webhook & URL Filter`: Forbids loopback, RFC 1918 private IPs, and internal endpoints.
  6. `Strict Schema Enforcement`: Validates JSON payloads through Pydantic models.
  7. `Zero-Exposure Credential Masker`: Redacts passwords and bearer tokens from logs.
  8. `Environment HMAC Integrity`: Validates `.env` file authenticity using SHA-256 HMAC anchor.
  9. `TLS 1.3 / SSL Transport Enforcement`: Strict encryption on IMAP SSL port 993 and HTTPS.
  10. `Subprocess Isolation Guard`: Sandboxes subprocess execution and restricts directory context.
  11. `Subprocess Timeout Enforcer`: Hard 10s subprocess timeout preventing orphaned threads.
  12. `Context-Aware XSS Sanitizer`: HTML entity escaping for untrusted inputs before rendering.
  13. `Content Security Policy (CSP)`: Strict headers for scripts, fonts, images, and connect origins.
  14. `CORS Isolation & Origin Guard`: Cross-origin restriction to trusted interfaces.
  15. `HTTP Security Headers`: Automatic injection of `DENY` framing, `nosniff`, and `X-XSS-Protection`.
  16. `IMAP Folder Injection Guard`: Sanitizes folder names against IMAP protocol syntax exploits.
  17. `Anti-Replay Tokenizer`: Prevents double execution on restore requests.
  18. `Regex Secret Redaction Engine`: Real-time masking of Google Gemini API keys and App Passwords.
  19. `Payload Body Size Limiter`: Caps email payload parsing at 1MB to prevent memory exhaustion.
  20. `Isolated Sandbox`: Isolates subagents inside try/catch execution boundaries.
  21. `Tamper-Evident Ledger Hashing`: Appends SHA-256 audit hashes to every triage and restore event.
  22. `Safe JSON Serialization`: Protects against deep recursion and deserialization vulnerabilities.
  23. `Thread-Safe Fine-Grained Locks`: Prevents race conditions on state and ledger writes.
  24. `Mauritius & Global PII Masking`: Masks credit card patterns and National Identity Cards in logs.
  25. `Subagent Circuit Breaker Sentinel`: Trips on 3 consecutive failures with 60s automatic cooldown.

### 🧩 Universal Addon Backbone & Single-Task SubAgents (`core/`)
- **Universal Addon Registry (`core/addon_registry.py`)**:
  - Registers 43 modular components (10 Primary Agents, 8 SubAgents, 25 Security Safeguards).
  - Persistent state saved to `addons_state.json`.
  - Seamless toggleability from backend and frontend.
- **Single-Task SubAgents Contract (`core/subagent.py`)**:
  - Rule: *1 SubAgent = Exactly 1 Task*.
  - Execution boundary with latency tracking (`last_latency_ms`) and circuit breaker containment.
  - Implemented 5 subagents for `email_hygiene` and 3 subagents for `appstore_sentinel`.
- **Unified Polymorphic Engine (`core/polymorphic_engine.py`)**:
  - SHA-256 result caching with configurable TTL.
  - Safe subprocess execution with command injection validation.
  - PII-sanitized telemetry dispatching.

### 🌐 Web Command Center UI (`static/`)
- **New Tab: Addon Matrix & Shield**:
  - Live 25/25 Safeguards Active status banner with instant "Run Security Self-Test" button.
  - Real-time SubAgent Fleet table tracking latency, call counts, circuit health, and modular toggle switches.
  - Filterable Addon Grid with instant iOS-style toggles across All, Agents, SubAgents, and Security Safeguards.

---

## [v2.2.0] - 2026-09-18 (Multi-Inbox & 5-Specialist Workforce Hub)

### 🚀 Added
- **Multi-Account Inbox Sentinel (Up to 5 Inboxes)**:
  - Supports simultaneous monitoring across Gmail, Outlook / Office 365, Yahoo Mail, iCloud, and custom IMAP servers.
  - Interactive account management modal on Web Command Center with connection testing and credentials validation.
  - Persistent encrypted configuration stored in `email_accounts.json`.
- **5 Complete Autonomous AI Employee Specialists**:
  1. `email_hygiene`: Multi-account anti-spam with 7-feature security pipeline and dry-run protection.
  2. `meeting_assistant`: Calendar audit, scheduling conflict resolution, and meeting prep dossiers.
  3. `lead_finder`: ICP fit scoring, company signal research, and personalized outreach pitch generation.
  4. `customer_support`: 24/7 ticket sentiment classification, contextual reply drafting, and emergency escalation.
  5. `mobile_dispatcher`: Comms Sentinel connected directly to Deven's mobile phone (+230 58169420) via WhatsApp/SMS.
- **Live Mission Control Telemetry**:
  - High-performance Server-Sent Events (SSE) streaming (`/api/events`) broadcasting live file actions, decision matrices, and scan heartbeats.
  - Full-screen Mission Control terminal with auto-scroll and log clearance.
- **Dynamic Configuration Modals**:
  - Auto-generated schema-based settings modals for every agent loaded in the workforce.

---

## [v2.0.0] - 2026-09-18 (Modular Backbone & Web Dashboard)

### 🚀 Added
- **Modular Agent Backbone (`core/`)**:
  - `core/base_agent.py`: `BaseAgent` abstract class defining the standardized contract (`run_cycle()`, `get_stats()`, `get_info()`).
  - `core/agent_manager.py`: Central registry and orchestrator with dynamic auto-discovery of any plugin inside `agents/`.
  - Multi-agent background scheduler running each agent at its configured schedule interval.
- **Dynamic Plugin Architecture (`agents/`)**:
  - `agents/email_hygiene/agent.py`: Flagship Email Hygiene Specialist inheriting from `BaseAgent`.
  - `agents/meeting_assistant/agent.py`: Second employee plugin demonstrating modular plug-and-play expansion.
- **Light Mode Web Command Center (`static/`)**:
  - Single-page application built with modern Light Mode design system (Inter font, card shadows, status badges).
  - **Workforce Hub Tab**: Shows dynamic cards for all loaded employee agents with status pills, enable/disable toggles, and manual run buttons.
  - **Email Triage Tab**: Live stream table, real-time stat counters, and dry-run safety badge.
  - **Undo & Trash Ledger Tab**: One-click restore action for trashed emails.
  - **AI Email Tester Tab**: Interactive payload simulator for testing Gemini reasoning live.
  - **Rules & Security Tab**: Form for managing VIP Whitelist, Blacklist TLDs/Keywords, and confidence thresholds directly from the UI.
- **FastAPI Unified Server (`server.py`)**:
  - REST endpoints for multi-agent management (`/api/agents`, `/api/agents/{id}/run`, `/api/agents/{id}/toggle`, `/api/scheduler/toggle`).
  - REST endpoints for email actions (`/api/status`, `/api/scan`, `/api/ledger`, `/api/restore`, `/api/simulate`, `/api/rules`).

---

## [v1.1.0] - 2026-09-18 (7 Production-Grade Security Features)

### 🛡️ Added
- **Feature 1 (Immunity Shield)**: Hardcoded bypass for 2FA, OTPs, verification codes, password resets, and domains in `WHITELIST_DOMAINS`.
- **Feature 2 (Two-Tier Routing)**: High-confidence spam (≥ 90%) moves to Trash; medium junk (70%–89%) quarantines to Review folder.
- **Feature 3 (Brand Spoofing Hunter)**: Detects phishing senders pretending to be PayPal, Apple, Google, Amazon, etc. from unauthorized domains.
- **Feature 4 (List-Unsubscribe Extractor)**: Extracts RFC 2369 unsubscribe headers and web links for audit reports.
- **Feature 5 (Daily Triage Digest)**: Writes persistent daily audit summaries in `daily_report.md`.
- **Feature 6 (Fast Blacklist Engine)**: Instantly trashes bad TLDs (`.xyz`, `.top`, `.buzz`) or banned keywords.
- **Feature 7 (Undo & Recovery Ledger)**: Logs all trashed/moved items in `trash_ledger.json` with CLI restore support (`agent.py --restore <UID>`).

### 🔧 Fixed
- Windows terminal CP1252 character encoding issues resolved with UTF-8 reconfigure and safe ASCII/Rich formatting.
- IMAP password sanitization (automatically strips spaces in Google App Passwords).

---

## [v1.0.0] - 2026-09-18 (Initial AI Email Agent MVP)

### 🌟 Initial Release
- `spam_classifier.py`: Initial Gemini 2.5 Flash structured reasoning engine.
- `email_client.py`: IMAP SSL connection, unread email search, MIME header decoding, and plain-text body extraction.
- `agent.py`: Coordinator tying the Brain and Hands together with a confidence threshold.
- `scheduler.py`: Basic hourly loop runner using Python's `schedule` library.
- `test_brain.py`: Mock test script with 4 synthetic test cases.
- `.env.example`: Secure configuration template for API keys and credentials.
