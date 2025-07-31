import json
from collections import Counter

MEMORY_FILE = "memory.json"
OUTPUT_FILE = "docs/trend.md"
TOP_N = 5

# メモリ読み込み
with open(MEMORY_FILE, "r", encoding="utf-8") as f:
    memory = json.load(f)

# カテゴリごとのタグ集計
category_tags = {}

for item in memory:
    category = item.get("category", "other")
    tags = item.get("tags", [])
    if not tags or category == "other":
        continue
    category_tags.setdefault(category.upper(), []).extend(tags)

# Markdown形式で出力
output_lines = []
for category, tags in category_tags.items():
    output_lines.append(f"## 📊 {category}")
    counter = Counter(tags)
    for tag, count in counter.most_common(TOP_N):
        output_lines.append(f"- {tag}: {count}回")
    output_lines.append("")

# 保存
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"📝 トレンドレポートを {OUTPUT_FILE} に保存しました")
