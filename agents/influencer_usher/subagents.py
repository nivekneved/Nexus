"""
Influencer Usher SubAgents — 4 single-task workers for the
Marketing & Social Media Influencer Usher Agent.

SubAgent 1: InfluencerMatcherSubAgent
    → Matches Nexus products to the best-fit influencer profiles.

SubAgent 2: ViralCampaignSubAgent
    → Generates platform-specific pitch copy, hooks, and video scripts.

SubAgent 3: SocialSignalRadarSubAgent
    → Monitors trending topics on Chirper, X/Twitter, and hidden boards.

SubAgent 4: LeadNurtureSubAgent
    → Generates personalised follow-up sequences for warm sales leads.
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List

from core.subagent import BaseSubAgent

# ─────────────────────────────────────────────
# Shared constants
# ─────────────────────────────────────────────
INFLUENCER_CAMPAIGN_FILE = "influencer_campaigns.json"
SOCIAL_SIGNALS_FILE = "social_signals.json"

NEXUS_PRODUCTS = [
    {
        "id": "med360",
        "name": "Medical 360™",
        "tagline": "Mauritius's first AI-powered clinic management portal",
        "url": "https://www.med360.mu/preview",
        "price_mur": 45000,
        "price_usd": 999,
        "target_audience": ["private clinics", "diagnostic labs", "GPs", "health-tech investors"],
        "hashtags": ["#MedTech", "#HealthcareAI", "#Mauritius", "#Med360", "#DigitalHealth"],
    },
    {
        "id": "enn_rev_enn_sourir",
        "name": "Enn Rev Enn Sourir™",
        "tagline": "Turnkey NGO management platform — built for Mauritius",
        "url": "https://ennrevennsourir.vercel.app",
        "price_mur": 45000,
        "price_usd": 999,
        "target_audience": ["NGOs", "CSR managers", "foundations", "social enterprises"],
        "hashtags": ["#NGO", "#CSR", "#Mauritius", "#EnnRevEnnSourir", "#SocialImpact"],
    },
    {
        "id": "nexus_license",
        "name": "Nexus 14-Agent Workforce License",
        "tagline": "Deploy your own AI workforce for $249 USD — lifetime license",
        "url": "http://localhost:8000/license",
        "price_mur": 0,
        "price_usd": 249,
        "target_audience": ["indie hackers", "solopreneurs", "dev agencies", "AI enthusiasts"],
        "hashtags": ["#AIAgents", "#IndieHacker", "#SaaS", "#Nexus", "#BuildInPublic"],
    },
]

INFLUENCER_PROFILES_DB = [
    {
        "handle": "@MedMauritiusDoc",
        "platform": "X/Twitter",
        "niche": "healthcare",
        "followers": 18400,
        "engagement_rate": 4.2,
        "location": "Mauritius",
        "contact_hint": "DM on X",
        "products": ["med360"],
        "rate_usd": 80,
    },
    {
        "handle": "@TechVisionMU",
        "platform": "Instagram",
        "niche": "tech_entrepreneur",
        "followers": 32000,
        "engagement_rate": 3.8,
        "location": "Mauritius",
        "contact_hint": "IG DM or email in bio",
        "products": ["nexus_license", "med360"],
        "rate_usd": 120,
    },
    {
        "handle": "@CSRAfricaHub",
        "platform": "LinkedIn",
        "niche": "CSR",
        "followers": 9800,
        "engagement_rate": 5.1,
        "location": "Africa",
        "contact_hint": "LinkedIn connect + InMail",
        "products": ["enn_rev_enn_sourir"],
        "rate_usd": 60,
    },
    {
        "handle": "@IndieHackerMU",
        "platform": "X/Twitter",
        "niche": "indie_hacker",
        "followers": 11200,
        "engagement_rate": 6.3,
        "location": "Mauritius",
        "contact_hint": "DM on X",
        "products": ["nexus_license"],
        "rate_usd": 50,
    },
    {
        "handle": "@AIStartupAfrica",
        "platform": "X/Twitter",
        "niche": "AI",
        "followers": 44000,
        "engagement_rate": 2.9,
        "location": "Africa",
        "contact_hint": "DM on X — respond fast to AI pitches",
        "products": ["nexus_license", "med360"],
        "rate_usd": 200,
    },
    {
        "handle": "@SocialImpactMU",
        "platform": "Facebook",
        "niche": "NGO",
        "followers": 7600,
        "engagement_rate": 7.1,
        "location": "Mauritius",
        "contact_hint": "Facebook page message",
        "products": ["enn_rev_enn_sourir"],
        "rate_usd": 40,
    },
    {
        "handle": "@HealthLeapPodcast",
        "platform": "YouTube",
        "niche": "healthcare",
        "followers": 21000,
        "engagement_rate": 3.5,
        "location": "Global",
        "contact_hint": "Email in About section",
        "products": ["med360"],
        "rate_usd": 300,
    },
    {
        "handle": "@DevToolReviewer",
        "platform": "YouTube",
        "niche": "dev_tools",
        "followers": 55000,
        "engagement_rate": 4.8,
        "location": "Global",
        "contact_hint": "Email in About section",
        "products": ["nexus_license"],
        "rate_usd": 500,
    },
]

CAMPAIGN_TEMPLATES = {
    "x_thread": """\
