import re

try:
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The customer directory modal
    customer_modal = """
    <!-- Customer Directory Modal -->
    <div id="customerDirectoryModal" class="modal-overlay" style="display: none; position: fixed; inset: 0; background: rgba(15,23,42,0.8); backdrop-filter: blur(4px); z-index: 9999; justify-content: center; align-items: center;">
      <div class="modal-content" style="max-width: 900px; width: 95%; padding: 24px; background: #fff; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle); padding-bottom: 16px; margin-bottom: 16px;">
          <h2 style="margin: 0; font-size: 1.4rem; font-weight: 900; color: var(--text-main);">👥 Customer Directory</h2>
          <button class="btn btn-secondary btn-sm" onclick="document.getElementById('customerDirectoryModal').style.display='none'">✕ Close</button>
        </div>

        <!-- Filters -->
        <div style="display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap;">
          <input type="text" class="form-input" placeholder="Search customer name or company..." style="flex: 1; font-size: 0.85rem;">
          <select class="form-input" style="font-size: 0.85rem; width: 150px;">
            <option value="">All Products</option>
            <option value="medical360">Medical 360</option>
            <option value="flightaddon">Flight Addon</option>
            <option value="smebot">SME WhatsApp Bot</option>
          </select>
          <select class="form-input" style="font-size: 0.85rem; width: 150px;">
            <option value="">Status: All</option>
            <option value="active">Active</option>
            <option value="churned">Churned</option>
          </select>
          <button class="btn btn-primary btn-sm">Filter</button>
        </div>

        <!-- Table -->
        <div style="max-height: 400px; overflow-y: auto;">
          <table style="width: 100%; text-align: left; border-collapse: collapse; font-size: 0.85rem;">
            <thead>
              <tr style="border-bottom: 2px solid var(--border-subtle); color: var(--text-muted);">
                <th style="padding: 10px; position: sticky; top: 0; background: #fff;">Customer</th>
                <th style="padding: 10px; position: sticky; top: 0; background: #fff;">Company</th>
                <th style="padding: 10px; position: sticky; top: 0; background: #fff;">Product</th>
                <th style="padding: 10px; position: sticky; top: 0; background: #fff;">LTV</th>
                <th style="padding: 10px; position: sticky; top: 0; background: #fff;">Status</th>
                <th style="padding: 10px; position: sticky; top: 0; background: #fff;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 12px 10px; font-weight: 700; color: var(--text-main);">Dr. Alain Wong</td>
                <td style="padding: 12px 10px; color: var(--text-muted);">Clinique du Nord</td>
                <td style="padding: 12px 10px;">Medical 360</td>
                <td style="padding: 12px 10px; font-weight: 700;">Rs 105,000</td>
                <td style="padding: 12px 10px;"><span class="badge" style="background: #ecfdf5; color: #047857;">Active</span></td>
                <td style="padding: 12px 10px;"><button class="btn btn-secondary btn-sm" style="font-size: 0.7rem; padding: 4px 8px;">Message</button></td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 12px 10px; font-weight: 700; color: var(--text-main);">Corinne Chung</td>
                <td style="padding: 12px 10px; color: var(--text-muted);">Rogers Capital</td>
                <td style="padding: 12px 10px;">NGO Portal</td>
                <td style="padding: 12px 10px; font-weight: 700;">Rs 90,000</td>
                <td style="padding: 12px 10px;"><span class="badge" style="background: #fef3c7; color: #b45309;">Pending Setup</span></td>
                <td style="padding: 12px 10px;"><button class="btn btn-secondary btn-sm" style="font-size: 0.7rem; padding: 4px 8px;">Message</button></td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 12px 10px; font-weight: 700; color: var(--text-main);">Fabrice Collet</td>
                <td style="padding: 12px 10px; color: var(--text-muted);">Blue Lagoon Cruises</td>
                <td style="padding: 12px 10px;">SME Booking Bot</td>
                <td style="padding: 12px 10px; font-weight: 700;">Rs 25,000</td>
                <td style="padding: 12px 10px;"><span class="badge" style="background: #ecfdf5; color: #047857;">Active</span></td>
                <td style="padding: 12px 10px;"><button class="btn btn-secondary btn-sm" style="font-size: 0.7rem; padding: 4px 8px;">Message</button></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border-subtle);">
          <span style="font-size: 0.8rem; color: var(--text-muted);">Showing 1-3 of 45 customers</span>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-secondary btn-sm" disabled>Previous</button>
            <button class="btn btn-secondary btn-sm">Next</button>
          </div>
        </div>
      </div>
    </div>
    """

    # We insert the modal just before the closing body tag
    html = html.replace('</body>', customer_modal + '\n</body>')

    # Update navigateToPage to handle modal for customer directory
    nav_patch = """
window.navigateToPage = function(pageId) {
  if (pageId === 'customer-directory') {
    const modal = document.getElementById('customerDirectoryModal');
    if (modal) modal.style.display = 'flex';
    return;
  }
"""
    html = html.replace("window.navigateToPage = function(pageId) {", nav_patch)

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Modals and JS functions updated!")

except Exception as e:
    print(f"Error: {e}")
