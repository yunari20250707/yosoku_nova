import os
import json
from datetime import datetime
from transformers import pipeline

# 🔧 要約モデル（Hugging Face）
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# 📅 最新ファイルを自動取得（data/news_articles/）
data_dir = "data/news_articles"
files = sorted(os.listdir(data_dir), reverse=True)
latest_file = [f for f in files if f.endswith(".json")][0]
file_path = os.path.join(data_dir, latest_file)

print(f"🧠 要約処理対象: {latest_file}")

# 🔄 読み込み
with open(file_path, "r", encoding="utf-8") as f:
    articles = json.load(f)

# ✅ 要約処理
summarized = []
for article in articles:
    text = article.get("text", "")
    if not text.strip():
        continue

    try:
        summary = summarizer(text[:1024], max_length=120, min_length=30, do_sample=False)[0]["summary_text"]
    except Exception as e:
        print(f"⚠️ 要約エラー: {article.get('title', '')} → {e}")
        summary = ""

    summarized.append({
        "title": article.get("title", ""),
        "url": article.get("url", ""),
        "published": article.get("published", ""),
        "summary": summary
    })

# 💾 保存先
output_dir = "summarized_articles"
os.makedirs(output_dir, exist_ok=True)

out_path = os.path.join(output_dir, latest_file.replace("rss_articles", "summaries"))
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(summarized, f, ensure_ascii=False, indent=2)

print(f"✅ 要約完了 → {out_path}")
