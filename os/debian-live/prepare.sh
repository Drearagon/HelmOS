#!/usr/bin/env bash
set -euo pipefail
# Sync the current repo's HelmOS app into the live-build includes directory.

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DEST="$(cd "$(dirname "$0")" && pwd)/config/includes.chroot/opt/HelmOS"

mkdir -p "$DEST"

rsync -a --delete \
  --exclude '.git' \
  --exclude 'os/debian-live' \
  --exclude '.github' \
  --exclude '.venv' \
  --exclude '__pycache__' \
  "$ROOT/HelmOS/" "$DEST/"

echo "[+] Synced HelmOS -> $DEST"
