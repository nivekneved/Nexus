---
name: production-resilient-serverless-architecture
description: Best practices for building and deploying FastAPI backend applications to serverless platforms like Vercel with zero timeout overhead, memory-efficient persistence, and robust error handling. Use when optimizing backend APIs, configuring Vercel routes, or preventing serverless file locks.
---

# Production-Resilient Serverless Architecture Skill

## Overview
This skill ensures that FastAPI applications and background services scale reliably in serverless environments (e.g., Vercel AWS Lambda) without memory bloat or file-lock timeouts.

## Core Capabilities
1. **Serverless Filesystem Management**:
   - Universal path resolution via `core.paths` (`DATA_DIR`, `REPORTS_DIR` routing to `/tmp/` in serverless).
   - Automatic trimming and pruning of persistent task logs to prevent 90MB+ file bloat.
2. **FastAPI & Vercel Routing Optimization**:
   - Explicit `vercel.json` route mappings for every frontend HTML page to eliminate 404 errors.
   - Comprehensive exception handling returning clean JSON error responses instead of unhandled 500 crashes.
3. **Low-Latency Startup**:
   - Lazy loading of heavy agent registries and memory stores to keep cold-start times under 500ms.
