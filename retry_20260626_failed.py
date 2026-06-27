#!/usr/bin/env python3
import json
import os
import time
import urllib.request
from PIL import Image
import io

# Reload news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260626.json', 'r', encoding='utf-8') as f:
    news_items = json.load(f)

api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

# Updated prompts for failed ones (safer versions)
retry_prompts = {
    6: "China US diplomatic meeting, business negotiation, two groups sitting at conference table, professional setting, soft lighting, photorealistic, ultra detailed, 8K",
    12: "medical research laboratory China, scientists working with advanced medical equipment, brain scan imaging on screen, clinical trial setting, photorealistic, ultra detailed, 8K",
    14: "Olympic Games celebration, athletes gathering, international sports event, Paris landmarks background, people celebrating, photorealistic, ultra detailed, 8K"
}

def generate_and_crop(news_id, prompt, max_retries=2):
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
                if isinstance(content, list) and len(content) > 0:
                    if 'url' in content[0]:
                        image_url = content[0]['url']
                
                if image_url:
                    headers_dl = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    req = urllib.request.Request(image_url, headers=headers_dl)
                    with urllib.request.urlopen(req, timeout=30) as response:
                        img_data = response.read()
                    
                    img = Image.open(io.BytesIO(img_data))
                    width, height = img.size
                    crop_height = int(height * 0.93)
                    img_cropped = img.crop((0, 0, width, crop_height))
                    
                    filename = f'/home/swg/.openclaw/workspace/news-blog/images/news_20260626_{news_id:02d}.png'
                    img_cropped.save(filename, 'PNG', quality=95)
                    print(f"[{news_id:02d}] Success (cropped {width}x{height} -> {width}x{crop_height})")
                    return True
                    
        except Exception as e:
            print(f"[{news_id:02d}] Attempt {attempt+1} error: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(4)
    
    return False

print("=== Retrying failed images (06, 12, 14) ===")
for news_id in [6, 12, 14]:
    item = next((x for x in news_items if x['id'] == news_id), None)
    prompt = retry_prompts[news_id]
    print(f"\n[{news_id:02d}] Retrying with safer prompt...")
    if generate_and_crop(news_id, prompt):
        print(f"[{news_id:02d}] SUCCESS")
    else:
        print(f"[{news_id:02d}] FAILED after retries - using fallback")
        # Try Pollinations as fallback
        from PIL import Image
        import requests
        safe_prompts = {
            6: "international business meeting diplomats",
            12: "brain science laboratory medical research",
            14: "Olympic sports celebration Paris"
        }
        fallback_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(safe_prompts[news_id])}?width=1024&height=952&nologo=true"
        try:
            req = urllib.request.Request(fallback_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as response:
                img_data = response.read()
            img = Image.open(io.BytesIO(img_data))
            filename = f'/home/swg/.openclaw/workspace/news-blog/images/news_20260626_{news_id:02d}.png'
            img.save(filename, 'PNG')
            print(f"[{news_id:02d}] Fallback Pollinations success")
        except Exception as e:
            print(f"[{news_id:02d}] Fallback also failed: {e}")
    time.sleep(3)

print("\n=== Retry complete ===")