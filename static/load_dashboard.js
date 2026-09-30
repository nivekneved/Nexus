// JavaScript to populate dynamic components in the consolidated UI

async function loadCEOData() {
  try {
    // 1. Fetch Consolidated Balances (Treasury Engine)
    const balRes = await fetch('/api/sovereignty/treasury');
    const balData = await balRes.json();

    const kpiToday = document.getElementById('kpiTodaySales');
    const kpiWeek = document.getElementById('kpiWeekSales');
    const kpiMonth = document.getElementById('kpiMonthTarget');

    if (balData.success) {
      if (kpiToday) kpiToday.textContent = `Rs ${balData.fiat_mur.toLocaleString()}`;
      // Basic mock math for missing endpoints just to wire the UI until specific endpoints exist
      if (kpiWeek) kpiWeek.textContent = `Rs ${(balData.fiat_mur * 3).toLocaleString()}`;
      if (kpiMonth) kpiMonth.textContent = `Rs 150,000`;
    }

    // 2. Fetch Recent Sales / Invoices (Finance)
    const invRes = await fetch('/api/finance/invoices');
    const invData = await invRes.json();
    const invoices = Array.isArray(invData) ? invData : (invData.invoices || []);
    window._allSalesInvoices = invoices;

    if (typeof window.renderSalesTable === 'function') {
      window.renderSalesTable(invoices);
    } else {
      const tbody = document.getElementById('recentSalesTableBody');
      if (tbody) {
        if (invoices.length === 0) {
          tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px; color: var(--text-muted);">No sales found.</td></tr>';
        } else {
          tbody.innerHTML = invoices.slice(0, 5).map(inv => {
            const badgeColor = inv.status === 'PAID' ? '#047857' : '#b45309';
            const badgeBg = inv.status === 'PAID' ? '#ecfdf5' : '#fef3c7';
            return `
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 12px 8px; color: var(--text-muted);">${inv.date || inv.created_at || 'Today'}</td>
                <td style="padding: 12px 8px; font-weight: 700; color: var(--text-main);">${inv.product_name || inv.description || inv.id}</td>
                <td style="padding: 12px 8px; color: var(--text-main);">1</td>
                <td style="padding: 12px 8px; color: #10b981; font-weight: 700;">Rs ${inv.amount}</td>
                <td style="padding: 12px 8px;"><span class="badge" style="background: ${badgeBg}; color: ${badgeColor};">${inv.status}</span></td>
                <td style="padding: 12px 8px;"><button class="btn btn-secondary btn-sm" style="font-size:0.7rem; padding: 4px 8px;" onclick="viewInvoice('${inv.id}')">🧾 Receipt</button></td>
              </tr>
            `;
          }).join('');
        }
      }
    }

    // 3. Fetch Products (Mauritius Sales Engine)
    const prodRes = await fetch('/api/mauritius/sectors');
    const prodData = await prodRes.json();

    const mrrContainer = document.getElementById('portfolioMrrContainer');
    if (mrrContainer && prodData.sectors) {
      mrrContainer.innerHTML = prodData.sectors.map(prod => `
        <div style="margin-bottom: 12px; background: var(--bg-main); border: 1px solid var(--border-color); border-left: 4px solid #0284c7; border-radius: 8px; padding: 12px;">
          <div style="font-weight: 700; font-size: 0.85rem; color: var(--text-main); margin-bottom: 2px;">${prod.icon} ${prod.title}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${prod.locations}</div>
          <div style="display:flex; justify-content:space-between; align-items:flex-end;">
            <div style="font-size: 0.85rem; font-weight: 800; color: #0284c7; margin-top: 6px;">${prod.retainer_fee}</div>
            <div style="display:flex; gap:4px;">
              <button class="btn btn-secondary btn-sm" style="font-size:0.65rem; padding: 2px 6px;" onclick="if(window.manageSector) window.manageSector('${prod.id || prod.title}', '${prod.title.replace(/'/g, "\\'")}', '${prod.retainer_fee}');">⚙️ Manage</button>
              <button class="btn btn-secondary btn-sm" style="font-size:0.65rem; padding: 2px 6px;" onclick="if(window.broadcastSector) window.broadcastSector('${prod.id || prod.title}', '${prod.title.replace(/'/g, "\\'")}');">✉️ Broadcast</button>
            </div>
          </div>
        </div>
      `).join('');
    }

  } catch(e) {
    console.error("Error loading CEO data:", e);
  }
}

async function loadCRMData() {
  try {
    const res = await fetch('/api/outreach/history');
    const data = await res.json();

    const inbox = document.getElementById('crmInboxList');
    if (inbox && data.contacts) {
      if (data.contacts.length === 0) {
        inbox.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--text-muted);">No contacts found.</div>';
      } else {
        inbox.innerHTML = data.contacts.slice(0, 10).map(c => `
          <div style="border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='#0284c7'" onmouseout="this.style.borderColor='var(--border-subtle)'" onclick="loadClientTimeline('${c.email}', '${c.name || 'Client'}', '${c.domain || 'N/A'}')">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
              <strong style="color: var(--text-main); font-size: 0.95rem;">${c.name || c.email}</strong>
              <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600;">${c.source}</span>
            </div>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">
              Status: ${c.status} | Last touch: ${c.last_contact_date || 'N/A'}
            </div>
          </div>
        `).join('');
      }
    }
  } catch(e) {
    console.error("Error loading CRM data:", e);
  }
}

window.loadClientTimeline = function(email, name, domain) {
  document.getElementById('crmClientHeader').innerHTML = `
    <div style="width: 40px; height: 40px; border-radius: 50%; background: #0284c7; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.2rem;">
      ${name.charAt(0).toUpperCase()}
    </div>
    <div>
      <div style="font-weight: 800; font-size: 1.05rem; color: #0f172a;">${name}</div>
      <div style="font-size: 0.8rem; color: #64748b;">${email} • ${domain}</div>
    </div>
  `;
  document.getElementById('crmTimelineList').innerHTML = `
    <div style="position: absolute; left: 6px; top: 8px; bottom: 0; width: 2px; background: #cbd5e1;"></div>
    <div style="position: relative; margin-bottom: 16px;">
      <div style="position: absolute; left: -20px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: #10b981; border: 2px solid #fff;"></div>
      <div style="font-size: 0.75rem; color: #64748b; font-weight: 700; margin-bottom: 2px;">Recently</div>
      <div style="font-size: 0.85rem; color: #334155;"><strong>Contact Synced</strong></div>
    </div>
  `;
};

async function loadOpsData() {
  try {
    const res = await fetch('/api/leads/pipeline');
    const data = await res.json();

    const leads = document.getElementById('opsExtractedLeads');
    if (leads && data.high_fit_leads) {
      if (data.high_fit_leads.length === 0) {
        leads.innerHTML = '<div style="text-align: center; padding: 20px; color: var(--text-muted); font-size: 0.85rem;">No recent extractions.</div>';
      } else {
        leads.innerHTML = data.high_fit_leads.map(l => `
          <div style="font-size: 0.8rem; padding: 8px; border: 1px solid #e2e8f0; border-radius: 6px; display: flex; justify-content: space-between;">
            <span><strong>${l.company || 'Unknown'}</strong> (${l.location || 'Unknown'})</span>
            <span style="color: #10b981;">MX Verified</span>
          </div>
        `).join('');
      }
    }
  } catch(e) {
    console.error("Error loading Ops data:", e);
  }
}

// Call on load
document.addEventListener('DOMContentLoaded', () => {
  loadCEOData();
  loadCRMData();
  loadOpsData();
});
