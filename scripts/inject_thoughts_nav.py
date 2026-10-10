# -*- coding: utf-8 -*-
"""
Nexus™ Nav Injection Script for Agent Thoughts Page
===================================================
Injects '🧠 Agent Thoughts' navigation link into the sidebar of all HTML files in the static directory.
"""

import os
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

THOUGHTS_NAV_SNIPPET = """          <a href="/agent-thoughts" class="nav-item" title="Live Agent Thoughts & Cognitive Stream">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M12 2a10 10 0 0 1 7.54 16.63L20 22l-3.37-.54A10 10 0 1 1 12 2z"/></svg>
            <span>🧠 Agent Thoughts</span>
          </a>"""

def inject_thoughts_nav():
    count = 0
    for html_file in STATIC_DIR.glob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if "/agent-thoughts" not in content:
            target = '<a href="/revenue"'
            if target in content:
                content = content.replace(target, THOUGHTS_NAV_SNIPPET + "\n" + target)
                html_file.write_text(content, encoding="utf-8")
                print(f"[InjectThoughts] Added Agent Thoughts nav to {html_file.name}")
                count += 1
            else:
                target2 = '<button class="nav-item" data-tab="revenue"'
                if target2 in content:
                    btn_snippet = """          <button class="nav-item" data-tab="agent-thoughts" onclick="window.location.href='/agent-thoughts'" title="Agent Thoughts">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M12 2a10 10 0 0 1 7.54 16.63L20 22l-3.37-.54A10 10 0 1 1 12 2z"/></svg>
            <span>🧠 Agent Thoughts</span>
          </button>"""
                    content = content.replace(target2, btn_snippet + "\n" + target2)
                    html_file.write_text(content, encoding="utf-8")
                    print(f"[InjectThoughts] Added Agent Thoughts nav to {html_file.name}")
                    count += 1
    print(f"[InjectThoughts] Successfully injected Agent Thoughts nav into {count} static files.")

if __name__ == "__main__":
    inject_thoughts_nav()
