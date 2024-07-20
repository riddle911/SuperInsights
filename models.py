from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RSSFeed(db.Model):
    """RSS 订阅信息模型"""
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    title = db.Column(db.String)
    pub_date = db.Column(db.TEXT)
    link = db.Column(db.String, unique=True, nullable=False)

class RawData(db.Model):
    """原始数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    title = db.Column(db.String)
    pub_date = db.Column(db.TEXT)
    link = db.Column(db.String, unique=True, nullable=False)
    raw_html = db.Column(db.String)  # 存储获取到的 HTML 内容

class SummaryData(db.Model):
    """摘要数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    link = db.Column(db.String, unique=True, nullable=False)
    pub_date = db.Column(db.TEXT)
    bj_pub_date = db.Column(db.DateTime)
    summary_title = db.Column(db.String)
    summary_content = db.Column(db.String)
    summary_image = db.Column(db.String, nullable=True)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'bj_pub_date': self.bj_pub_date,
            'pub_date': self.pub_date,
            'summary_title': self.summary_title,
            'summary_content': self.summary_content,
            'summary_image': self.summary_image
        }
    
    
