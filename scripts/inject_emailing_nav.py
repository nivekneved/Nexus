# -*- coding: utf-8 -*-
"""
Nexus™ Nav Injection Script for Emailing Page
=============================================
Injects '✉️ Emailing' navigation link into the sidebar of all HTML files in the static directory.
"""

import os
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

EMAIL_NAV_SNIPPET = """          <a href="/emailing" class="nav-item" title="Mass Emailing & Campaigns">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <span>✉️ Emailing</span>
          </a>"""

def inject_emailing_nav():
    count = 0
    for html_file in STATIC_DIR.glob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if "/emailing" not in content:
            target = '<a href="/ports"'
            if target in content:
                content = content.replace(target, EMAIL_NAV_SNIPPET + "\n" + target)
                html_file.write_text(content, encoding="utf-8")
                print(f"[InjectEmailing] Added Emailing nav to {html_file.name}")
                count += 1
            else:
                target2 = '<button class="nav-item" data-tab="ports"'
                if target2 in content:
                    btn_snippet = """          <button class="nav-item" data-tab="emailing" onclick="window.location.href='/emailing'" title="Mass Emailing">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <span>✉️ Emailing</span>
          </button>"""
                    content = content.replace(target2, btn_snippet + "\n" + target2)
                    html_file.write_text(content, encoding="utf-8")
                    print(f"[InjectEmailing] Added Emailing nav to {html_file.name}")
                    count += 1
    print(f"[InjectEmailing] Successfully injected Emailing nav into {count} static files.")

if __name__ == "__main__":
    inject_emailing_nav()
