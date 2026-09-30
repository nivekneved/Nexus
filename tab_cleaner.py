import re

try:
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    menu_replacement = """      <nav class="nav-menu" id="mainNavMenu">

        <div class="nav-section-header" style="cursor: default;">
          <span class="nav-section-title">Nexus Control Hub</span>
        </div>

        <div class="nav-collapsible" style="display: flex; flex-direction: column; gap: 4px;">
          <!-- 1. CEO Cockpit -->
          <button class="nav-item active" data-tab="ceo-cockpit" id="navItemJarvisHQ" title="Solo Founder Dashboard">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4f46e5" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            <span>CEO Cockpit</span>
            <span style="margin-left: auto; font-size: 0.65rem; font-weight: 800; background: #4f46e5; color: #fff; padding: 1px 7px; border-radius: 10px;">HQ</span>
          </button>

          <!-- 2. CRM & Communications -->
          <button class="nav-item" data-tab="domain-comms" id="navItemComms" title="CRM & Communications">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <span>Communications (CRM)</span>
          </button>

          <!-- 3. Operations & Lead Gen -->
          <button class="nav-item" data-tab="domain-operations" id="navItemOps" title="Operations & Lead Generation">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            <span>Operations & Leads</span>
          </button>

          <!-- 4. Treasury & Markets -->
          <button class="nav-item" data-tab="domain-commerce" id="navItemCommerce" title="Treasury & Markets">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/><path d="M12 14v2"/><path d="M10 15h4"/></svg>
            <span>Treasury & Markets</span>
          </button>

          <!-- 5. System Ops & Fleet -->
          <button class="nav-item" data-tab="workforce" id="navItemWorkforce" title="Agent Workforce & Settings">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <span>Agent Workforce & Ops</span>
          </button>
        </div>
      </nav>"""

    nav_pattern = re.compile(r'<nav class="nav-menu" id="mainNavMenu">.*?</nav>', re.DOTALL)
    html = nav_pattern.sub(menu_replacement, html)

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Nav menu consolidated successfully!")

except Exception as e:
    print(f"Error: {e}")
