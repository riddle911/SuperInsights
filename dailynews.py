from datetime import datetime, timedelta
from config import Config
from models import SummaryData
from flask import Flask, render_template

def dailynews():
    today = datetime.now()
    markdown_text = "# 每日新闻\n\n"  # 初始化 Markdown 字符串
    days_ago_list = range(0, 3)  # 定义要展示的天数范围，从0天到3天

    for days_ago in days_ago_list:
        for summary in SummaryData.query.all():
            if (today - summary.bj_pub_date).days == days_ago:
                markdown_text += f"""
## 🚀{summary.summary_title}

![]({summary.summary_image})

{summary.summary_content}

日期：{summary.bj_pub_date.strftime('%Y-%m-%d')} 

---
"""  # 使用 --- 分隔不同的新闻条目

    return render_template('dailynews.html', markdown_text=markdown_text)