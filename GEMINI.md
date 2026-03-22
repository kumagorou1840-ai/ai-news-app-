# AI News App - Gemini Project Guidelines

## 🚀 プロジェクトの目的
AIエージェントと最新のAIニュースを配信するニュースレター・アプリ。

## 📅 運用ルール
- **ニュースの更新**: `src/data/newsDatabase.ts` に日々のニュースを蓄積する。
- **自動生成**: `update_news_database.py` を使用して、今日の日付までの不足分を自動生成・追記する。
- **初期表示**: `src/App.tsx` は、`newsDatabase` 内の最新の日付を自動的に初期表示するように設定されている。

## 📦 GitHub リポジトリ
- **URL**: `https://github.com/kumagorou1840-ai/ai-news-app-.git`
- **ブランチ**: `master`
- **操作**: 変更を加えた際は、必ずこのリモートリポジトリにプッシュし、最新の状態を維持すること。

## 🛠️ 開発・実行コマンド
- **アプリ起動**: デスクトップの `AIニュースを起動.bat` を使用する。
- **開発サーバー**: `npm run dev` (Vite)
- **データ更新**: `python update_news_database.py`

---
*Created on 2026-03-22 by よっちゃん*
