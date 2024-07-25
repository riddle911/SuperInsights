import json

class Config:
    # 读取配置文件
    with open('config.json', 'r') as f:
        config_data = json.load(f)

    # 获取 RSS feed 列表
    RSS_FEEDS = config_data.get('feeds', [])
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rss.db'
    OPENAI_API_KEY =''
    FETCH_INTERVAL = 3600  # 默认抓取间隔1小时
    OPENAI_URL = ' '
    OPENAI_MODEL = ' '
