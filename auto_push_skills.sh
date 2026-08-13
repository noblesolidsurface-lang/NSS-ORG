#!/bin/bash
# Auto-commits and pushes any changes under nss-org-repo/skills to GitHub.
# Runs on a schedule via the com.nss.autopushskills LaunchAgent.
set -euo pipefail

export PATH="/Users/kylebridgan/.local/bin:$PATH"
REPO_DIR="/Users/kylebridgan/nss-org-repo"
LOG_FILE="$REPO_DIR/auto_push.log"

cd "$REPO_DIR"

if [ -z "$(git status --porcelain)" ]; then
  exit 0
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git add -A
git commit -m "Auto-update: skill changes as of $TIMESTAMP" >> "$LOG_FILE" 2>&1
git push origin main >> "$LOG_FILE" 2>&1
echo "$TIMESTAMP - pushed changes" >> "$LOG_FILE"
