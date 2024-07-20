from flask import Flask, jsonify, render_template_string
from sqlalchemy import false
from config import Config
from flask_cors import CORS
from models import db, RSSFeed, RawData, SummaryData
from rss_updater import update_rss_feeds
from data_processor import fetch_html_and_update_raw_data, generate_summaries_and_save
import atexit

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rss.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database initialized and tables created.")

@app.route('/index')
def index():
    summarydata = SummaryData.query.all()
    summary_list = [summary.to_dict() for summary in summarydata]

    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>简报系统</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .summary-card {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                margin: 10px 0;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .summary-card img {
                max-width: 50%;
                height: auto;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h1>简报系统</h1>
        {% for summary in summary_list %}
            <div class="summary-card">
                <h2>{{ summary.summary_title }}</h2>
                <p>{{ summary.pub_date }}</p>
                {% if summary.summary_image %}
                    <img src="{{ summary.summary_image }}" alt="{{ summary.title }}">
                <p>{{ summary.summary_content }}</p>
                {% endif %}
            </div>
        {% endfor %}
    </body>
    </html>
    """

    return render_template_string(template, summary_list=summary_list)

@app.route('/update')
def update_data():
    has_new_data = update_rss_feeds()
    if has_new_data:
        fetch_html_and_update_raw_data()
    return jsonify({'message': 'RSS feeds updated successfully.'})

@app.route('/generate_summaries')
def generate_summaries():
    generate_summaries_and_save()
    return jsonify({'message': 'Summaries generated and saved successfully. Existing summaries have been overwritten.'})

# 获取所有 SummaryData 数据
@app.route('/api/summarydata', methods=['GET'])
def get_summarydata():
    summarydata = SummaryData.query.all()
    return jsonify([summarydatum.to_dict() for summarydatum in summarydata])

def shutdown_scheduler():
    print("Scheduler is not running.")

atexit.register(shutdown_scheduler)

if __name__ == '__main__':
    print("Starting Flask application.")
    app.run(port=5000)