#!/usr/bin/env bash
set -euo pipefail

ROOT="/root/contest-pages-test"
LOG="$ROOT/cron.run.log"

{
  echo "===== $(date '+%F %T') START ====="
  cd "$ROOT"

  "$ROOT/venv/bin/python" build.py

  # 如果没有任何变更，则跳过
  if git diff --quiet; then
    echo "[INFO] no changes after build"
    echo "===== $(date '+%F %T') END ====="
    exit 0
  fi

  git add data.json index.html details 2>/dev/null || true

  git config user.name "ECS-Contest-Bot"
  git config user.email "ecs-contest-bot@users.noreply.github.com"

  git commit -m "auto: update $(date '+%F %T')"
  git push origin main

  echo "[OK] pushed"
  echo "===== $(date '+%F %T') END ====="
} >> "$LOG" 2>&1
