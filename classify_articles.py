import json
import re
import os
from datetime import date

MEMORY_FILE = "memory.json"

CATEGORY_KEYWORDS = {
    "economy": [
        "金利", "インフレ", "金融", "円安", "経済", "日銀", "景気", "株価", "物価", "企業", "決算",
        "赤字", "黒字", "価格", "値下がり", "値上がり", "株式市場", "証券", "補償",
        "投資", "企業業績", "ガソリン", "燃料", "自動車業界", "コマーシャル", "広告", "起業",
        "スタートアップ", "売り上げ", "デパート", "テーマパーク", "農水省", "米", "観光",
        "企業流出", "国債", "入札", "応札倍率", "工場", "閉鎖"
    ],
    "politics": [
        "選挙", "政府", "議会", "総理", "外交", "政策", "政党", "与党", "野党",
        "経産相", "関税引き下げ", "制度", "内部資料", "裏金"
    ],
    "technology": [
        "AI", "人工知能", "テクノロジー", "IT", "デジタル", "5G", "サイバー", "DX",
        "決済", "タッチ", "業務提携", "システム", "サービス", "電子マネー", "アプリ", "IoT", "デジタル決済",
        "3Dプリンター", "データセンター", "EV", "電気自動車", "生産開始", "人工衛星"
    ],
    "health": [
        "医療", "健康", "コロナ", "ワクチン", "感染", "病院", "薬", "がん", "認知症"
    ],
    "environment": [
        "気候変動", "環境", "エネルギー", "再生可能", "脱炭素", "温暖化", "二酸化炭素",
        "不漁", "漁獲", "サンマ", "水産資源", "漁業", "海洋環境", "収穫量", "原発", "建て替え", "農業"
    ],
    "international": [
        "アメリカ", "中国", "ウクライナ", "ロシア", "国連", "G7", "外交関係",
        "トランプ", "大統領", "米関税", "関税交渉", "為替", "ドル", "アメリカ経済",
        "貿易協定", "メキシコ", "インドネシア"
    ]
}

def classify(text):
    tags = []
    categories = set()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if re.search(kw, text):
                tags.append(kw)
                categories.add(category)
    return list(categories)[0] if categories else "other", list(set(tags))

# メモリ読み込み
with open(MEMORY_FILE, "r", encoding="utf-8") as f:
    memory = json.load(f)

updated = 0
for item in memory:
    if item.get("category") in ["unknown", None, "", "other"]:
        text = item.get("summary", "").strip() or item.get("title", "").strip()
        category, tags = classify(text)
        item["category"] = category
        item["tags"] = tags
        updated += 1

# 上書き保存
with open(MEMORY_FILE, "w", encoding="utf-8") as f:
    json.dump(memory, f, ensure_ascii=False, indent=2)

print(f"✅ 分類完了: {updated}件を分類しました")

# 🔽 今日の日付で分類結果を別ファイルに保存
today_str = str(date.today())
output_dir = "classified_articles"
os.makedirs(output_dir, exist_ok=True)
output_file = f"{output_dir}/{today_str}_classified.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(memory, f, ensure_ascii=False, indent=2)

print(f"✅ 分類結果を {output_file} に保存しました")
