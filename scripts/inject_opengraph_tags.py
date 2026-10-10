# -*- coding: utf-8 -*-
"""
Nexus™ OpenGraph & Virality Tag Injection Script
================================================
Injects professional OpenGraph and Twitter card meta tags into all static HTML template files
to maximize social sharing virality and preview conversion rates.
"""

import os
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

OG_TAGS = """  <!-- OpenGraph & Social Virality Meta Tags -->
  property="og:title" content="Nexus™ — Sovereign AI Agent Workforce & Autonomous Commerce">
  <meta property="og:description" content="Deploy autonomous multi-agent sovereign software entities that self-fund compute via AI micro-ventures and live PayPal / Base L2 commerce.">
  <meta property="og:image" content="https://nexusbots-nu.vercel.app/static/nexus-banner.jpg">
  <meta property="og:url" content="https://nexusbots-nu.vercel.app">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Nexus™ — Sovereign AI Agent Workforce">
  <meta name="twitter:description" content="Autonomous multi-agent sovereign software entity powered by Gemini 2.5 SOTA reasoning.">"""

def inject_og():
    count = 0
    for html_file in STATIC_DIR.glob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if "og:title" not in content:
            if "</head>" in content:
                content = content.replace("</head>", OG_TAGS + "\n</head>")
                html_file.write_text(content, encoding="utf-8")
                print(f"[InjectOG] Added OpenGraph tags to {html_file.name}")
                count += 1
    print(f"[InjectOG] Successfully injected OpenGraph tags into {count} static files.")

if __name__ == "__main__":
    inject_og()
