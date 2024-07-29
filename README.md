
# 🚀 SuperInsights

[中文版本](https://github.com/riddle911/SuperInsights/blob/main/README_CN.md)

🚀 **No need to write crawlers, get key information instantly, and power your open-source intelligence!**

SuperInsights is a tool based on Large Language Models (LLMs) designed to extract and summarize critical information from specified web pages. 

Even if you don't know how to write crawlers, you can use it completely. It automatically scrapes web content and supports analysis, summarization, and translation (if needed) using models compatible with OpenAI's API.

This tool aims to help users quickly gather industry intelligence information. Whether you're tracking the latest technology trends or collecting market dynamics, SuperInsights has got you covered! 💪

You can leverage this project to quickly build daily industry reports, market intelligence systems, sentiment monitoring, and more.

## Features

- **🌐 Web Scraping**: Automatically parses the content of specified URLs using the JINA Reader for reliable and effective web scraping.
- **💡 Smart Summarization**: Utilizes LLMs to generate concise and clear content summaries.
- **📦 Local Lightweight Database Support**: Uses SQLite for convenient local maintenance.
- **🔗 Rich LLM Support Services**: Supports OpenAI and other online LLM inference services compatible with OpenAI's API.
- **📊 Basic Frontend Display System**: Provides a simple frontend page based on the MVC pattern to display data, instead of accessing the database directly.

## System Frontend Display

![image](https://github.com/user-attachments/assets/2bf08923-2699-4c1b-8bd9-035a871e76d7)

## Installation

### Prerequisites
- Local development environment with Python 3.12.2, but other Python versions may be used.

### Quick Start

1. Clone this repository to your local environment

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Some necessary configurations:
   - First, in `config.json`, set up the information sources you want to track. This software supports RSS URLs by default.
     - What is RSS? Please search to understand more. Most news websites provide RSS Feeds. If not, you can use services like [PolitePol](https://politepol.com/) to convert any website into an RSS Feed.
     - In `config.json`, set up examples like this:
       ```json
       "feeds": [
          {
            "url": "https://example.com/feed",
            "num_entries": "all", 
            "update_frequency": 3600 
          }
       ]
       ```
   - The `num_entries` configuration: You can set it to "all" or a number. "all" means to fetch all data by default, and a number means to fetch the top N items.
   
   - Secondly, configure `config.py`:
     ```python
     import json
     
     class Config:
         # Read configuration file
         with open('config.json', 'r') as f:
             config_data = json.load(f)
     
         # Get RSS feed list
         RSS_FEEDS = config_data.get('feeds', [])
         SQLALCHEMY_DATABASE_URI = 'sqlite:///rss.db'
         JINA_API_KEY = '' # jinareader's key, obtain from https://jina.ai/
         OPENAI_API_KEY = '' # Obtain from your LLM service provider
         FETCH_INTERVAL = 3600  # Default fetching interval 1 hour
         OPENAI_URL = ''  # Obtain from your LLM service provider
         OPENAI_MODEL = ''  # Obtain from your LLM service provider
     ```
5. **Prompt Configuration**
   - In `openai_processor.py`, the author has pre-set a prompt that you can modify according to your needs.

6. Run the example script:
   ```bash
   python main.py
   ```

## Usage Guide

After running the program, several specific endpoints are available to execute tasks and access data:

| Parameter              | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `/update`              | Updates RSS Feed URLs and parses the web page content for each URL, storing the raw data in the database. |
| `/generate_summaries`  | Submits all scraped raw data to the LLM for processing.                     |
| `/api/summarydata`     | Retrieves all processed data.                                               |
| `/index`               | A simple frontend page displaying all processed data.                       |

## Pending Features and Updates

- [ ] Automate the program execution with configurable time intervals for scraping and processing.
- [ ] Enhance the frontend page functionality and potentially migrate to React or Vue.
- [ ] Optimize the speed of scraping and LLM processing.

Professional developers are welcome to join and contribute!

## Contact the Author

For more technical and product exchanges, or if you wish to contact the author, we hope to collaborate with more friends in the areas of AI Agents and large language models!

You can reach me through these channels:

- Email: sleepwater911@gmail.com
- WeChat: Search for the WeChat ID "mapxiaotu"

---

Thank you to all contributors and supporters! 👏

If you find this project helpful, please consider giving it a star ⭐️, which will be our greatest encouragement!
