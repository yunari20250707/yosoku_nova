import os
import json
import shutil
from datetime import datetime
from pytz import timezone

PREDICTIONS_DIR = "predicted_future"
REPORTS_DIR = "daily_reports"
DOCS_INDEX_PATH = "docs/index.md"
HTML_INDEX_PATH = "index.html"

def load_latest_prediction():
    """最新の予測ファイルを読み込む（ファイル内の日付も返す）"""
    json_files = [
        f for f in os.listdir(PREDICTIONS_DIR) if f.endswith(".json")
    ]

    def extract_date(filename):
        try:
            return datetime.strptime(filename.split("_")[0], "%Y-%m-%d")
        except ValueError:
            return datetime.min

    sorted_files = sorted(json_files, key=extract_date, reverse=True)

    for file in sorted_files:
        path = os.path.join(PREDICTIONS_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return data, data[0].get("date", "unknown")
    return None, None

def generate_report_content(prediction_data, report_date):
    if isinstance(prediction_data, list) and len(prediction_data) > 0:
        first_item = prediction_data[0]
        category = first_item.get("category", "その他")
        summary = first_item.get("summary", "概要なし")
        prediction = first_item.get("prediction", "予測内容なし")
    else:
        category = "その他"
        summary = "概要なし"
        prediction = "予測内容なし"

    return f"""\
【未来予測レポート】📅 {report_date}

🗂 カテゴリ: {category}

📝 要約:
{summary}

🔮 未来予測:
{prediction}

---

🧠 powered by NOVA｜未来予測AI
"""

def save_report(content, report_date):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filename = f"report_{report_date}_predictions.txt"
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✅] レポートを保存しました: {path}")
    return path

def generate_html_report(txt_content):
    html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>未来予測レポート｜NOVA</title>
    <style>
        body { font-family: sans-serif; line-height: 1.8; margin: 2em; background: #f9f9f9; }
        h1 { color: #333; }
        p { margin-bottom: 1em; }
    </style>
</head>
<body>
"""
    for line in txt_content.splitlines():
        if line.strip() == "":
            html += "<br>\n"
        elif line.startswith("【"):
            html += f"<h1>{line}</h1>\n"
        else:
            html += f"<p>{line}</p>\n"
    html += '<div style="margin-top:2em;font-size:0.9em;color:#666;">🧠 powered by NOVA｜未来予測AI</div>\n</body>\n</html>'
    return html

def main():
    data, report_date = load_latest_prediction()
    if not data:
        print("[⚠️] 予測データが見つかりません。")
        return

    content = generate_report_content(data, report_date)
    output_path = save_report(content, report_date)

    shutil.copyfile(output_path, DOCS_INDEX_PATH)
    print(f"[📄] docs/index.md にコピーしました。")

    html = generate_html_report(content)
    with open(HTML_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[🌐] HTMLファイルを作成: {HTML_INDEX_PATH}")

if __name__ == "__main__":
    main()
