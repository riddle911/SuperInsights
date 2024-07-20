from flask import Flask, jsonify, render_template_string,render_template
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

# 获取所有 SummaryData 数据,仅后端返回json
@app.route('/api/summarydata', methods=['GET'])
def get_summarydata():
    summarydata = SummaryData.query.all()
    return jsonify([summarydatum.to_dict() for summarydatum in summarydata])

@app.route('/index')
def index():
    summarydata = SummaryData.query.all()
    summary_list = [summary.to_dict() for summary in summarydata]
    return render_template('index.html', summary_list=summary_list)


def shutdown_scheduler():
    print("Scheduler is not running.")

atexit.register(shutdown_scheduler)

if __name__ == '__main__':
    print("Starting Flask application.")
    app.run(port=5000)