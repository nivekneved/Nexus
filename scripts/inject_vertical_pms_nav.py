# -*- coding: utf-8 -*-
"""
Nexus™ Nav Injection Script for 14 Vertical PMs Page
====================================================
Injects '👔 14 Vertical PMs' navigation link into the sidebar of all HTML files in the static directory.
"""

import os
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

PM_NAV_SNIPPET = """          <a href="/vertical-pms" class="nav-item" title="14 Vertical Project Managers & Lead Swarm">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <span>👔 14 Vertical PMs</span>
          </a>"""

def inject_pm_nav():
    count = 0
    for html_file in STATIC_DIR.glob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if "/vertical-pms" not in content:
            target = '<a href="/emailing"'
            if target in content:
                content = content.replace(target, PM_NAV_SNIPPET + "\n" + target)
                html_file.write_text(content, encoding="utf-8")
                print(f"[InjectPM] Added 14 Vertical PMs nav to {html_file.name}")
                count += 1
            else:
                target2 = '<button class="nav-item" data-tab="emailing"'
                if target2 in content:
                    btn_snippet = """          <button class="nav-item" data-tab="vertical-pms" onclick="window.location.href='/vertical-pms'" title="14 Vertical PMs">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <span>👔 14 Vertical PMs</span>
          </button>"""
                    content = content.replace(target2, btn_snippet + "\n" + target2)
                    html_file.write_text(content, encoding="utf-8")
                    print(f"[InjectPM] Added 14 Vertical PMs nav to {html_file.name}")
                    count += 1
    print(f"[InjectPM] Successfully injected 14 Vertical PMs nav into {count} static files.")

if __name__ == "__main__":
    inject_pm_nav()
