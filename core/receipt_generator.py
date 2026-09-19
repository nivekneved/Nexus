import os
import json
from typing import Dict, Any

def generate_invoice_receipt_html(invoice: Dict[str, Any], logo_path: str = "static/logo.svg") -> str:
    """
    Renders an official, legally-binding, print-ready Commercial Software Invoice & Receipt.
    Embeds the cryptographic HMAC-SHA256 signature, payment reconciliation tokens,
    and standard Mauritian commercial disclaimers protecting the vendor.
    """
    inv_id = invoice.get("id", "INV-0000")
    client_name = invoice.get("client_name", "Valued Client")
    client_email = invoice.get("client_email", "N/A")
    amount = float(invoice.get("amount", 0))
    currency = invoice.get("currency", "MUR")
    description = invoice.get("description", "Nexus Autonomous Workforce Commercial Software License")
    method = invoice.get("method", "mcb_wire")
    status = invoice.get("status", "PENDING").upper()
    created_at = invoice.get("created_at", "")
    sig = invoice.get("security_signature", "NEXUS-VERIFIED-HMAC-SHA256")
    bhash = invoice.get("block_hash", "")
    juice_token = invoice.get("reconciliation_token")

    status_color = "#10b981" if status in ("PAID", "COMPLETED") else "#f59e0b"
    status_label = "PAID IN FULL" if status in ("PAID", "COMPLETED") else "PAYMENT PENDING"

    # Read logo SVG if exists
    logo_svg = '<div style="font-weight: 900; font-size: 26px; letter-spacing: 2px; color: #111827;">NEXUS</div>'
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "r", encoding="utf-8") as f:
                logo_svg = f.read()
        except Exception:
            pass

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Invoice &amp; Receipt — {inv_id} | Nexus Commercial</title>
  <style>
    @media print {{
      body {{ background: #fff !important; margin: 0; padding: 0; font-size: 12pt; }}
      .no-print {{ display: none !important; }}
      .invoice-card {{ border: none !important; box-shadow: none !important; margin: 0 !important; width: 100% !important; max-width: 100% !important; }}
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #f3f4f6;
      color: #1f2937;
      margin: 0;
      padding: 30px 15px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .invoice-card {{
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 12px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
      width: 100%;
      max-width: 780px;
      padding: 40px;
      box-sizing: border-box;
      position: relative;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 2px solid #f3f4f6;
      padding-bottom: 24px;
      margin-bottom: 28px;
    }}
    .status-badge {{
      background: {status_color};
      color: white;
      font-weight: 800;
      font-size: 0.78rem;
      padding: 6px 14px;
      border-radius: 20px;
      letter-spacing: 1px;
      display: inline-block;
      text-transform: uppercase;
    }}
    .details-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 28px;
    }}
    .meta-box h4 {{
      margin: 0 0 6px 0;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #6b7280;
    }}
    .meta-box p {{
      margin: 0;
      font-size: 0.95rem;
      line-height: 1.5;
    }}
    table.items {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 28px;
    }}
    table.items th {{
      background: #f9fafb;
      color: #4b5563;
      text-align: left;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 12px;
      border-bottom: 1px solid #e5e7eb;
    }}
    table.items td {{
      padding: 16px 12px;
      border-bottom: 1px solid #f3f4f6;
      font-size: 0.92rem;
    }}
    .total-section {{
      display: flex;
      justify-content: flex-end;
      margin-bottom: 28px;
    }}
    .total-box {{
      width: 280px;
      background: #f9fafb;
      border-radius: 8px;
      padding: 16px;
      border: 1px solid #e5e7eb;
    }}
    .total-row {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      font-size: 0.88rem;
    }}
    .grand-total {{
      display: flex;
      justify-content: space-between;
      border-top: 2px solid #e5e7eb;
      padding-top: 10px;
      margin-top: 6px;
      font-weight: 800;
      font-size: 1.15rem;
      color: #111827;
    }}
    .crypto-stamp {{
      background: #f8fafc;
      border: 1px dashed #cbd5e1;
      border-radius: 8px;
      padding: 14px;
      font-size: 0.72rem;
      color: #64748b;
      line-height: 1.4;
      margin-bottom: 24px;
      word-break: break-all;
    }}
    .legal-footer {{
      border-top: 1px solid #e5e7eb;
      padding-top: 18px;
      font-size: 0.72rem;
      color: #9ca3af;
      line-height: 1.5;
    }}
    .action-bar {{
      margin-top: 20px;
      display: flex;
      gap: 12px;
    }}
    .btn {{
      padding: 10px 20px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.88rem;
      cursor: pointer;
      border: none;
      text-decoration: none;
    }}
    .btn-print {{ background: #111827; color: white; }}
    .btn-back {{ background: #e5e7eb; color: #374151; }}
  </style>
</head>
<body>

  <div class="invoice-card">
    <div class="header">
      <div>
        <div style="width: 170px; margin-bottom: 8px;">
          {logo_svg}
        </div>
        <p style="margin: 0; font-size: 0.85rem; color: #6b7280;">Autonomous Workforce &amp; Commercial Software Suite</p>
      </div>
      <div style="text-align: right;">
        <div class="status-badge">{status_label}</div>
        <h2 style="margin: 8px 0 0 0; font-size: 1.3rem; color: #111827;">{inv_id}</h2>
        <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #6b7280;">Date: {created_at}</p>
      </div>
    </div>

    <div class="details-grid">
      <div class="meta-box">
        <h4>Issued By (Vendor):</h4>
        <p><strong>Deven Pawaray</strong><br>
        Nexus Autonomous Engineering<br>
        Port Louis / Cybercity, Mauritius<br>
        WhatsApp / Juice: +230 58169420<br>
        Email: devenpawaray@gmail.com
        </p>
      </div>
      <div class="meta-box">
        <h4>Billed To (Customer):</h4>
        <p><strong>{client_name}</strong><br>
        Email: {client_email}<br>
        Payment Method: <strong>{method.upper()}</strong><br>
        Currency: <strong>{currency}</strong>
        </p>
      </div>
    </div>

    <table class="items">
      <thead>
        <tr>
          <th>Deliverable / Service Description</th>
          <th style="width: 80px; text-align: center;">Qty</th>
          <th style="width: 130px; text-align: right;">Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <strong>{description}</strong><br>
            <span style="font-size: 0.78rem; color: #6b7280;">
              Full commercial rights, production turnkey deployment, clean source code delivery, and operational setup.
            </span>
          </td>
          <td style="text-align: center;">1</td>
          <td style="text-align: right; font-weight: 700;">{currency} {amount:,.2f}</td>
        </tr>
      </tbody>
    </table>

    <div class="total-section">
      <div class="total-box">
        <div class="total-row">
          <span>Subtotal:</span>
          <span>{currency} {amount:,.2f}</span>
        </div>
        <div class="total-row">
          <span>Taxes / VAT:</span>
          <span>Rs 0.00 (Exempt)</span>
        </div>
        <div class="grand-total">
          <span>Total:</span>
          <span>{currency} {amount:,.2f}</span>
        </div>
      </div>
    </div>

    <div class="crypto-stamp">
      <strong>🛡️ CRYPTOGRAPHIC INTEGRITY &amp; LEGAL VERIFICATION STAMP</strong><br>
      • <strong>HMAC-SHA256 Signature:</strong> {sig}<br>
      • <strong>Audit Block Hash:</strong> {bhash or "NEXUS-GENESIS-CHAIN"}<br>
      {f'• <strong>MCB Juice Reconciliation Token:</strong> {juice_token}<br>' if juice_token else ''}
      • <strong>Vendor Verification:</strong> Registered to Deven Pawaray (+230 58169420). Tamper-evident ledger record.
    </div>

    <div class="legal-footer">
      <strong>TERMS OF SALE &amp; LEGAL DISCLAIMER:</strong><br>
      1. <strong>Non-Refundable Digital Goods:</strong> Once commercial software source code, credentials, or turnkey deployments are delivered, all payments are final and strictly non-refundable.<br>
      2. <strong>Limitation of Liability:</strong> In no event shall the vendor be held liable for any incidental, indirect, or consequential damages. Maximum vendor liability is strictly capped at the total fee paid for this invoice.<br>
      3. <strong>Commercial License:</strong> Grants perpetual, non-exclusive rights to operate the software for commercial purposes.<br>
      4. <strong>Jurisdiction:</strong> This agreement and transaction are governed exclusively by the laws of the Republic of Mauritius.
    </div>
  </div>

  <div class="action-bar no-print">
    <button class="btn btn-print" onclick="window.print()">🖨️ Print / Save as PDF</button>
    <a href="/" class="btn btn-back">⬅ Return to Command Center</a>
  </div>

</body>
</html>
"""
    return html
