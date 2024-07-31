import requests
from config import Config
import json

openai_key = Config.OPENAI_API_KEY
openai_url = Config.OPENAI_URL
MODEL = Config.OPENAI_MODEL

def generate_summary(jina_data):
    #print(f"Generating summary for HTML content.")
    prompt = '''你的任务是作为一个高级翻译和编辑，理解发给你的内容，从中生产加工输出以下信息：标题、正文、图片。确保你的响应符合以下JSON结构，准确反映提取的数据，不做修改：```json
    {
    "title": "文章标题",
    "content": "文章摘要",
    "image": "文章包含的图片链接，保留url，如果没有留空"
    }
```重要的是你的输出严格遵守这种格式。
    -严格确保统一翻译为中文
    -不翻译公司名称、人名    '''
    siliconflow_url = openai_url
    siliconflow_payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "assistant",
                "content": f"{prompt}{jina_data}"  # 将 jina_data 添加到 SiliconFlow 的 messages
            }
        ]
    }
    siliconflow_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {openai_key}"
    }

    try:
        # 使用 requests 发送请求到 SiliconFlow，设置超时时间为 15 秒
        siliconflow_response = requests.post(siliconflow_url, json=siliconflow_payload, headers=siliconflow_headers, timeout=15)
        siliconflow_response.raise_for_status()  # 检查 HTTP 状态码，如果发生错误，则抛出异常

        # 解析 SiliconFlow 的响应
        response = siliconflow_response.json()
        result_content = response['choices'][0]['message']['content']

        # 处理 SiliconFlow 的响应
        print("Generated summary successfully.")
        # 解析 result_content 中的 JSON 数据
        try:
            # 去掉 JSON 字符串前后的 ```json 标记
            json_str = result_content.strip().lstrip('```json').rstrip('```').strip()
            parsed_json = json.loads(json_str)
            return parsed_json
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"SiliconFlow 请求错误：{e}")
        return None
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        return None
