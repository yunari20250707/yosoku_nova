import os
import json
import shutil
from datetime import datetime

PREDICTIONS_DIR = "predicted_future"
REPORTS_DIR = "daily_reports"
DOCS_INDEX_PATH = "docs/index.md"
HTML_INDEX_PATH = "index.html"

def load_latest_prediction():
    """最新の予測結果ファイルを読み込む"""
    files = sorted(os.listdir(PREDICTIONS_DIR), reverse=True)
    for file in files:
        if file.endswith(".json"):
            path = os.path.join(PREDICTIONS_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f), file
    return None, None

def generate_report_content(prediction_data):
    """予測データからレポート本文を生成"""
    date = prediction_data.get("date", "不明な日付")
    category = prediction_data.get("category", "その他")
    summary = prediction_data.get("summary", "概要なし")
    prediction = prediction_data.get("prediction", "予測内容なし")
    
    return f"""\
【未来予測レポート】📅 {date}

🗂 カテゴリ: {category}

📝 要約:
{summary}

🔮 未来予測:
{prediction}

---

🧠 powered by NOVA｜未来予測AI
"""

def save_report(content, base_filename):
    """生成したレポートを daily_reports に保存"""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    filename = f"report_{base_filename.replace('.json', '.txt')}"
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✅] レポートを保存しました: {path}")
    return path  # ← ここでパスを返す！

def generate_html_report(txt_content):
    """テキストをHTMLに変換する"""
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
    data, filename = load_latest_prediction()
    if not data:
        print("[⚠️] 予測データが見つかりません。")
        return

    # レポート作成と保存
    content = generate_report_content(data)
    output_path = save_report(content, filename)

    # Markdownにコピー
    shutil.copyfile(output_path, DOCS_INDEX_PATH)
    print(f"[📄] docs/index.md にコピーしました。")

    # HTMLも作成して index.html に出力
    html = generate_html_report(content)
    with open(HTML_INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[🌐] HTMLファイルを作成: {HTML_INDEX_PATH}")

if __name__ == "__main__":
    main()
