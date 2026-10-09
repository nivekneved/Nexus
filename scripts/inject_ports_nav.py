# -*- coding: utf-8 -*-
"""
Nexus™ Nav Injection Script for Ports Page
==========================================
Automatically injects the '🔍 Ports' navigation item into the sidebar menu
of all HTML files in the static directory.
"""

import os
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

PORTS_NAV_SNIPPET = """          <a href="/ports" class="nav-item" id="navItemPorts" title="Port Scanner & Network Recon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>🔍 Ports</span>
          </a>"""

def inject_nav():
    count = 0
    for html_file in STATIC_DIR.glob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if "/ports" not in content:
            # Find a good anchor in sidebar extras section (e.g., navItemSimulator or navItemAddons)
            target = '<a href="/simulator"'
            if target in content:
                new_content = content.replace(target, PORTS_NAV_SNIPPET + "\n" + target)
                html_file.write_text(new_content, encoding="utf-8")
                print(f"[InjectNav] Added Ports nav to {html_file.name}")
                count += 1
            else:
                target2 = '<a href="/addons"'
                if target2 in content:
                    new_content = content.replace(target2, PORTS_NAV_SNIPPET + "\n" + target2)
                    html_file.write_text(new_content, encoding="utf-8")
                    print(f"[InjectNav] Added Ports nav to {html_file.name}")
                    count += 1
    print(f"[InjectNav] Successfully injected Ports nav into {count} static files.")

if __name__ == "__main__":
    inject_nav()
