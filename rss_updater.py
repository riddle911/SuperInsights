from rss_parser import parse_rss_feed
from models import RSSFeed, RawData, db
from config import Config

def update_rss_feeds():
    """更新 RSS 订阅并保存到 RawData 和 RSSFeed 表中"""
    urls = Config.RSS_URLS
    print(f"Updating RSS feeds for URLs: {urls}")
    has_new_data = False
    for url in urls:
        print(f"Parsing RSS feed from: {url}")
        entries = parse_rss_feed(url)
        for entry in entries:
            # 检查 RSSFeed 表中是否已存在相同链接的记录
            existing_feed = RSSFeed.query.filter_by(link=entry['link']).first()
            if existing_feed:
                print(f"Skipping duplicate entry with link: {entry['link']}")
                continue

            # 创建 RSSFeed 对象
            rss_feed = RSSFeed(
                url=url,
                title=entry['title'],
                pub_date=entry['pub_date'],
                link=entry['link']
            )

            # 添加 RSSFeed 对象到数据库
            db.session.add(rss_feed)

            # 创建 RawData 对象
            raw_data = RawData(
                url=url,
                title=entry['title'],
                pub_date=entry['pub_date'],
                link=entry['link']
            )

            # 添加 RawData 对象到数据库
            db.session.add(raw_data)
            db.session.commit()
            print(f"Added entry to RawData and RSSFeed tables: {entry['title']}")
            has_new_data = True

    return has_new_data