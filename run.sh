#!/usr/bin/env bash
set -euo pipefail

ROOT="/root/contest-pages-test"
LOG="$ROOT/cron.run.log"

{
  echo "===== $(date '+%F %T') START ====="
  cd "$ROOT"

  # 0) 先同步远端，避免 push 时才发现分叉
  #    如果你担心 cron 被卡住，也可以加 timeout（见下方注释）
  git fetch origin main >/dev/null 2>&1 || true
  # 若本地没有提交且远端有更新，rebase 会把本地提交“平滑”叠到最新远端之上
  git pull --rebase origin main || {
    echo "[ERROR] git pull --rebase failed. Please resolve conflicts manually."
    echo "===== $(date '+%F %T') END (FAILED) ====="
    exit 1
  }

  # 1) 执行 Python 构建（生成 index.html / data.json / details/）
  "$ROOT/venv/bin/python" build.py

  # 2) 加入暂存区：内容 + 静态资源 + 配置 + 代码 + 模板
  git add \
    index.html data.json details static contests.yaml build.py templates \
    2>/dev/null || true

  # 3) 如果暂存区无变化，退出
  if git diff --cached --quiet; then
    echo "[INFO] no changes detected (content & assets are up-to-date)"
    echo "===== $(date '+%F %T') END ====="
    exit 0
  fi

  # 4) 打印“将要提交的文件清单”
  echo "[INFO] changes to be committed:"
  git diff --cached --name-status || true

  # 5) 配置 Git 身份（自动提交用）
  git config user.name "ECS-Contest-Bot"
  git config user.email "ecs-contest-bot@users.noreply.github.com"

  # 6) 提交
  git commit -m "auto: update content & assets $(date '+%F %T')"

  # 7) 推送（Cloudflare Pages 会监听 main 并自动部署）
  git push origin main || {
    echo "[ERROR] git push failed."
    echo "Tip: check if remote changed; run git pull --rebase and retry."
    echo "===== $(date '+%F %T') END (FAILED) ====="
    exit 1
  }

  echo "[OK] pushed successfully"
  echo "===== $(date '+%F %T') END ====="
} >> "$LOG" 2>&1

