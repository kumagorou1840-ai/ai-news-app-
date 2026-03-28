import os
import re
from datetime import datetime, timedelta

# 設定
DB_PATH = 'src/data/newsDatabase.ts'
# 実行時の日付を自動取得
TARGET_DATE = datetime.now().strftime('%Y-%m-%d')

def get_latest_date(content):
    dates = re.findall(r"\'(\d{4}-\d{2}-\d{2})\'\:", content)
    return max(dates) if dates else None

def generate_news_for_date(date_str):
    # 本来はここでAI APIを叩くが、今回はテンプレートを生成
    # 実際の運用ではエージェント（私）がここを埋めることも可能
    return f"""  '{date_str}': {{
    general: [
      {{
        id: {date_str.replace('-', '')}01,
        title: "{date_str}の最新AIトピック",
        summary: "本日もAI業界では革新的な動きがありました。",
        fullContent: "詳細な内容は自動生成プロセスによって順次更新されます。AI技術の進化は止まりません。",
        category: 'Trends',
        source: 'AI News Network'
      }}
    ],
    agents: [
      {{
        id: {date_str.replace('-', '')}11,
        title: "{date_str}のエージェント動向",
        summary: "自律型エージェントの進化が加速しています。",
        fullContent: "エージェント同士の連携により、複雑なタスクがより簡単に解決される時代になっています。",
        category: 'Autonomous',
        source: 'Agent Insights'
      }}
    ]
  }},"""

def update_database():
    if not os.path.exists(DB_PATH):
        print(f"Error: {DB_PATH} not found.")
        return

    with open(DB_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    latest_date_str = get_latest_date(content)
    if not latest_date_str:
        print("No dates found in database.")
        return

    latest_date = datetime.strptime(latest_date_str, '%Y-%m-%d')
    today = datetime.strptime(TARGET_DATE, '%Y-%m-%d')

    if latest_date >= today:
        print("Database is already up to date.")
        return

    # 不足している日付のデータを生成
    new_entries = []
    current_date = latest_date + timedelta(days=1)
    while current_date <= today:
        d_str = current_date.strftime('%Y-%m-%d')
        print(f"Generating news for {d_str}...")
        new_entries.append(generate_news_for_date(d_str))
        current_date += timedelta(days=1)

    # データを挿入（'newsDatabase: Record<string, DailyDatabase> = {' の直後に挿入）
    insertion_point = "export const newsDatabase: Record<string, DailyDatabase> = {"
    if insertion_point in content:
        updated_content = content.replace(insertion_point, insertion_point + "\n" + "\n".join(reversed(new_entries)))
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("Update complete!")
    else:
        print("Could not find insertion point in newsDatabase.ts")

if __name__ == "__main__":
    update_database()
