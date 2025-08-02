import json
import re
from collections import Counter

with open("memory.json", "r", encoding="utf-8") as f:
    memory = json.load(f)

others = [item for item in memory if item.get("category") == "other"]

words = []
for item in others:
    text = item.get("title", "") + item.get("summary", "")
    words.extend(re.findall(r'\w{2,}', text))

common_words = Counter(words).most_common(50)

print("🧠 otherに多く出現する単語トップ50：\n")
for word, count in common_words:
    print(f"{word}: {count}")

