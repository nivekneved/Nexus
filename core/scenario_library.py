"""
Nexus Workforce Engine — Real Live Daily Scenarios Library
=============================================================================
Contains at least 25 real, live, daily operational scenarios for each of the
5 core user types:
  1. Comms (Communications, Inbound Triage, WhatsApp, VIP Escalations)
  2. Operations (System Integrity, SQLite Backups, Budget Guards, Safeguards)
  3. Commerce (Digital Vending Machine, MCB Juice / PayPal Invoicing, Treasury)
  4. Research (Mauritius Market Intelligence, Lead Prospecting, CVE Radar)
  5. CEO / Executive (Strategic Orchestration, Rs 150k MUR Roadmap, Social Blitz)

Total: 125 production-ready scenarios.
"""

from typing import Dict, Any, List, Optional

DAILY_SCENARIOS: Dict[str, List[Dict[str, Any]]] = {
    # ═════════════════════════════════════════════════════════════════════════
    # 1. COMMS USER TYPE (25 Daily Real-World Scenarios)
    # ═════════════════════════════════════════════════════════════════════════
    "comms": [
        {
            "id": "comms_01",
            "title": "⚡ VIP Client Inquiry Rapid Response (<90s)",
            "category": "VIP Support",
            "urgency": "Urgent",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "VIP SLA Guarantee: Rapid Response Turnaround",
            "badge": "PRIORITY COMMS DISPATCH",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Enterprise Medical / Financial Retainer Accounts",
            "description": "Immediate personalized acknowledgement confirming priority ticket status and active AI remediation in progress.",
            "body": (
                "Dear Partner,\n\n"
                "Thank you for contacting the Nexus Executive Desk. We have received your high-priority inquiry.\n\n"
                "Our autonomous monitoring agents and Principal Architect (Deven Pawaray) have already reviewed the telemetry. "
                "Remediation is actively underway, and our engineering team will provide a formal resolution memo within 45 minutes.\n\n"
                "For urgent direct phone escalation: +230 58169420.\n\n"
                "Sincerely,\nNexus Executive Communications Desk"
            ),
            "callouts": ["Response Time: < 90 Seconds", "Escalation: Level 3 Principal Architect", "Channel: Dual Email & WhatsApp Gateway"],
            "cta_label": "Dispatch Priority Response"
        },
        {
            "id": "comms_02",
            "title": "📧 Cold B2B Lead Follow-Up — Touch 2 Value Add",
            "category": "Sales Outreach",
            "urgency": "High",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "B2B Sequence: Value-Add Operational Audit",
            "badge": "OUTBOUND SEQUENCE",
            "gradient": "linear-gradient(135deg, #0369a1 0%, #0c4a6e 100%)",
            "target_audience": "Mauritius Hospitality & Private Clinic Directors",
            "description": "Second touch in cold outbound sequence offering a 3-point operational bottleneck audit without pitch fluff.",
            "body": (
                "Hi [First Name],\n\n"
                "I know you are busy managing operations at [Company Name].\n\n"
                "Rather than pitching software, I put together a 3-point workflow audit of how hospitality and clinic operators in Mauritius "
                "are reclaiming 15+ hours weekly by replacing manual WhatsApp booking replies with self-hosted AI.\n\n"
                "Would it be helpful if I sent over the 2-minute Loom teardown? No strings attached.\n\n"
                "Best regards,\nDeven Pawaray\nFounder, Nexus AI (+230 58169420)"
            ),
            "callouts": ["Zero Sales Fluff", "Personalized Teardown Hook", "Mauritius DPA Compliant"],
            "cta_label": "Send Touch 2 Follow-Up"
        },
        {
            "id": "comms_03",
            "title": "🛡️ Scheduled Maintenance & Zero-Downtime Notice",
            "category": "System Comms",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Scheduled Platform Upgrade & Database Re-Indexing",
            "badge": "INFRASTRUCTURE UPDATE",
            "gradient": "linear-gradient(135deg, #475569 0%, #1e293b 100%)",
            "target_audience": "All Active Portal Clients",
            "description": "Professional heads-up for nighttime SQLite WAL optimization and kernel patching with zero customer disruption.",
            "body": (
                "Dear Valued Client,\n\n"
                "As part of our commitment to sovereign data integrity and 99.9% uptime, Nexus will conduct a scheduled 15-minute maintenance window "
                "tonight at 02:00 AM MUT (Mauritius Time).\n\n"
                "What to expect:\n"
                "• All client web portals and WhatsApp booking bots will remain fully operational via failover hot-standby.\n"
                "• Security patches and database WAL checkpoints will be applied automatically.\n\n"
                "No action is required on your part. Thank you for partnering with Nexus AI."
            ),
            "callouts": ["Failover Standby Active", "Zero Downtime Window", "2:00 AM MUT Schedule"],
            "cta_label": "Broadcast Maintenance Notice"
        },
        {
            "id": "comms_04",
            "title": "🚨 Security Incident All-Clear Memo",
            "category": "Incident Response",
            "urgency": "High",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Security Audit & Automated Threat Neutralization Memo",
            "badge": "INCIDENT CLEARANCE",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Enterprise Compliance & IT Directors",
            "description": "Reassuring formal statement following an automated firewall block of unauthorized probing.",
            "body": (
                "To: IT Security & Compliance Committee\n\n"
                "Nexus Autopilot Shields detected and neutralized an anomalous IP probing pattern at 03:14 MUT. "
                "Our automated rate-limiting jail immediately blacklisted the offending CIDR block.\n\n"
                "Audit Summary:\n"
                "✔ Zero data compromise or exfiltration.\n"
                "✔ All cryptographic SQLite hashes verified against origin ledger.\n"
                "✔ 25/25 enterprise safeguards verified online and fully compliant with Mauritius DPA 2017.\n\n"
                "Full security audit logs are archived in your private compliance vault."
            ),
            "callouts": ["Zero Data Leakage", "Automated IP Blacklist", "Mauritius DPA 2017 Verified"],
            "cta_label": "Send Incident Clearance"
        },
        {
            "id": "comms_05",
            "title": "🤝 Client Onboarding & Sovereign Setup Welcome",
            "category": "Onboarding",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Welcome to Nexus: Your Dedicated AI Fleet is Provisioned",
            "badge": "CLIENT ONBOARDING",
            "gradient": "linear-gradient(135deg, #4f46e5 0%, #312e81 100%)",
            "target_audience": "Newly Signed Retainer Clients",
            "description": "Warm executive onboarding package including portal credentials, WhatsApp bot direct links, and emergency protocols.",
            "body": (
                "Dear [Client Name],\n\n"
                "Welcome to the future of autonomous operations. Your dedicated Nexus fleet has been provisioned and hardened.\n\n"
                "Your Quick Start Essentials:\n"
                "1. Private Executive Portal: [Portal URL]\n"
                "2. Direct WhatsApp Dispatch Line: +230 58169420\n"
                "3. Dedicated Account Lead: Deven Pawaray\n\n"
                "We have scheduled your 15-minute calibration check-in for tomorrow at 10:00 AM. We look forward to scaling your business."
            ),
            "callouts": ["Turnkey Portal Credentials", "1-on-1 Calibration Call", "Dedicated Fleet Online"],
            "cta_label": "Dispatch Welcome Packet"
        },
        {
            "id": "comms_06",
            "title": "📱 Polite WhatsApp Payment Reminder (MCB Juice)",
            "category": "Billing Comms",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Gentle Account Settlement Notice via MCB Juice",
            "badge": "PAYMENT REMINDER",
            "gradient": "linear-gradient(135deg, #d97706 0%, #78350f 100%)",
            "target_audience": "Local Clients with Outstanding Invoices",
            "description": "Courteous WhatsApp reminder with 1-click Juice instructions to clear overdue balance smoothly.",
            "body": (
                "Bonjour [Client Name] 👋,\n\n"
                "J'espère que vous passez une excellente journée !\n\n"
                "Ceci est un petit rappel concernant la facture *[Invoice ID]* d'un montant de *Rs [Amount] MUR* arrivée à échéance.\n\n"
                "Pour régler instantanément via MCB Juice :\n"
                "📱 Numéro : *58169420* (Deven Pawaray)\n"
                "📝 Référence : *[Invoice ID]*\n\n"
                "Dès réception, votre reçu officiel avec signature cryptographique sera généré automatiquement. Merci pour votre collaboration !"
            ),
            "callouts": ["MCB Juice Ready (+230 58169420)", "1-Click Direct Settlement", "Automated Official Receipt"],
            "cta_label": "Dispatch WhatsApp Reminder"
        },
        {
            "id": "comms_07",
            "title": "📈 Quarterly Retainer Renewal & Expansion Proposal",
            "category": "Client Growth",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Executive Quarterly Business Review (QBR) & Retainer Renewal",
            "badge": "RETAINER RENEWAL",
            "gradient": "linear-gradient(135deg, #059669 0%, #047857 100%)",
            "target_audience": "Existing Retainer Clients (Month 3+)",
            "description": "Evidence-backed renewal memo highlighting hours saved, inquiry conversion increases, and upcoming AI capabilities.",
            "body": (
                "Dear [Client Executive],\n\n"
                "Over the past 90 days, your Nexus autonomous fleet has achieved:\n"
                "• 412 customer booking inquiries processed automatically.\n"
                "• Average response latency cut from 3.5 hours to 42 seconds.\n"
                "• Estimated operational savings: Rs 85,000 MUR in staff overtime.\n\n"
                "Attached is our renewal manifest for Q4, locked at your grandfathered rate of Rs 45,000/mo. "
                "Shall we schedule a brief 10-minute touchpoint this Thursday to finalize next quarter's roadmap?"
            ),
            "callouts": ["Quantified ROI Proof", "Grandfathered Pricing Lock", "Executive Touchpoint"],
            "cta_label": "Send Renewal Proposal"
        },
        {
            "id": "comms_08",
            "title": "📅 Meeting Reschedule with Self-Service Link",
            "category": "Coordination",
            "urgency": "Low",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Calendar Alignment & Rescheduling Courtesy",
            "badge": "CALENDAR NOTICE",
            "gradient": "linear-gradient(135deg, #64748b 0%, #334155 100%)",
            "target_audience": "Prospective B2B Clients & Partners",
            "description": "Smooth, respectful notification offering alternative morning/afternoon slots.",
            "body": (
                "Hi [Name],\n\n"
                "Due to an urgent production client deployment this afternoon, I must respectfully request that we push our scheduled check-in.\n\n"
                "I apologize for any disruption. Here are three alternate slots that work on my end:\n"
                "1. Tomorrow (Tuesday) at 10:30 AM MUT\n"
                "2. Tomorrow (Tuesday) at 02:00 PM MUT\n"
                "3. Wednesday at 11:00 AM MUT\n\n"
                "Let me know which suits you best, or reply with your preferred time.\n\nWarm regards,\nDeven Pawaray"
            ),
            "callouts": ["3 Frictionless Options", "Courteous Tone", "Zero Back-and-Forth"],
            "cta_label": "Send Reschedule Request"
        },
        {
            "id": "comms_09",
            "title": "🧘 Inbound Complaint De-escalation & Action Plan",
            "category": "Client Care",
            "urgency": "Urgent",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Personal Commitment & 3-Step Root Cause Resolution",
            "badge": "SERVICE RECOVERY",
            "gradient": "linear-gradient(135deg, #b91c1c 0%, #7f1d1d 100%)",
            "target_audience": "Dissatisfied Client / Glitch Escalation",
            "description": "Direct, empathetic accountability from founder with concrete next steps and compensation gesture.",
            "body": (
                "Dear [Client Name],\n\n"
                "I am writing to you directly regarding the issue you experienced with [Feature/Service] earlier today.\n\n"
                "I take full personal responsibility. That does not meet our standard of excellence. Here is what we have done:\n"
                "1. Identified the root cause: [Brief explanation without tech jargon].\n"
                "2. Patched and hotfixed the logic: Live verified at 14:20 MUT.\n"
                "3. Applied a credit of Rs 5,000 MUR to your next billing cycle as our apology for the inconvenience.\n\n"
                "I am available on my direct line (+230 58169420) if you would like to discuss this further."
            ),
            "callouts": ["Direct Founder Accountability", "Immediate Hotfix Deployed", "Commercial Credit Granted"],
            "cta_label": "Send Service Recovery Memo"
        },
        {
            "id": "comms_10",
            "title": "📋 Contractor Scope & Deliverable Handover Briefing",
            "category": "Operations Comms",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Engineering Sprint Scope & Milestone Acceptance Criteria",
            "badge": "VENDOR HANDOVER",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #1e3a8a 100%)",
            "target_audience": "Contractors, Freelancers, Technical Vendors",
            "description": "Clear milestone specifications with cryptographic acceptance tests and payment trigger conditions.",
            "body": (
                "Hi [Vendor/Developer Name],\n\n"
                "Please find below the confirmed scope for Milestone 2:\n\n"
                "Deliverables:\n"
                "• Integration of Base L2 Treasury Webhook listener in Python FastAPI.\n"
                "• Unit tests passing with >90% coverage.\n"
                "• Zero external unvetted dependencies.\n\n"
                "Compensation: $350 USD (or Rs 16,000 MUR) payable immediately upon SHA-256 verification and merge into main.\n\n"
                "Target Delivery: Friday 18:00 MUT."
            ),
            "callouts": ["Clear Acceptance Tests", "Instant Settlement Trigger", "Strict Boundary Conditions"],
            "cta_label": "Dispatch Scope Briefing"
        },
        {
            "id": "comms_11",
            "title": "🎉 Webinar / Live Masterclass Exclusive Invitation",
            "category": "Marketing Comms",
            "urgency": "Low",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Exclusive Briefing: How Local AI Slashes Mauritius Business Payroll",
            "badge": "MASTERCLASS INVITE",
            "gradient": "linear-gradient(135deg, #7c3aed 0%, #4338ca 100%)",
            "target_audience": "Mauritius SME Owners & Founders",
            "description": "High-conversion invitation to an exclusive 30-minute teardown session of autonomous local agent fleets.",
            "body": (
                "Hi [First Name],\n\n"
                "On Thursday at 14:00 MUT, I am hosting a private 30-minute live demonstration for 12 selected business founders in Mauritius:\n\n"
                "Topic: 'Replacing $50/mo SaaS Subscriptions with Sovereign Local AI Employees.'\n\n"
                "We will show live screen shares of autonomous WhatsApp booking bots, instant MCB Juice reconciliation, and local LLM document triage.\n\n"
                "Reserve your seat (free for verified founders): [Link]\n\nHope to see you there!\nDeven Pawaray"
            ),
            "callouts": ["Capped at 12 Founders", "Live Screen Demonstrations", "Free Value Proposition"],
            "cta_label": "Send Masterclass Invite"
        },
        {
            "id": "comms_12",
            "title": "📰 Local Tech Press & Media Pitch",
            "category": "PR Comms",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Story Pitch: Mauritius Solo Engineer Builds Sovereign 18-Agent AI Fleet",
            "badge": "MEDIA PITCH",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Mauritius Business Mag, L'Express, Defi Media Tech Editors",
            "description": "Compelling local innovation hook highlighting sovereign AI, data privacy, and tech sovereignty in Cybercity Ebene.",
            "body": (
                "Dear [Journalist Name],\n\n"
                "While global tech firms pour billions into cloud subscriptions, a Mauritian startup based in Cybercity Ebene has developed "
                "an autonomous local AI workforce capable of running entirely on sovereign hardware under Mauritius Data Protection Act 2017 standards.\n\n"
                "The founder, Deven Pawaray, has deployed 18 autonomous agents that triage emails, manage client accounts, and process instant local currency (MCB Juice) transactions.\n\n"
                "Would you be interested in an exclusive interview on how Mauritius can become a regional hub for sovereign AI?"
            ),
            "callouts": ["Local Cybercity Ebene Angle", "Data Sovereignty Focus", "Exclusive Interview Offer"],
            "cta_label": "Send Media Pitch"
        },
        {
            "id": "comms_13",
            "title": "🛍️ WhatsApp Instant Order & Delivery Confirmation",
            "category": "Commerce Comms",
            "urgency": "Urgent",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Instant Delivery: Your $1 Digital Tool is Ready",
            "badge": "ORDER FULFILLMENT",
            "gradient": "linear-gradient(135deg, #059669 0%, #10b981 100%)",
            "target_audience": "Digital Vending Machine Buyers",
            "description": "Instant 1-second delivery message with direct script download link, license key, and MCB Juice receipt.",
            "body": (
                "Thank you for your purchase! 🚀\n\n"
                "Your standalone utility *[Product Name]* has been generated and verified.\n\n"
                "📦 Download Link: [Direct Link]\n"
                "🔑 Commercial License Key: `NX-2026-[HASH]`\n"
                "⚡ Execution: Single-file Python script, zero cloud subscriptions required.\n\n"
                "Questions or feedback? Reply directly to this WhatsApp line. Enjoy your autonomous tool!"
            ),
            "callouts": ["Instant Delivery < 1s", "Commercial License Stamped", "Single-File Python Script"],
            "cta_label": "Dispatch Order Confirmation"
        },
        {
            "id": "comms_14",
            "title": "🌟 Client Net Promoter Score (NPS) & Review Request",
            "category": "Customer Success",
            "urgency": "Low",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "How are we doing? Quick 1-Question Check-In",
            "badge": "NPS FEEDBACK",
            "gradient": "linear-gradient(135deg, #6366f1 0%, #4338ca 100%)",
            "target_audience": "Active Clients (30+ Days Post Deployment)",
            "description": "Frictionless 1-click rating request to collect glowing testimonials and identify optimization targets.",
            "body": (
                "Hi [Client Name],\n\n"
                "It has been one month since we launched your Nexus autonomous system.\n\n"
                "On a scale of 1 to 10, how likely are you to recommend Nexus AI to another founder or business owner in your network?\n\n"
                "[1 - Poor]  [5 - Average]  [10 - Absolute Game Changer]\n\n"
                "If you have 30 seconds, reply with your biggest win so far — your feedback directly shapes our weekly agent updates.\n\nWarm regards,\nDeven"
            ),
            "callouts": ["1-Click Effortless Reply", "Identifies Referral Champions", "Continuous Improvement"],
            "cta_label": "Send NPS Request"
        },
        {
            "id": "comms_15",
            "title": "🤝 Referral Partnership & Commission Incentive",
            "category": "Partner Growth",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Earn 20% Recurring Commission: Nexus Agency Partner Program",
            "badge": "PARTNERSHIP PITCH",
            "gradient": "linear-gradient(135deg, #059669 0%, #065f46 100%)",
            "target_audience": "Web Agencies, IT Consultants, Accountants in Mauritius",
            "description": "Lucrative referral partnership pitch offering 20% lifetime cut on every client introduced to Nexus retainers.",
            "body": (
                "Hi [Partner Name],\n\n"
                "Many of your existing web development or accounting clients are likely looking for AI automation, WhatsApp bots, and CRM triage.\n\n"
                "Instead of building it from scratch, Nexus offers a white-label partner program:\n"
                "• You refer the client or bundle our AI workforce.\n"
                "• We handle 100% of engineering, hosting, and 24/7 maintenance.\n"
                "• You receive a guaranteed 20% recurring monthly commission (Rs 9,000 MUR/mo per client).\n\n"
                "Are you open to a quick 5-minute phone chat to review the partner agreement?"
            ),
            "callouts": ["20% Lifetime Recurring Cut", "Zero Engineering Overhead", "White-Label Ready"],
            "cta_label": "Send Partner Pitch"
        },
        {
            "id": "comms_16",
            "title": "📊 Quarterly Business Review (QBR) Calendar Invitation",
            "category": "Client Retention",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Quarterly Operations Review & Performance Telemetry",
            "badge": "QBR INVITATION",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #075985 100%)",
            "target_audience": "Tier-1 Retainer Accounts",
            "description": "Executive calendar hold for a structured 20-minute quarterly audit presentation.",
            "body": (
                "Dear [Executive Sponsor],\n\n"
                "As we close out the quarter, I would like to invite you and your operations leadership to our 20-minute QBR session.\n\n"
                "Agenda:\n"
                "1. Telemetry Audit: Inbound volume, response times, and error rate metrics.\n"
                "2. Financial Impact: Quantified staff hours recovered and cost savings.\n"
                "3. Next Quarter Enhancements: Integrating new Gemini 2.5 voice and document triage agents.\n\n"
                "Please accept the calendar invite or let me know if an alternate time suits you better."
            ),
            "callouts": ["20-Minute Concise Format", "Quantified Data Telemetry", "Next Quarter Roadmap"],
            "cta_label": "Send QBR Invitation"
        },
        {
            "id": "comms_17",
            "title": "📜 SLA Guarantee Certificate & Quality Assurance",
            "category": "Compliance Comms",
            "urgency": "Low",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Official 99.9% Service Level Agreement (SLA) Certificate",
            "badge": "SLA CERTIFICATION",
            "gradient": "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
            "target_audience": "Enterprise Compliance Officers",
            "description": "Cryptographically signed document certifying uptime, local data storage guarantees, and penalty terms.",
            "body": (
                "Attention: Office of Compliance and Information Security\n\n"
                "Please find attached your formal Nexus Service Level Agreement (SLA) Certificate for the 2026 fiscal year.\n\n"
                "Key Covenant Highlights:\n"
                "✔ 99.9% Portal & API Availability.\n"
                "✔ Sub-90-second response latency on priority webhooks.\n"
                "✔ 100% Data Residence in Sovereign Local Storage (Zero unauthorized foreign cloud mirroring).\n\n"
                "Signed cryptographically by Deven Pawaray, Founder & Principal Architect."
            ),
            "callouts": ["99.9% Uptime Commitment", "Zero Foreign Mirroring", "Cryptographically Stamped"],
            "cta_label": "Issue SLA Certificate"
        },
        {
            "id": "comms_18",
            "title": "🚀 Cross-Sell Pitch: Autonomous WhatsApp Add-on",
            "category": "Account Expansion",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Upgrade Opportunity: 24/7 Conversational WhatsApp Booking Engine",
            "badge": "ACCOUNT UPGRADE",
            "gradient": "linear-gradient(135deg, #059669 0%, #15803d 100%)",
            "target_audience": "Clients using only Web Portal without WhatsApp",
            "description": "Compelling upgrade pitch demonstrating how adding WhatsApp integration captures after-hours revenue automatically.",
            "body": (
                "Hi [Client Name],\n\n"
                "Your web portal is performing well, but our telemetry shows that 42% of customer inquiries in Mauritius occur between 18:00 and 22:00 via WhatsApp.\n\n"
                "We have built a turnkey WhatsApp Add-on that connects directly to your existing database, quoting prices and taking bookings instantly.\n\n"
                "Since you are an existing portal client, setup is discounted to Rs 15,000 MUR (one-time). "
                "Can I activate this on your staging instance for you to test?"
            ),
            "callouts": ["Captures 42% After-Hours Leads", "Turnkey Database Sync", "Discounted Existing Client Rate"],
            "cta_label": "Send Upgrade Pitch"
        },
        {
            "id": "comms_19",
            "title": "🔒 Non-Disclosure Agreement (NDA) & Data Privacy Packet",
            "category": "Legal Comms",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Mutual NDA & Mauritius DPA 2017 Compliance Packet",
            "badge": "LEGAL COMPLIANCE",
            "gradient": "linear-gradient(135deg, #334155 0%, #1e293b 100%)",
            "target_audience": "Enterprise Prospects Pre-Discovery Call",
            "description": "Standard mutual NDA and data sovereignty covenant to establish complete confidentiality prior to codebase review.",
            "body": (
                "Dear [Legal Counsel / Corporate Lead],\n\n"
                "Prior to our technical discovery session, we are pleased to provide our standard Mutual Non-Disclosure Agreement.\n\n"
                "Nexus adheres strictly to the Mauritius Data Protection Act 2017 and GDPR equivalent principles. "
                "All proprietary schemas, API credentials, and internal customer databases remain your exclusive sovereign property.\n\n"
                "Please review the attached digital document for signature, or provide your corporate template."
            ),
            "callouts": ["Mauritius DPA 2017 Standard", "Strict Mutual Protection", "Ready for Digital Sign-Off"],
            "cta_label": "Dispatch NDA Packet"
        },
        {
            "id": "comms_20",
            "title": "🎄 Seasonal Founder Message with Retainer Bonus",
            "category": "Relationship Comms",
            "urgency": "Low",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Year-End Appreciation & Exclusive Q1 Automation Bonus",
            "badge": "SEASONAL GREETING",
            "gradient": "linear-gradient(135deg, #c026d3 0%, #701a75 100%)",
            "target_audience": "All Active and Past Clients",
            "description": "Heartfelt personal holiday message from founder with a free automation voucher for the new year.",
            "body": (
                "Dear [Client Name],\n\n"
                "As the year draws to a close, I wanted to personally thank you for trusting Nexus AI as your autonomous systems partner.\n\n"
                "As our token of appreciation, we have credited your account with a complimentary *Custom Python Automation Sprint* "
                "(valued at Rs 15,000 MUR), valid for any new workflow you want automated in Q1.\n\n"
                "Wishing you, your family, and your team a restful holiday season and an extraordinary year ahead!\n\nWarmest regards,\nDeven Pawaray"
            ),
            "callouts": ["Personal Touch from Founder", "Rs 15,000 Free Automation Sprint", "Builds Long-Term Loyalty"],
            "cta_label": "Send Seasonal Greeting"
        },
        {
            "id": "comms_21",
            "title": "👋 Respectful 'Breakup' Email for Ghosted Prospects",
            "category": "Sales Outreach",
            "urgency": "Low",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Closing Your File: Is Autonomous AI Still on Your Radar?",
            "badge": "BREAKUP EMAIL",
            "gradient": "linear-gradient(135deg, #475569 0%, #334155 100%)",
            "target_audience": "Unresponsive Inbound Leads (14+ Days Inactive)",
            "description": "High-converting psychological takeaway email that gently closes the file, prompting a 30% reply resurgence.",
            "body": (
                "Hi [First Name],\n\n"
                "I haven't heard back from you, so I assume that automating [Company Name]'s operations is no longer a priority for this quarter.\n\n"
                "Totally understand — priorities shift and timing is everything.\n\n"
                "I am archiving your file on our end so I don't clutter your inbox. "
                "If you ever decide to revisit replacing manual admin with autonomous AI down the road, you know where to find me.\n\nBest of luck with scaling!\nDeven Pawaray"
            ),
            "callouts": ["30%+ Re-engagement Rate", "Removes Sales Pressure", "Professional & Clean"],
            "cta_label": "Send Breakup Email"
        },
        {
            "id": "comms_22",
            "title": "🛠️ Technical Support Post-Mortem & Fix Notice",
            "category": "Technical Comms",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Post-Mortem Memo: Ticket #4812 Resolved and Validated",
            "badge": "POST-MORTEM NOTICE",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #1e40af 100%)",
            "target_audience": "Technical Stakeholders following a reported bug",
            "description": "Clear transparent explanation of root cause, immediate fix, and long-term automated prevention shield.",
            "body": (
                "To: [Client IT Lead]\n\n"
                "We have closed Support Ticket #4812 (WhatsApp webhook timeout during network switch).\n\n"
                "Root Cause Analysis:\n"
                "• A transient DNS resolution delay at our upstream gateway caused a 4-second timeout.\n"
                "Remediation Applied:\n"
                "• Implemented local SQLite retry buffer with 3-second exponential backoff.\n"
                "• Zero messages dropped; all queued payloads cleared successfully.\n\n"
                "All systems are operating within optimal latency thresholds (<250ms)."
            ),
            "callouts": ["Complete Root Cause Transparency", "Exponential Backoff Shield", "Verified <250ms Latency"],
            "cta_label": "Send Post-Mortem Memo"
        },
        {
            "id": "comms_23",
            "title": "👔 Executive C-Level Introduction & Strategic Alignment",
            "category": "Executive Comms",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Strategic Alignment: Autonomous Workforce Architecture for [Company]",
            "badge": "EXECUTIVE OUTREACH",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Managing Directors & Group CEOs in Mauritius",
            "description": "High-level strategic pitch addressing operating margin expansion and sovereign data compliance.",
            "body": (
                "Dear [Managing Director Name],\n\n"
                "I am reaching out to share how leadership teams across Mauritius are navigating the transition to autonomous AI.\n\n"
                "Nexus provides turnkey, self-hosted AI workforces that operate within your own sovereign network — eliminating expensive SaaS seats while automating high-friction workflows like invoice chasing, patient/guest triage, and compliance auditing.\n\n"
                "I would welcome the opportunity to arrange an executive briefing at your convenience.\n\nRespectfully,\nDeven Pawaray\nFounder, Nexus AI"
            ),
            "callouts": ["C-Suite Strategic Tone", "Margin Expansion Focus", "Sovereign Infrastructure"],
            "cta_label": "Send Executive Introduction"
        },
        {
            "id": "comms_24",
            "title": "🧾 Supplier Invoice Query & Discrepancy Clarification",
            "category": "Vendor Relations",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Billing Reconciliation Inquiry: Invoice #9021 Line-Item Review",
            "badge": "VENDOR INQUIRY",
            "gradient": "linear-gradient(135deg, #d97706 0%, #92400e 100%)",
            "target_audience": "Hardware or Cloud Compute Suppliers",
            "description": "Firm yet professional inquiry regarding unverified billing line items to protect company cash flow.",
            "body": (
                "Attention: Accounts Receivable\n\n"
                "During our automated ledger audit of Invoice #9021 (dated 2026-09-20), our system flagged a discrepancy:\n\n"
                "• Invoiced Amount: $214.50 USD\n"
                "• Approved Service Agreement Rate: $180.00 USD\n"
                "• Unreconciled Delta: $34.50 USD (labeled 'Compute Overage')\n\n"
                "Our autonomous monitoring telemetry indicates our cluster remained strictly within tier limits. "
                "Kindly review and provide a credit memo or amended invoice."
            ),
            "callouts": ["Telemetry Evidence Backed", "Protects Operating Budget", "Professional & Fact-Based"],
            "cta_label": "Send Billing Clarification"
        },
        {
            "id": "comms_25",
            "title": "🚨 Emergency WhatsApp Alert to Founder (Deven Pawaray)",
            "category": "Internal Escalation",
            "urgency": "Urgent",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "URGENT SYSTEM ESCALATION: Immediate Attention Required",
            "badge": "FOUNDER DIRECT ALERT",
            "gradient": "linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%)",
            "target_audience": "Sir Deven Pawaray (+230 58169420)",
            "description": "High-priority direct WhatsApp ping dispatched by autonomous watchdog when human intervention is mandatory.",
            "body": (
                "🚨 *NEXUS AUTONOMOUS ESCALATION — SIR DEVEN*\n\n"
                "Watchdog Level 1 Alert triggered at [Timestamp]:\n"
                "• An unexpected anomaly requires your direct cryptographic authorization.\n"
                "• Safeguard: Spending cap protection or high-value invoice confirmation.\n"
                "• Immediate Action: Please review and sign off via Executive Cockpit:\n"
                "http://127.0.0.1:8000\n\n"
                "System standing by in failsafe state."
            ),
            "callouts": ["Dispatched to +230 58169420", "Failsafe Lockdown Engaged", "Immediate Cockpit Link"],
            "cta_label": "Dispatch Emergency Alert"
        }
    ],

    # ═════════════════════════════════════════════════════════════════════════
    # 2. OPERATIONS USER TYPE (25 Daily Real-World Scenarios)
    # ═════════════════════════════════════════════════════════════════════════
    "operations": [
        {
            "id": "ops_01",
            "title": "🛡️ Automated Daily SQLite WAL Backup & SHA-256 Stamp",
            "category": "Data Integrity",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Cryptographic SQLite WAL Snapshot & Integrity Verification",
            "badge": "DATABASE BACKUP",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Local System Engine",
            "description": "Flushes SQLite write-ahead log, creates a compressed timestamped archive, and computes SHA-256 integrity seal.",
            "body": (
                "Executing Cryptographic Database Snapshot:\n"
                "1. Checkpoint WAL log into primary data file (data/nexus_workforce.db).\n"
                "2. Bundle memory/ and products/ catalogs into backups/snapshot_[timestamp].tar.gz.\n"
                "3. Compute SHA-256 checksum and append to backups/manifest.json.\n"
                "Result: Backup completed successfully. Zero lock contention."
            ),
            "callouts": ["WAL Flushed Clean", "SHA-256 Stamped", "Zero Downtime"],
            "cta_label": "Execute Snapshot"
        },
        {
            "id": "ops_02",
            "title": "💰 Cloud Compute Budget Watchdog ($180 Hard Cap Guard)",
            "category": "FinOps Guard",
            "urgency": "Urgent",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Cloud Compute Ceiling Enforcement ($180 Limit)",
            "badge": "BUDGET WATCHDOG",
            "gradient": "linear-gradient(135deg, #d97706 0%, #78350f 100%)",
            "target_audience": "Cloud Infrastructure",
            "description": "Inspects current monthly cloud spend across APIs and throttles background batches if spend nears threshold.",
            "body": (
                "FinOps Budget Watchdog Sweep:\n"
                "• Monthly Budget Cap: $180.00 USD\n"
                "• Current Month-to-Date Accrual: $14.20 USD\n"
                "• Status: 100% within safe operational corridor (<10% utilized).\n"
                "• Action: Free tier local fallback enabled for batch embeddings."
            ),
            "callouts": ["Budget Cap: $180.00", "Current Run Rate: Safe", "Auto-Throttle Armed"],
            "cta_label": "Run Budget Audit"
        },
        {
            "id": "ops_03",
            "title": "🧹 Orphaned Zombie Process Sweep & RAM Reclamation",
            "category": "Resource Health",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Zombie Subprocess Reaper & Garbage Collection",
            "badge": "RAM OPTIMIZATION",
            "gradient": "linear-gradient(135deg, #475569 0%, #1e293b 100%)",
            "target_audience": "Node Operating System",
            "description": "Terminates stale child worker threads and frees dormant memory back to host OS.",
            "body": (
                "Scanning Active Process Tree:\n"
                "• Inspected 24 worker subprocesses.\n"
                "• Identified 2 orphaned Python background threads (>2h idle).\n"
                "• Safely terminated PID 18492 and PID 19024.\n"
                "• Reclaimed 340 MB host RAM."
            ),
            "callouts": ["340 MB Reclaimed", "Zero Impact on Active Tasks", "Process Tree Clean"],
            "cta_label": "Reclaim System RAM"
        },
        {
            "id": "ops_04",
            "title": "🔐 SSL / TLS Certificate Expiry Radar & Renewal",
            "category": "Security Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "SSL/TLS Sovereign Certificate Validity Audit",
            "badge": "SECURITY SWEEP",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Public Domain Endpoints",
            "description": "Verifies HTTPS certificate expiration date on production domain and renews automated ACME certificates.",
            "body": (
                "SSL Certificate Audit Results:\n"
                "• Target: nexus-workforce.vercel.app & internal reverse proxies.\n"
                "• Certificate Issuer: Let's Encrypt / Vercel Edge Authority.\n"
                "• Expiration: 78 days remaining.\n"
                "• Grade: A+ (HSTS enabled, TLS 1.3 enforced)."
            ),
            "callouts": ["78 Days Remaining", "Grade A+ Security", "Auto-Renewal Armed"],
            "cta_label": "Audit SSL Certificates"
        },
        {
            "id": "ops_05",
            "title": "💾 Local Storage Threshold Monitor (>85% Disk Alert)",
            "category": "Storage Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Disk Space Utilization & Auto-Pruning Sweep",
            "badge": "STORAGE AUDIT",
            "gradient": "linear-gradient(135deg, #dc2626 0%, #991b1b 100%)",
            "target_audience": "Host Storage Drive",
            "description": "Checks primary drive space, rotating legacy debug logs to ensure free buffer remains above safety limit.",
            "body": (
                "Storage Utilization Report:\n"
                "• Drive C: Total 475 GB | Free 142 GB (29.8% Free Capacity).\n"
                "• Log Directory: 24.2 MB across 18 files.\n"
                "• Pruning Action: Compressed 14 logs older than 7 days into .gz archives.\n"
                "• Status: Green / Healthy."
            ),
            "callouts": ["142 GB Available Buffer", "Old Logs Compressed", "Drive Health: Optimal"],
            "cta_label": "Run Storage Health Check"
        },
        {
            "id": "ops_06",
            "title": "🛡️ 25 Enterprise Safeguards Verification Sweep",
            "category": "Safeguards",
            "urgency": "Urgent",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Full 25-Point Defense Safeguard Integrity Scan",
            "badge": "SAFEGUARDS SHIELD",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0c4a6e 100%)",
            "target_audience": "Core Security Engine",
            "description": "Audits all 25 active system safeguards including OTP immunity, spending lock, and directory isolation.",
            "body": (
                "Safeguard Matrix Audit:\n"
                "✔ 1. OTP Bypass Immunity: Active\n"
                "✔ 2. Path Traversal Shield: Active\n"
                "✔ 3. Rate-Limiting Jail: Active\n"
                "✔ 4. Cloud Spend Cap ($180): Active\n"
                "✔ 5. MCB Juice Replay Shield: Active\n"
                "... All 25 safeguards confirmed operational with 0 exceptions."
            ),
            "callouts": ["25/25 Shields Active", "Zero Vulnerabilities", "Mauritius DPA Compliant"],
            "cta_label": "Verify All Safeguards"
        },
        {
            "id": "ops_07",
            "title": "🚫 Rate-Limiting & DDOS IP Jail Enforcement",
            "category": "Network Defense",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Inbound Traffic Scrubbing & Malicious IP Blacklist",
            "badge": "FIREWALL ENFORCEMENT",
            "gradient": "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
            "target_audience": "Network Firewall / FastAPIRoute Guards",
            "description": "Scans inbound request logs for brute-force patterns and writes offenders to the temporary firewall blocklist.",
            "body": (
                "Firewall Scrubbing Log:\n"
                "• Inbound Requests Last 60m: 1,482\n"
                "• Flagged Abnormal Probes: 4 requests to /wp-admin and /.env\n"
                "• Action: Added origin IPs (185.220.101.4, 91.240.118.2) to 24-hour drop jail.\n"
                "• Zero legitimate client impact."
            ),
            "callouts": ["4 Attack Probes Dropped", "Automated IP Jail", "Zero False Positives"],
            "cta_label": "Enforce IP Jail"
        },
        {
            "id": "ops_08",
            "title": "🌿 Git Repository Health & Clean Working Tree Check",
            "category": "Codebase Ops",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Git Version Control Audit & Untracked File Scan",
            "badge": "GIT INTEGRITY",
            "gradient": "linear-gradient(135deg, #15803d 0%, #166534 100%)",
            "target_audience": "Repository Directory",
            "description": "Verifies repo status, ensuring no uncommitted secrets or orphaned debug scripts linger in production branch.",
            "body": (
                "Git Repository Audit:\n"
                "• Branch: main (synchronized with origin/main).\n"
                "• Staged Files: 0\n"
                "• Secrets Scan: Scanned all files against patterns (regex: API_KEY, SECRET). Clean.\n"
                "• Working Tree: Ready for clean automated deployment."
            ),
            "callouts": ["Zero Leaked Secrets", "Main Branch Synced", "Clean State"],
            "cta_label": "Verify Git Health"
        },
        {
            "id": "ops_09",
            "title": "🔄 Failed Background Task Dead-Letter Queue Flush",
            "category": "Queue Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Dead-Letter Queue (DLQ) Triage & Auto-Retry",
            "badge": "QUEUE RECOVERY",
            "gradient": "linear-gradient(135deg, #c2410c 0%, #7c2d12 100%)",
            "target_audience": "Task Dispatcher",
            "description": "Reviews tasks that failed during network dropouts, parses error stack traces, and re-executes cleanly.",
            "body": (
                "Dead-Letter Queue Inspection:\n"
                "• Tasks Evaluated: 3 queued social broadcasts.\n"
                "• Root Cause: Transient HTTP 503 from external social gateway.\n"
                "• Retry Result: 3/3 dispatched successfully on retry cycle 2.\n"
                "• DLQ Buffer: 0 pending items."
            ),
            "callouts": ["3/3 Tasks Recovered", "Zero Dropped Payloads", "Clean DLQ Buffer"],
            "cta_label": "Flush & Retry DLQ"
        },
        {
            "id": "ops_10",
            "title": "🔍 Secret Key & .env Leakage Audit Across Workspace",
            "category": "Secrets Ops",
            "urgency": "Urgent",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Workspace Secret Scanning & Credential Shield",
            "badge": "SECRETS AUDIT",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #312e81 100%)",
            "target_audience": "Full Codebase Root",
            "description": "Scans all 400+ repository files for accidentally hardcoded tokens, passwords, or private encryption keys.",
            "body": (
                "Credential Hygiene Scan:\n"
                "• Files Scanned: 412 Python, JS, HTML, JSON files.\n"
                "• High Entropy Strings Inspected: 1,840\n"
                "• Findings: All production tokens strictly loaded via environment variables (.env).\n"
                "• Verification: .gitignore properly protects sensitive data files."
            ),
            "callouts": ["412 Files Verified", "Zero Hardcoded Secrets", "Strict .gitignore Shield"],
            "cta_label": "Scan for Secrets"
        },
        {
            "id": "ops_11",
            "title": "⚡ High CPU / Thread Starvation Self-Healing Check",
            "category": "Performance Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "CPU Load Balancing & Event Loop Liveness",
            "badge": "PERFORMANCE SHIELD",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #075985 100%)",
            "target_audience": "FastAPI Async Event Loop",
            "description": "Measures asyncio event loop lag to guarantee sub-millisecond response times for client API requests.",
            "body": (
                "Event Loop Liveness Report:\n"
                "• Event Loop Lag: 0.84 milliseconds (Standard: <10ms).\n"
                "• CPU Load: 4.2% across 8 cores.\n"
                "• Worker Status: Uvicorn master process fully responsive.\n"
                "• Starvation Risk: Zero."
            ),
            "callouts": ["0.84ms Loop Latency", "CPU Load: 4.2%", "Zero Thread Starvation"],
            "cta_label": "Check Event Loop Liveness"
        },
        {
            "id": "ops_12",
            "title": "📦 Python Dependency Vulnerability Sweep (pip-audit)",
            "category": "Dependency Ops",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Third-Party Package Security & CVE Verification",
            "badge": "VULNERABILITY AUDIT",
            "gradient": "linear-gradient(135deg, #15803d 0%, #14532d 100%)",
            "target_audience": "Virtualenv Environment",
            "description": "Scans installed packages against official PyPI vulnerability database for known CVEs.",
            "body": (
                "Dependency Security Scan:\n"
                "• Packages Evaluated: 34 installed libraries (FastAPI, Uvicorn, Pydantic, etc.).\n"
                "• Vulnerabilities Found: 0 Known Vulnerabilities.\n"
                "• Supply Chain Health: 100% Verified Clean."
            ),
            "callouts": ["34 Packages Audited", "0 Known CVEs", "Supply Chain Verified"],
            "cta_label": "Run Dependency Audit"
        },
        {
            "id": "ops_13",
            "title": "⏱️ API Latency & 99th Percentile SLA Benchmark",
            "category": "SLA Benchmark",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "End-to-End Endpoint Latency Benchmark",
            "badge": "LATENCY BENCHMARK",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #1d4ed8 100%)",
            "target_audience": "Production API Routes",
            "description": "Executes local benchmark across core endpoints (/api/status, /api/tasks, /api/finance/invoices).",
            "body": (
                "Benchmark Telemetry Results:\n"
                "• /api/status: 2.1 ms (p99: 4.8 ms)\n"
                "• /api/finance/receivables: 6.4 ms (p99: 11.2 ms)\n"
                "• /api/tasks/generate-sample: 18.2 ms (p99: 28.0 ms)\n"
                "• SLA Compliance: 100% compliant with sub-100ms contract."
            ),
            "callouts": ["Sub-20ms Average Response", "p99 < 30ms", "Enterprise Grade"],
            "cta_label": "Run Latency Benchmark"
        },
        {
            "id": "ops_14",
            "title": "🔗 Webhook HMAC Signature Security Validation",
            "category": "Webhook Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Webhook Tamper-Proof Cryptographic Verification",
            "badge": "HMAC VALIDATION",
            "gradient": "linear-gradient(135deg, #4338ca 0%, #312e81 100%)",
            "target_audience": "Payment & Messaging Gateways",
            "description": "Tests incoming webhook parsers with synthetic replay packets to ensure forged payloads are strictly rejected.",
            "body": (
                "Webhook Defense Simulation:\n"
                "• Injected Test Payload with invalid HMAC SHA-256 header.\n"
                "• Gateway Response: HTTP 401 Unauthorized (Blocked in 1.2ms).\n"
                "• Replay Shield: Dropped duplicate timestamp token.\n"
                "• Result: Zero spoofing vulnerability."
            ),
            "callouts": ["Forged Payloads Blocked", "Replay Protection Verified", "Instant HTTP 401 Rejection"],
            "cta_label": "Test Webhook Shields"
        },
        {
            "id": "ops_15",
            "title": "🧹 Cache Pruning & Expired Session Cleanse",
            "category": "Cache Ops",
            "urgency": "Low",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Session Store Maintenance & Memory Cleanse",
            "badge": "CACHE CLEANSE",
            "gradient": "linear-gradient(135deg, #64748b 0%, #475569 100%)",
            "target_audience": "In-Memory Session Store",
            "description": "Purges expired auth tokens and temporary CSRF nonces to prevent state accumulation.",
            "body": (
                "Session Maintenance Manifest:\n"
                "• Scanned Active Session Store: 18 entries.\n"
                "• Expired Sessions Purged: 6 (>24h since activity).\n"
                "• Nonces Invalidated: 12 consumed payment nonces.\n"
                "• Memory Footprint: Minimalized."
            ),
            "callouts": ["Expired Tokens Flushed", "CSRF Nonces Cleared", "Zero State Bloat"],
            "cta_label": "Prune Expired Sessions"
        },
        {
            "id": "ops_16",
            "title": "🗄️ Database Connection Pool Leak Detection",
            "category": "Database Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "SQLite Cursor & Connection Leak Audit",
            "badge": "DB POOL AUDIT",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "SQLite Database Connector",
            "description": "Audits database connection context managers ensuring zero lingering locks or unclosed file handles.",
            "body": (
                "Connection Pool Audit:\n"
                "• Open Connections: 1 active read-write pool.\n"
                "• Unclosed Cursors: 0\n"
                "• Lock Timeouts Last 24h: 0\n"
                "• Status: Clean transactional boundaries maintained."
            ),
            "callouts": ["Zero Leaked Cursors", "Zero Lock Timeouts", "100% Context Clean"],
            "cta_label": "Audit Connection Pool"
        },
        {
            "id": "ops_17",
            "title": "📜 Log Rotation & Gzip Compression Manifest",
            "category": "Log Ops",
            "urgency": "Low",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Log File Archival & Gzip Compression",
            "badge": "LOG ROTATION",
            "gradient": "linear-gradient(135deg, #334155 0%, #1e293b 100%)",
            "target_audience": "logs/ Directory",
            "description": "Rotates application server logs exceeding 10MB into compressed archives with retention limits.",
            "body": (
                "Log Rotation Execution:\n"
                "• Rotated: server.log (12.4 MB) -> server_20260927.log.gz (840 KB).\n"
                "• Active Log: Created fresh server.log with standard header.\n"
                "• Retention Enforcement: Kept last 30 rotated days; deleted logs >60 days old."
            ),
            "callouts": ["93% Compression Ratio", "Active Log Fresh", "Automated Retention"],
            "cta_label": "Rotate Application Logs"
        },
        {
            "id": "ops_18",
            "title": "🌐 Multi-Region DNS Resolution & Uptime Ping",
            "category": "Network Ops",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Global DNS Propagation & Edge Uptime Audit",
            "badge": "UPTIME PING",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Public DNS Nameservers",
            "description": "Pings primary portal from 4 simulated regions (Mauritius, London, Frankfurt, Singapore) to verify reachability.",
            "body": (
                "Global Edge Uptime Report:\n"
                "• Port Louis (MU): 12 ms latency (100% reachability)\n"
                "• London (UK): 138 ms latency (100% reachability)\n"
                "• Frankfurt (DE): 142 ms latency (100% reachability)\n"
                "• Singapore (SG): 84 ms latency (100% reachability)\n"
                "• Global Health: All nodes reporting green."
            ),
            "callouts": ["100% Reachability", "Port Louis: 12ms", "Global Edge Validated"],
            "cta_label": "Execute Global Uptime Ping"
        },
        {
            "id": "ops_19",
            "title": "🤖 Autonomous Daemon Autopilot Heartbeat Verification",
            "category": "Autopilot Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "24/7 Autopilot Loop Status & Heartbeat Liveness",
            "badge": "HEARTBEAT AUDIT",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Core Autopilot Background Loop",
            "description": "Verifies that the autonomous overnight daemon is firing its scheduled 30-minute sweeps continuously.",
            "body": (
                "Autopilot Heartbeat Telemetry:\n"
                "• Daemon State: ACTIVE & AUTONOMOUS\n"
                "• Last Heartbeat: 4 minutes ago\n"
                "• Cycles Completed Last 24h: 48/48 (100% on schedule)\n"
                "• Next Execution Window: In 26 minutes."
            ),
            "callouts": ["48/48 Cycles Completed", "Heartbeat Healthy", "Zero Missed Sweeps"],
            "cta_label": "Verify Daemon Heartbeat"
        },
        {
            "id": "ops_20",
            "title": "🔥 Disaster Recovery Simulation & Cold-Start Dry Run",
            "category": "Disaster Recovery",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Disaster Recovery Dry Run: 3-Second Cold Restore",
            "badge": "DR SIMULATION",
            "gradient": "linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%)",
            "target_audience": "Staging Sandbox",
            "description": "Restores the latest backup into a temporary SQLite database to verify data restorability and schema validity.",
            "body": (
                "Disaster Recovery Simulation:\n"
                "• Target Backup: backups/snapshot_latest.tar.gz\n"
                "• Extracted to isolated scratch/ directory.\n"
                "• SQLite Schema Verification: `PRAGMA integrity_check` -> ok.\n"
                "• Restored Records: 124 memory items, 14 products, 18 invoices.\n"
                "• Cold-Start Recovery Time: 2.8 seconds."
            ),
            "callouts": ["2.8s Cold-Start Time", "PRAGMA Check: OK", "100% Data Fidelity"],
            "cta_label": "Run Disaster Recovery Test"
        },
        {
            "id": "ops_21",
            "title": "🔒 Sovereign Directory Access & File Permission Lockdown",
            "category": "Permissions Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Filesystem ACL & Directory Isolation Enforcement",
            "badge": "ACL LOCKDOWN",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Local Workspace Directories",
            "description": "Verifies that core data files cannot be read or overwritten by unauthenticated local accounts.",
            "body": (
                "Filesystem Security Audit:\n"
                "• Evaluated: data/, memory/, backups/, .env\n"
                "• ACL Check: Restricted to current user (Deven Pawaray) and service daemon.\n"
                "• World-Writable Paths: 0 found.\n"
                "• Sandbox Integrity: Enforced."
            ),
            "callouts": ["Zero World-Writable Files", "User ACL Restricted", "Sovereign Isolation"],
            "cta_label": "Enforce File Permissions"
        },
        {
            "id": "ops_22",
            "title": "📱 WhatsApp Gateway Daemon Socket Reconnection",
            "category": "Messaging Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "WhatsApp Gateway WebSocket Health & Auto-Heal",
            "badge": "GATEWAY HEALTH",
            "gradient": "linear-gradient(135deg, #059669 0%, #047857 100%)",
            "target_audience": "WhatsApp Socket Gateway",
            "description": "Tests connectivity to WhatsApp API daemon, resetting stale keep-alive sessions before dropouts occur.",
            "body": (
                "WhatsApp Gateway Probe:\n"
                "• Gateway Socket: CONNECTED\n"
                "• Dispatch Line: +230 58169420\n"
                "• Ping Latency: 180 ms\n"
                "• Status: Clean message buffer ready for outbound dispatches."
            ),
            "callouts": ["Socket Connected", "+230 58169420 Ready", "Zero Inbound Queue Lag"],
            "cta_label": "Test WhatsApp Gateway"
        },
        {
            "id": "ops_23",
            "title": "💳 PayPal & MCB Juice Webhook Listener Health Check",
            "category": "Payment Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Payment Gateway Listener & Webhook Probe",
            "badge": "PAYMENT WEBHOOKS",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "FastAPI Payment Route Handlers",
            "description": "Verifies that IPN listeners and Juice verification endpoints respond to health pings within 5 milliseconds.",
            "body": (
                "Payment Listener Health Check:\n"
                "• Route: /api/finance/payment-link -> 200 OK (1.8 ms)\n"
                "• Route: /api/finance/invoices/{id}/verify-juice -> 200 OK (2.4 ms)\n"
                "• Route: /api/paypal/webhook -> 200 OK (1.9 ms)\n"
                "• Ready to capture and settle live transactions."
            ),
            "callouts": ["100% Listener Uptime", "< 3ms Latency", "Settlement Rails Active"],
            "cta_label": "Verify Payment Listeners"
        },
        {
            "id": "ops_24",
            "title": "☕ Automated Morning Error Log Summary for Executive Standup",
            "category": "Reporting Ops",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Daily Operations Intelligence & Error Log Digest",
            "badge": "EXECUTIVE DIGEST",
            "gradient": "linear-gradient(135deg, #475569 0%, #1e293b 100%)",
            "target_audience": "Sir Deven Pawaray",
            "description": "Parses the overnight error log, deduplicating warnings and presenting a clean 3-bullet morning briefing.",
            "body": (
                "Morning Operations Standup Digest:\n"
                "• Total Requests Processed (Last 24h): 4,892\n"
                "• Critical Errors: 0\n"
                "• Minor Warnings: 2 (handled retry on external DNS lookup)\n"
                "• System Uptime: 99.98%\n"
                "• Conclusion: Fleet fully primed for peak business hours."
            ),
            "callouts": ["Zero Critical Errors", "4,892 Requests Handled", "99.98% Uptime"],
            "cta_label": "Compile Morning Digest"
        },
        {
            "id": "ops_25",
            "title": "🛡️ Host OS Kernel & Patch Status Vulnerability Flagging",
            "category": "OS Ops",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Host Operating System Security Baseline Audit",
            "badge": "HOST SECURITY",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Host Windows / Linux Environment",
            "description": "Inspects system patch levels, firewall rules, and open ports to guarantee zero unauthorized listen ports.",
            "body": (
                "Host Security Baseline Audit:\n"
                "• Listening Ports: 8000 (FastAPI), 443 (HTTPS via Tunnel). Zero stray ports.\n"
                "• Firewall State: Windows Defender Active with strict ingress rules.\n"
                "• Memory Integrity Shield: Enabled.\n"
                "• Compliance Status: Hardened."
            ),
            "callouts": ["Strict Listening Ports Only", "Ingress Firewall Active", "Host Hardened"],
            "cta_label": "Audit Host Baseline"
        }
    ],

    # ═════════════════════════════════════════════════════════════════════════
    # 3. COMMERCE & TREASURY USER TYPE (25 Daily Real-World Scenarios)
    # ═════════════════════════════════════════════════════════════════════════
    "commerce": [
        {
            "id": "commerce_01",
            "title": "🛒 1-Click $1 Python Script Compilation & Store Publishing",
            "category": "Digital Store",
            "urgency": "High",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Publish New $1 Standalone Python Utility to Live Catalog",
            "badge": "PRODUCT FACTORY",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Digital Vending Machine Customers",
            "description": "Compiles a tested, standalone Python tool into products/, updates custom_catalog.json, and makes it available for 1-click checkout.",
            "body": (
                "New Digital Product Staging:\n"
                "• Product: Nexus™ Bulk PDF Invoicer\n"
                "• Architecture: Standalone single-file Python CLI script\n"
                "• Pricing: $1.00 USD / Rs 45 MUR (1-click PayPal & MCB Juice)\n"
                "• Rights: Full commercial usage rights included\n"
                "Ready to compile, save into products/, and publish live to /store."
            ),
            "callouts": ["$1.00 USD / Rs 45 MUR", "1-Second Instant Delivery", "100% Gross Margin"],
            "cta_label": "Publish to Live Store"
        },
        {
            "id": "commerce_02",
            "title": "📱 MCB Juice Instant Transfer Verification & Settle",
            "category": "Settlement",
            "urgency": "Urgent",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Reconcile MCB Juice Transfer & Generate Stamped Receipt",
            "badge": "JUICE RECONCILIATION",
            "gradient": "linear-gradient(135deg, #d97706 0%, #78350f 100%)",
            "target_audience": "Mauritius Client Payments",
            "description": "Validates client MCB Juice transaction reference number against replay shield and automatically marks invoice as SETTLED.",
            "body": (
                "Processing MCB Juice Reconciliation:\n"
                "• Client Transfer Ref: JCE94120418\n"
                "• Beneficiary: Deven Pawaray (+230 58169420)\n"
                "• Amount: Rs 45,000 MUR\n"
                "• Anti-Replay Verification: PASSED (New unique transaction code)\n"
                "• Action: Mark invoice COMPLETED, generate official cryptographic tax receipt."
            ),
            "callouts": ["Instant Verification", "Replay Shield Passed", "Official MRA Receipt"],
            "cta_label": "Reconcile Juice Payment"
        },
        {
            "id": "commerce_03",
            "title": "💳 PayPal 1-Click Invoice Generation for International Client",
            "category": "Invoicing",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Generate Instant PayPal Payment Link ($249.00 USD)",
            "badge": "PAYPAL INVOICE",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "US/UK/EU Commercial License Buyers",
            "description": "Generates a cryptographically signed PayPal invoice URL with pre-filled amounts and instant webhook fulfillment.",
            "body": (
                "PayPal Commercial Invoice Manifest:\n"
                "• Client: DevAgency UK Ltd (alex@devagency.co.uk)\n"
                "• Product: Nexus Autonomous Fleet Commercial Lifetime License\n"
                "• Amount: $249.00 USD\n"
                "• Webhook Action: Auto-dispatch full source code zip upon payment capture."
            ),
            "callouts": ["1-Click Checkout", "Instant Automated Delivery", "$249.00 USD Settlement"],
            "cta_label": "Generate PayPal Link"
        },
        {
            "id": "commerce_04",
            "title": "🧾 MRA-Compliant Tax Receipt Generation (Section 50L CSR)",
            "category": "Tax & Compliance",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Issue MRA Section 50L Tax Deductible Official Receipt",
            "badge": "MRA TAX RECEIPT",
            "gradient": "linear-gradient(135deg, #15803d 0%, #166534 100%)",
            "target_audience": "Corporate CSR & Donation Retainers",
            "description": "Mints an official printable PDF receipt with Mauritius Revenue Authority tax deduction accreditation details.",
            "body": (
                "Generating Official Tax Receipt:\n"
                "• Recipient: Corporate CSR Donor\n"
                "• Donation Target: Enn Rev Enn Sourir (Child Medical Treatment Fund)\n"
                "• Amount: Rs 25,000 MUR\n"
                "• Tax Benefit: 15% MRA Section 50L Deduction Qualified\n"
                "• Cryptographic Integrity Seal: Applied."
            ),
            "callouts": ["15% MRA Tax Deduction", "Section 50L Compliant", "Printable PDF Receipt"],
            "cta_label": "Mint MRA Tax Receipt"
        },
        {
            "id": "commerce_05",
            "title": "⛓️ Base L2 Blockchain Treasury Sweep & USDC Verification",
            "category": "Treasury",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Base L2 Sovereign Vault Audit & USDC Sweep",
            "badge": "BLOCKCHAIN TREASURY",
            "gradient": "linear-gradient(135deg, #4338ca 0%, #312e81 100%)",
            "target_audience": "Nexus Sovereign Vault",
            "description": "Queries Base L2 smart contract vault for incoming USDC payments and sweeps them to cold multisig storage.",
            "body": (
                "Base L2 Treasury Synchronizer:\n"
                "• Network: Base Mainnet (Chain ID 8453)\n"
                "• Vault Balance: 1,420.50 USDC\n"
                "• Gas Fee: $0.002 USD\n"
                "• Sweep Status: Confirmed and cryptographically verified on-chain."
            ),
            "callouts": ["Base L2 Mainnet", "Gas Fee: < $0.01", "Verifiable On-Chain"],
            "cta_label": "Sync Base Treasury"
        },
        {
            "id": "commerce_06",
            "title": "🏷️ Dynamic Catalog Pricing Adjustment ($1.00 USD / Rs 45 MUR)",
            "category": "Catalog Ops",
            "urgency": "Low",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Catalog Real-Time FX Pricing Update",
            "badge": "PRICING SYNC",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #334155 100%)",
            "target_audience": "Store Frontend",
            "description": "Synchronizes store pricing across 14 micro-tools based on live USD/MUR exchange rates to maintain exact $1 parity.",
            "body": (
                "Dynamic Pricing Synchronization:\n"
                "• Live FX Rate: 1 USD = 45.20 MUR\n"
                "• Updated: 14 tools in products/custom_catalog.json\n"
                "• Domestic Price: Rs 45.00 MUR (rounded for clean MCB Juice payments)\n"
                "• International Price: $1.00 USD."
            ),
            "callouts": ["14 Tools Updated", "Clean Rs 45 MUR Parity", "Instant Store Sync"],
            "cta_label": "Update Store Pricing"
        },
        {
            "id": "commerce_07",
            "title": "🏃 Abandoned Cart WhatsApp Recovery Trigger",
            "category": "Conversion",
            "urgency": "High",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Recover Abandoned Tool Checkout via WhatsApp",
            "badge": "CART RECOVERY",
            "gradient": "linear-gradient(135deg, #059669 0%, #10b981 100%)",
            "target_audience": "Shoppers who entered phone but didn't pay",
            "description": "Sends a friendly 1-click WhatsApp message with direct Juice instructions to recover dropped checkouts.",
            "body": (
                "Bonjour 👋,\n\n"
                "Nous avons remarqué que vous avez initié l'achat de *Nexus™ Instant Invoicer* sans finaliser votre commande.\n\n"
                "Votre outil est prêt ! Pour finaliser en 1 clic par Juice :\n"
                "📱 Envoyez *Rs 45* au *58169420* (Deven Pawaray).\n"
                "Votre lien de téléchargement s'activera immédiatement. Besoin d'aide ? Répondez à ce message !"
            ),
            "callouts": ["38% Recovery Rate", "Frictionless 1-Click Juice", "Automated Timing"],
            "cta_label": "Send Cart Recovery"
        },
        {
            "id": "commerce_08",
            "title": "📦 Monthly Retainer Batch Invoicing (Rs 45,000 MUR Accounts)",
            "category": "Invoicing",
            "urgency": "High",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Automated 1st-of-Month B2B Retainer Invoicing Batch",
            "badge": "BATCH INVOICING",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #1e40af 100%)",
            "target_audience": "All Active Monthly Retainer Clients",
            "description": "Generates, registers in SQLite ledger, and dispatches monthly invoices to all active B2B retainer accounts simultaneously.",
            "body": (
                "Batch Invoicing Execution:\n"
                "• Client Accounts: 3 Active Enterprise Retainers\n"
                "• Invoice Amount: Rs 45,000 MUR each (Total: Rs 135,000 MUR)\n"
                "• Payment Rails: MCB Wire / Juice (+230 58169420)\n"
                "• Due Date: Net 15\n"
                "• Dispatch: Automated PDF generation and WhatsApp delivery."
            ),
            "callouts": ["Rs 135,000 MUR Total Value", "Net 15 Stamped", "Batch Automated"],
            "cta_label": "Execute Batch Invoicing"
        },
        {
            "id": "commerce_09",
            "title": "📜 High-Ticket Commercial Licensing Agreement Issuance",
            "category": "Licensing",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Commercial Enterprise Source License Agreement ($1,000 USD)",
            "badge": "ENTERPRISE LICENSE",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Enterprise White-Label Customers",
            "description": "Mints a non-exclusive, perpetual commercial source license certificate granting full white-label redistribution rights.",
            "body": (
                "Commercial License Staging:\n"
                "• Licensee: Sovereign Tech Ltd\n"
                "• Grant: Perpetual White-Label Deployment for 18 Autonomous Agents\n"
                "• Consideration: $1,000 USD (or Rs 45,000 MUR)\n"
                "• Restrictions: Zero resale of source as an unbundled competitor\n"
                "• Cryptographic Seal: SHA-256 certificate stamped."
            ),
            "callouts": ["Full White-Label Rights", "Perpetual Validity", "Cryptographic Protection"],
            "cta_label": "Issue Enterprise License"
        },
        {
            "id": "commerce_10",
            "title": "💸 Instant Refund & Credit Memo Issuance with Anti-Replay",
            "category": "Disputes & Refunds",
            "urgency": "High",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Customer Satisfaction Refund & Cryptographic Credit Memo",
            "badge": "REFUND SETTLEMENT",
            "gradient": "linear-gradient(135deg, #d97706 0%, #92400e 100%)",
            "target_audience": "Dissatisfied Store Customer",
            "description": "Issues an immediate 100% money-back refund on a $1 tool or invoice, invalidating the license key cleanly.",
            "body": (
                "Processing Credit Memo / Refund:\n"
                "• Order Ref: ORD-9182 ($1.00 USD / Rs 45 MUR)\n"
                "• Reason: Customer requested alternate tool format\n"
                "• Action: Reversal processed via original rail (MCB Juice / PayPal)\n"
                "• Ledger: License key revoked; ledger balanced with zero fee penalty."
            ),
            "callouts": ["100% Money-Back Honor", "License Cleanly Revoked", "Zero Chargeback Risk"],
            "cta_label": "Process Clean Refund"
        },
        {
            "id": "commerce_11",
            "title": "💱 Real-Time Foreign Exchange (FX) Reconciliation",
            "category": "Treasury",
            "urgency": "Low",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Multi-Currency Balance Sheet Revaluation (USD, MUR, EUR)",
            "badge": "FX REVALUATION",
            "gradient": "linear-gradient(135deg, #475569 0%, #1e293b 100%)",
            "target_audience": "Internal Financial Ledger",
            "description": "Revalues cash reserves held in MUR (MCB Bank) and USD (PayPal & Base L2) into unified MUR reporting.",
            "body": (
                "Treasury Revaluation Summary:\n"
                "• Cash in MUR (MCB Juice / Current Acc): Rs 64,200.00 MUR\n"
                "• Foreign Assets (USD): $1,420.00 USD @ 45.20 = Rs 64,184.00 MUR\n"
                "• Combined Liquid Treasury: Rs 128,384.00 MUR\n"
                "• Runway: Infinite (Zero cloud infrastructure debt)."
            ),
            "callouts": ["Unified MUR Balance Sheet", "Rs 128,384 Liquid", "Zero Cloud Debt"],
            "cta_label": "Run FX Revaluation"
        },
        {
            "id": "commerce_12",
            "title": "🤝 Affiliate Referral Commission Calculation & Payout",
            "category": "Affiliate Ops",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Partner Referral Payout Slip Generation (20% Cut)",
            "badge": "AFFILIATE PAYOUT",
            "gradient": "linear-gradient(135deg, #059669 0%, #065f46 100%)",
            "target_audience": "Registered Agency Partners",
            "description": "Calculates monthly affiliate earnings from closed client retainers and formats instant Juice transfer instructions.",
            "body": (
                "Affiliate Settlement Manifest:\n"
                "• Partner: Cybercity Digital Agency\n"
                "• Referred Client: HealthClinic Grand Baie (Rs 45,000 MUR Retainer)\n"
                "• Commission Rate: 20% Guaranteed\n"
                "• Payout Amount: Rs 9,000.00 MUR\n"
                "• Delivery: Instant MCB Juice Transfer."
            ),
            "callouts": ["20% Partner Cut", "Rs 9,000 MUR Settled", "Builds Partner Loyalty"],
            "cta_label": "Generate Payout Slip"
        },
        {
            "id": "commerce_13",
            "title": "🔑 Cryptographic License Key Stamping & Validation",
            "category": "Digital Rights",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "HMAC-SHA256 Software License Stamping",
            "badge": "LICENSE KEY MINT",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #1e3a8a 100%)",
            "target_audience": "Software Buyers",
            "description": "Generates a verifiable offline license key tied to customer email and hardware fingerprint.",
            "body": (
                "License Stamping Engine:\n"
                "• User: client@mauritiustech.mu\n"
                "• Product: Nexus SEO Keyword SERP Tracker\n"
                "• License Signature: `NX-2026-8F92-A1C4-MUR`\n"
                "• Verification: 100% offline mathematical validation (No phone-home DRM)."
            ),
            "callouts": ["100% Offline DRM", "Cryptographically Signed", "Hardware Sovereign"],
            "cta_label": "Mint License Key"
        },
        {
            "id": "commerce_14",
            "title": "⚠️ Recurring Subscription Failure Alert & Dunning Sequence",
            "category": "Dunning",
            "urgency": "High",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Payment Method Expiry & Friendly Retainer Dunning",
            "badge": "DUNNING NOTICE",
            "gradient": "linear-gradient(135deg, #c2410c 0%, #7c2d12 100%)",
            "target_audience": "Retainer Client with Expired Card",
            "description": "Diplomatic reminder that a card charge failed, providing alternative 1-click MCB Juice or bank transfer rails.",
            "body": (
                "Dear [Client Finance Lead],\n\n"
                "Our automated billing system attempted to process your monthly retainer invoice (#INV-3829), but the bank returned a 'Card Expired' notice.\n\n"
                "To prevent any interruption to your 24/7 AI fleet, you can settle instantly via:\n"
                "1. MCB Juice (+230 58169420, Ref: INV-3829)\n"
                "2. Direct Bank Wire (MCB Account: 000443260370)\n\n"
                "Thank you for keeping your account in good standing!"
            ),
            "callouts": ["Zero Disruption Warning", "Instant Alternative Rails", "Respectful Tone"],
            "cta_label": "Send Dunning Notice"
        },
        {
            "id": "commerce_15",
            "title": "📊 Daily Cash Flow & Liquidity Report for Sir Deven",
            "category": "Reporting",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Executive Morning Cash Flow & Liquidity Intelligence",
            "badge": "CASH FLOW REPORT",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Sir Deven Pawaray",
            "description": "Summarizes all inflows, pending receivables, and net profit margins across all payment channels over the last 24h.",
            "body": (
                "Daily Cash Flow Telemetry:\n"
                "• Settled Inflow (Last 24h): Rs 45,045 MUR\n"
                "  - 1x Retainer Settlement: Rs 45,000 MUR\n"
                "  - 1x Digital Tool Sale: Rs 45 MUR ($1.00)\n"
                "• Outstanding Receivables: Rs 0.00 MUR (100% collected!)\n"
                "• Net Operating Margin: 98.4%\n"
                "• Progress to Rs 150k MUR Target: 30.0% Complete."
            ),
            "callouts": ["Rs 45,045 Settled", "98.4% Operating Margin", "Zero Bad Debt"],
            "cta_label": "Generate Cash Flow Report"
        },
        {
            "id": "commerce_16",
            "title": "🚫 Fraudulent Juice Reference Detection & Blacklist",
            "category": "Fraud Prevention",
            "urgency": "Urgent",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Anti-Fraud Alert: Counterfeit Transfer Reference Blocked",
            "badge": "FRAUD SHIELD",
            "gradient": "linear-gradient(135deg, #b91c1c 0%, #7f1d1d 100%)",
            "target_audience": "Security Watchdog",
            "description": "Catches spoofed or re-submitted Juice transaction codes and locks out the submitting IP automatically.",
            "body": (
                "Anti-Fraud Watchdog Action:\n"
                "• Submitted Ref: JCE94120418\n"
                "• Analysis: Match found in historical settlement ledger (Used on 2026-09-18).\n"
                "• Attempted Exploit: Replay attack on $1 download portal.\n"
                "• Defense: Blocked download token, recorded incident, blacklisted IP."
            ),
            "callouts": ["Replay Attack Neutralized", "Zero Inventory Loss", "Automated IP Blacklist"],
            "cta_label": "Audit Fraud Incident"
        },
        {
            "id": "commerce_17",
            "title": "🎟️ Promo Code & Launch Discount Voucher Campaign",
            "category": "Promotions",
            "urgency": "Low",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Create Launch Promo Campaign (50% Off Retainer Setup)",
            "badge": "PROMO CAMPAIGN",
            "gradient": "linear-gradient(135deg, #7c3aed 0%, #4338ca 100%)",
            "target_audience": "Local SME Prospects",
            "description": "Mints a time-limited promotional voucher code with usage caps for Mauritius business networking events.",
            "body": (
                "Promotional Campaign Configuration:\n"
                "• Code: `NEXUS-EBENE-2026`\n"
                "• Benefit: 50% discount on initial AI fleet setup (Rs 7,500 MUR value)\n"
                "• Cap: First 5 Mauritius companies only\n"
                "• Expiration: 14 days\n"
                "• Status: Active in payment checkout controller."
            ),
            "callouts": ["5-Company Exclusive Cap", "Rs 7,500 MUR Incentive", "14-Day Expiration"],
            "cta_label": "Activate Promo Campaign"
        },
        {
            "id": "commerce_18",
            "title": "📋 Custom Enterprise Quotation Builder with Scope Breakdown",
            "category": "Quotations",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Formal Enterprise Quote: Turnkey Autonomous Operations",
            "badge": "ENTERPRISE QUOTE",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Enterprise Prospect",
            "description": "Compiles a transparent itemized quotation including setup, hosting, security safeguards, and training.",
            "body": (
                "Quotation #QT-2026-44:\n"
                "• Client: Mauritius Hospitality Holdings\n"
                "• Scope: VillaFlow WhatsApp AI Concierge + Medical Emergency Protocol\n"
                "• Implementation: Rs 25,000 MUR (one-time)\n"
                "• Monthly Fleet Maintenance: Rs 35,000 MUR/mo\n"
                "• Total Commitment (Year 1): Rs 445,000 MUR\n"
                "• Validity: 30 days."
            ),
            "callouts": ["Itemized Scope Breakdown", "30-Day Rate Lock", "Enterprise Specification"],
            "cta_label": "Generate Formal Quote"
        },
        {
            "id": "commerce_19",
            "title": "📦 Digital Product Superpack Zip Bundling & Checksum",
            "category": "Fulfillment",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Rebuild & Checksum Nexus Dev Superpack (All 14 Tools)",
            "badge": "SUPERPACK BUNDLE",
            "gradient": "linear-gradient(135deg, #059669 0%, #15803d 100%)",
            "target_audience": "Developer Superpack Buyers",
            "description": "Packages all 14 standalone micro-tools into products/nexus_dev_superpack.zip and generates SHA-256 validation stamp.",
            "body": (
                "Superpack Rebuild Manifest:\n"
                "• Included Tools: 14 single-file Python scripts\n"
                "• Extras: Complete documentation, sample datasets, commercial license\n"
                "• Compression: Zip Deflate (4.3 MB)\n"
                "• SHA-256 Checksum: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`\n"
                "• Ready for instant $5.00 delivery."
            ),
            "callouts": ["14 Tools Included", "SHA-256 Verified", "Instant Fulfillment Ready"],
            "cta_label": "Rebuild Superpack"
        },
        {
            "id": "commerce_20",
            "title": "📁 Expense Categorization & Receipt Archival for Tax Season",
            "category": "Bookkeeping",
            "urgency": "Low",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Automated Bookkeeping & MRA Tax Ledger Archival",
            "badge": "EXPENSE AUDIT",
            "gradient": "linear-gradient(135deg, #334155 0%, #1e293b 100%)",
            "target_audience": "Company Accountant",
            "description": "Logs all operational expenses (domain renewals, hardware parts) with attached PDF vouchers ready for annual filing.",
            "body": (
                "Expense Classification Ledger:\n"
                "• Period: Current Fiscal Quarter\n"
                "• Total Operating Expenses: Rs 4,820 MUR ($106 USD)\n"
                "• Categories: Domain Infrastructure (Rs 1,200), Server Hardware (Rs 3,620)\n"
                "• Cloud SaaS Subscriptions: Rs 0 (100% Sovereign!)\n"
                "• MRA Tax Deductibility: Verified."
            ),
            "callouts": ["Zero Cloud SaaS Overhead", "Organized MRA Categories", "Tax Ready"],
            "cta_label": "Archive Expense Records"
        },
        {
            "id": "commerce_21",
            "title": "🤝 Client Deposit Settle & Escrow Release Acknowledgment",
            "category": "Milestones",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Milestone 1 Acceptance & Deposit Clearance Confirmation",
            "badge": "ESCROW RELEASE",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Custom Enterprise Project Client",
            "description": "Confirms receipt of 50% mobilization deposit and unlocks sprint development environments.",
            "body": (
                "Milestone 1 Settlement Notice:\n"
                "• Project: Turnkey Hospital Portal Deployment\n"
                "• Mobilization Deposit: Rs 22,500 MUR (50% of Rs 45,000 contract)\n"
                "• Status: Funds cleared via MCB Wire\n"
                "• Action: Sprint 1 codebase initialized; staging URL shared with client."
            ),
            "callouts": ["50% Mobilization Cleared", "Sprint 1 Unlocked", "Staging Provisioned"],
            "cta_label": "Send Escrow Clearance"
        },
        {
            "id": "commerce_22",
            "title": "⚠️ Overdue Invoice Escalation Level 2 with Interest Notice",
            "category": "Collections",
            "urgency": "High",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Formal Overdue Settlement Notice: Level 2 Notice",
            "badge": "COLLECTIONS LEVEL 2",
            "gradient": "linear-gradient(135deg, #c2410c 0%, #7c2d12 100%)",
            "target_audience": "Accounts Payable (30+ Days Overdue)",
            "description": "Stern, legally compliant notification regarding unpaid commercial balances nearing suspension threshold.",
            "body": (
                "Attention: Head of Finance / Accounts Payable\n\n"
                "Re: Unsettled Invoice #INV-2901 (Rs 45,000 MUR — 32 Days Past Due)\n\n"
                "Despite multiple courtesy reminders, this balance remains outstanding. "
                "Per Section 4.2 of our commercial agreement, accounts exceeding 35 days overdue are subject to temporary automated agent suspension.\n\n"
                "Please settle via MCB Juice (+230 58169420) or wire by tomorrow 17:00 MUT to avoid service disruption."
            ),
            "callouts": ["Legally Compliant Notice", "Service Suspension Shield", "Immediate Wire/Juice Rails"],
            "cta_label": "Send Level 2 Notice"
        },
        {
            "id": "commerce_23",
            "title": "🖥️ Physical On-Premise AI Appliance Hardware Invoicing",
            "category": "Hardware Sales",
            "urgency": "Standard",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Hardware Invoice: Nexus Sovereign Local AI Appliance (Mini PC)",
            "badge": "HARDWARE INVOICE",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Clinic / Law Firm wanting physical hardware box",
            "description": "Issues official invoice for pre-configured, air-gapped Mini PC loaded with Nexus AI fleet.",
            "body": (
                "Hardware Invoice Manifest:\n"
                "• Item: Nexus Sovereign Appliance (Intel i7, 32GB RAM, 1TB NVMe, Pre-Installed Fleet)\n"
                "• Price: Rs 65,000 MUR (Hardware + Setup + 1-Year Local Warranty)\n"
                "• Delivery: Ebene Cybercity / On-Site Installation Included\n"
                "• Terms: 50% deposit, balance on physical delivery."
            ),
            "callouts": ["Physical Air-Gapped Box", "Rs 65,000 MUR Turnkey", "On-Site Installation Included"],
            "cta_label": "Generate Hardware Invoice"
        },
        {
            "id": "commerce_24",
            "title": "🔒 Zero-Knowledge Financial Proof for Stakeholders",
            "category": "Financial Proof",
            "urgency": "Low",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Cryptographic Solvency & Revenue Attestation Memo",
            "badge": "SOLVENCY PROOF",
            "gradient": "linear-gradient(135deg, #15803d 0%, #064e3b 100%)",
            "target_audience": "Bank / Corporate Partner / Investor",
            "description": "Generates a verifiable proof of positive cash flow and zero debt without exposing individual client names.",
            "body": (
                "Financial Attestation Summary:\n"
                "• Debt: Rs 0.00 MUR (Zero debt or external venture obligations)\n"
                "• Operating Cash Reserve: > 6 Months Operating Buffer\n"
                "• Revenue Stream: Diversified across B2B retainers and digital micro-products\n"
                "• Verification Hash: Stamped by local SQLite WAL ledger."
            ),
            "callouts": ["Zero Debt Verified", "6+ Months Cash Runway", "Privacy-Preserving Proof"],
            "cta_label": "Generate Solvency Memo"
        },
        {
            "id": "commerce_25",
            "title": "🎯 End-of-Month Earnings Milestone vs Rs 150k MUR Target",
            "category": "Target Milestone",
            "urgency": "High",
            "platform": "store_commerce",
            "task_type": "commerce_task",
            "headline": "Revenue Goal Radar: Rs 150,000 MUR Target Tracking",
            "badge": "EARNINGS MILESTONE",
            "gradient": "linear-gradient(135deg, #059669 0%, #10b981 100%)",
            "target_audience": "Sir Deven Pawaray",
            "description": "Analyzes the remaining gap to hit Rs 150,000 MUR monthly earnings and highlights fastest cash acceleration paths.",
            "body": (
                "Revenue Acceleration Analysis:\n"
                "• Monthly Goal: Rs 150,000 MUR\n"
                "• Collected to Date: Rs 45,045 MUR\n"
                "• Remaining Gap: Rs 104,955 MUR\n"
                "• High-Probability Path to Hit Target:\n"
                "  1. Close 2x Pending Mauritius Clinic/Hospitality Retainers (2 x Rs 45,000 = Rs 90,000 MUR)\n"
                "  2. Sell 8x Founder Lifetime Source Licenses (8 x $249 = Rs 90,000 MUR)\n"
                "• Execution Horizon: 12 Days Remaining."
            ),
            "callouts": ["Goal: Rs 150,000 MUR", "2 Deals to Close Gap", "High-Converting Actions"],
            "cta_label": "Review Revenue Plan"
        }
    ],

    # ═════════════════════════════════════════════════════════════════════════
    # 4. RESEARCH & INTELLIGENCE USER TYPE (25 Daily Real-World Scenarios)
    # ═════════════════════════════════════════════════════════════════════════
    "research": [
        {
            "id": "research_01",
            "title": "🏥 Mauritius Niche Lead Scouting: Private Clinics & Diagnostics",
            "category": "Lead Scouting",
            "urgency": "High",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Discover Qualified Clinic & Medical Practice Leads (Mauritius)",
            "badge": "CLINIC INTELLIGENCE",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Private Clinics in Ebene, Curepipe, Port Louis",
            "description": "Identifies clinics running appointments manually via phone/ledger and drafts targeted Medical 360 solution hooks.",
            "body": (
                "Clinic Intelligence Briefing:\n"
                "• Target Sector: Private Diagnostic & Dental Practices (Mauritius)\n"
                "• Discovered Prospects: 12 qualified clinics without automated patient portals\n"
                "• Primary Pain Point: Secretariat overwhelmed with 80+ daily phone booking queries\n"
                "• Proposed Solution: Medical 360™ Patient & Appointment Portal (Rs 45,000 MUR)\n"
                "• Outreach Readiness: Direct WhatsApp & email contact lines extracted."
            ),
            "callouts": ["12 High-Value Leads", "Overwhelmed Secretariat Pain", "Rs 45,000 Turnkey Retainer"],
            "cta_label": "Import Clinic Leads"
        },
        {
            "id": "research_02",
            "title": "🏝️ Mauritius Niche Lead Scouting: Inbound Travel DMCs & Villas",
            "category": "Lead Scouting",
            "urgency": "High",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Scout Luxury Villa & Tourism Operators (Grand Baie / Le Morne)",
            "badge": "TOURISM INTELLIGENCE",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Boutique Hospitality & Receptive Travel Agencies",
            "description": "Finds tourism operators losing after-hours bookings to competitors and packages the VillaFlow WhatsApp bot pitch.",
            "body": (
                "Hospitality Lead Intelligence:\n"
                "• Target: Luxury boutique villas and catamaran charter operators\n"
                "• Operational Gap: Zero response between 18:00 and 08:00 MUT (International guest queries lost)\n"
                "• Best-Fit Solution: VillaFlow 24/7 Bilingual WhatsApp Concierge (Rs 25,000 setup + Rs 15,000/mo)\n"
                "• ROI Multiplier: Just 1 recovered booking per month covers full retainer cost."
            ),
            "callouts": ["Recovers After-Hours Bookings", "1 Deal Pays for Full Year", "Bilingual FR/EN"],
            "cta_label": "Import Hospitality Leads"
        },
        {
            "id": "research_03",
            "title": "🏢 Ebene Cybercity FinTech & BPO Corporate Scouting",
            "category": "Corporate Scouting",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Cybercity Ebene BPO & FinTech Automation Prospecting",
            "badge": "BPO INTELLIGENCE",
            "gradient": "linear-gradient(135deg, #4338ca 0%, #312e81 100%)",
            "target_audience": "Mid-Market BPOs and Management Companies",
            "description": "Maps IT leadership across Ebene Cybercity needing sovereign email triage under Mauritius Data Protection Act.",
            "body": (
                "Cybercity Corporate Prospecting:\n"
                "• Discovered: 8 corporate management companies handling high email volume\n"
                "• Compliance Mandate: Strict data sovereignty requirements under DPA 2017\n"
                "• Hook: Sovereign local AI fleet running on-premise without US cloud data leakage\n"
                "• Deal Size: Rs 65,000 - Rs 120,000 MUR implementation."
            ),
            "callouts": ["Mauritius DPA 2017 Compliance", "Cybercity Ebene Focus", "High-Ticket Enterprise"],
            "cta_label": "Import Corporate Leads"
        },
        {
            "id": "research_04",
            "title": "🔎 Competitor Pricing & SaaS Feature Matrix Benchmark",
            "category": "Competitive Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Competitor Teardown: Why Nexus Wins on Zero SaaS Tax",
            "badge": "COMPETITIVE INTEL",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Sales Strategy Engine",
            "description": "Compares Nexus one-time / retainer model against Zendesk, HubSpot, and Zapier to equip Sir with sharp objection handles.",
            "body": (
                "Competitive Benchmark Matrix:\n"
                "• Competitor Stack (HubSpot + Zendesk + Zapier): $380/mo recurring ($4,560/year)\n"
                "• Data Residence: US cloud servers (GDPR / DPA cross-border risk)\n"
                "• Nexus Solution: Rs 45,000 MUR one-time + sovereign hardware ownership\n"
                "• Sales Killshot: 'Nexus pays for itself in 4 months and eliminates monthly subscription bills forever.'"
            ),
            "callouts": ["Saves $4,560/year", "100% Data Residence", "4-Month Full Payback"],
            "cta_label": "Review Competitor Matrix"
        },
        {
            "id": "research_05",
            "title": "🛡️ GitHub CVE Radar Scan for Upstream Python Packages",
            "category": "Security Research",
            "urgency": "High",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Automated GitHub Security Advisory Radar",
            "badge": "CVE RADAR",
            "gradient": "linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%)",
            "target_audience": "System Dependencies",
            "description": "Queries GitHub Advisory Database for zero-day vulnerabilities affecting FastAPI, Uvicorn, or cryptography libs.",
            "body": (
                "CVE Radar Scan Results:\n"
                "• Repositories Monitored: fastapi, uvicorn, pydantic, sqlite3, requests\n"
                "• Critical Advisories Past 7 Days: 0\n"
                "• Moderate Advisories: 0\n"
                "• Status: Clean operational bill of health."
            ),
            "callouts": ["Zero Critical Advisories", "Active GitHub Advisory Sync", "Zero-Day Shield"],
            "cta_label": "Execute CVE Radar Scan"
        },
        {
            "id": "research_06",
            "title": "🚀 Global Indie Hacker & Product Hunt Trend Radar",
            "category": "Product Discovery",
            "urgency": "Low",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Trending Micro-Tool Demand Discovery (Product Hunt / HN)",
            "badge": "TREND RADAR",
            "gradient": "linear-gradient(135deg, #7c3aed 0%, #4338ca 100%)",
            "target_audience": "$1 Digital Store Ideation",
            "description": "Scrapes top trending developer pain points to identify new micro-tools for the Nexus $1 Digital Vending Machine.",
            "body": (
                "Trend Discovery Briefing:\n"
                "• Top Trending Search: 'Automated SQLite Backup Script' & 'Local PDF Watermarker'\n"
                "• Opportunity: Developers hate monthly subscriptions for basic file transformations\n"
                "• Recommendation: Package 'Nexus™ Standalone PDF Watermarker' for $1.00 USD / Rs 45 MUR."
            ),
            "callouts": ["High Buyer Intent", "Build Once, Sell Forever", "$1 Instant Impulse Buy"],
            "cta_label": "Ideate New Tool"
        },
        {
            "id": "research_07",
            "title": "📜 Mauritius Data Protection Act 2017 Regulatory Audit",
            "category": "Regulatory Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Mauritius DPA 2017 Legal Compliance Checklist",
            "badge": "REGULATORY AUDIT",
            "gradient": "linear-gradient(135deg, #15803d 0%, #166534 100%)",
            "target_audience": "Local Enterprise Pitches",
            "description": "Validates Nexus architecture against all 8 principles of the Mauritius Data Protection Act 2017.",
            "body": (
                "DPA 2017 Regulatory Assessment:\n"
                "✔ Principle 1 (Lawfulness & Fairness): Explicit opt-in client consent logged in SQLite.\n"
                "✔ Principle 2 (Purpose Limitation): Data used strictly for specified automation.\n"
                "✔ Principle 5 (Data Security): AES-256 local encryption; zero foreign mirroring.\n"
                "• Verdict: 100% compliant with Data Protection Office (DPO) standards."
            ),
            "callouts": ["100% DPO Mauritius Compliant", "AES-256 Encryption", "Zero Foreign Mirroring"],
            "cta_label": "Generate DPA Audit Memo"
        },
        {
            "id": "research_08",
            "title": "📱 Local B2B Decision Maker Phone & WhatsApp Enrichment",
            "category": "Data Enrichment",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Contact Data Enrichment: Direct Phone & Verified WhatsApp",
            "badge": "DATA ENRICHMENT",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0c4a6e 100%)",
            "target_audience": "Mauritius B2B Prospects",
            "description": "Enriches raw company names with verified Mauritian mobile numbers (+230) and Managing Director names.",
            "body": (
                "Enrichment Batch Progress:\n"
                "• Input: 10 Mauritius target companies\n"
                "• Enriched: 10/10 verified with Managing Director / General Manager names\n"
                "• Mobile Coverage: 9/10 direct +230 numbers identified for WhatsApp outreach\n"
                "• Ready for 1-click tailored outreach."
            ),
            "callouts": ["90% Direct Mobile Match", "Verified C-Level Decision Makers", "+230 Mauritius Numbers"],
            "cta_label": "Enrich Lead Dataset"
        },
        {
            "id": "research_09",
            "title": "✍️ High-Converting Cold Email Subject Line A/B Test Research",
            "category": "Copywriting Intel",
            "urgency": "Low",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Cold Outreach Subject Line Benchmark (Mauritius Market)",
            "badge": "COPY TESTING",
            "gradient": "linear-gradient(135deg, #6366f1 0%, #4338ca 100%)",
            "target_audience": "Email Outbound Sequences",
            "description": "Analyzes historical open rates to determine the top-performing subject line formats for Mauritian executives.",
            "body": (
                "Subject Line Performance Analysis:\n"
                "• Winner A: 'Quick question regarding [Company] WhatsApp bookings' (64.2% Open Rate)\n"
                "• Winner B: '[Company] operations bottleneck audit' (58.9% Open Rate)\n"
                "• Loser C: 'Introducing Nexus AI Solutions' (18.4% Open Rate — Avoid generic sales pitch!)\n"
                "• Recommendation: Use Winner A for all hospitality prospects."
            ),
            "callouts": ["64.2% Open Rate", "Eliminates Generic Pitches", "Tested on Local Inboxes"],
            "cta_label": "Apply Top Subject Line"
        },
        {
            "id": "research_10",
            "title": "💻 Enterprise Client Tech Stack Fingerprinting",
            "category": "Tech Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Prospect Architecture & Technology Stack Fingerprint",
            "badge": "TECH FINGERPRINT",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "High-Value Enterprise Prospect",
            "description": "Inspects target company website HTTP headers, CMS, and DNS to identify slow loading times and legacy tooling.",
            "body": (
                "Tech Stack Teardown for [Target Company]:\n"
                "• CMS: Legacy WordPress 5.8 (Last updated 2 years ago)\n"
                "• PageSpeed Mobile Score: 38/100 (Takes 5.4 seconds to load)\n"
                "• Booking Mechanism: Static HTML email contact form (Zero auto-confirmation)\n"
                "• Pitch Angle: 'Your site takes 5.4s to load and loses mobile bookings; our turnkey portal loads in 0.4s.'"
            ),
            "callouts": ["Identifies Real Tech Debt", "Evidence-Based Sales Hook", "Sharp Technical Edge"],
            "cta_label": "Fingerprint Prospect"
        },
        {
            "id": "research_11",
            "title": "📈 Total Addressable Market (TAM) Analysis: Mauritius AI Automation",
            "category": "Market Sizing",
            "urgency": "Low",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Mauritius B2B Market Sizing & Revenue Ceiling Analysis",
            "badge": "TAM SIZING",
            "gradient": "linear-gradient(135deg, #059669 0%, #047857 100%)",
            "target_audience": "Nexus Strategic Roadmap",
            "description": "Calculates total market opportunity across tourism, medical, financial, and legal sectors in Mauritius.",
            "body": (
                "Mauritius AI Automation TAM Calculation:\n"
                "• Registered SMEs in Target Verticals: ~3,400 companies\n"
                "• Serviceable Addressable Market (SAM): 420 mid-market firms with >15 staff\n"
                "• Serviceable Obtainable Market (SOM): 50 retainer clients @ Rs 45k/mo\n"
                "• Annual Potential at 50 Clients: Rs 27,000,000 MUR / year ($600,000 USD)\n"
                "• Current Penetration: < 2% (Massive blue ocean runway)."
            ),
            "callouts": ["Rs 27M MUR Market Potential", "Blue Ocean in Mauritius", "50-Client Target"],
            "cta_label": "View Market Sizing Memo"
        },
        {
            "id": "research_12",
            "title": "🏛️ CSR Tax Exemption (MRA 50L) Corporate Budget Radar",
            "category": "CSR Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Corporate CSR Budget Unlocking Strategy (Enn Rev Enn Sourir)",
            "badge": "CSR BUDGET RADAR",
            "gradient": "linear-gradient(135deg, #d97706 0%, #78350f 100%)",
            "target_audience": "Mauritius Banks and Conglomerates (IBL, ENL, CIEL)",
            "description": "Maps annual CSR allocation cycles of top Mauritian conglomerates to pitch corporate crowdfunding sponsorship.",
            "body": (
                "Corporate CSR Radar:\n"
                "• Regulatory Mandate: Mauritius companies must allocate 2% of book profits to CSR\n"
                "• Target Conglomerates: IBL Group, Rogers, CIEL, MCB Foundation\n"
                "• Key Pitch: Sponsor Enn Rev Enn Sourir NGO child medical fund with transparent blockchain-backed fund tracking\n"
                "• MRA Benefit: Full 15% tax deduction under Section 50L."
            ),
            "callouts": ["2% Mandatory CSR Budgets", "MRA Section 50L Tax Shield", "High Corporate Goodwill"],
            "cta_label": "Prospect CSR Donors"
        },
        {
            "id": "research_13",
            "title": "🧠 Open Source LLM & Model Efficiency Benchmark",
            "category": "Model Research",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Local LLM vs Gemini 2.5 Flash Cost & Speed Benchmark",
            "badge": "MODEL BENCHMARK",
            "gradient": "linear-gradient(135deg, #7c3aed 0%, #312e81 100%)",
            "target_audience": "Core AI Pipeline",
            "description": "Compares token cost, latency, and response quality between Gemini 2.5 Flash and quantized local models.",
            "body": (
                "LLM Engine Efficiency Benchmark:\n"
                "• Gemini 2.5 Flash: 420ms response, $0.075 / 1M input tokens (Superior for complex extraction)\n"
                "• Local Quantized Llama-3-8B: 850ms response, $0.00 marginal cost (Ideal for offline confidential triage)\n"
                "• Hybrid Policy: Route public/creative tasks to Gemini; route confidential customer PII locally."
            ),
            "callouts": ["$0.00 Marginal Local Cost", "420ms Gemini Response", "Privacy-Preserving Hybrid"],
            "cta_label": "Run Model Benchmark"
        },
        {
            "id": "research_14",
            "title": "🌐 SEO Keyword SERP Tracker for 'AI Automation Mauritius'",
            "category": "SEO Intel",
            "urgency": "Low",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Google Search Ranking: AI & Autonomous Workforce (Mauritius)",
            "badge": "SEO TRACKER",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Inbound Organic Traffic",
            "description": "Tracks Google rankings for high-intent B2B search terms across Mauritius and the Indian Ocean region.",
            "body": (
                "SERP Rank Tracking Report:\n"
                "• 'AI Automation Mauritius': Rank #1 (Organic)\n"
                "• 'WhatsApp Booking Bot Mauritius': Rank #2 (Organic)\n"
                "• 'Autonomous AI Workforce': Rank #4\n"
                "• Recommended Action: Add case study on Alison / Enn Rev Enn Sourir to capture CSR keywords."
            ),
            "callouts": ["#1 for AI Automation Mauritius", "Zero Paid Ad Spend Required", "High Inbound Authority"],
            "cta_label": "Audit SEO Rankings"
        },
        {
            "id": "research_15",
            "title": "📢 Social Sentiment & Competitor Brand Mention Monitoring",
            "category": "Sentiment Intel",
            "urgency": "Low",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Mauritius Tech Social Listening & Competitor Mentions",
            "badge": "SOCIAL LISTENING",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #1e40af 100%)",
            "target_audience": "Brand Reputation",
            "description": "Monitors LinkedIn and Twitter for discussions around business automation in Cybercity and Mauritius.",
            "body": (
                "Social Sentiment Sweep:\n"
                "• Monitored Keywords: 'Mauritius AI', 'Cybercity automation', 'Deven Pawaray'\n"
                "• Sentiment Breakdown: 92% Positive / Informative, 8% Inquiries\n"
                "• Opportunity Identified: 2 founders on LinkedIn complaining about expensive HubSpot license renewals."
            ),
            "callouts": ["92% Positive Sentiment", "Identified 2 Warm Leads", "Real-Time Opportunity Catch"],
            "cta_label": "Review Social Mentions"
        },
        {
            "id": "research_16",
            "title": "⚡ Client Website Speed & Conversion Friction Teardown",
            "category": "Audit Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Automated PageSpeed & UX Friction Teardown Report",
            "badge": "UX SPEED AUDIT",
            "gradient": "linear-gradient(135deg, #d97706 0%, #78350f 100%)",
            "target_audience": "Cold Outbound Attachment",
            "description": "Generates a 1-page visual audit showing prospective clients exactly how much money they lose to slow page loads.",
            "body": (
                "Prospect Website Friction Audit:\n"
                "• Prospect: Grand Baie Boat Charters\n"
                "• Mobile Load Time: 6.2 seconds (74% bounce rate)\n"
                "• Booking Form: 12 mandatory fields (massive friction)\n"
                "• Nexus Teardown Solution: 1-click WhatsApp instant quote button reduces booking time to 15 seconds."
            ),
            "callouts": ["Exposes 74% Drop-Off", "Generates High Urgency", "Turnkey Nexus Fix"],
            "cta_label": "Generate Friction Report"
        },
        {
            "id": "research_17",
            "title": "🏛️ Government Procurement & E-Tender Automation Radar",
            "category": "Tender Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Mauritius E-Procurement Portal Automation Opportunities",
            "badge": "TENDER RADAR",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Public Sector Opportunities",
            "description": "Monitors public e-procurement notices from Mauritius government bodies for software modernization RFPs.",
            "body": (
                "Procurement Radar Digest:\n"
                "• Active Public Tenders: 2 digitization RFPs from state-owned enterprises\n"
                "• Keywords: 'Document Management', 'Automated Triage', 'Citizen Portal'\n"
                "• Feasibility: Nexus architecture meets 100% of data residency and security prerequisites."
            ),
            "callouts": ["Monitors Public Tenders", "100% Residency Compliant", "Large Contract Sizes"],
            "cta_label": "Inspect Tender Notices"
        },
        {
            "id": "research_18",
            "title": "🚢 Port Louis Logistics & Customs Clearing Pain Point Discovery",
            "category": "Industry Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Freight Forwarder & Customs Clearing Automation Needs",
            "badge": "LOGISTICS INTEL",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Logistics Companies in Port Louis",
            "description": "Interviews freight agents regarding Bill of Lading data entry bottlenecks to package custom document extractor.",
            "body": (
                "Logistics Vertical Intelligence:\n"
                "• Target: 24 Freight forwarding agents in Port Louis harbor area\n"
                "• Core Pain: Manual typing of Bill of Lading PDF tables into customs trade software\n"
                "• Opportunity: Autonomous OCR & PDF Parser micro-tool ($1 tool or Rs 35k/mo retainer)\n"
                "• Time Saved: 3 hours daily per customs clerk."
            ),
            "callouts": ["Saves 3 Hours Daily", "High Repeat Demand", "Harbor Business Focus"],
            "cta_label": "Prospect Logistics Leads"
        },
        {
            "id": "research_19",
            "title": "💳 Cross-Border Payment Rail Fee Analysis (Wise vs PayPal vs Juice)",
            "category": "Fintech Intel",
            "urgency": "Low",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Merchant Payment Processing Fee Optimization Matrix",
            "badge": "FEE OPTIMIZATION",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Nexus Treasury Engine",
            "description": "Calculates exact fee drag across payment processors to guide international clients to the lowest fee rail.",
            "body": (
                "Payment Processor Drag Analysis:\n"
                "• MCB Juice: 0.0% Fee (Local P2P transfer — pure 100% margin)\n"
                "• Base L2 Blockchain (USDC): $0.002 flat fee (<0.01% drag)\n"
                "• Wise Wire: 0.45% FX spread\n"
                "• PayPal Standard: 3.49% + $0.49 (High fee drag)\n"
                "• Routing Rule: Prioritize MCB Juice domestically; prioritize Base L2 / Wise internationally."
            ),
            "callouts": ["0.0% Fee on MCB Juice", "Base L2 < 0.01% Drag", "Maximizes Net Retained Profit"],
            "cta_label": "Review Payment Rails"
        },
        {
            "id": "research_20",
            "title": "📉 AI Agent Fleet Token Consumption & Cost Optimization",
            "category": "Telemetry Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Token Economy Telemetry: Maximizing ROI per Inference Call",
            "badge": "TOKEN TELEMETRY",
            "gradient": "linear-gradient(135deg, #7c3aed 0%, #4338ca 100%)",
            "target_audience": "Internal Architecture",
            "description": "Analyzes token usage across all 18 agents to trim system prompt bloat and keep monthly compute under $15.",
            "body": (
                "Token Telemetry Audit:\n"
                "• Total Tokens Consumed This Month: 1.84 Million Tokens\n"
                "• Total Inference Expense: $0.14 USD\n"
                "• Optimization: Prompt compression trimmed 35% unnecessary preamble across agents\n"
                "• Margin Efficiency: Extraordinary (Inference cost is 0.0003% of revenue)."
            ),
            "callouts": ["$0.14 Monthly LLM Spend", "35% Prompt Compression", "Maximum Profit Margin"],
            "cta_label": "Optimize Token Usage"
        },
        {
            "id": "research_21",
            "title": "💡 Micro-Tool Demand Discovery on Reddit & HackerNews",
            "category": "Product Research",
            "urgency": "Low",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Developer Micro-Pain Discovery: Python Standalone Utilities",
            "badge": "COMMUNITY INTEL",
            "gradient": "linear-gradient(135deg, #c2410c 0%, #7c2d12 100%)",
            "target_audience": "Digital Vending Machine Catalog",
            "description": "Monitors /r/python and /r/indiehackers for recurring tool requests to manufacture in under 60 minutes.",
            "body": (
                "Community Demand Mining:\n"
                "• High Frequency Request: 'Tool to monitor competitor prices without headless browser crash'\n"
                "• Nexus Solution: Nexus™ Lightweight Crypto & Price Alert Utility (Already built in products/!)\n"
                "• Distribution Strategy: Post free code snippet with link to full $1 version."
            ),
            "callouts": ["Uncovers Real Demand", "60-Minute Tool Build Time", "Built-In Audience"],
            "cta_label": "Mine Developer Demand"
        },
        {
            "id": "research_22",
            "title": "📑 High-Yield B2B Retainer Proposal Template Benchmarking",
            "category": "Sales Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Proposal Win Rate Analysis & MEDDPICC Close Framework",
            "badge": "PROPOSAL BENCHMARK",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Sales Operations",
            "description": "Audits why certain client proposals close in 48 hours while others stall, updating our master template.",
            "body": (
                "Proposal Win Rate Post-Mortem:\n"
                "• Top Closing Factor: Including a live functional demo link in the first 2 paragraphs\n"
                "• Secondary Factor: Clear 1-month money-back performance guarantee\n"
                "• Action: Updated default proposal template to lead with clickable demo."
            ),
            "callouts": ["Live Demo Leads Close Fast", "Money-Back Assurance", "Proven MEDDPICC Framework"],
            "cta_label": "Update Proposal Template"
        },
        {
            "id": "research_23",
            "title": "⚖️ Sovereign AI Code Ownership & Legal Precedent Audit",
            "category": "Legal Intel",
            "urgency": "Low",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "IP Protection: Autonomous Software Code Copyright & Licensing",
            "badge": "IP PROTECTION",
            "gradient": "linear-gradient(135deg, #334155 0%, #1e293b 100%)",
            "target_audience": "Corporate IP Protection",
            "description": "Reviews Mauritius Copyright Act and international precedents confirming human author ownership of AI-assisted codebases.",
            "body": (
                "Intellectual Property Legal Assessment:\n"
                "• Author: Deven Pawaray (Sole human architect and prompt engineer)\n"
                "• Codebase Status: 100% copyrighted proprietary asset under Mauritius law\n"
                "• Client Licensing: Structured as perpetual commercial licenses without equity transfer."
            ),
            "callouts": ["100% Deven Pawaray Owned", "Perpetual License Structure", "Clean Commercial IP"],
            "cta_label": "View IP Protection Memo"
        },
        {
            "id": "research_24",
            "title": "🏢 Local Business Directory Scraping (MCCI & CCI France-Maurice)",
            "category": "Directory Intel",
            "urgency": "Standard",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Chamber of Commerce Member Directory Ingestion",
            "badge": "DIRECTORY INGESTION",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0c4a6e 100%)",
            "target_audience": "Chamber of Commerce Members",
            "description": "Aggregates public company registries from MCCI and French Chamber to populate the qualified CRM pipeline.",
            "body": (
                "Directory Mining Summary:\n"
                "• Source: Public Mauritius Chamber of Commerce & Industry (MCCI) member lists\n"
                "• Records Extracted: 48 active enterprise companies\n"
                "• Deduplication: Cleaned against existing client list\n"
                "• Ready for ICP qualification scoring."
            ),
            "callouts": ["48 Enterprise Members", "Zero Duplicates", "High Credibility ICP"],
            "cta_label": "Ingest Directory Leads"
        },
        {
            "id": "research_25",
            "title": "🎯 Strategic AI Threat & Blue Ocean Opportunity Review",
            "category": "Strategic Intel",
            "urgency": "High",
            "platform": "lead_crm",
            "task_type": "research_task",
            "headline": "Quarterly Agency Threat Assessment & Strategic Roadmap",
            "badge": "STRATEGIC THREATS",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Sir Deven Pawaray",
            "description": "Analyzes big-tech moves (OpenAI agent updates, Microsoft Copilot) and solidifies Nexus unbreachable moats.",
            "body": (
                "Quarterly Strategic Moat Analysis:\n"
                "• External Threat: Big Tech pushing cloud-tethered subscription AI\n"
                "• Nexus Unbreachable Moat:\n"
                "  1. 100% Sovereign Local Execution (Zero US data transfer)\n"
                "  2. Deep Mauritius Banking Rails (MCB Juice +230 58169420 instant checkout)\n"
                "  3. Custom single-file micro-tools at $1.00 USD / Rs 45 MUR impulse pricing\n"
                "• Verdict: Nexus is positioned in an uncontested blue ocean."
            ),
            "callouts": ["Sovereign Local Moat", "Local MCB Juice Monopoly", "Uncontested Blue Ocean"],
            "cta_label": "Review Strategic Roadmap"
        }
    ],

    # ═════════════════════════════════════════════════════════════════════════
    # 5. CEO / EXECUTIVE / MARKETING USER TYPE (25 Daily Real-World Scenarios)
    # ═════════════════════════════════════════════════════════════════════════
    # ═════════════════════════════════════════════════════════════════════════
    # 5. CEO / EXECUTIVE / MARKETING USER TYPE (25 Daily Real-World Scenarios)
    # Reworked to Drive High-Ticket White-Label Turnkey Sales & IP Transfer
    # ═════════════════════════════════════════════════════════════════════════
    "ceo": [
        {
            "id": "ceo_01",
            "title": "🏥 Medical 360™ Clinic Suite: White-Label Pitch (Rs 105k + Rs 15k/yr)",
            "category": "White-Label Sales",
            "urgency": "High",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Enterprise Pitch: Medical 360™ Turnkey Clinic & Hospital Suite",
            "badge": "MEDICAL 360 PITCH",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Private Clinic & Polyclinic Directors (Mauritius)",
            "description": "High-converting white-label sales pitch for Medical 360 featuring frontend patient portal (Rs 45k) and backend admin engine (Rs 60k).",
            "body": (
                "Bonjour Dr. / Directeur,\n\n"
                "Managing patient appointments, blood bank registries, and lab test results on paper or disparate tools wastes hours daily.\n\n"
                "We offer **Medical 360™** as a complete **white-label turnkey solution with full IP transfer**:\n"
                "• Frontend Patient Portal (The Bait): Rs 45,000 MUR\n"
                "• Backend & Admin Operations Engine (+33% Premium): Rs 60,000 MUR\n"
                "• Complete Full-Stack IP Handover: Rs 105,000 MUR (~$2,330 USD)\n"
                "• Annual Maintenance Package: Rs 15,000 MUR / year\n\n"
                "Instant settlement via MCB Juice (+230 58169420) or Bank Transfer (000443260370).\n"
                "Pouvons-nous planifier une démo cette semaine?\n\n"
                "Deven Pawaray (+230 58169420)"
            ),
            "callouts": ["Rs 105k Upfront IP Transfer", "Rs 15k/yr Maintenance Annuity", "MCB Juice Ready (+230 58169420)"],
            "cta_label": "Dispatch Medical 360 Pitch"
        },
        {
            "id": "ceo_02",
            "title": "🤝 Enn Rev Enn Sourir™ NGO & CSR Platform Pitch (Rs 105k + Rs 15k/yr)",
            "category": "White-Label Sales",
            "urgency": "High",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Enterprise Proposal: Enn Rev Enn Sourir™ CSR & NGO Platform",
            "badge": "CSR PLATFORM PITCH",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Corporate CSR Funds & Foundation Directors",
            "description": "Bilingual white-label proposal for Enn Rev Enn Sourir featuring MRA Section 50L 15% tax deduction receipts and hospital payout tracking.",
            "body": (
                "Bonjour,\n\n"
                "Managing corporate CSR funds requires 100% surgical transparency and automated MRA Section 50L tax deduction receipts (15%).\n\n"
                "We deliver **Enn Rev Enn Sourir™** as a fully branded white-label platform with full IP transfer:\n"
                "• Frontend Donor Portal: Rs 45,000 MUR\n"
                "• Backend CSR Treasury & Audit Engine: Rs 60,000 MUR\n"
                "• Total Upfront IP Transfer: Rs 105,000 MUR (~$2,330 USD)\n"
                "• Annual Maintenance: Rs 15,000 MUR / year\n\n"
                "Direct bank transfer to MCB (000443260370) or Juice (+230 58169420).\n"
                "Shall we schedule a 10-minute demo?\n\n"
                "Deven Pawaray (+230 58169420)"
            ),
            "callouts": ["MRA Section 50L Compliant", "Surgical Audit Transparency", "Rs 15k/yr Maintenance Annuity"],
            "cta_label": "Dispatch CSR Pitch"
        },
        {
            "id": "ceo_03",
            "title": "✈️ i-Travellix™ Luxury Travel SaaS White-Label Pitch (Rs 117k + Rs 15k/yr)",
            "category": "White-Label Sales",
            "urgency": "High",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Enterprise Proposal: i-Travellix™ Luxury Travel & Tour Operator Suite",
            "badge": "TRAVEL SAAS PITCH",
            "gradient": "linear-gradient(135deg, #7c3aed 0%, #4338ca 100%)",
            "target_audience": "Inbound Tour Operators & DMCs (Mauritius & Regional)",
            "description": "White-label proposal for i-Travellix featuring live GDS flight search, 5-star resort catalogs, and multi-currency checkout with full IP transfer.",
            "body": (
                "Bonjour,\n\n"
                "Inbound tour operators and DMCs lose direct bookings to high-commission aggregators.\n\n"
                "We offer **i-Travellix™** as a complete white-label travel suite with full IP ownership transfer:\n"
                "• Frontend Booking Engine (The Bait): Rs 50,000 MUR\n"
                "• Backend GDS & Operations Engine: Rs 67,000 MUR\n"
                "• Total Upfront IP Handover: Rs 117,000 MUR (~$2,580 USD)\n"
                "• Annual Maintenance: Rs 15,000 MUR / year\n\n"
                "Settlement via MCB Bank (000443260370) or Base L2 USDC.\n"
                "Pouvons-nous organiser une présentation?\n\n"
                "Deven Pawaray (+230 58169420)"
            ),
            "callouts": ["Live GDS Flight Integration", "Rs 117k Upfront IP Handover", "Rs 15k/yr Maintenance Annuity"],
            "cta_label": "Dispatch Travel Pitch"
        },
        {
            "id": "ceo_04",
            "title": "💬 WhatsApp Flight Addon White-Label Pitch (Rs 40k + Rs 15k/yr)",
            "category": "White-Label Sales",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "White-Label Proposal: WhatsApp Conversational Flight & Booking Addon",
            "badge": "WHATSAPP ADDON PITCH",
            "gradient": "linear-gradient(135deg, #25d366 0%, #128c7e 100%)",
            "target_audience": "Airlines, Travel Agencies & Portals",
            "description": "White-label pitch for the 24/7 conversational WhatsApp bot addon for flight status and bookings.",
            "body": (
                "Bonjour,\n\n"
                "Deliver 24/7 instant WhatsApp support for flight status, baggage rules, and bookings directly on your clients' phones.\n\n"
                "• Frontend Bot Interface: Rs 15,000 MUR\n"
                "• Backend NLP & Dispatch Engine: Rs 25,000 MUR\n"
                "• Total Upfront IP Transfer: Rs 40,000 MUR (~$880 USD)\n"
                "• Annual Maintenance: Rs 15,000 MUR / year\n\n"
                "MCB Juice: +230 58169420 | MCB Account: 000443260370.\n"
                "Let's deploy in 48 hours.\n\n"
                "Deven Pawaray (+230 58169420)"
            ),
            "callouts": ["24/7 WhatsApp Autopilot", "Rs 40k Upfront IP Transfer", "48-Hour Deployment"],
            "cta_label": "Dispatch WhatsApp Addon Pitch"
        },
        {
            "id": "ceo_05",
            "title": "🎯 Daily Rs 150,000 MUR Revenue Trajectory & White-Label Pipeline Audit",
            "category": "Revenue Strategy",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Cognitive Audit: Tracking White-Label Sales Toward Rs 150k MUR Target",
            "badge": "REVENUE AUDIT",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Sir Deven Pawaray",
            "description": "J.A.R.V.I.S. financial audit verifying white-label turnkey sales and maintenance annuity inflows against the monthly target.",
            "body": (
                "J.A.R.V.I.S. Revenue Telemetry:\n"
                "• Monthly Revenue Target: Rs 150,000 MUR\n"
                "• Active White-Label Sales & Maintenance Inflows: Verified\n"
                "• Pipeline Conversion Focus:\n"
                "  1. Close 1 Medical 360™ Client -> Rs 105,000 MUR upfront + Rs 15,000/yr\n"
                "  2. Close 1 Enn Rev Enn Sourir™ NGO -> Rs 105,000 MUR upfront + Rs 15,000/yr\n"
                "• Cloud Compute Burn: $12.40 USD (Well below $180 cap, guaranteeing 99% gross margins)."
            ),
            "callouts": ["Rs 150k MUR Monthly Target", "Annual Maintenance Annuities", "99% Operating Margin"],
            "cta_label": "Run Revenue Audit"
        },
        {
            "id": "ceo_06",
            "title": "📄 White-Label Intellectual Property (IP) Transfer Agreement Drafting",
            "category": "Legal & IP",
            "urgency": "High",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Standard Software IP Transfer & White-Label Licensing Agreement",
            "badge": "IP TRANSFER AGREEMENT",
            "gradient": "linear-gradient(135deg, #475569 0%, #1e293b 100%)",
            "target_audience": "Incoming Turnkey Client",
            "description": "Standardized legal contract confirming full source code delivery, perpetual white-label usage rights, and annual maintenance terms.",
            "body": (
                "SOFTWARE IP TRANSFER & COMMENCEMENT AGREEMENT\n\n"
                "1. Transfer of Ownership: Upon full settlement of the upfront white-label fee (Rs 105,000 MUR), Nexus AI irrevocably transfers all intellectual property rights and source code for [Platform Name] to the Client.\n"
                "2. Maintenance & Support: Includes the annual maintenance package at Rs 15,000 MUR/year for updates and security patches.\n"
                "3. Governing Law: Republic of Mauritius.\n\n"
                "Signed,\nDeven Pawaray, Managing Principal"
            ),
            "callouts": ["Full Source Code Handover", "Maur Mauritius Jurisdiction", "Annual Maintenance Terms"],
            "cta_label": "Generate IP Agreement"
        },
        {
            "id": "ceo_07",
            "title": "💎 Base L2 Sovereign Crypto Treasury Rebalance & MCB Off-Ramp",
            "category": "Treasury Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Base L2 Treasury Sync: Converting USDC to MCB Bank (000443260370)",
            "badge": "CRYPTO TREASURY",
            "gradient": "linear-gradient(135deg, #0052ff 0%, #001f5c 100%)",
            "target_audience": "Base L2 Wallet 0xEAE558282090d878582ec4C4C1C2470f9826b1F2",
            "description": "Executes pre-flight policy verifier checks ($15 single-tx ceiling, $50 daily cap) and initiates off-ramp to MCB account.",
            "body": (
                "Base L2 Treasury & Off-Ramp Execution:\n"
                "• Wallet Address: 0xEAE558282090d878582ec4C4C1C2470f9826b1F2 (Chain 8453)\n"
                "• Pending USDC Balance: Verified via Secp256k1 keypair\n"
                "• Off-ramp Target: MCB Bank Account 000443260370 (Mauritian Rupees)\n"
                "• Policy Guardrails: Enforced ($15 single-tx ceiling / $50 daily limit)\n"
                "• Status: Ready for execution."
            ),
            "callouts": ["Base L2 Chain 8453", "Secp256k1 Keypair Signing", "MCB Bank 000443260370"],
            "cta_label": "Execute Treasury Off-Ramp"
        },
        {
            "id": "ceo_08",
            "title": "🛡️ Annual Maintenance Invoice & Annuity Collection Blitz",
            "category": "Billing Operations",
            "urgency": "High",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Annuity Billing Notice: Annual Maintenance Package (Rs 15,000 MUR)",
            "badge": "MAINTENANCE ANNUITY",
            "gradient": "linear-gradient(135deg, #d97706 0%, #78350f 100%)",
            "target_audience": "Existing Turnkey Software Clients",
            "description": "Automated billing notice for the mandatory yearly Rs 15,000 maintenance package covering security patches and system updates.",
            "body": (
                "Dear Partner,\n\n"
                "Your annual software maintenance package for your white-label platform is due this month.\n\n"
                "• Annual Maintenance Fee: Rs 15,000 MUR (~$330 USD)\n"
                "• Covers: Continuous security patches, database optimizations, and priority technical support.\n"
                "• Payment Rails:\n"
                "  - MCB Juice: +230 58169420\n"
                "  - Bank Transfer: MCB Account 000443260370\n\n"
                "Thank you for keeping your infrastructure secure and updated.\n\n"
                "Nexus Executive Billing Desk"
            ),
            "callouts": ["Rs 15,000/yr Annuity", "MCB Juice (+230 58169420)", "Secures Ongoing Support"],
            "cta_label": "Dispatch Maintenance Invoice"
        },
        {
            "id": "ceo_09",
            "title": "🎙️ Executive Morning Voice Briefing with J.A.R.V.I.S. (Alt+J)",
            "category": "Executive Routine",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "J.A.R.V.I.S. Morning Executive Audio & Telemetry Briefing",
            "badge": "J.A.R.V.I.S. BRIEFING",
            "gradient": "linear-gradient(135deg, #00f0ff 0%, #0369a1 100%)",
            "target_audience": "Sir Deven Pawaray",
            "description": "Synthesizes overnight white-label inquiries, maintenance collections, and server telemetry into a crisp audio briefing.",
            "body": (
                "Good morning, Sir Deven.\n\n"
                "All systems nominal. Overnight security audits completed with zero vulnerabilities detected.\n\n"
                "Commercial update: 1 inquiry for Medical 360™ received via WhatsApp, and our finance watchdog confirmed receipt of an annual maintenance transfer.\n\n"
                "Standing by for your voice directive, Sir. Press [Alt + J] to speak."
            ),
            "callouts": ["Voice-Ready Audio Script", "Press [Alt + J] to Speak", "Complete System Overview"],
            "cta_label": "Play Morning Brief"
        },
        {
            "id": "ceo_10",
            "title": "🌍 Bilingual Mauritius Outreach Campaign (English / French Parity)",
            "category": "B2B Outreach",
            "urgency": "High",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Bilingual Campaign: Turnkey Software Solutions for Mauritius",
            "badge": "BILINGUAL OUTREACH",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #1e3a8a 100%)",
            "target_audience": "Mauritian Business Owners & Executives",
            "description": "Simultaneous English and French email and WhatsApp pitch sequence targeting local enterprises.",
            "body": (
                "Bonjour / Hello,\n\n"
                "Nous aidons les entreprises mauriciennes à automatiser leurs opérations avec des solutions logicielles clés en main avec transfert complet de propriété intellectuelle.\n\n"
                "We help Mauritian businesses deploy complete turnkey software systems with full source code and IP transfer (Medical 360, Enn Rev Enn Sourir, i-Travellix).\n\n"
                "Pouvons-nous organiser un appel de 10 minutes?\n\n"
                "Deven Pawaray (+230 58169420)"
            ),
            "callouts": ["100% Bilingual Parity", "Maur Mauritius DPA Compliant", "MCB Juice Ready (+230 58169420)"],
            "cta_label": "Dispatch Bilingual Campaign"
        },
        {
            "id": "ceo_11",
            "title": "📊 FinOps Cloud Cost & Gross Margin Enforcement ($180 Hard Cap)",
            "category": "FinOps Strategy",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "FinOps Audit: Protecting 99% Margins Below $180 Cloud Cap",
            "badge": "MARGIN AUDIT",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Executive Cockpit",
            "description": "Verifies cloud compute expenditure across AWS/Vercel to guarantee operating expenses remain strictly under the $180 limit.",
            "body": (
                "FinOps Telemetry Audit:\n"
                "• Monthly Cloud Spend Cap: $180.00 USD\n"
                "• Actual Current Spend: $11.20 USD (SQLite local WAL architecture efficiency)\n"
                "• Gross Operating Margin: 99.02%\n"
                "• Status: Zero runaway background loops detected."
            ),
            "callouts": ["$180 Hard Cap Enforced", "$11.20 Actual Spend", "99% Gross Margin"],
            "cta_label": "Run FinOps Audit"
        },
        {
            "id": "ceo_12",
            "title": "🤝 Strategic Partner Referral & Commission Payout Audit",
            "category": "Partner Operations",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Partner Network Audit: White-Label Reseller Commissions",
            "badge": "PARTNER AUDIT",
            "gradient": "linear-gradient(135deg, #7c3aed 0%, #4338ca 100%)",
            "target_audience": "Partner Network",
            "description": "Audits referral tracking and calculates commission payouts for white-label software introductions.",
            "body": (
                "Partner Referral Audit:\n"
                "• Active Reseller Partners: 4 Digital Agencies\n"
                "• Pending Referral Payouts: Rs 15,000 MUR per successful turnkey introduction\n"
                "• Payment Execution: Settled instantly via MCB Juice (+230 58169420)\n"
                "• Status: All accounts reconciled."
            ),
            "callouts": ["Automated Partner Payouts", "MCB Juice Settlement", "Zero Discrepancies"],
            "cta_label": "Run Partner Audit"
        },
        {
            "id": "ceo_13",
            "title": "🛡️ SQLite WAL Integrity & Zero-Regression Backup Snapshot",
            "category": "SRE Operations",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "SRE Snapshot: Air-Gapped SQLite WAL Backup & Integrity Check",
            "badge": "SRE SNAPSHOT",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Regression Sentinel",
            "description": "Creates an immediate cryptographic backup of the unified workforce database before any client handover or update.",
            "body": (
                "SQLite WAL Backup Execution:\n"
                "• Database Path: data/nexus_workforce.db\n"
                "• Integrity Check: PASS (Zero corruption detected)\n"
                "• Snapshot Created: .shadow_bak/nexus_workforce_snapshot.bak\n"
                "• Status: Air-gapped restore point secured."
            ),
            "callouts": ["Air-Gapped Backup", "Zero Corruption Verified", "Instant Restore Point"],
            "cta_label": "Create Instant Snapshot"
        },
        {
            "id": "ceo_14",
            "title": "🗺️ Q4 White-Label Expansion & Enterprise Scaling Roadmap",
            "category": "Roadmap Strategy",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Q4 Execution Plan: Scaling Turnkey Software Deployments",
            "badge": "ROADMAP AUDIT",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Executive Cockpit",
            "description": "Reviews milestones for expanding turnkey software offerings across Mauritius and regional Indian Ocean markets.",
            "body": (
                "Q4 Strategic Roadmap:\n"
                "1. Target: Secure 5 enterprise white-label turnkey clients (Medical 360 / Enn Rev Enn Sourir).\n"
                "2. Maintenance Annuity Target: Rs 75,000/mo in recurring yearly maintenance contracts.\n"
                "3. Operational Goal: Maintain sub-48-hour white-label handover turnaround.\n"
                "• Status: Execution on track."
            ),
            "callouts": ["5 Enterprise Targets", "Recurring Maintenance Annuity", "Sub-48h Handover"],
            "cta_label": "Review Roadmap"
        },
        {
            "id": "ceo_15",
            "title": "💼 Key Account Retention & White-Label Onboarding Review",
            "category": "Client Retention",
            "urgency": "High",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Founder-to-Client Onboarding & White-Label Handoff Check-In",
            "badge": "CLIENT ONBOARDING",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "New Turnkey Software Client",
            "description": "Personalized onboarding message confirming full source code handover, domain mapping, and maintenance schedule.",
            "body": (
                "Dear [Client Director],\n\n"
                "Welcome to your newly deployed white-label platform. Your full source code, IP transfer documentation, and admin credentials are now active.\n\n"
                "Our team is standing by to ensure smooth adoption. My direct WhatsApp line is +230 58169420.\n\n"
                "Sincerely,\nDeven Pawaray, Managing Principal"
            ),
            "callouts": ["Full Source Code Handover", "Direct WhatsApp Line", "White-Glove Welcome"],
            "cta_label": "Send Onboarding Welcome"
        },
        {
            "id": "ceo_16",
            "title": "🏦 Mauritius Banking Ecosystem & MCB Integration Strategy",
            "category": "Banking Strategy",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Institutional Memo: Expanding MCB Juice & Bank API Workflows",
            "badge": "BANKING STRATEGY",
            "gradient": "linear-gradient(135deg, #d97706 0%, #78350f 100%)",
            "target_audience": "Banking & Fintech Partners",
            "description": "Strategy memo outlining automated payment reconciliation via MCB Juice (+230 58169420) and MCB Account (000443260370).",
            "body": (
                "Institutional Fintech Strategy:\n\n"
                "Nexus leverages Mauritian banking rails (MCB Juice and direct bank transfers) to achieve instant, zero-fee payment settlement for turnkey software deployments.\n\n"
                "Goal: Standardize automated verification for all local B2B software sales."
            ),
            "callouts": ["MCB Juice Integration", "Zero-Fee Settlement", "Standardized B2B Rail"],
            "cta_label": "Dispatch Strategy Memo"
        },
        {
            "id": "ceo_17",
            "title": "📈 Stakeholder & Advisory Board Monthly Financial Report",
            "category": "Investor Relations",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Executive Stakeholder Briefing: White-Label Sales & Unit Economics",
            "badge": "STAKEHOLDER BRIEF",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Advisors & Stakeholders",
            "description": "Detailed monthly financial update highlighting white-label turnkey revenue, maintenance annuities, and unit economics.",
            "body": (
                "Monthly Stakeholder Briefing:\n"
                "• Upfront White-Label Inflows: Verified\n"
                "• Annual Maintenance Annuity Pipeline: Growing\n"
                "• Operating Expenses: $11.20 USD (99% Margin)\n"
                "• Status: Exceptional capital efficiency and growth."
            ),
            "callouts": ["White-Label Inflows", "Maintenance Annuities", "99% Operating Margin"],
            "cta_label": "Send Stakeholder Brief"
        },
        {
            "id": "ceo_18",
            "title": "🤖 Autonomous Agent Swarm Coordination & Task Allocation",
            "category": "Fleet Ops",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Swarm Coordination: Synchronizing Lead Finder & Outreach Agents",
            "badge": "SWARM ORCHESTRATION",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0c4a6e 100%)",
            "target_audience": "Agent Mesh",
            "description": "Optimizes multi-agent task execution to ensure 100% synchronization across B2B outreach and billing pipelines.",
            "body": (
                "Swarm Orchestration Status:\n"
                "• Lead Finder Agent: Scanning Mauritius clinic and NGO registers\n"
                "• Outreach Agent: Dispatched bilingual proposal drafts\n"
                "• Finance Watchdog: Standing by for invoice reconciliation\n"
                "• Status: Swarm operating at peak efficiency."
            ),
            "callouts": ["Multi-Agent Sync", "Automated Prospecting", "Peak Efficiency"],
            "cta_label": "Coordinate Swarm"
        },
        {
            "id": "ceo_19",
            "title": "📜 Data Sovereignty & Mauritius DPA 2017 Compliance Audit",
            "category": "Legal Compliance",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Legal Compliance Audit: Mauritius Data Protection Act 2017 & GDPR",
            "badge": "DPA 2017 COMPLIANCE",
            "gradient": "linear-gradient(135deg, #15803d 0%, #166534 100%)",
            "target_audience": "Compliance Watchdog",
            "description": "Verifies strict adherence to Mauritian data protection laws, suppression registries, and consent tracking.",
            "body": (
                "Data Protection Audit (Mauritius DPA 2017):\n"
                "• Local Storage: 100% SQLite WAL local persistence (zero third-party data hoarding)\n"
                "• Consent Tracking: Active suppression registry operational\n"
                "• Opt-Out Handling: Automatic 24-hour removal compliance\n"
                "• Status: 100% Legally Compliant."
            ),
            "callouts": ["Maur Mauritius DPA 2017", "Local SQLite Persistence", "100% Compliant"],
            "cta_label": "Run Compliance Audit"
        },
        {
            "id": "ceo_20",
            "title": "🚨 Emergency Master Kill Switch & Failsafe Simulation",
            "category": "Safety Ops",
            "urgency": "Urgent",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Safety Protocol: Emergency Master Kill Switch Test",
            "badge": "KILL SWITCH TEST",
            "gradient": "linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%)",
            "target_audience": "System Safety Watchdog",
            "description": "Simulates immediate system-wide agent suspension and state persistence under emergency conditions.",
            "body": (
                "Emergency Kill Switch Test:\n"
                "• Signal Received: Immediate agent pause\n"
                "• Response Time: 35ms\n"
                "• State Persistence: Saved to SQLite WAL\n"
                "• Status: Failsafe verified."
            ),
            "callouts": ["35ms Instant Pause", "SQLite State Persistence", "Failsafe Verified"],
            "cta_label": "Test Kill Switch"
        },
        {
            "id": "ceo_21",
            "title": "📦 White-Label Enterprise Handover Package Assembly",
            "category": "Product Delivery",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Assembly Line: Preparing Complete White-Label Client Handoff",
            "badge": "HANDOVER ASSEMBLY",
            "gradient": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
            "target_audience": "Engineering Lead",
            "description": "Bundles frontend portal, backend admin engine, source code repository, and deployment documentation for client transfer.",
            "body": (
                "White-Label Handover Package:\n"
                "• Frontend Portal (Bait): Included\n"
                "• Backend & Admin Engine (+33%): Included\n"
                "• Source Code Repository & IP Docs: Included\n"
                "• Annual Maintenance Contract (Rs 15,000/yr): Configured\n"
                "• Status: Package ready for secure transfer."
            ),
            "callouts": ["Complete Source Code", "IP Transfer Docs", "Maintenance Setup"],
            "cta_label": "Assemble Handover Package"
        },
        {
            "id": "ceo_22",
            "title": "🎥 Client Video Testimonial & Case Study Briefing",
            "category": "Case Study",
            "urgency": "Standard",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Testimonial Request: Documenting Turnkey Software Success",
            "badge": "TESTIMONIAL REQUEST",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #075985 100%)",
            "target_audience": "Satisfied Turnkey Client",
            "description": "Polite outreach requesting a brief video testimonial on how the white-label platform transformed their operations.",
            "body": (
                "Dear [Client Director],\n\n"
                "Now that your white-label platform is fully operational, would you be open to recording a brief 60-second video sharing your experience with Nexus?\n\n"
                "Your success story helps us showcaseMauritian technical excellence.\n\n"
                "Warm regards,\nDeven Pawaray"
            ),
            "callouts": ["High-Value Social Proof", "Showcases Mauritian Innovation", "Polite Request"],
            "cta_label": "Request Testimonial"
        },
        {
            "id": "ceo_23",
            "title": "📊 12-Month Financial Projections & Maintenance Annuity Forecast",
            "category": "Financial Modeling",
            "urgency": "Standard",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Financial Model: 12-Month Turnkey Sales & Maintenance Annuities",
            "badge": "FINANCIAL FORECAST",
            "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            "target_audience": "Executive Cockpit",
            "description": "Projects annual revenue combining upfront white-label IP fees (Rs 105k-117k) and recurring yearly maintenance packages (Rs 15k/yr).",
            "body": (
                "12-Month Financial Projection Model:\n"
                "• Upfront White-Label Sales (4 Clients): Rs 440,000 MUR\n"
                "• Annual Maintenance Annuities (4 Clients x Rs 15,000): Rs 60,000 MUR / year recurring\n"
                "• Operating Expenses: $135 total cloud/server cost\n"
                "• Net Profit Margin: 98.8%\n"
                "• Status: Highly scalable annuity model."
            ),
            "callouts": ["Upfront IP Fees", "Recurring Maintenance Annuities", "98.8% Net Margin"],
            "cta_label": "Generate Forecast"
        },
        {
            "id": "ceo_24",
            "title": "🍽️ VIP Founder Networking & Mauritius Tech Leadership Dinner",
            "category": "Networking",
            "urgency": "Low",
            "platform": "email_whatsapp",
            "task_type": "comms_draft",
            "headline": "Invitation: Executive Tech & Business Leaders Dinner (Cybercity)",
            "badge": "LEADERSHIP DINNER",
            "gradient": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
            "target_audience": "Mauritius Enterprise Leaders",
            "description": "Exclusive invitation for enterprise directors to discuss turnkey software adoption and autonomous operations.",
            "body": (
                "Dear [Director Name],\n\n"
                "You are cordially invited to an exclusive executive dinner in Cybercity next Wednesday to discuss the future of sovereign software automation in Mauritius.\n\n"
                "RSVP: +230 58169420.\n\n"
                "Warm regards,\nDeven Pawaray"
            ),
            "callouts": ["Exclusive Enterprise Invite", "Cybercity Venue", "High-Level Networking"],
            "cta_label": "Send Dinner Invite"
        },
        {
            "id": "ceo_25",
            "title": "🧠 J.A.R.V.I.S. Neural Core Memory & Sales Heuristic Tuning",
            "category": "Cognitive Ops",
            "urgency": "High",
            "platform": "system_ops",
            "task_type": "operations_task",
            "headline": "Neural Tune: Optimizing J.A.R.V.I.S. for White-Label Closing",
            "badge": "NEURAL TUNING",
            "gradient": "linear-gradient(135deg, #00f0ff 0%, #0284c7 100%)",
            "target_audience": "J.A.R.V.I.S. Neural Core",
            "description": "Fine-tunes J.A.R.V.I.S. cognitive weights to prioritize high-ticket white-label pitching and MCB Juice payment verification.",
            "body": (
                "J.A.R.V.I.S. Neural Core Fine-Tuning:\n"
                "• Objective: Maximize white-label turnkey closing efficiency\n"
                "• Heuristics Updated: Frontend bait + 33% backend premium positioning\n"
                "• Payment Rails: MCB Juice (+230 58169420) & Base L2 verified\n"
                "• Latency: Sub-40ms response time.\n"
                "• Status: Neural core fully optimized for revenue generation."
            ),
            "callouts": ["White-Label Closing Heuristics", "Sub-40ms Latency", "100% Revenue Optimized"],
            "cta_label": "Tune Neural Core"
        }
    ]
}


def get_all_scenarios() -> Dict[str, List[Dict[str, Any]]]:
    """Returns the complete library of all 125 scenarios grouped by user type."""
    return DAILY_SCENARIOS


def get_scenarios_for_user_type(user_type: str) -> List[Dict[str, Any]]:
    """Returns the 25 scenarios specifically for the requested user type."""
    key = user_type.lower().strip()
    if key in ["comms", "communications"]:
        return DAILY_SCENARIOS["comms"]
    elif key in ["operations", "ops"]:
        return DAILY_SCENARIOS["operations"]
    elif key in ["commerce", "treasury", "sales"]:
        return DAILY_SCENARIOS["commerce"]
    elif key in ["research", "intel", "intelligence"]:
        return DAILY_SCENARIOS["research"]
    elif key in ["ceo", "executive", "marketing", "social"]:
        return DAILY_SCENARIOS["ceo"]
    return DAILY_SCENARIOS.get(key, DAILY_SCENARIOS["ceo"])


def get_scenario_by_id(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Finds a single scenario by its unique ID across all user types."""
    for user_type, scenarios in DAILY_SCENARIOS.items():
        for sc in scenarios:
            if sc["id"] == scenario_id:
                return {**sc, "user_type": user_type}
    return None
