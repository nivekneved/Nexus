import re

try:
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Create the new Operations pane
    ops_replacement = """      <section class="tab-pane" id="pane-domain-operations">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
          <h2 style="font-size: 1.4rem; font-weight: 900; color: var(--text-main); margin:0;">Operations & Lead Generation</h2>
          <button class="btn btn-primary" style="font-weight: 800; background: #d97706;">
            🚀 Deploy New Campaign ➔
          </button>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">

          <!-- Lead Gathering Engine -->
          <div class="card-panel" style="padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle); padding-bottom: 12px; margin-bottom: 16px;">
              <h3 style="margin: 0; font-size: 1.1rem; font-weight: 800;">Autonomous Lead Scraper</h3>
              <span class="badge" style="background: #fef3c7; color: #b45309;">Active</span>
            </div>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 16px;">
              Extracts target leads from public databases (CBRD, LinkedIn, Google Maps).
            </p>

            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; margin-bottom: 16px;">
              <div style="font-weight: 700; font-size: 0.85rem; margin-bottom: 8px;">Run Extraction:</div>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <button class="btn btn-secondary btn-sm" style="font-size: 0.75rem;">Mauritius CBRD Registry</button>
                <button class="btn btn-secondary btn-sm" style="font-size: 0.75rem;">Google Maps (Clinics)</button>
                <button class="btn btn-secondary btn-sm" style="font-size: 0.75rem;">LinkedIn B2B</button>
              </div>
            </div>

            <!-- Recent Leads -->
            <h4 style="font-size: 0.9rem; font-weight: 700; margin: 0 0 10px 0;">Recently Extracted</h4>
            <div style="display: flex; flex-direction: column; gap: 8px; max-height: 200px; overflow-y: auto;">
              <div style="font-size: 0.8rem; padding: 8px; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; justify-content: space-between;">
                <span><strong>City Clinic</strong> (Port Louis)</span>
                <span style="color: #10b981;">MX Verified</span>
              </div>
              <div style="font-size: 0.8rem; padding: 8px; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; justify-content: space-between;">
                <span><strong>Apex Island Rentals</strong> (Plaine Magnien)</span>
                <span style="color: #10b981;">MX Verified</span>
              </div>
            </div>
          </div>

          <!-- Social Media & Post Creation -->
          <div class="card-panel" style="padding: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle); padding-bottom: 12px; margin-bottom: 16px;">
              <h3 style="margin: 0; font-size: 1.1rem; font-weight: 800;">Social Media War Room</h3>
              <span class="badge" style="background: #fdf2f8; color: #be185d;">Ghostwriter AI</span>
            </div>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 16px;">
              Generates platform-specific content to drive inbound leads.
            </p>

            <div style="margin-bottom: 16px;">
              <textarea class="form-input" rows="3" placeholder="What do you want to promote today? (e.g., 'We just launched the Medical 360 suite')" style="font-size: 0.85rem; width: 100%; box-sizing: border-box;"></textarea>
              <div style="display: flex; justify-content: flex-end; margin-top: 8px;">
                <button class="btn btn-secondary btn-sm" style="font-weight: 700;">✨ Auto-Draft Post</button>
              </div>
            </div>

            <!-- Scheduled / Active Campaigns -->
            <h4 style="font-size: 0.9rem; font-weight: 700; margin: 0 0 10px 0;">Active Campaigns</h4>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              <div style="font-size: 0.8rem; padding: 8px; border: 1px solid #e2e8f0; border-left: 3px solid #0284c7; border-radius: 6px;">
                <strong>LinkedIn:</strong> "Why Mauritius clinics need automation..." (Scheduled 14:00)
              </div>
              <div style="font-size: 0.8rem; padding: 8px; border: 1px solid #e2e8f0; border-left: 3px solid #10b981; border-radius: 6px;">
                <strong>WhatsApp Blast:</strong> Flight Addon Promotion (Running: 45/100 sent)
              </div>
            </div>

          </div>

        </div>
      </section>"""

    ops_pattern = re.compile(r'<section class="tab-pane" id="pane-domain-operations">.*?</section>\s*(?=<!-- TAB)', re.DOTALL)
    html = ops_pattern.sub(ops_replacement + "\n", html)

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Operations pane consolidated successfully!")

except Exception as e:
    print(f"Error: {e}")
