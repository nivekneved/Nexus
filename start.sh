#!/usr/bin/env bash
# Nexus Autonomous AI Workforce — 1-Click Launch Script (Linux / macOS)

set -e

echo "====================================================================="
echo "          NEXUS AUTONOMOUS AI WORKFORCE (VERSION 2.5.1)              "
echo "     14 AI Employees | 44 SubAgents | 25 Safeguards | Enterprise     "
echo "====================================================================="
echo ""

# Check python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed. Please install Python 3.10+."
    exit 1
fi

# Virtualenv
if [ ! -d ".venv" ]; then
    echo "[*] Creating virtual environment in .venv..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "[*] Verifying dependencies..."
pip install -r requirements.txt --quiet

# Check .env
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "[*] Creating .env from .env.example..."
    cp .env.example .env
fi

echo ""
echo "====================================================================="
echo "   NEXUS ENGINE ONLINE: http://localhost:8000                        "
echo "   Financial Security & Anti-Fraud Shield Active                     "
echo "   Press Ctrl+C to stop the workforce                                "
echo "====================================================================="
echo ""

python3 server.py
