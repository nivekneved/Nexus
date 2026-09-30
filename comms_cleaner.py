import re

try:
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Create the new CRM / Communications pane
    comms_replacement = """      <section class="tab-pane" id="pane-domain-comms">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
          <h2 style="font-size: 1.4rem; font-weight: 900; color: var(--text-main); margin:0;">CRM & Communications</h2>
          <button class="btn btn-primary" onclick="alert('Opening AI Email Studio...')" style="font-weight: 800; background: #0284c7;">
            ✉️ Compose AI Message ➔
          </button>
        </div>

        <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px;">

          <!-- Inbox & Active Chats -->
          <div class="card-panel" style="padding: 20px; min-height: 500px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle); padding-bottom: 12px; margin-bottom: 16px;">
              <h3 style="margin: 0; font-size: 1.1rem; font-weight: 800;">Multi-Channel Inbox</h3>
              <span class="badge" style="background: #e0f2fe; color: #0284c7;">2 Unread</span>
            </div>

            <div style="display: flex; flex-direction: column; gap: 12px;">
              <!-- Message 1 -->
              <div style="border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='#0284c7'" onmouseout="this.style.borderColor='var(--border-subtle)'">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                  <strong style="color: var(--text-main); font-size: 0.95rem;">Alain Wong (Clinique du Nord)</strong>
                  <span style="font-size: 0.75rem; color: #0284c7; font-weight: 700;">WhatsApp • 10m ago</span>
                </div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">
                  "Can we schedule the deployment of Medical 360 for next Tuesday?"
                </div>
                <div style="display: flex; gap: 8px;">
                  <button class="btn btn-secondary btn-sm" style="font-size: 0.7rem; padding: 4px 8px;">Reply with Dates</button>
                  <button class="btn btn-secondary btn-sm" style="font-size: 0.7rem; padding: 4px 8px;">Draft Invoice</button>
                </div>
              </div>

              <!-- Message 2 -->
              <div style="border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='#0284c7'" onmouseout="this.style.borderColor='var(--border-subtle)'">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                  <strong style="color: var(--text-main); font-size: 0.95rem;">Corinne Chung (Rogers Capital)</strong>
                  <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600;">Email • 2h ago</span>
                </div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">
                  "We have reviewed the CSR platform demo. Please send the commercial agreement."
                </div>
              </div>
            </div>
          </div>

          <!-- Client History & Timeline -->
          <div class="card-panel" style="padding: 20px; background: #f8fafc;">
            <h3 style="margin: 0 0 16px 0; font-size: 1.1rem; font-weight: 800;">Client Dossier & Timeline</h3>

            <!-- Selected Client Header -->
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0;">
              <div style="width: 40px; height: 40px; border-radius: 50%; background: #0284c7; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.2rem;">
                A
              </div>
              <div>
                <div style="font-weight: 800; font-size: 1.05rem; color: #0f172a;">Alain Wong</div>
                <div style="font-size: 0.8rem; color: #64748b;">Clinique du Nord • Medical 360 Suite</div>
              </div>
            </div>

            <!-- Timeline -->
            <div style="position: relative; padding-left: 20px;">
              <!-- Timeline Line -->
              <div style="position: absolute; left: 6px; top: 8px; bottom: 0; width: 2px; background: #cbd5e1;"></div>

              <div style="position: relative; margin-bottom: 16px;">
                <div style="position: absolute; left: -20px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: #10b981; border: 2px solid #fff;"></div>
                <div style="font-size: 0.75rem; color: #64748b; font-weight: 700; margin-bottom: 2px;">Today, 09:15 AM</div>
                <div style="font-size: 0.85rem; color: #334155;"><strong>Payment Received:</strong> Rs 45,000 (Juice)</div>
              </div>

              <div style="position: relative; margin-bottom: 16px;">
                <div style="position: absolute; left: -20px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: #3b82f6; border: 2px solid #fff;"></div>
                <div style="font-size: 0.75rem; color: #64748b; font-weight: 700; margin-bottom: 2px;">Yesterday, 14:20 PM</div>
                <div style="font-size: 0.85rem; color: #334155;"><strong>Demo Sent:</strong> Medical 360 Custom Preview</div>
              </div>

              <div style="position: relative;">
                <div style="position: absolute; left: -20px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: #cbd5e1; border: 2px solid #fff;"></div>
                <div style="font-size: 0.75rem; color: #64748b; font-weight: 700; margin-bottom: 2px;">Sept 25, 2026</div>
                <div style="font-size: 0.85rem; color: #334155;"><strong>Lead Captured:</strong> Via Hidden Boards Scraper</div>
              </div>
            </div>

            <button class="btn btn-secondary" style="width: 100%; margin-top: 24px; font-weight: 700; font-size: 0.8rem;">
              View Full History / Edit Details
            </button>
          </div>

        </div>
      </section>"""

    comms_pattern = re.compile(r'<section class="tab-pane" id="pane-domain-comms">.*?</section>\s*(?=<!-- TAB)', re.DOTALL)
    html = comms_pattern.sub(comms_replacement + "\n", html)

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Comms pane consolidated successfully!")

except Exception as e:
    print(f"Error: {e}")