import feedparser
import pandas as pd
from datetime import datetime

# RSS Feed URLs
RSS_FEEDS = {
    "MoneyControl": "https://www.moneycontrol.com/rss/MCtopnews.xml",
    "Economic Times": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "BBC Global": "http://feeds.bbci.co.uk/news/world/rss.xml"
}

def fetch_latest_news():
    """
    Fetches news from defined RSS feeds.
    Returns a list of dictionaries containing title, summary, link, source, and published date.
    """
    news_items = []
    
    # User-Agent to avoid 403 Forbidden
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching news from RSS feeds...")

    for source_name, url in RSS_FEEDS.items():
        try:
            # feedparser handles User-Agent via the `request_headers` argument if using internal fetcher, 
            # but standard usage is usually sufficient. 
            # However, sometimes we need to be explicit if feedparser's default fails.
            # feedparser.parse can take a URL.
            
            feed = feedparser.parse(url, agent=headers['User-Agent']) # agent param acts as User-Agent
            
            if feed.bozo:
                print(f"Warning: Issue parsing feed from {source_name}: {feed.bozo_exception}")
                # Continue processing what we got, if any
            
            for entry in feed.entries[:10]: # Limit to top 10 per feed to avoid overload
                summary = entry.get('summary', '') or entry.get('description', '')
                
                # HTML cleanup could be done here if needed, but we'll leave it raw or basic strip for now
                # In a real app we might use BeautifulSoup to clean summary text
                
                news_items.append({
                    "title": entry.get('title', 'No Title'),
                    "summary": summary,
                    "link": entry.get('link', '#'),
                    "source": source_name,
                    "published": entry.get('published', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                })
                
        except Exception as e:
            print(f"Error fetching {source_name}: {e}")
            continue

    print(f"Fetched {len(news_items)} total news items.")
    return news_items

if __name__ == "__main__":
    # Test run
    items = fetch_latest_news()
    for item in items[:3]:
        print(item)
