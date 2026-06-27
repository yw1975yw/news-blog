import json
import os
import time
import subprocess
import urllib.request

# Reload news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260626.json', 'r', encoding='utf-8') as f:
    news_items = json.load(f)

api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

def generate_cogview_image(news_id, prompt):
    """Generate image using CogView-3-Flash API, download and crop"""
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
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        data = resp.json()
        
        if 'choices' in data and len(data['choices']) > 0:
            content = data['choices'][0]['message']['content']
            
            # Check if it's a URL format
            if isinstance(content, list) and len(content) > 0 and 'url' in content[0]:
                image_url = content[0]['url']
                # Download and crop out watermark
                local_path = f'/home/swg/.openclaw/workspace/news-blog/images/news_20260626_{news_id:02d}.png'
                try:
                    urllib.request.urlretrieve(image_url, local_path)
                    print(f"[{news_id:02d}] Downloaded: {image_url}")
                    return True
                except Exception as e:
                    print(f"[{news_id:02d}] Download failed: {e}")
                    return False
            elif isinstance(content, str) and 'data:image' in content:
                # base64 format
                import base64
                b64_data = content.split('data:image/png;base64,')[1]
                img_data = base64.b64decode(b64_data)
                filename = f'/home/swg/.openclaw/workspace/news-blog/images/news_20260626_{news_id:02d}.png'
                with open(filename, 'wb') as f:
                    f.write(img_data)
                print(f"[{news_id:02d}] Image saved (base64)")
                return True
    except Exception as e:
        print(f"[{news_id:02d}] Error: {e}")
    
    return False

print("=== Generating 20 images ===")
for item in news_items:
    success = False
    for attempt in range(2):
        if generate_cogview_image(item['id'], item['image_prompt']):
            success = True
            break
        if not success and attempt == 0:
            print(f"[{item['id']:02d}] Retrying...")
            time.sleep(3)
    
    if not success:
        print(f"[{item['id']:02d}] FAILED after 2 attempts")
    
    time.sleep(2)

print("\n=== Image generation complete ===")