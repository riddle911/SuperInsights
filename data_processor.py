from html_fetcher import fetch_html
from openai_processor import generate_summary
from models import RawData, SummaryData, db
from datetime import datetime
import pytz

def convert_to_beijing_time(rss_time_str):
    """将 RSS 时间字符串转换为北京时间。

    Args:
      rss_time_str: RSS 时间字符串，例如 "Tue, 27 Oct 2021 11:05:29 +0000"

    Returns:
      北京时间 datetime 对象
    """
    beijing_tz = pytz.timezone('Asia/Shanghai')
    dt = datetime.strptime(rss_time_str, "%a, %d %b %Y %H:%M:%S %z")
    dt_utc = dt.astimezone(pytz.utc)
    dt_beijing = dt_utc.astimezone(beijing_tz)
    return dt_beijing 

def fetch_html_and_update_raw_data():
    """获取 HTML 内容并更新 RawData 表中的 raw_html 字段"""
    raw_data_entries = RawData.query.filter(RawData.raw_html.is_(None)).all()
    print(f"Fetching HTML content for {len(raw_data_entries)} RawData entries.")
    for entry in raw_data_entries:
        print(f"Fetching HTML content for link: {entry.link}")
        jina_data = next(fetch_html([entry.link]))[1]
        entry.raw_html = jina_data
        db.session.commit()
        print(f"Updated RawData entry with raw_html for link: {entry.link}")

def generate_summaries_and_save():
    """生成摘要并保存到 SummaryData 表中,同时处理datetime"""
    # db.session.query(SummaryData).delete()  #  如果需要每次都清空 SummaryData 表，请取消注释
    raw_data_entries = RawData.query.filter(RawData.raw_html.isnot(None)).all()
    print(f"Generating summaries for {len(raw_data_entries)} RawData entries.")
    for entry in raw_data_entries:
        print(f"Generating summary for HTML content from: {entry.link}")
        summary_data = generate_summary(entry.raw_html)
        # 将 RSS 时间字符串转换为北京时间
        if summary_data:
            bj_pub_date = convert_to_beijing_time(entry.pub_date)
            # 检查 SummaryData 中是否已经存在此链接
            existing_summary = SummaryData.query.filter_by(link=entry.link).first()
            if existing_summary:
                print(f"Summary for link {entry.link} already exists, skipping.")
                continue  # 跳过此链接
            
            summary = SummaryData(
                title=entry.title,
                link=entry.link,
                pub_date = entry.pub_date,
                bj_pub_date = bj_pub_date,
                summary_title=summary_data.get('title', ''),
                summary_content=summary_data.get('content', ''),
                summary_image=summary_data.get('image', ''),
            )
            db.session.add(summary)
            db.session.commit()
            print(f"Added summary for link: {entry.link} to SummaryData table.")  