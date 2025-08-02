import json

with open("memory.json", "r", encoding="utf-8") as f:
    memory = json.load(f)

others = [item for item in memory if item.get("category") == "other"]

print(f"🧐 other分類: {len(others)} 件\n")

for i, item in enumerate(others[:30]):  # まずは30件だけ見る
    print(f"\n【{i+1}】")
    print(f"📌 タイトル: {item.get('title')}")
    print(f"📝 サマリ: {item.get('summary')[:150]}")

