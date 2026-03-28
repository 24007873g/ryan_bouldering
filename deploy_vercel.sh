#!/bin/bash
# Vercel 自動化部署腳本
# 用於本地測試或 CI/CD pipeline

set -e

# 安裝 Vercel CLI
npm install -g vercel

# 登入 Vercel（首次執行需互動）
# vercel login <your-email>

# 設定環境變數（可用 .env.production.local 或 Vercel 後台設定）
# echo "Transaction_pooler=your_postgres_url" >> .env.production.local
# echo "GITHUB_TOKEN=your_github_token" >> .env.production.local

# 部署到 Vercel
vercel --prod --confirm

echo "✅ 部署完成！請至 Vercel 後台確認專案狀態。"
