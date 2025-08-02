import os
import json
from datetime import date
from glob import glob

# ▼ 今日の日付を取得
today = date.today().strftime("%Y-%m-%d")
summary_file = f"memory/{today}_summary.json"
memory_file = "memory.json"

# フォルダがなければ作成
os.makedirs("memory", exist_ok=True)

# memory.json の読み込み（初回は空）
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as f:
        try:
            memory = json.load(f)
        except json.JSONDecodeError:
            memory = []
else:
    memory = []

# ▼ 記事ファイルの読み込み
article_files = glob("data/news_articles/*.json")

if not article_files:
    print("⚠️ 学習対象ファイルが見つかりません。スキップします。")
else:
    new_entries = 0
    today_summary = []

    for file_path in article_files:
        print(f"🧠 学習中: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                articles = json.load(f)
        except Exception as e:
            print(f"❌ 読み込み失敗: {file_path} → {e}")
            continue

        for article in articles:
            entry = {
                "date": today,
                "title": article.get("title", ""),
                "category": "unknown",
                "source": article.get("source", ""),
                "summary": article.get("content", "")[:200],
                "prediction": "未予測",
                "tags": []
            }
            memory.append(entry)
            today_summary.append(entry)
            new_entries += 1

    # ▼ memory.json に保存
    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

    # ▼ 日付別 summary ファイルも保存
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(today_summary, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(article_files)}ファイルから {new_entries} 件を記憶しました！")
    print(f"📝 保存完了: {summary_file}")
