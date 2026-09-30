import re

try:
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Apply cursor pointer and onclick functions to KPI cards
    html = html.replace('<div class="ceo-kpi-card" style="border-left: 4px solid #10b981;">',
                        '<div class="ceo-kpi-card" style="border-left: 4px solid #10b981; cursor: pointer; transition: transform 0.2s;" onclick="filterSalesTable(\'today\')" onmouseover="this.style.transform=\'scale(1.02)\'" onmouseout="this.style.transform=\'scale(1)\'">')
    html = html.replace('<div class="ceo-kpi-card" style="border-left: 4px solid #3b82f6;">',
                        '<div class="ceo-kpi-card" style="border-left: 4px solid #3b82f6; cursor: pointer; transition: transform 0.2s;" onclick="filterSalesTable(\'yesterday\')" onmouseover="this.style.transform=\'scale(1.02)\'" onmouseout="this.style.transform=\'scale(1)\'">')
    html = html.replace('<div class="ceo-kpi-card" style="border-left: 4px solid #8b5cf6;">',
                        '<div class="ceo-kpi-card" style="border-left: 4px solid #8b5cf6; cursor: pointer; transition: transform 0.2s;" onclick="filterSalesTable(\'week\')" onmouseover="this.style.transform=\'scale(1.02)\'" onmouseout="this.style.transform=\'scale(1)\'">')
    html = html.replace('<div class="ceo-kpi-card" style="border-left: 4px solid #f59e0b;">',
                        '<div class="ceo-kpi-card" style="border-left: 4px solid #f59e0b; cursor: pointer; transition: transform 0.2s;" onclick="filterSalesTable(\'all\')" onmouseover="this.style.transform=\'scale(1.02)\'" onmouseout="this.style.transform=\'scale(1)\'">')

    # Add Action column to the Sales table header
    html = html.replace('<th style="padding: 8px;">Status</th>', '<th style="padding: 8px;">Status</th>\n                  <th style="padding: 8px;">Action</th>')

    # Add Action buttons to the Sales table rows
    html = html.replace('<td style="padding: 12px 8px;"><span class="badge" style="background: #ecfdf5; color: #047857;">Paid (Juice)</span></td>\n                </tr>',
                        '<td style="padding: 12px 8px;"><span class="badge" style="background: #ecfdf5; color: #047857;">Paid (Juice)</span></td>\n                  <td style="padding: 12px 8px;"><button class="btn btn-secondary btn-sm" style="font-size:0.7rem; padding: 4px 8px;" onclick="viewInvoice(\'INV-001\')">👁️ View</button></td>\n                </tr>')
    html = html.replace('<td style="padding: 12px 8px;"><span class="badge" style="background: #eff6ff; color: #1d4ed8;">Paid (PayPal)</span></td>\n                </tr>',
                        '<td style="padding: 12px 8px;"><span class="badge" style="background: #eff6ff; color: #1d4ed8;">Paid (PayPal)</span></td>\n                  <td style="padding: 12px 8px;"><button class="btn btn-secondary btn-sm" style="font-size:0.7rem; padding: 4px 8px;" onclick="viewInvoice(\'INV-002\')">👁️ View</button></td>\n                </tr>')

    # Add Action buttons to Portfolio MRR cards
    html = html.replace('<div style="font-size: 0.85rem; font-weight: 800; color: #0284c7; margin-top: 6px;">$1,200/mo</div>\n            </div>',
                        '<div style="display:flex; justify-content:space-between; align-items:flex-end;"><div style="font-size: 0.85rem; font-weight: 800; color: #0284c7; margin-top: 6px;">$1,200/mo</div>\n            <div style="display:flex; gap:4px;"><button class="btn btn-secondary btn-sm" style="font-size:0.65rem; padding: 2px 6px;" onclick="alert(\'Managing Medical 360 SaaS\')">⚙️ Manage</button><button class="btn btn-secondary btn-sm" style="font-size:0.65rem; padding: 2px 6px;" onclick="alert(\'Broadcasting to Medical 360 clients\')">✉️ Broadcast</button></div></div>\n            </div>')
    html = html.replace('<div style="font-size: 0.85rem; font-weight: 800; color: #059669; margin-top: 6px;">$850/mo</div>\n            </div>',
                        '<div style="display:flex; justify-content:space-between; align-items:flex-end;"><div style="font-size: 0.85rem; font-weight: 800; color: #059669; margin-top: 6px;">$850/mo</div>\n            <div style="display:flex; gap:4px;"><button class="btn btn-secondary btn-sm" style="font-size:0.65rem; padding: 2px 6px;" onclick="alert(\'Managing i-Travellix\')">⚙️ Manage</button><button class="btn btn-secondary btn-sm" style="font-size:0.65rem; padding: 2px 6px;" onclick="alert(\'Broadcasting to i-Travellix clients\')">✉️ Broadcast</button></div></div>\n            </div>')
    html = html.replace('<div style="font-size: 0.85rem; font-weight: 800; color: #7c3aed; margin-top: 6px;">$500/mo</div>\n            </div>',
                        '<div style="display:flex; justify-content:space-between; align-items:flex-end;"><div style="font-size: 0.85rem; font-weight: 800; color: #7c3aed; margin-top: 6px;">$500/mo</div>\n            <div style="display:flex; gap:4px;"><button class="btn btn-secondary btn-sm" style="font-size:0.65rem; padding: 2px 6px;" onclick="alert(\'Managing WhatsApp AI Bot\')">⚙️ Manage</button><button class="btn btn-secondary btn-sm" style="font-size:0.65rem; padding: 2px 6px;" onclick="alert(\'Broadcasting to Bot subscribers\')">✉️ Broadcast</button></div></div>\n            </div>')

    # Add missing filterSalesTable and viewInvoice JS functions
    js_funcs = """
window.filterSalesTable = function(period) {
    alert("Filtering Sales Table for: " + period.toUpperCase());
    // Implementation can show/hide rows based on the period string
};

window.viewInvoice = function(invoiceId) {
    alert("Viewing " + invoiceId + "... Routing to Treasury Engine Invoice Renderer.");
};
"""
    html = html.replace('window.toggleCeoLaunchpad = function() {', js_funcs + '\nwindow.toggleCeoLaunchpad = function() {')

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("CEO Cockpit updated successfully!")

except Exception as e:
    print(f"Error: {e}")
