import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数読み込み（.env内の OPENAI_API_KEY 取得）
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 日付設定
today = datetime.now().strftime("%Y-%m-%d")
input_path = f"articles/{today}_nikkei.json"
output_path = f"memory/{today}_summary.json"

# 入力記事の読み込み
if not os.path.exists(input_path):
    print(f"❌ 記事ファイルが存在しません: {input_path}")
    exit()

with open(input_path, "r", encoding="utf-8") as f:
    articles = json.load(f)

# 出力保存用リスト
summaries = []

# 要約ループ
for i, article in enumerate(articles, 1):
    print(f"🧠 要約中: {article['title']}")

    content = article["title"] + "\n\n" + article["content"]
    prompt = f"""
以下は日本の経済ニュースです。内容を読み、重要な情報だけを抜き出し、以下の3点にまとめてください：

1. 記事の主な内容を200文字以内で要約
2. 抽出されたキーワード（3〜5語）
3. 今後の日本経済への影響や懸念点（あれば）

--- 記事 ---
{content}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        summary_text = response.choices[0].message.content.strip()
        summaries.append({
            "title": article["title"],
            "url": article["url"],
            "summary": summary_text,
            "timestamp": article["publishedAt"]
        })

    except Exception as e:
        print(f"⚠️ 要約エラー: {e}")

# 保存処理
os.makedirs("memory", exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(summaries, f, ensure_ascii=False, indent=2)

print(f"✅ 学習データ保存完了: {output_path}")
