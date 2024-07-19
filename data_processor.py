from html_fetcher import fetch_html
from openai_processor import generate_summary
from models import RawData, SummaryData, db

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
    """生成摘要并保存到 SummaryData 表中"""
    db.session.query(SummaryData).delete()
    raw_data_entries = RawData.query.filter(RawData.raw_html.isnot(None)).all()
    print(f"Generating summaries for {len(raw_data_entries)} RawData entries.")
    for entry in raw_data_entries:
        print(f"Generating summary for HTML content from: {entry.link}")
        summary_data = generate_summary(entry.raw_html)
        if summary_data:
            summary = SummaryData(
                title=entry.title,
                link=entry.link,
                pub_date = entry.pub_date,
                summary_title=summary_data.get('title', ''),
                summary_content=summary_data.get('content', ''),
                summary_image=summary_data.get('image', ''),
            )
            db.session.add(summary)
            db.session.commit()
            print(f"Added summary for link: {entry.link} to SummaryData table.")