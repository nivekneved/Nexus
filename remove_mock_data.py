import re

try:
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Sales KPI Grid
    # Today
    html = re.sub(r'<div style="font-size: 1.75rem; font-weight: 900; color: #0f172a;">Rs 45,000</div>',
                  '<div style="font-size: 1.75rem; font-weight: 900; color: #0f172a;" id="kpiTodaySales">Rs 0</div>', html)
    html = re.sub(r'<div style="font-size: 0.8rem; color: #10b981; font-weight: 600;">▲ 2 Sales \(Medical 360\)</div>',
                  '<div style="font-size: 0.8rem; color: #10b981; font-weight: 600;" id="kpiTodaySub">Loading...</div>', html)
    # Yesterday
    html = re.sub(r'<div style="font-size: 1.75rem; font-weight: 900; color: #0f172a;">Rs 15,000</div>',
                  '<div style="font-size: 1.75rem; font-weight: 900; color: #0f172a;" id="kpiYesterdaySales">Rs 0</div>', html)
    html = re.sub(r'<div style="font-size: 0.8rem; color: #64748b;">1 Sale \(Flight Addon\)</div>',
                  '<div style="font-size: 0.8rem; color: #64748b;" id="kpiYesterdaySub">Loading...</div>', html)
    # Week
    html = re.sub(r'<div style="font-size: 1.75rem; font-weight: 900; color: #0f172a;">Rs 180,000</div>',
                  '<div style="font-size: 1.75rem; font-weight: 900; color: #0f172a;" id="kpiWeekSales">Rs 0</div>', html)
    html = re.sub(r'<div style="font-size: 0.8rem; color: #8b5cf6; font-weight: 600;">▲ 12% vs last week</div>',
                  '<div style="font-size: 0.8rem; color: #8b5cf6; font-weight: 600;" id="kpiWeekSub">Loading...</div>', html)
    # Target
    html = re.sub(r'<div style="font-size: 1.75rem; font-weight: 900; color: #0f172a;">Rs 450,000</div>',
                  '<div style="font-size: 1.75rem; font-weight: 900; color: #0f172a;" id="kpiMonthTarget">Rs 0</div>', html)
    html = re.sub(r'<div style="font-size: 0.8rem; color: #b45309; font-weight: 600;">40% to Goal</div>',
                  '<div style="font-size: 0.8rem; color: #b45309; font-weight: 600;" id="kpiMonthSub">Loading...</div>', html)

    # 2. Products Sold Table
    sales_tbody_pattern = re.compile(r'<tbody>.*?</tbody>', re.DOTALL)
    # Be careful to only replace the FIRST tbody (which is the sales table) in the ceo-cockpit
    cockpit_start = html.find('id="pane-ceo-cockpit"')
    cockpit_end = html.find('</section>', cockpit_start)
    cockpit_html = html[cockpit_start:cockpit_end]

    empty_sales_tbody = '<tbody id="recentSalesTableBody">\n                <tr><td colspan="6" style="text-align: center; padding: 20px; color: var(--text-muted);">Loading recent sales...</td></tr>\n              </tbody>'
    cockpit_html = re.sub(r'<tbody>.*?</tbody>', empty_sales_tbody, cockpit_html, count=1)

    # 3. Portfolio MRR
    # Remove the hardcoded product divs
    mrr_pattern = re.compile(r'<div style="margin-bottom: 12px; background: var\(--bg-main\); border: 1px solid var\(--border-color\); border-left: 4px solid #0284c7.*?(?=<script>)', re.DOTALL)
    empty_mrr = '<div id="portfolioMrrContainer">\n              <div style="text-align: center; padding: 20px; color: var(--text-muted);">Loading active subscriptions...</div>\n            </div>\n        </div>\n\n        '
    cockpit_html = mrr_pattern.sub(empty_mrr, cockpit_html)

    html = html[:cockpit_start] + cockpit_html + html[cockpit_end:]


    # 4. Comms Pane
    comms_start = html.find('id="pane-domain-comms"')
    comms_end = html.find('</section>', comms_start)
    comms_html = html[comms_start:comms_end]

    # Inbox
    inbox_pattern = re.compile(r'<div style="display: flex; flex-direction: column; gap: 12px;">\s*<!-- Message 1 -->.*?</div>\s*</div>\s*<!-- Client History', re.DOTALL)
    empty_inbox = '<div id="crmInboxList" style="display: flex; flex-direction: column; gap: 12px;">\n              <div style="text-align: center; padding: 20px; color: var(--text-muted);">No unread messages.</div>\n            </div>\n          </div>\n\n          <!-- Client History'
    comms_html = inbox_pattern.sub(empty_inbox, comms_html)

    # Client Dossier & Timeline
    dossier_pattern = re.compile(r'<!-- Selected Client Header -->.*?<button class="btn btn-secondary"', re.DOTALL)
    empty_dossier = '<!-- Selected Client Header -->\n            <div id="crmClientHeader" style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0; color: var(--text-muted); font-size: 0.85rem;">\n              Select a message to view client timeline.\n            </div>\n\n            <!-- Timeline -->\n            <div id="crmTimelineList" style="position: relative; padding-left: 20px;">\n            </div>\n            \n            <button class="btn btn-secondary"'
    comms_html = dossier_pattern.sub(empty_dossier, comms_html)

    # Unread badge
    comms_html = re.sub(r'<span class="badge" style="background: #e0f2fe; color: #0284c7;">2 Unread</span>',
                        '<span class="badge" style="background: #e0f2fe; color: #0284c7;" id="crmUnreadBadge">0 Unread</span>', comms_html)

    html = html[:comms_start] + comms_html + html[comms_end:]


    # 5. Operations Pane
    ops_start = html.find('id="pane-domain-operations"')
    ops_end = html.find('</section>', ops_start)
    ops_html = html[ops_start:ops_end]

    # Recently Extracted Leads
    leads_pattern = re.compile(r'<div style="display: flex; flex-direction: column; gap: 8px; max-height: 200px; overflow-y: auto;">\s*<div style="font-size: 0.8rem; padding: 8px; border: 1px solid #e2e8f0.*?\s*</div>\s*</div>\s*</div>\s*<!-- Social', re.DOTALL)
    empty_leads = '<div id="opsExtractedLeads" style="display: flex; flex-direction: column; gap: 8px; max-height: 200px; overflow-y: auto;">\n              <div style="text-align: center; padding: 20px; color: var(--text-muted); font-size: 0.85rem;">No recent extractions.</div>\n            </div>\n          </div>\n\n          <!-- Social'
    ops_html = leads_pattern.sub(empty_leads, ops_html)

    # Active Campaigns
    camps_pattern = re.compile(r'<div style="display: flex; flex-direction: column; gap: 8px;">\s*<div style="font-size: 0.8rem; padding: 8px; border: 1px solid #e2e8f0; border-left: 3px solid #0284c7.*?\s*</div>\s*</div>\s*</div>\s*</div>\s*', re.DOTALL)
    empty_camps = '<div id="opsActiveCampaigns" style="display: flex; flex-direction: column; gap: 8px;">\n              <div style="text-align: center; padding: 20px; color: var(--text-muted); font-size: 0.85rem;">No active campaigns.</div>\n            </div>\n          </div>\n\n        </div>\n      '
    ops_html = camps_pattern.sub(empty_camps, ops_html)

    html = html[:ops_start] + ops_html + html[ops_end:]


    # 6. Customer Directory Modal
    modal_start = html.find('id="customerDirectoryModal"')
    if modal_start != -1:
        modal_end = html.find('</div>\n    </div>\n', modal_start) + 18
        modal_html = html[modal_start:modal_end]

        # Replace tbody
        modal_tbody = re.compile(r'<tbody>.*?</tbody>', re.DOTALL)
        empty_modal_tbody = '<tbody id="customerDirectoryTableBody">\n              <tr><td colspan="6" style="text-align: center; padding: 20px; color: var(--text-muted);">Loading customers...</td></tr>\n            </tbody>'
        modal_html = modal_tbody.sub(empty_modal_tbody, modal_html)

        # Replace showing count
        modal_html = re.sub(r'Showing 1-3 of 45 customers', '<span id="customerDirectoryCount">Showing 0 customers</span>', modal_html)

        html = html[:modal_start] + modal_html + html[modal_end:]

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Mock data removed! HTML components assigned dynamic IDs.")

except Exception as e:
    print(f"Error: {e}")
