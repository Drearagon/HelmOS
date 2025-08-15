#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Ensure app files are staged
./prepare.sh

# Configure live-build
./auto/config

# Build ISO
sudo lb build

echo
echo "[+] Build complete. Look for live-image-amd64.hybrid.iso in $(pwd)"
