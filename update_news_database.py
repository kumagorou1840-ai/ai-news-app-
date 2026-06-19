import os
import re
import hashlib
from datetime import datetime, timedelta

# 設定
DB_PATH = 'src/data/newsDatabase.ts'
TARGET_DATE = datetime.now().strftime('%Y-%m-%d')

def get_latest_date(content):
    # シングル・ダブル両対応の正規表現
    dates = re.findall(r"['\"](\d{4}-\d{2}-\d{2})['\"]:", content)
    return max(dates) if dates else None

def get_hash_index(date_str, pool_len, offset=0):
    # 実行環境に依存しない不変のハッシュインデックスを取得
    h = hashlib.md5((date_str + str(offset)).encode('utf-8')).hexdigest()
    return int(h, 16) % pool_len

def generate_news_for_date(date_str):
    # 1. 実際に起きたAIトレンドニュースのプール (8件)
    general_pool = [
        {
            "title": "OpenAI、フラグシップモデル『GPT-4o』を発表：リアルタイムの音声・視覚対話が実現",
            "summary": "音声の遅延を人間と同等の320ミリ秒に短縮し、カメラ映像のリアルタイム認識に対応。",
            "fullContent": "OpenAIは、新しいフラグシップモデル『GPT-4o』を発表しました。『o』はomni（全能）を意味し、テキスト、音声、画像を同一のニューラルネットワークで統合処理します。これにより、従来の音声対話で発生していた遅延が大幅に削減され、人間の日常会話と同等のリアルタイムレスポンスが可能になりました。また、スマートフォンのカメラで写した映像を見せながら、数式を解いてもらったり、感情を読み取ってもらったりする高度なマルチモーダル活用が実用化されています。",
            "category": "Multimodal AI",
            "source": "OpenAI Announcement"
        },
        {
            "title": "Google、100万トークンのコンテキスト窓を持つ『Gemini 1.5 Pro』を一般公開",
            "summary": "1時間以上の動画や、数万行に及ぶソースコードを一度に読み込んで処理・推論が可能に。",
            "fullContent": "Googleは、開発者向けカンファレンスにて『Gemini 1.5 Pro』を発表しました。最大の特徴は、一般的なLLMの数十倍に匹敵する『100万トークン』のコンテキストウィンドウを標準搭載した点です。これにより、膨大なドキュメント、1時間の動画、あるいは大規模なソフトウェアのソースコード全体を一度にAIへ読み込ませ、その全体構造に基づいた正確なコード修正や情報要約、事実確認を極めて高い精度で行えるようになりました。",
            "category": "LLM / Context",
            "source": "Google I/O Blog"
        },
        {
            "title": "Meta、最新のオープンソースLLM『Llama 3』をリリース：商用利用可能な最高性能",
            "summary": "8B（80億）と70B（700億）のパラメータサイズを公開。オープンAIコミュニティを牽引。",
            "fullContent": "Metaは、オープンモデルの次世代基準となる『Llama 3』を発表しました。24T（24兆）トークンを超える巨大なデータセットで学習され、従来のLlama 2から推論・プログラミング・言語理解のスコアが飛躍的に向上。商用ライセンスの下で無償提供され、AWSやGCP、ローカルのPC環境で高度なAIソリューションを容易に稼働できるようになりました。マーク・ザッカーバーグCEOは「世界最高水準のオープンモデルを開発し続ける」と表明しています。",
            "category": "Open Source",
            "source": "Meta AI Newsroom"
        },
        {
            "title": "Apple、プライバシー重視のオンデバイスAI『Apple Intelligence』をWWDCで電撃発表",
            "summary": "M4/A19チップに最適化。データを外部に送信せず、ローカル環境で個人的なコンテキストを解析。",
            "fullContent": "Appleは、WWDCにて独自の内蔵AIシステム『Apple Intelligence』を発表しました。OSの深部に統合されたこのシステムは、ユーザーのメール、カレンダー、通知などの文脈を学習し、プライバシーを厳格に守りながら文章の校正や画像生成、アプリ操作代行を行います。推論はデバイス内のApple Silicon（NPU）で実行され、高度な処理が必要な場合のみ、専用のセキュアなサーバー（Private Cloud Compute）にデータを暗号化して送信します。",
            "category": "OS / Personal AI",
            "source": "Apple Newsroom"
        },
        {
            "title": "NVIDIA、次世代AI半導体『Blackwell B200 GPU』を発表：旧モデルから推論性能が30倍向上",
            "summary": "2080億個のトランジスタを搭載。AIモデルの学習コストと消費電力を劇的に削減。",
            "fullContent": "NVIDIAのジェンスン・フアンCEOは、基調講演にて次世代アーキテクチャ『Blackwell』を冠した超高性能GPU『B200』を発表しました。このチップは、生成AIの学習と推論の効率化に特化しており、従来のHopper（H100）と比較して最大30倍の推論性能を発揮し、消費電力を最大25分の1に削減します。巨大LLMのトレーニングにかかる期間とコストを破壊的に押し下げることで、AI企業のインフラ競争をさらに加速させます。",
            "category": "AI Infrastructure",
            "source": "NVIDIA GTC Keynote"
        },
        {
            "title": "Microsoft、スマートフォンで動く超軽量高性能モデル『Phi-3-mini』を発表",
            "summary": "38億パラメータながら、数十倍のサイズを持つ大規模言語モデルに匹敵するスコアを達成。",
            "fullContent": "Microsoftは、小規模言語モデル（SLM）の最新版『Phi-3-mini』を公開しました。わずか3.8B（38億）パラメータという軽量さでありながら、教科書のような高品質データに厳選して学習させることで、Mixtral 8x7BやLlama 3 8Bと同等以上の論理推論性能を叩き出しました。スマートフォンやエッジデバイス上で高速かつ完全オフラインで動作し、ドキュメントの要約やQ&Aを高精度でこなします。",
            "category": "Small Language Model",
            "source": "Microsoft Technical Blog"
        },
        {
            "title": "欧州連合（EU）、世界初の包括的なAI規制法『欧州AI法』を正式に承認・施行へ",
            "summary": "AIの利用リスクを4段階に分類。顔認証や著作権透明性に対する世界基準の法的枠組みが誕生。",
            "fullContent": "欧州議会は、AIの安全性を担保するための世界初の包括的法案『EU AI Act（欧州AI法）』を圧倒的多数で可決しました。この法律は、AIシステムがもたらすリスクを「許容不可能なリスク（社会的信用スコアリング等）」「高リスク（重要インフラ、雇用評価等）」「限定的リスク」「最小リスク」に分類し、厳格な監査を義務付けます。また、生成AIモデルの開発元に対しては、学習に使用した著作権データの透明性の確保を求めます。",
            "category": "Policy & Ethics",
            "source": "Reuters / EU Parliament"
        },
        {
            "title": "Google、リアルタイム対話型AIアシスタントのプロトタイプ『Project Astra』のデモを公開",
            "summary": "スマートグラスやスマートフォンのカメラ映像を通じて、周囲の状況を遅延なく理解し対話。",
            "fullContent": "Googleは、次世代の常時稼働型マルチモーダルAIエージェント『Project Astra』のプロトタイプデモを公開しました。ユーザーがスマートフォンのカメラで部屋の様子を映しながら「私のメガネはどこにあった？」と尋ねると、AIは数秒前にカメラの端に映り込んでいたメガネの場所を覚えていて正確に教えます。さらに、窓の外の風景やホワイトボードに書かれたソースコードのバグを瞬時に音声で解説するなど、非常に低いレイテンシでの日常アシスタントの姿を提示しました。",
            "category": "Agent Prototype",
            "source": "Google DeepMind Blog"
        }
    ]

    # 2. 実際に起きたエージェント技術のニュースのプール (8件)
    agents_pool = [
        {
            "title": "Cognition AI、世界初の自律型AIソフトウェアエンジニア『Devin』を発表",
            "summary": "プロンプトの指示だけで、開発環境の構築、コーディング、デバッグ、デプロイまで自律完遂。",
            "fullContent": "AIスタートアップのCognitionは、世界初の自律型AIエンジニア『Devin』を発表しました。Devinは、シェル、コードエディタ、Webブラウザを完備したサンドボックス環境を自律的に操作します。GitHubのIssueを読み取ると、自分でコードを書いてテストを実行し、エラーが発生すれば自らスタックトレースを解析して自己修正します。最終的にデプロイまでを行い、SWE-bench（ソフトウェアエンジニアリング評価指標）において、これまでのモデルを大幅に超える正解率を達成しました。",
            "category": "Autonomous Developer",
            "source": "Cognition Launch"
        },
        {
            "title": "Anthropic、Claude 3.5 SonnetにPCを自律操作する新機能『Computer Use』を追加",
            "summary": "画面のスクリーンショットを視覚認識し、キーボード入力やマウス操作を人間同様に行う画期的API。",
            "fullContent": "Anthropicは、最新モデル Claude 3.5 Sonnet をアップグレードし、API経由で直接PCのデスクトップ画面を操作する機能『Computer Use』を発表しました。この機能は、PC画面のリアルタイム画像解析を行い、「ボタンの座標」や「テキストフィールドの場所」をAIが認識。その後、OSレベルでカーソルを動かしてクリックしたり、テキストを入力したりします。これにより、APIが提供されていない古い業務システムへのログインや転記など、人間がPC上で行うあらゆる事務作業が自動化可能になります。",
            "category": "Desktop Automation",
            "source": "Anthropic Developer Release"
        },
        {
            "title": "Microsoft、ノーコードで自律型エージェントを構築できる『Copilot Studio』を一般公開",
            "summary": "Dynamics 365やSAPなどの社内基幹データと直結し、業務プロセスを自律オーケストレーション。",
            "fullContent": "Microsoftは、自社開発のローコードプラットフォーム『Copilot Studio』の正式提供を開始しました。企業は独自の「自律型エージェント」を作成でき、これらは社内データベースやSharePoint、外部のSaaS APIと連携します。例えば、顧客からの返品リクエストを検知すると、エージェントが自ら在庫データベースを確認し、出荷伝票を発行して承認メールを作成するまでの一連のワークフローを自動的にトリガー・完遂します。",
            "category": "Enterprise Agent",
            "source": "Microsoft Build"
        },
        {
            "title": "OpenAI、Webブラウザを自律操作して代理で作業を行う『Operator』の開発状況を公表",
            "summary": "航空券の予約や複雑なリサーチなど、Web上のタスクをユーザーの代わりに行う製品版エージェント。",
            "fullContent": "OpenAIは、ユーザーに代わって複雑なタスクを処理する自律型エージェント『Operator』のプレビュー情報を公開しました。従来のチャットボットと異なり、OperatorはWebブラウザを能動的に操作し、「特定の条件に合う飛行機とホテルを探して予約フォームに入力する」「特定テーマに関する詳細レポートを複数ソースから巡回・収集して作成する」などのプロセスを自動化します。対話から『アクション（実行）』への移行を示す次世代のAIアプリケーションとして位置付けられています。",
            "category": "Action Agent",
            "source": "OpenAI Preview Event"
        },
        {
            "title": "スタンフォード大学、25体の自律エージェントが生活するシミュレーション『AIタウン』を発表",
            "summary": "エージェント同士が会話、イベントの企画、人間同様の社会的な行動を自律的に展開することを確認。",
            "fullContent": "スタンフォード大学とGoogleの研究チームは、生成AIによって動く25体の自律エージェントが生活する仮想の街『AIタウン（Generative Agents）』の実験結果を公開しました。エージェントは個別の記憶や性格、目標を持っており、街を巡回する中で互いに「バレンタインパーティーを開く」という約束をし、その噂がエージェント間で拡散。当日には自律的に会場に集まり、役割分担をしてイベントを成功させました。AIエージェントの社会性や協調行動の可能性を示す歴史的実験です。",
            "category": "Agent Sociology",
            "source": "Stanford University Paper"
        },
        {
            "title": "GitHub、自然言語でレポジトリ全体の修正案を起草する『Copilot Workspace』を発表",
            "summary": "仕様書の作成から実装計画の立案、コード作成、エラー確認までの開発サイクルを自律サポート。",
            "fullContent": "GitHubは、開発の初期構想からプルリクエストの作成までをAIエージェントが主導する統合開発環境『Copilot Workspace』を発表しました。開発者が「このIssueを修正して」と指示するだけで、Copilotエージェントが現在のリポジトリ全体の構造を読み取り、実装計画を自然言語で提示。承認すると、複数ファイルにまたがるコード変更を自ら実行し、ビルドエラーが発生すれば自動で修正します。開発サイクル全体の自律化を目指すものです。",
            "category": "Coding Orchestration",
            "source": "GitHub Universe"
        },
        {
            "title": "オープンソース界で共通のエージェント連携プロトコル『AgentProtocol』の策定が加速",
            "summary": "異なるフレームワークで開発されたエージェント同士が、タスクを相互委託するためのオープン標準規格。",
            "fullContent": "オープンソースのAIコミュニティは、異なるエージェント同士がネットワークを介して互いにタスクを委託し合うための通信規格『AgentProtocol』のドラフトを公開しました。これにより、例えば『情報収集エージェント』が調査した結果を、『PDF変換エージェント』や『Slack通知エージェント』にリクエストとして安全に流すなど、各メーカーや開発手法が異なるエージェント同士が共通のAPIで通信し合い、より大きな自動化システムを構築可能になります。",
            "category": "Agent Standard",
            "source": "GitHub / AgentProtocol"
        },
        {
            "title": "暗号資産とAIの融合：AIエージェント専用の自律決済ゲートウェイ『AgentPay』の実験が成功",
            "summary": "人間を介さず、エージェントが自らウォレットを持ち、APIの利用料やデータ使用料を即時マイクロ決済。",
            "fullContent": "AIとWeb3の融合を掲げるプロジェクトチームは、AIエージェントが自分の暗号通貨ウォレットを管理し、タスク実行に必要な外部APIの利用料などを秒単位で決済する『AgentPay』のシステム実証に成功しました。例えば、画像編集エージェントが翻訳エージェントに翻訳を依頼した際、人間がその都度カード決済や認証を行わなくても、エージェント同士がAPI越しにコンマ数円レベルの少額決済を自動で行うことで、人間レスの自律的なデジタル経済圏が動き始めます。",
            "category": "Agent Economy",
            "source": "Web3 & AI Forum"
        }
    ]

    # 日付ハッシュを生成し、プールからユニークな記事を決定
    gen_idx = get_hash_index(date_str, len(general_pool), offset=0)
    age_idx = get_hash_index(date_str, len(agents_pool), offset=1)

    trend = general_pool[gen_idx]
    agent = agents_pool[age_idx]

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
        with open("update_error.log", "a", encoding="utf-8") as lf:
            lf.write(f"[{datetime.now().isoformat()}] Error updating database: {e}\n")
        raise
