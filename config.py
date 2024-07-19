import json

class Config:
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    
    RSS_URLS = config_data.get('rss_urls', [])
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rss.db'
    JINA_API_KEY = 'jina_69774ca7f6eb4afeb2a11f83076720041YFr3qoNM2hGp5DFlAPJ_UZfISmh'
    SILICONFLOW_API_KEY = 'sk-ltntgjbizjfarxzuocugfsxrbdjgefydhiemorhqnfmitshl'
    FETCH_INTERVAL = 3600  # 默认抓取间隔1小时
    OPENAI_URL = 'https://api.siliconflow.cn/v1/chat/completions'
    OPENAI_MODEL = 'deepseek-ai/DeepSeek-V2-Chat'