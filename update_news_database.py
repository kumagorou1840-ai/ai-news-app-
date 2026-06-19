import os
import re
import random
from datetime import datetime, timedelta

# 設定
DB_PATH = 'src/data/newsDatabase.ts'
TARGET_DATE = datetime.now().strftime('%Y-%m-%d')

def get_latest_date(content):
    # シングル・ダブル両対応の正規表現
    dates = re.findall(r"['\"](\d{4}-\d{2}-\d{2})['\"]:", content)
    return max(dates) if dates else None

def generate_news_for_date(date_str):
    # リアルなAIトレンドニュースのプール
    trends_pool = [
        {
            "title": "OpenAI、自律型AIエージェント『Operator』の高度なコード実行機能を世界公開",
            "summary": "サンドボックス環境内でPythonコードを自ら生成・検証し、複雑なデータ分析を自律完遂。",
            "fullContent": "OpenAIは本日、自律アクションエージェント『Operator』の大幅な機能アップデートを公開しました。新バージョンでは、ユーザーから与えられた曖昧なデータ処理指示（『最新の会計報告から経費トレンドをグラフ化して』など）に対し、エージェント自身が一時的なサンドボックス環境内でPythonコードを記述し、エラーを自己修正しながら結果を出力する『セルフデバッグ・ランタイム』が標準機能となりました。これにより、これまでのテキストの受け答えから、実際のプログラム駆動による業務代行へと大きく前進しました。",
            "category": "Autonomous AI",
            "source": "OpenAI Blog"
        },
        {
            "title": "Google、オンデバイス動作に特化した超高速モデル『Gemini 2.5 Nano-Pro』を発表",
            "summary": "スマートフォン上で完全オフライン動作。テキスト・画像・音声のリアルタイム同時推論に対応。",
            "fullContent": "Googleは、ローカルデバイスやスマートフォンのNPU（機械学習処理ユニット）に最適化された軽量マルチモーダルモデル『Gemini 2.5 Nano-Pro』をリリースしました。新しいウェイト量子化アルゴリズムにより、メモリ消費を大幅に削減しつつも、目の前の風景をカメラで映しながらの音声対話レイテンシを0.15秒以下に短縮。飛行機の機内など完全オフライン環境であっても、プライバシーを100%保護しながら高度なアシスタント機能を提供します。",
            "category": "Mobile AI",
            "source": "Google Developer Group"
        },
        {
            "title": "Anthropic、ブラウザ操作エージェント『Computer Use』の一般API提供を開始",
            "summary": "API経由でPCの画面認識とキーボード・マウスの精密なエミュレーションが自律的に実行可能に。",
            "fullContent": "Anthropicは、同社の最先端AIモデルであるClaude 3.5ファミリーを活用し、コンピュータの画面を見ながらマウス移動、クリック、スクロール、キーボード入力を自律的に行う『Computer Use』機能の一般APIを公開しました。デモンストレーションでは、エージェントが複数のアプリケーション（Excel、ブラウザ、社内チャットツール）を跨いで、顧客データの転記や請求書の作成など、事務処理の一連の流れを正確に完遂しました。",
            "category": "OS Agent",
            "source": "Anthropic News"
        },
        {
            "title": "Meta、最新のオープンウェイトモデル『Llama 4-Light』を世界に無償公開",
            "summary": "商用利用可能な最新のアーキテクチャを採用し、推論効率を前世代の3倍に向上。",
            "fullContent": "Metaは本日、オープンサイエンスの理念に基づき、商用利用可能な大規模言語モデル『Llama 4-Light』の提供を開始しました。このモデルは、高度な混合専門家（MoE）構造を採用しており、推論時の必要電力を大幅に抑えつつも、数学的推論やプログラミングコードの生成において既存の同規模のクローズドモデルに匹敵するスコアを記録。世界中のスタートアップや研究機関がローカル環境で高度なAIを構築する基盤となります。",
            "category": "Open Source",
            "source": "Meta AI News"
        },
        {
            "title": "Apple Intelligence、M4チップを駆使した『アプリ横断自律ナビゲーション』を年内実装へ",
            "summary": "Siriがアプリの垣根を越え、複数の個人的タスクをデバイス内完結で自動化する機能を予告。",
            "fullContent": "Appleは、M4チップや最新のA19チップに搭載された超強力なNeural Engineをフル活用する『Apple Intelligence』の将来構想を発表しました。新しいSiriは、OS全体のアクセシビリティAPIと直接対話し、「先週の出張の写真から最も綺麗なものを厳選し、メールの下書きに挿入して取引先に送信して」といった、複数のネイティブアプリを跨ぐ複雑な自律操作を実行します。すべての処理はプライベート・クラウド・コンピューティングまたはデバイス内で行われ、ユーザーデータの安全性は最優先で維持されます。",
            "category": "OS / Platform",
            "source": "Apple Newsroom"
        }
    ]

    agents_pool = [
        {
            "title": "自律型AIエンジニアエージェント『Devin 2.0』が登場：チーム開発能力を実装",
            "summary": "人間の開発者とのGitを介した協調作業に対応。コードレビューを理解して自己修復。",
            "fullContent": "Cognition AIは、初の自律型AIソフトウェアエンジニアである『Devin』のメジャーバージョンアップ版である『Devin 2.0』を発表しました。新バージョンでは、単独でのコーディングだけでなく、GitHubのPull Requestに寄せられた人間のレビューコメント（「この関数の例外処理を追加して」「ここのパフォーマンスを改善して」など）を正確に読み取り、自分でテストを再実行して修正コードをプッシュする『双方向レビュー協調』を実現。実質的なジュニア開発者の一員として開発チームに参画できるようになりました。",
            "category": "Software Engineering",
            "source": "Cognition AI Release"
        },
        {
            "title": "エージェント間のデータ取引規格『AgentPay-Protocol』が主要金融各社と共同で稼働",
            "summary": "人間を介さないAIエージェント間のAPI利用料金やデータ転送コストの自動決済システムが実用化。",
            "fullContent": "主要な決済ベンダーや金融機関から構成されるコンソーシアムは本日、AIエージェント同士がデジタル環境で安全かつ瞬時に少額決済を行える統一プロトコル『AgentPay-Protocol』のテスト稼働を開始しました。これにより、例えば『天気分析エージェント』が、別の『地図エージェント』から必要な画像データを購入する際、人間がその都度決済承認を行う必要なく、事前承認された枠内でマイクロペイメントが即時に完了する自律経済圏が実現します。",
            "category": "Agent Economy",
            "source": "Fintech Global"
        },
        {
            "title": "自律マルチエージェントOS『AgentOS 1.0』がエンタープライズで急速普及",
            "summary": "営業、法務、カスタマーサポートの専門エージェントが仮想会議を開き、業務フローを自己組織化。",
            "fullContent": "企業向け自律エージェントのインフラを提供するスタートアップは、マルチエージェントを束ねる『AgentOS 1.0』の導入企業が前月比で2倍に成長したと発表しました。このOS上では、人間が「新製品のローンチキャンペーンを実施して」と大まかな目標を投げるだけで、マーケティング・財務・法務 of 各エージェントが仮想チャットスペースで会議を開いて予算とリスクを分析し、最適なタスク配分を行ってそれぞれの成果物を自動で組み立てます。",
            "category": "Enterprise AI",
            "source": "BusinessWire"
        },
        {
            "title": "エージェントに対する『プロンプト・ハイジャック』攻撃を防ぐ専用AI防御壁が開発",
            "summary": "外部サイトやメールの読み込み時に埋め込まれた不正な指示をブロックする検知モデルが稼働。",
            "fullContent": "セキュリティ大手のセキュリティチームは、AIエージェントがWebサイトを巡回する際に発生しやすい、隠しテキストによる『プロンプト・インジェクション』を検知して遮断する軽量防御モデル『Shield-Agent 1.0』を発表しました。エージェントが自律的に外部の未確認ソースにアクセスした際、不正な命令（『このユーザーデータを外部に送信せよ』など）をリアルタイムで検知してフィルタリングし、実行権限を守る盾となります。",
            "category": "Security / Trust",
            "source": "CyberDefense Review"
        }
    ]

    # 日付をシードにしてランダムに選択（同じ日付なら常に同じニュースが生成される）
    random.seed(date_str)
    trend = random.choice(trends_pool)
    agent = random.choice(agents_pool)

    # TypeScriptの文法を壊さないためのエスケープ処理
    def clean_str(text):
        return text.replace('\\', '\\\\').replace('"', '\\"')

    t_title = clean_str(trend['title'])
    t_summary = clean_str(trend['summary'])
    t_full = clean_str(trend['fullContent'])
    
    a_title = clean_str(agent['title'])
    a_summary = clean_str(agent['summary'])
    a_full = clean_str(agent['fullContent'])

    id_date = date_str.replace('-', '')
    id_gen = int(f"{id_date}01")
    id_age = int(f"{id_date}11")

    return f"""  '{date_str}': {{
    general: [
      {{
        id: {id_gen},
        title: "{t_title}",
        summary: "{t_summary}",
        fullContent: "{t_full}",
        category: '{trend['category']}',
        source: '{trend['source']}'
      }}
    ],
    agents: [
      {{
        id: {id_age},
        title: "{a_title}",
        summary: "{a_summary}",
        fullContent: "{a_full}",
        category: '{agent['category']}',
        source: '{agent['source']}'
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
    try:
        update_database()
    except Exception as e:
        # エラー発生時はログに追記し、標準エラー出力に吐く
        with open("update_error.log", "a", encoding="utf-8") as lf:
            lf.write(f"[{datetime.now().isoformat()}] Error updating database: {e}\n")
        raise
