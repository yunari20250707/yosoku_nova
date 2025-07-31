import feedparser
from newspaper import Article
import json
import os
from datetime import datetime

# 対象RSSリスト
RSS_FEEDS = [
    "https://www3.nhk.or.jp/rss/news/cat5.xml",
    "https://www.nikkei.com/rss/economy.xml",
]

# 保存先ディレクトリ
SAVE_DIR = "data/news_articles"
MEMORY_PATH = "memory.json"  # 記憶ファイルのパス

def save_to_memory(articles, memory_path=MEMORY_PATH):
    """過去の記憶を保存する"""
    try:
        with open(memory_path, "r", encoding="utf-8") as f:
            memory = json.load(f)
    except FileNotFoundError:
        memory = []

    today_str = datetime.now().strftime("%Y-%m-%d")
    memory.append({"date": today_str, "articles": articles})

    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

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

        # 🧠 記憶に保存
        save_to_memory(all_articles)

    return all_articles

if __name__ == "__main__":
    print("🚀 Plan C｜RSSニュース取得開始")
    fetch_rss_articles()
