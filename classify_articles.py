import os
import json
from transformers import pipeline

# 🔧 カテゴリ分類モデル（zero-shot）
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# 📂 最新要約ファイルを取得
data_dir = "summarized_articles"
files = sorted(os.listdir(data_dir), reverse=True)
latest_file = [f for f in files if f.endswith(".json")][0]
file_path = os.path.join(data_dir, latest_file)

print(f"🧭 分類対象: {latest_file}")

# 📖 カテゴリ候補ラベル
labels = [
    "経済・金融", "政治・行政", "国際・外交", "災害・天気",
    "科学・技術", "社会・事件", "環境・エネルギー", "その他"
]

# 🔄 要約読み込み
with open(file_path, "r", encoding="utf-8") as f:
    summaries = json.load(f)

# ✅ 分類実行
classified = []
for article in summaries:
    summary = article.get("summary", "")
    if not summary:
        continue

    try:
        result = classifier(summary, labels, multi_label=False)
        best_label = result["labels"][0]
    except Exception as e:
        print(f"⚠️ 分類エラー: {article.get('title', '')} → {e}")
        best_label = "未分類"

    article["category"] = best_label
    classified.append(article)

# 💾 保存先
output_dir = "classified_articles"
os.makedirs(output_dir, exist_ok=True)

out_path = os.path.join(output_dir, latest_file.replace("summaries", "classified"))
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(classified, f, ensure_ascii=False, indent=2)

print(f"✅ 分類完了 → {out_path}")
