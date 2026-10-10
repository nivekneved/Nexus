# -*- coding: utf-8 -*-
"""
Nexus™ Nav Injection Script for Ports & DB Backup Pages
======================================================
Injects '🔍 Ports' and '💾 DB Backup & Restore' navigation links into the sidebar
of all HTML files in the static directory (including index.html).
"""

import os
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

NAV_SNIPPETS = [
    """          <a href="/ports" class="nav-item" title="Port Scanner & Network Recon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>🔍 Ports</span>
          </a>""",
    """          <a href="/db-backup" class="nav-item" title="Database Backup & Restore">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
            <span>💾 DB Backup & Restore</span>
          </a>"""
]

def inject_navs():
    count = 0
    for html_file in STATIC_DIR.glob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        modified = False

        if "/ports" not in content:
            target = '<a href="/simulator"'
            if target in content:
                content = content.replace(target, NAV_SNIPPETS[0] + "\n" + target)
                modified = True
            else:
                target2 = '<button class="nav-item" data-tab="simulator"'
                if target2 in content:
                    # For index.html which uses buttons
                    btn_snippet = """          <button class="nav-item" data-tab="ports" onclick="window.location.href='/ports'" title="Port Scanner">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <span>🔍 Ports</span>
          </button>"""
                    content = content.replace(target2, btn_snippet + "\n" + target2)
                    modified = True

        if "/db-backup" not in content:
            target = '<a href="/simulator"'
            if target in content:
                content = content.replace(target, NAV_SNIPPETS[1] + "\n" + target)
                modified = True
            else:
                target2 = '<button class="nav-item" data-tab="simulator"'
                if target2 in content:
                    btn_snippet2 = """          <button class="nav-item" data-tab="db-backup" onclick="window.location.href='/db-backup'" title="DB Backup & Restore">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
            <span>💾 DB Backup & Restore</span>
          </button>"""
                    content = content.replace(target2, btn_snippet2 + "\n" + target2)
                    modified = True

        if modified:
            html_file.write_text(content, encoding="utf-8")
            print(f"[InjectNavs] Added Ports & DB Backup navs to {html_file.name}")
            count += 1

    print(f"[InjectNavs] Successfully injected navs into {count} static files.")

if __name__ == "__main__":
    inject_navs()
