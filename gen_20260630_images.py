import json
import urllib.request
import urllib.error
import base64
import os
import time

# Load news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260630.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

# CogView API settings
api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

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
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            api_url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            
            # Extract base64 image data
            if 'data:image/png;base64,' in content:
                base64_data = content.split('data:image/png;base64,')[1]
            else:
                base64_data = content
            
            # Decode and save
            image_data = base64.b64decode(base64_data)
            filename = f"{output_dir}/news_20260630_{news_num}.png"
            with open(filename, 'wb') as f:
                f.write(image_data)
            
            print(f"SUCCESS: {news_num}")
            return True
            
    except Exception as e:
        print(f"FAILED: {news_num} - {e}")
        return False

# Generate images
for i, item in enumerate(news_data):
    print(f"[{i+1}/20] Generating {item['number']}...")
    generate_image(item)
    time.sleep(0.5)

print("Done!")