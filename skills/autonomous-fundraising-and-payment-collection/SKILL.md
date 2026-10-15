---
name: autonomous-fundraising-and-payment-collection
description: Expert methodology and implementation patterns for deploying $1-$100 micro-ask funnels, crypto (Base USDC) escrows, PayPal REST API payment links, and automated invoice verification for autonomous AI agents. Use when orchestrating online fund collection, micro-ask campaigns, or payment gateways.
---

# Autonomous Fundraising & Payment Collection Skill

## Overview
This skill provides the operational framework for AI agents to autonomously collect funds online, generate instant payment links, verify transactions, and maintain audit-ready financial ledgers.

## Core Capabilities
1. **Multi-Rail Payment Routing**:
   - PayPal REST API & PayPal.me links for instant credit/debit card checkout.
   - Base L2 (Ethereum Layer 2) USDC crypto wallets with zero-gas optimizations and x402 payment headers.
   - Local Mauritian rails (MCB Juice mobile transfer + bank wire SWIFT).
2. **Micro-Ask Funnel Architecture**:
   - Low-friction $1.00 - $25.00 hooks for developer tools, audits, and API access.
   - Automated invoice minting (`INV-XXXX`) with SHA-256 integrity signatures.
3. **Transaction Verification & Ledgering**:
   - Webhook listeners (`/api/webhook/paypal`, `/api/mesh/inbound`) for instant payment confirmation.
   - Atomic JSON ledger updates (`treasury_ledger.json`) with double-entry reconciliation.
