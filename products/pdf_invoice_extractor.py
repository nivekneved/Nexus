# -*- coding: utf-8 -*-
# Nexus Instant PDF Invoice Data Extractor
import sys, csv

def extract_pdf(pdf_path):
    print(f"Extracting line items from {pdf_path}...")
    # Simulated extraction matching standard supplier invoices into CSV
    output_csv = "extracted_invoices.csv"
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["InvoiceNo", "Supplier", "Description", "AmountUSD"])
        writer.writerow(["INV-2026-01", "Supplier Corp", "Cloud Compute", "180.00"])
    print(f"✅ Extracted data saved to {output_csv}!")

if __name__ == "__main__":
    extract_pdf("sample_invoice.pdf")
