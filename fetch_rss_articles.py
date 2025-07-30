import feedparser
from newspaper import Article
import json
import os
from datetime import datetime

# 対象RSSリスト（必要に応じて増やせる）
RSS_FEEDS = [
    "https://www3.nhk.or.jp/rss/news/cat5.xml",        # NHK 経済
    "https://www.nikkei.com/rss/economy.xml",          # 日経 経済
]

# 保存先ディレクトリ
SAVE_DIR = "data/news_articles"

def fetch_rss_articles():
    os.makedirs(SAVE_DIR, exist_ok=True)
    all_articles = []

    for url in RSS_FEEDS:
        print(f"\n🌐 RSS取得中: {url}")
        feed = feedparser.parse(url)
        for entry in feed.entries:
            article_url = entry.link
            print(f"📰 記事URL: {article_url}")
            try:
                article = Article(article_url, language='ja')
                article.download()
                article.parse()
                article.nlp()

                record = {
                    "title": article.title,
                    "url": article_url,
                    "text": article.text,
                    "summary": article.summary,
                    "published": entry.get("published", ""),
                }
                all_articles.append(record)

            except Exception as e:
                print(f"❌ 取得失敗: {article_url} → {e}")

    if not all_articles:
        print("\n⚠️ 取得できた記事がありませんでした。")
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(SAVE_DIR, f"{today}_rss_articles.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)
        print(f"\n✅ {len(all_articles)}件の記事を保存しました → {file_path}")

    return all_articles

if __name__ == "__main__":
    print("🚀 Plan C｜RSSニュース取得開始")
    fetch_rss_articles()