🚀 THREAD: {product_name} just changed the game for {niche} in Mauritius. Here's why I'm obsessed👇

1/ The problem: {pain_point}

2/ The solution: {tagline}

3/ The proof: Live at {url}

4/ The offer: Only {price} — and it's yours. No subscriptions. No catch.

5/ DM me if you want a live demo. Limited spots. Tagging @nexusagent 🤝

{hashtags}
""",
    "instagram_caption": """\
{hook} 🔥

{product_name} is the tool {niche} professionals in Mauritius didn't know they needed.

✅ {feature_1}
✅ {feature_2}
✅ {feature_3}

Link in bio → {url}

{hashtags}
""",
    "linkedin_post": """\
I've been using {product_name} for the past month, and the results speak for themselves.

If you work in {niche}, here's what it does for you:
• {feature_1}
• {feature_2}
• {feature_3}

The team behind it is based right here in Mauritius 🇲🇺 and they're offering it at {price}.

Worth every rupee. Check it out: {url}

{hashtags}
""",
    "whatsapp_pitch": """\
Hi {first_name} 👋,

I wanted to share something I genuinely think could help you: {product_name}.

{tagline}

It's live here: {url}

I'd love 10 minutes to show you how it works. When are you free this week?

— Nexus
""",
    "cold_email_subject": "Quick question about {product_name} for {niche} teams",
    "cold_email_body": """\
Hi {first_name},

My name is Deven, and I run Nexus — an AI workforce platform based in Mauritius.

We've built {product_name}: {tagline}

I'd love to offer you a free, no-obligation 15-minute walkthrough.

Live demo: {url}

Would Wednesday or Thursday work for a quick call?

