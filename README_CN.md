
# 🚀 SuperInsights

🚀 **不用辛苦写爬虫，也能顷刻获取关键信息，助力开源情报加工！**

SuperInsights 是一个基于 Large Language Models (LLMs) 的工具，用于从指定的网页中提取并总结关键信息。即使你不会写爬虫，也可以完全使用。它能够自动抓取网页内容，支持对接兼容 OpenAI 语言模型对其进行分析、总结以及翻译（如果需要）。

该工具旨在帮助用户快速获取行业情报信息。无论是跟踪最新的技术趋势还是收集市场动态，SuperInsights 都能助你一臂之力！💪

你可以利用这个项目，快速搭建**行业日报、市场情报、舆情监测**等多种系统......

## 功能

- **🌐 网页抓取**：自动解析指定URL的内容，引入 JINA Reader 抓取网页信息，稳定、效果良好。
- **💡 智能总结**：利用LLM生成简洁明了的内容摘要。
- **📦 本地轻量化数据库支撑**：采用 SQLite 数据库，本地维护便捷。
- **🔗 丰富的LLM支撑服务**：支持 OpenAI 及兼容 OpenAI 接口的在线 LLM 推理服务。
- **📊 基础的前端展示系统**：提供一个基于 MVC 开发的简单的前端展示页面，用以向用户展示数据。

## 支持数据源

- 支持各种公开可访问的网站
- 不支持需要登录验证的网站
- 不支持微信公众号、社交媒体（微博、X）等，如有需求可联系作者定制。

## 系统前端展示

![image](https://github.com/user-attachments/assets/2bf08923-2699-4c1b-8bd9-035a871e76d7)


## 安装

### 前提条件
- 本地开发环境 Python 3.12.2，但可以尝试其他 Python 版本。

### 快速开始

1. 克隆此仓库到您的本地环境

2. 安装依赖项:
   ```bash
   pip install -r requirements.txt
   ```

3. 一些必要配置:
   - 首先，在 `config.json` 设置你需要关注的信息源，本软件默认支持 RSS URL。
     - 什么是RSS？请搜索了解，大部分资讯类网站均有 RSS Feed 提供。若无，可通过 [PolitePol](https://politepol.com/) 等服务将任意网站转换为 RSS Feed。
     - 在 `config.json` 中，设置示例如下：
       ```json
       "feeds": [
          {
            "url": "https://example.com/feed",
            "num_entries": "all", 
            "update_frequency": 3600 
          }
       ]
       ```
   其中，num_entries的配置：可配置参数为 "all" 或数字，"all" 代表每次默认抓取所有数据，数字代表抓取前 N 条数据。
   
   - 其次，在 `config.py` 中配置：
     ```python
     import json
     
     class Config:
         # 读取配置文件
         with open('config.json', 'r') as f:
             config_data = json.load(f)
     
         # 获取 RSS feed 列表
         RSS_FEEDS = config_data.get('feeds', [])
         SQLALCHEMY_DATABASE_URI = 'sqlite:///rss.db'
         # JINA_API_KEY = '' # jinareader的key，通过 https://jina.ai/ 获取
         OPENAI_API_KEY = '' # 通过你的 LLM 服务商获取
         FETCH_INTERVAL = 3600  # 默认抓取间隔 1 小时
         OPENAI_URL = ''  # 通过你的 LLM 服务商获取
         OPENAI_MODEL = ''  # 通过你的 LLM 服务商获取
     ```
5. **Prompt 配置**
   - 在 `openai_processor.py` 文件中，作者预置了一个 prompt，你可以按需修改。

6. 运行示例脚本:
   ```bash
   python main.py
   ```

## 使用指南

程序运行后，可通过几个特定接口执行任务，访问数据:

| 参数                  | 描述                                                                 |
|-----------------------|----------------------------------------------------------------------|
| `/update`             | 更新 RSS Feed URL，并解析每个 URL 对应的网页内容，获取 raw data 存入数据库  | 
| `/generate_summaries` | 将所有抓取的 raw data 数据提交 LLM 解析                                   | 
| `/api/summarydata`    | 获取所有解析后的数据                                                 | 
| `/index`              | 一个简单的前端页面，展示所有解析的数据                                | 

## 尚待解决及更新的功能

- [ ] 程序自动化执行，可配置按不同时间进行抓取解析
- [ ] 前端页面功能丰富，有条件迁移至React或Vue
- [ ] 抓取及LLM处理的速度优化

希望专业开发者加入一起参与！

## 联系作者

更多技术与产品交流，或欢迎联系作者，希望在 AI Agent 及大模型方面与更多朋友有交流合作！

你可以通过以下途径找到我：

- Email: sleepwater911@gmail.com
- WeChat: 搜索微信 ID "mapxiaotu"

---

感谢所有贡献者和支持者！👏

如果你觉得这个项目对你有所帮助，请考虑给予一个 star ⭐️，这将是对我们最大的鼓励！
