import feedparser
from newspaper import Article
import json
import os
from datetime import datetime

# 日付を取得
date_str = datetime.now().strftime("%Y-%m-%d")

# RSSフィード一覧（必要ならここに他媒体も追加）
RSS_FEEDS = {
    "nhk": "https://www3.nhk.or.jp/rss/news/cat5.xml",
    "nikkei": "https://www.nikkei.com/rss/newstopics.rdf",
}

# 保存処理（空リストでも保存）
def save_articles(articles, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"✅ 保存完了: {filepath}")
    # 🔍 保存ファイル存在チェックログ
    if os.path.exists(filepath):
        print(f"📦 確認: ファイル存在 → {filepath}")
    else:
        print(f"⚠️ エラー: ファイルが存在しません → {filepath}")

# メイン処理
def fetch_rss_articles():
    print("🚀 Plan C | RSSニュース取得開始")
    for source, url in RSS_FEEDS.items():
        print(f"🌐 RSS取得中：{url}")
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries:
            try:
                article = Article(entry.link)
                article.download()
                article.parse()
                articles.append({
                    "title": article.title,
                    "text": article.text,
                    "url": entry.link,
                    "published": entry.get("published", ""),
                })
                print(f"📄 記事URL: {entry.link}")
            except Exception as e:
                print(f"❌ 取得失敗: {entry.link} → {e}")

        # 保存（記事が0件でも保存する）
        save_path = f"articles/{date_str}_{source}.json"
        save_articles(articles, save_path)

if __name__ == "__main__":
    fetch_rss_articles()