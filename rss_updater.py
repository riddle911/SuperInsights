import feedparser
from datetime import datetime
import json
import time
from models import RSSFeed, RawData, db

# 从配置文件加载 RSS feed 列表
def load_rss_feeds_from_config(config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config["feeds"]
    except FileNotFoundError:
        print(f"配置文件 {config_path} 不存在，请创建配置文件。")
        return []

# 解析 RSS feed
def parse_rss_feed(url, config_path="config.json"):
    """解析 RSS feed 并根据配置文件获取拉取数量和更新频次。

    Args:
        url (str): RSS feed URL
        config_path (str, optional): 配置文件路径。Defaults to "config.json".

    Returns:
        list: 解析后的 RSS 条目列表
    """
    print(f"Parsing RSS feed from: {url}")
    feed = feedparser.parse(url)
    entries = []

    # 加载配置文件
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"配置文件 {config_path} 不存在，请创建配置文件。")
        return None

    # 找到对应 URL 的配置信息
    feed_config = next((feed for feed in config["feeds"] if feed["url"] == url), None)

    if feed_config:
        num_entries = feed_config.get("num_entries", "all")
        #update_frequency = feed_config.get("update_frequency", 3600)  # 默认更新频率为 1 小时

        if num_entries == "all":
            for entry in feed.entries:
                entries.append({
                    'title': entry.title,
                    'pub_date': entry.published,
                    'link': entry.link
                })
        else:
            try:
                num_entries = int(num_entries)
                for i, entry in enumerate(feed.entries):
                    if i < num_entries:
                        entries.append({
                            'title': entry.title,
                            'pub_date': entry.published,
                            'link': entry.link
                        })
                    else:
                        break
            except ValueError:
                print(f"配置文件中 {url} 的拉取数量无效，请检查配置文件。")
                return None

        # 休眠，等待下次更新
        #time.sleep(update_frequency)

    else:
        print(f"配置文件中没有找到 {url} 的配置信息。")

    print(f"Parsed {len(entries)} entries from: {url}")
    return entries

# 更新 RSS 订阅
def update_rss_feeds():
    """更新 RSS 订阅并保存到 RawData 和 RSSFeed 表中"""
    urls = load_rss_feeds_from_config()
    print(f"Updating RSS feeds for URLs: {urls}")
    has_new_data = False
    for feed_config in urls:
        url = feed_config["url"]
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
