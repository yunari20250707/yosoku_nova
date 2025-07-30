import requests
import os
import json
from datetime import datetime
from config import NEWS_HISTORY_DIR, NEWS_API_KEY, timestamp

def fetch_today_news():
    # キーワード候補を順に試す
    keywords = ["経済", "金融", "市場", "日本", "ビジネス", "物価", "政府", "投資"]
    for keyword in keywords:
        print(f"🔍 試行中キーワード: {keyword}")
        url = (
            "https://newsapi.org/v2/everything?"
            f"q={keyword}&pageSize=10&sortBy=publishedAt&language=ja&apiKey={NEWS_API_KEY}"
        )
        res = requests.get(url)

        if res.status_code != 200:
            print("❌ ニュース取得失敗:", res.text)
            continue

        data = res.json()
        print("📦 APIレスポンス全体：\n", json.dumps(data, ensure_ascii=False, indent=2))

        if data.get("articles"):
            # 最初に見つかったニュースでOK
            top_article = data["articles"][0]
            title = top_article.get("title", "").strip()
            desc = top_article.get("description", "").strip()
            if title or desc:
                return f"{title}。{desc}"

    # 全て失敗したら、最終手段として固定ニュースを返す
    print("⚠️ ニュース記事が見つかりませんでした。")
    return "本日のニュース記事は見つかりませんでしたが、NOVAは前日データまたは予備教材を用いて学習を継続します。"

if __name__ == "__main__":
    print("🔁 ニュース取得処理を開始します…")
    news_text = fetch_today_news()
    print("📩 取得結果：", news_text)

    if news_text and "見つかりません" not in news_text:
        filename = f"{timestamp()}.json"
        filepath = os.path.join(NEWS_HISTORY_DIR, filename)
        os.makedirs(NEWS_HISTORY_DIR, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"text": news_text}, f, ensure_ascii=False, indent=2)

        print(f"✅ 保存完了: {filepath}")
    else:
        print("⚠️ 保存対象のニュースがありませんでしたが、予備テキストでNOVAは学習を継続します。")
