#!/usr/bin/env python3
import urllib.request
import json
import os
import time

date_short = "20260613"
images_dir = "/home/swg/.openclaw/workspace/news-blog/images"
api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

# Retry failed images with different prompts
failed_items = [
    {"num": "08", "prompt": "Diplomats in suits shaking hands across table in modern conference room, American and Chinese national flags on wall, formal international meeting, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "11", "prompt": "Smartphone displaying digital payment interface with Chinese currency symbol, glowing holographic yuan sign, mobile wallet concept, futuristic urban background, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
]

for item in failed_items:
    num = item['num']
    filename = f"news_{date_short}_{num}.png"
    output_path = os.path.join(images_dir, filename)
    prompt = item['prompt']
    
    try:
        payload = {"model": "cogview-3-flash", "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            api_url, data=data,
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            image_url = content[0]['url']
            
            img_req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(img_req, timeout=90) as img_resp:
                img_data = img_resp.read()
                with open(output_path, 'wb') as f:
                    f.write(img_data)
        
        print(f"ok {num}")
    except Exception as e:
        print(f"fail {num}: {e}")
    
    time.sleep(2)

# Verify all 20 images exist
print("\nVerifying all 20 images:")
all_ok = True
for i in range(1, 21):
    num = f"{i:02d}"
    path = os.path.join(images_dir, f"news_{date_short}_{num}.png")
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    print(f"  {num}: {'ok' if exists and size > 1000 else 'MISSING/EMPTY'} ({size} bytes)")
    if not exists or size < 1000:
        all_ok = False

print(f"\nAll images ready: {all_ok}")