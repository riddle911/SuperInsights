import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config import Config
from models import SummaryData

def send_email(subject, html_content):
    msg = MIMEMultipart()
    msg['From'] = Config.MAIL_DEFAULT_SENDER
    msg['To'] = Config.MAIL_RECIPIENT
    msg['Subject'] = subject

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
    server.starttls()
    server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
    server.sendmail(Config.MAIL_DEFAULT_SENDER, Config.MAIL_RECIPIENT, msg.as_string())
    server.quit()

def generate_html_content(summary_data, custom_title):
    now = datetime.now()
    current_date = now.strftime("%Y年%m月%d日")
    current_time = now.strftime("%H:%M:%S")

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>

    body {{
        font-family: 'Inter', sans-serif;
        background-color: #f3f4f6;
        color: #374151;
        margin: 0;
        padding: 0;
    }}

    .container {{
        max-width: 600px;
        margin: 0 auto;
        padding: 10px;
    }}

    .header {{
        text-align: center;
        margin-bottom: 20px;
    }}

    .header h1 {{
        font-size: 20px;
        font-weight: 600;
        color: #1f2937;
    }}

    .header p {{
        font-size: 14px;
        color: #6b7280;
    }}

    .news-container {{
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
        padding: 20px;
    }}

    .news-title {{
        font-size: 20px;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 10px;
    }}

    .news-content {{
        font-size: 16px;
        color: #4b5563;
        margin-bottom: 10px;
    }}

    .news-img {{
        width: 100%;
        border-radius: 8px;
        margin-bottom: 10px;
    }}

    .news-link {{
        display: inline-block;
        background-color: #3b82f6;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 5px;
    }}

    </style>
    </head>
    <body>
    <div class="container">
        <div class="header">
            <h1>{current_date} 信息简报</h1>
            <p>编制时间：{current_date} {current_time}</p>
        </div>
    """

    for summary in summary_data:
        html_template += f"""
        <div class="news-container">
            <h2 class="news-title">{summary['summary_title']}</h2>
        """
        if summary['summary_image']:  # 如果 img 链接不为空
            html_template += f"""
            <img class="news-img" src="{summary['summary_image']}" alt="{summary['summary_title']}">
            """
        html_template += f"""
            <p class="news-content">{summary['summary_content']}</p>
            <a class="news-link" href="{summary['link']}">阅读更多</a>
        </div>
        """

    html_template += """
    </div>
    </body>
    </html>
    """

    return html_template

def send_summary_email():
    """发送汇总邮件"""
    yesterday = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')  # 获取昨天的日期

    # 从数据库中筛选出昨天发布的数据
    summarydata = SummaryData.query.filter(
        SummaryData.bj_pub_date.like(f"{yesterday}%")  # 使用like模糊查询匹配昨天的数据
    ).all()
    
    summary_list = [summary.to_dict() for summary in summarydata]    
    custom_title = f"{datetime.now().strftime('%Y年%m月%d日')} 信息简报"
    html_content = generate_html_content(summary_list, custom_title)
    
    send_email(custom_title, html_content)