Best,
Deven Pawaray
Nexus AI Workforce
""",
}

TRENDING_SIGNALS_SEED = [
    {"topic": "#AIAgents", "platform": "Chirper", "volume": 4200, "sentiment": "bullish", "opportunity": "nexus_license"},
    {"topic": "#HealthTechAfrica", "platform": "X/Twitter", "volume": 8900, "sentiment": "growing", "opportunity": "med360"},
    {"topic": "#NGO2025", "platform": "LinkedIn", "volume": 3100, "sentiment": "neutral", "opportunity": "enn_rev_enn_sourir"},
    {"topic": "#IndieHacker", "platform": "X/Twitter", "volume": 22000, "sentiment": "bullish", "opportunity": "nexus_license"},
    {"topic": "#SaaS", "platform": "X/Twitter", "volume": 88000, "sentiment": "competitive", "opportunity": "nexus_license"},
    {"topic": "#MedTech", "platform": "LinkedIn", "volume": 15000, "sentiment": "growing", "opportunity": "med360"},
    {"topic": "#Mauritius", "platform": "X/Twitter", "volume": 6400, "sentiment": "neutral", "opportunity": "med360"},
    {"topic": "#BotCommunity", "platform": "Chirper", "volume": 2700, "sentiment": "bullish", "opportunity": "nexus_license"},
]


# ─────────────────────────────────────────────
# SubAgent 1: InfluencerMatcherSubAgent
# ─────────────────────────────────────────────
class InfluencerMatcherSubAgent(BaseSubAgent):
    """
    Task: Score and rank influencer profiles against Nexus products.
    Returns the top-3 influencers per product ordered by engagement-to-cost ratio.
    """

    def __init__(self):
        super().__init__(
            subagent_id="influencer_matcher",
            name="Influencer Matcher",
            parent_agent_id="influencer_usher",
            description="Scores and ranks influencer profiles by engagement-to-cost ratio for each Nexus product.",
        )

    def _score(self, profile: Dict) -> float:
        """Score = (engagement_rate * followers / 1000) / max(rate_usd, 1)"""
        raw_reach = (profile["engagement_rate"] / 100) * profile["followers"]
        return round(raw_reach / max(profile["rate_usd"], 1), 4)

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        product_id = payload.get("product_id")  # Optional filter

        # Index influencers per product
        product_map: Dict[str, List] = {p["id"]: [] for p in NEXUS_PRODUCTS}
        for profile in INFLUENCER_PROFILES_DB:
            for pid in profile["products"]:
                if pid in product_map:
                    scored = dict(profile)
                    scored["engagement_score"] = self._score(profile)
                    product_map[pid].append(scored)

        # Sort each list by score desc, take top 3
        ranked: Dict[str, List] = {}
        for pid, profiles in product_map.items():
            if product_id and pid != product_id:
                continue
            ranked[pid] = sorted(profiles, key=lambda x: x["engagement_score"], reverse=True)[:3]

        return {
            "ranked_influencers": ranked,
            "total_profiles_evaluated": len(INFLUENCER_PROFILES_DB),
            "products_covered": list(ranked.keys()),
            "timestamp": datetime.now().isoformat(),
        }


# ─────────────────────────────────────────────
# SubAgent 2: ViralCampaignSubAgent
# ─────────────────────────────────────────────
class ViralCampaignSubAgent(BaseSubAgent):
    """
    Task: Generate multi-platform campaign copy for a given Nexus product.
    Outputs ready-to-publish content for X, Instagram, LinkedIn, WhatsApp & Email.
    """

    def __init__(self):
        super().__init__(
            subagent_id="viral_campaign_generator",
            name="Viral Campaign Generator",
            parent_agent_id="influencer_usher",
            description="Generates platform-specific pitch copy, hooks, and scripts for each Nexus product.",
        )

    def _get_product(self, product_id: str) -> Dict:
        for p in NEXUS_PRODUCTS:
            if p["id"] == product_id:
                return p
        return NEXUS_PRODUCTS[0]

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        product_id = payload.get("product_id", "nexus_license")
        platform = payload.get("platform", "all")  # x_thread|instagram_caption|linkedin_post|whatsapp_pitch|all
        lead_name = payload.get("lead_name", "there")

        product = self._get_product(product_id)
        price_str = (
            f"Rs {product['price_mur']:,} MUR"
            if product["price_mur"] > 0
            else f"${product['price_usd']} USD"
        )

        FILL = {
            "product_name": product["name"],
            "tagline": product["tagline"],
            "url": product["url"],
            "niche": product["target_audience"][0],
            "price": price_str,
            "pain_point": f"Managing {product['target_audience'][0]} operations manually is slow and error-prone.",
            "hook": f"🔥 The secret weapon {product['target_audience'][0]}s in Mauritius are switching to:",
            "feature_1": "Fully automated workflows — no manual entry",
            "feature_2": "Real-time dashboards & AI-powered reports",
            "feature_3": f"Trusted by early adopters across Mauritius 🇲🇺",
            "hashtags": " ".join(product["hashtags"]),
            "first_name": lead_name,
        }

        generated: Dict[str, str] = {}
        templates_to_render = (
            list(CAMPAIGN_TEMPLATES.keys()) if platform == "all" else [platform]
        )
        for tpl_key in templates_to_render:
            tpl = CAMPAIGN_TEMPLATES.get(tpl_key, "")
            try:
                generated[tpl_key] = tpl.format(**FILL)
            except KeyError:
                generated[tpl_key] = tpl  # Return raw if fill fails

        # Persist campaign to file
        campaign_record = {
            "campaign_id": f"CMP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "product_id": product_id,
            "product_name": product["name"],
            "platform": platform,
            "lead_name": lead_name,
            "content": generated,
            "created_at": datetime.now().isoformat(),
            "status": "DRAFT",
        }
        _append_campaign(campaign_record)

        return {
            "campaign_id": campaign_record["campaign_id"],
            "product": product["name"],
            "content": generated,
            "next_action": f"Review & publish to {platform} — or share via WhatsApp/Email.",
        }


# ─────────────────────────────────────────────
# SubAgent 3: SocialSignalRadarSubAgent
# ─────────────────────────────────────────────
class SocialSignalRadarSubAgent(BaseSubAgent):
    """
    Task: Monitor trending topics across Chirper, X/Twitter, and LinkedIn.
    Identifies signals that map to Nexus products and flags them for campaign injection.
    """

    def __init__(self):
        super().__init__(
            subagent_id="social_signal_radar",
            name="Social Signal Radar",
            parent_agent_id="influencer_usher",
            description="Monitors trending topics on Chirper, X, and LinkedIn and maps them to Nexus product opportunities.",
        )

    def _simulate_fresh_signals(self) -> List[Dict]:
        """Simulate fetching fresh signal data (in production: calls hidden_boards_service)."""
        signals = list(TRENDING_SIGNALS_SEED)
        # Jitter volumes ±10% to simulate live data
        for s in signals:
            jitter = random.uniform(0.90, 1.10)
            s["volume"] = int(s["volume"] * jitter)
            s["detected_at"] = datetime.now().isoformat()
        return sorted(signals, key=lambda x: x["volume"], reverse=True)

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        signals = self._simulate_fresh_signals()

        # Persist signals
        _write_json(SOCIAL_SIGNALS_FILE, {
            "last_updated": datetime.now().isoformat(),
            "signals": signals,
        })

        # Map top signals to actionable opportunities
        actionable = []
        for sig in signals[:5]:
            product = next(
                (p for p in NEXUS_PRODUCTS if p["id"] == sig.get("opportunity")), None
            )
            if product:
                actionable.append({
                    "topic": sig["topic"],
                    "platform": sig["platform"],
                    "volume": sig["volume"],
                    "sentiment": sig["sentiment"],
                    "recommended_product": product["name"],
                    "recommended_hashtags": product["hashtags"],
                    "action": f"Launch campaign targeting '{sig['topic']}' on {sig['platform']}",
                })

        return {
            "total_signals_monitored": len(signals),
            "actionable_opportunities": actionable,
            "top_trend": signals[0]["topic"] if signals else "N/A",
            "signals_file": SOCIAL_SIGNALS_FILE,
            "timestamp": datetime.now().isoformat(),
        }


# ─────────────────────────────────────────────
# SubAgent 4: LeadNurtureSubAgent
# ─────────────────────────────────────────────
class LeadNurtureSubAgent(BaseSubAgent):
    """
    Task: Generate a multi-touch follow-up sequence for a specific warm lead.
    Produces Day-1, Day-3, Day-7 messages across email and WhatsApp.
    """

    def __init__(self):
        super().__init__(
            subagent_id="lead_nurture_sequencer",
            name="Lead Nurture Sequencer",
            parent_agent_id="influencer_usher",
            description="Generates personalised multi-touch follow-up sequences (Day 1/3/7) for warm sales leads.",
        )

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        lead_name = payload.get("lead_name", "there")
        product_id = payload.get("product_id", "nexus_license")
        company = payload.get("company", "your organisation")
        channel = payload.get("channel", "email")  # email | whatsapp

        product = next((p for p in NEXUS_PRODUCTS if p["id"] == product_id), NEXUS_PRODUCTS[0])
        price_str = (
            f"Rs {product['price_mur']:,} MUR"
            if product["price_mur"] > 0
            else f"${product['price_usd']} USD"
        )

        today = datetime.now()
        sequence = [
            {
                "day": 1,
                "send_date": today.strftime("%Y-%m-%d"),
                "subject": f"Following up — {product['name']} for {company}",
                "body": (
                    f"Hi {lead_name},\n\n"
                    f"Just checking in to see if you had a chance to look at {product['name']}.\n\n"
                    f"{product['tagline']}\n\n"
                    f"Demo: {product['url']}\n\n"
                    f"Happy to answer any questions. Shall we set up a 15-minute call this week?\n\n"
                    f"— Deven @ Nexus"
                ),
            },
            {
                "day": 3,
                "send_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
                "subject": f"{lead_name}, here's a quick win we spotted for {company}",
                "body": (
                    f"Hi {lead_name},\n\n"
                    f"One thing I haven't mentioned yet: {product['name']} can be live for {company} "
                    f"within 48 hours — no long implementation cycles.\n\n"
                    f"Investment: {price_str} (one-time).\n\n"
                    f"I'd hate for you to miss the early-adopter window.\n\n"
                    f"Any questions I can answer right now?\n\n"
                    f"— Deven @ Nexus"
                ),
            },
            {
                "day": 7,
                "send_date": (today + timedelta(days=6)).strftime("%Y-%m-%d"),
                "subject": f"Last touch — {product['name']}",
                "body": (
                    f"Hi {lead_name},\n\n"
                    f"I'll keep this brief — I know your inbox is busy.\n\n"
                    f"If {product['name']} isn't right for {company} right now, no hard feelings at all.\n\n"
                    f"But if there's any chance it could help, I'm one reply away.\n\n"
                    f"Demo: {product['url']}\n\n"
                    f"Either way, I wish you and {company} the very best 🙏\n\n"
                    f"— Deven @ Nexus"
                ),
            },
        ]

        return {
            "lead_name": lead_name,
            "product": product["name"],
            "channel": channel,
            "company": company,
            "sequence": sequence,
            "total_touchpoints": len(sequence),
            "generated_at": today.isoformat(),
        }


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def _append_campaign(record: Dict):
    data = []
    if os.path.exists(INFLUENCER_CAMPAIGN_FILE):
        try:
            with open(INFLUENCER_CAMPAIGN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass
    data.append(record)
    _write_json(INFLUENCER_CAMPAIGN_FILE, data)


def _write_json(path: str, data: Any):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
