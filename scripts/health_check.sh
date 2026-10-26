#!/usr/bin/env bash
# High-Performance Linux Health Check Launcher
set -euo pipefail

echo "========================================================"
echo "  LINUX SYSTEM MONITORING & HEALTH CHECK LAUNCHER"
echo "========================================================"

# Check Python environment
if ! command -v python3 &> /dev/null; then
    echo "[!] Error: python3 is not installed or not in PATH."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${SCRIPT_DIR}"

echo "[*] Collecting system metrics..."
python3 -m src.cli --all "$@"

echo "========================================================"
echo "[+] Health check completed successfully."
