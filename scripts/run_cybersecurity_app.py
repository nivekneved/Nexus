import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# -*- coding: utf-8 -*-
"""
Standalone Anthropic Cybersecurity Skills Web App Launcher
=============================================================================
Runs the interactive cybersecurity application powered by 'anthropic-cybersecurity-skills'.
Features:
  - Live HTTP Headers Security Audit
  - SSL/TLS Cryptographic Surface Probing
  - Safe TCP Edge Port Scanning
  - Agentic AI Tool Policy & Schema Validator
  - 818 Skills Directory with Instant Search across 34 Domains & 6 Frameworks
  - 1-Click Agentskills.io Agent Installer

Usage:
  python run_cybersecurity_app.py [--port 8888]
"""

import os
import sys
import argparse
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from core.cybersecurity_service import cybersecurity_service

app = FastAPI(title="Anthropic Cybersecurity Skills App", version="1.3.0")

class AuditRequest(BaseModel):
    type: str
    target: str
    tool_name: Optional[str] = "search_docs"
    args: Optional[Dict[str, Any]] = None

class InstallRequest(BaseModel):
    skill_name: str

@app.get("/")
@app.get("/cybersecurity")
def serve_dashboard():
    html_path = os.path.abspath("static/cybersecurity.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return HTMLResponse("<h1>Cybersecurity dashboard HTML not found</h1>", status_code=404)

@app.get("/api/cybersecurity/skills")
def api_list_skills(query: str = "", domain: str = "", limit: int = 50, offset: int = 0):
    return cybersecurity_service.list_skills(query=query, domain=domain, limit=limit, offset=offset)

@app.get("/api/cybersecurity/skills/{skill_name}")
def api_skill_detail(skill_name: str):
    res = cybersecurity_service.get_skill_detail(skill_name)
    if not res.get("success"):
        raise HTTPException(status_code=404, detail=res.get("error", "Skill not found"))
    return res

@app.post("/api/cybersecurity/run")
def api_run_audit(req: AuditRequest):
    audit_type = req.type.lower()
    target = req.target.strip()

    if audit_type == "headers":
        return cybersecurity_service.run_security_headers_audit(target)
    elif audit_type == "ssl":
        return cybersecurity_service.run_ssl_tls_inspection(target)
    elif audit_type == "ports":
        return cybersecurity_service.run_port_scan(target)
    elif audit_type == "policy":
        sample_args = req.args or {"query": "system prompt leak test"}
        return cybersecurity_service.run_agentic_policy_gate(req.tool_name or "search_docs", sample_args)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported audit type: {req.type}")

@app.post("/api/cybersecurity/install")
def api_install_skill(req: InstallRequest):
    res = cybersecurity_service.install_skill_for_agents(req.skill_name)
    return res

def main():
    parser = argparse.ArgumentParser(description="Run Anthropic Cybersecurity Skills App")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8888, help="Bind port (default: 8888)")
    args = parser.parse_args()

    print(f"\n=======================================================")
    print(f"🛡️  ANTHROPIC CYBERSECURITY SKILLS APP ONLINE")
    print(f"=======================================================")
    print(f"Total Skills Available: {len(cybersecurity_service.skills_index)}")
    print(f"URL: http://{args.host}:{args.port}/cybersecurity")
    print(f"=======================================================\n")

    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
