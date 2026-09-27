#!/usr/bin/env bash
# Nexus Workforce - 1-Click Restore Utility for Linux / macOS
echo "========================================================================="
echo "      NEXUS WORKFORCE & ENTERPRISE SUITE - 1-CLICK RESTORE SYSTEM        "
echo "========================================================================="
echo ""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/restore.py" "$@"
