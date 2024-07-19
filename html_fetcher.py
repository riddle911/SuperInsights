import requests
from collections import deque
import time
from config import Config

jina_key = Config.JINA_API_KEY

def fetch_html(urls):
    queue = deque(urls)
    headers = {
        "Authorization": f"Bearer {jina_key}",  # Replace with your authorization information
        "Accept": "application/json"
    }
    while queue:
        url = queue.popleft()
        print(f"Fetching HTML content from: {url}")
        jina_url = f"https://r.jina.ai/{url}"
        response = requests.get(jina_url, headers=headers)
        if response.status_code == 200:
            # Assuming the response contains the HTML content in the 'data' field
            data = response.json().get('data', {})
            content = data.get('content', '')
            yield url, content
            print(f"Fetched HTML content from: {url}")
        else:
            print(f"Request to r.jina.ai failed, status code: {response.status_code}")
        if len(queue) > 0:
            time.sleep(6)  # Control 10 messages per minute