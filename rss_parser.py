import feedparser
from datetime import datetime

def parse_rss_feed(url):
    print(f"Parsing RSS feed from: {url}")
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
        entries.append({
            'title': entry.title,
            'pub_date': entry.published,
            'link': entry.link
        })
    print(f"Parsed {len(entries)} entries from: {url}")
    return entries