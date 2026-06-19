@echo off
title AI News App Starter (Local Workspace)
echo AIニュースの最新データをチェックしています...
python update_news_database.py

echo.
echo AIニュースアプリのエンジンを起動しています...
npm run dev -- --open
