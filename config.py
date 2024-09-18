import json

class Config:
    # 读取配置文件
    with open('config.json', 'r') as f:
        config_data = json.load(f)

    # 获取 RSS feed 列表
    RSS_FEEDS = config_data.get('feeds', [])
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rss.db'
    OPENAI_API_KEY ='sk-otwhtpqjkhwffxrwmonqnlhhmjejakhptmjjnliybvmyonys' 
    FETCH_INTERVAL = 3600  # 默认抓取间隔1小时
    OPENAI_URL = 'https://api.siliconflow.cn/v1/chat/completions'
    OPENAI_MODEL = 'THUDM/glm-4-9b-chat'
    JINA_API_KEY = 'jina_12b404b1924f4573b9649a437f0bd9caDOnJhX8sq--UW2Fisme2p3Egi7nT'

     # 邮件配置
    MAIL_SERVER = 'smtp.qq.com'  # 替换为实际的SMTP服务器地址
    MAIL_PORT = 587  # 替换为实际的SMTP端口
    MAIL_USERNAME = 'riddle911@qq.com'  # 替换为实际的发件人邮箱
    MAIL_PASSWORD = 'vacmjtmhfnotdgch'  # 替换为实际的SMTP密码
    MAIL_DEFAULT_SENDER = 'riddle911@qq.com'  # 替换为实际的发件人邮箱
    MAIL_RECIPIENT = 'sleepwater911@gmail.com'  # 替换为实际的收件人邮箱
    #MAIL_RECIPIENT = '382988698@qq.com'  # 替换为实际的收件人邮箱