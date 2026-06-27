#!/usr/bin/env python3
import json
import os
import time
import subprocess
import urllib.request
from PIL import Image
import io

# Reload news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260626.json', 'r', encoding='utf-8') as f:
    news_items = json.load(f)

api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

def generate_and_crop(news_id, prompt, max_retries=2):
    """Generate image using CogView-3-Flash API, download, crop watermark"""
    import requests
    
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=90)
            data = resp.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0]['message']['content']
                
                image_url = None
                
                # Check URL format
                if isinstance(content, list) and len(content) > 0:
                    if 'url' in content[0]:
                        image_url = content[0]['url']
                
                if image_url:
                    # Download image
                    headers_download = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    req = urllib.request.Request(image_url, headers=headers_download)
                    with urllib.request.urlopen(req, timeout=30) as response:
                        img_data = response.read()
                    
                    # Open and crop watermark (bottom ~100px)
                    img = Image.open(io.BytesIO(img_data))
                    width, height = img.size
                    
                    # Crop to remove bottom watermark area (keep top 90%)
                    crop_height = int(height * 0.93)
                    img_cropped = img.crop((0, 0, width, crop_height))
                    
                    filename = f'/home/swg/.openclaw/workspace/news-blog/images/news_20260626_{news_id:02d}.png'
                    img_cropped.save(filename, 'PNG', quality=95)
                    print(f"[{news_id:02d}] Saved (cropped {width}x{height} -> {width}x{crop_height}): {filename}")
                    return True
                    
        except Exception as e:
            print(f"[{news_id:02d}] Attempt {attempt+1} error: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(3)
    
    return False

print("=== Generating 20 images ===")
successes = 0
for item in news_items:
    if generate_and_crop(item['id'], item['image_prompt']):
        successes += 1
    else:
        print(f"[{item['id']:02d}] FAILED")
    time.sleep(2)

print(f"\n=== Done: {successes}/{len(news_items)} images generated ===")