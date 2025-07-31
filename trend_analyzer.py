import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta

MEMORY_FILE = "memory.json"

def load_memory():
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_trends(days=7):
    memory = load_memory()
    now = datetime.now()
    cutoff = now - timedelta(days=days)

    trends = defaultdict(Counter)

    for item in memory:
        category = item.get("category", "other")
        tags = item.get("tags", [])
        date_str = item.get("date")

        # 日付が無ければスキップ
        if not date_str:
            continue

        try:
            dt = datetime.fromisoformat(date_str)
        except ValueError:
            continue

        if dt >= cutoff:
            for tag in tags:
                trends[category][tag] += 1

    return trends

if __name__ == "__main__":
    trend_data = analyze_trends(days=7)
    for category, counter in trend_data.items():
        print(f"📊 {category.upper()}")
        for tag, count in counter.most_common(5):
            print(f"  - {tag}: {count}回")
        print()
