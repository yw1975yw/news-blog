#!/usr/bin/env python3
"""Generate news images for 2026年06月30日 using CogView API."""

import json
import urllib.request
import base64
import time
import os

# Load news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260630.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
output_dir = "/home/swg/.openclaw/workspace/news-blog/images"
os.makedirs(output_dir, exist_ok=True)

def generate_image(news_item):
    """Generate image using CogView API"""
    news_num = news_item['number']
    prompt = news_item['prompt']
    
    try:
        payload = {
            "model": "cogview-3-flash",
            "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
        }
        
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            
            # Handle different response formats
            if isinstance(content, list):
                # Format: [{"url": "https://..."}]
                image_url = content[0]['url']
                # Download from URL
                with urllib.request.urlopen(image_url, timeout=60) as img_resp:
                    image_data = img_resp.read()
            elif isinstance(content, str) and "data:image" in content:
                # Format: "data:image/png;base64,XXXXX"
                b64_data = content.split("data:image/png;base64,")[1]
                image_data = base64.b64decode(b64_data)
            elif isinstance(content, str):
                # Just base64 string
                image_data = base64.b64decode(content)
            else:
                print(f"FAILED: {news_num} - Unknown content type: {type(content)}")
                return False
            
            filename = f"{output_dir}/news_20260630_{news_num}.png"
            with open(filename, "wb") as f:
                f.write(image_data)
            
            print(f"SUCCESS: {news_num} - saved to {filename}")
            return True
            
    except Exception as e:
        print(f"FAILED: {news_num} - {e}")
        return False

# Generate images
for i, item in enumerate(news_data):
    print(f"[{i+1}/20] Generating {item['number']}...")
    success = generate_image(item)
    if not success:
        print(f"  RETRY {item['number']}...")
        time.sleep(3)
        generate_image(item)
    time.sleep(1)

print("\nDone!")