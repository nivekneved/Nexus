import os
import re

STATIC_DIR = r"C:\Users\deven\OneDrive\Desktop\Agents\static"

NEW_NAV = """      <nav class="nav-menu" id="mainNavMenu">

        <div class="nav-section-header" style="cursor: default;">
          <span class="nav-section-title">Nexus Money Machine</span>
        </div>

        <div class="nav-collapsible" style="display: flex; flex-direction: column; gap: 4px;">
          <!-- 1. Seek -->
          <a href="/seek" class="nav-item" id="navItemSeek" title="Seek Clients & Leads">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4f46e5" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <span>1. Seek (Scout & OSINT)</span>
          </a>

          <!-- 2. Connect -->
          <a href="/connect" class="nav-item" id="navItemConnect" title="Connect & Engage with Leads">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <span>2. Connect (Omnichannel)</span>
            <span style="margin-left: auto; font-size: 0.65rem; font-weight: 800; background: #0284c7; color: #fff; padding: 1px 7px; border-radius: 10px;">Live</span>
          </a>

          <!-- 3. Propose -->
          <a href="/operations" class="nav-item" id="navItemPropose" title="Make Propositions to Clients">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>
            <span>3. Propose</span>
          </a>

          <!-- 4. Sell -->
          <a href="/commerce" class="nav-item" id="navItemSell" title="Selling Tools & Storefronts">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2"><path d="M20 7H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            <span>4. Sell</span>
          </a>

          <!-- 5. Quote & Invoice -->
          <a href="/workforce" class="nav-item" id="navItemInvoice" title="Quote & Invoice">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 14l2 2 4-4"/></svg>
            <span>5. Quote & Invoice</span>
          </a>

          <a href="/store" target="_blank" class="nav-item" id="navItemStore" title="Open Digital Micro-Store" style="text-decoration: none; color: inherit;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
            <span>🛒 Digital Store</span>
            <span style="margin-left: auto; font-size: 0.65rem; font-weight: 800; background: #0284c7; color: #fff; padding: 1px 7px; border-radius: 10px;">$1-$99</span>
          </a>

          <a href="/revenue" class="nav-item" id="navItemRevenueCockpit" title="Conversion Funnel">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            <span>📈 Revenue & Funnel</span>
          </a>
        </div>

        <div class="nav-section-header" style="cursor: pointer; margin-top: 14px; border-top: 1px solid var(--border-subtle); padding-top: 10px;" id="navExtrasHeader" onclick="const g=document.getElementById('navGroupExtras'); const c=document.getElementById('extrasChevron'); if(g.style.display==='none'){g.style.display='flex'; c.innerHTML='&#9662;';}else{g.style.display='none'; c.innerHTML='&#9656;';}">
          <span class="nav-section-title" style="display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem;">
            <span>6. Extras & Advanced Tools</span>
            <span id="extrasChevron" class="chevron">&#9662;</span>
          </span>
        </div>

        <div class="nav-collapsible" id="navGroupExtras" style="display: none; flex-direction: column; gap: 4px; margin-top: 4px;">
          <a href="/agent-thoughts" class="nav-item" title="Live Agent Thoughts">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M12 2a10 10 0 0 1 7.54 16.63L20 22l-3.37-.54A10 10 0 1 1 12 2z"/></svg>
            <span>🧠 Agent Thoughts</span>
          </a>
          <a href="/autopilot" class="nav-item" id="navItemAutopilot" title="24/7 Night Shift Autopilot">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            <span>🌙 24/7 Autopilot</span>
          </a>
          <a href="/terminal" class="nav-item" id="navItemTerminal" title="Activity Feed">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            <span>📋 Activity Feed</span>
          </a>
          <a href="/addons" class="nav-item" id="navItemAddons" title="Security Fortress & Addons">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span>🛡️ Security Fortress</span>
          </a>
          <a href="/emailing" class="nav-item" title="Mass Emailing & Campaigns">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <span>✉️ Mass Emailing</span>
          </a>
          <a href="/sovereign" class="nav-item" id="navItemSovereign" title="Sovereign Core">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M20.24 12.24a6 6 0 0 0-8.48-8.48L5 10.5V19h8.5l6.74-6.76z"/><line x1="16" y1="8" x2="2" y2="22"/></svg>
            <span>🫀 Sovereign Soul</span>
          </a>
        </div>
      </nav>"""

nav_pattern = re.compile(r'<nav class="nav-menu" id="mainNavMenu">.*?</nav>', re.DOTALL)

count = 0
for file in os.listdir(STATIC_DIR):
    if file.endswith('.html'):
        filepath = os.path.join(STATIC_DIR, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if '<nav class="nav-menu" id="mainNavMenu">' in content:
            new_content = nav_pattern.sub(NEW_NAV, content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1

print(f"[ARGON MAX] UI Refactor Complete. Synchronized unified Connect Hub across {count} HTML interfaces.")
