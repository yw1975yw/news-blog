#!/usr/bin/env python3
import json
import base64
import subprocess
import os
import time

# Load news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260621.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

news_items = data['news']
today_date_short = data['date_short']
images_dir = '/home/swg/.openclaw/workspace/news-blog/images'

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

results = []
failed = []

for item in news_items:
    num = item['number']
    prompt = item['prompt']
    output_path = f"{images_dir}/news_{today_date_short}_{num}.png"
    
    print(f"Generating image {num}/20: {item['title'][:30]}...")
    
    # Build request
    request_body = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    # Call API via curl
    cmd = [
        'curl', '-s', '-X', 'POST', API_URL,
        '-H', f'Authorization: Bearer {API_KEY}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(request_body)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        response = json.loads(result.stdout)
        
        if 'choices' in response and len(response['choices']) > 0:
            content = response['choices'][0]['message']['content']
            # Extract base64 image
            if 'data:image/png;base64,' in content:
                b64_data = content.split('data:image/png;base64,')[1]
                image_data = base64.b64decode(b64_data)
                
                with open(output_path, 'wb') as img_file:
                    img_file.write(image_data)
                
                print(f"  ✓ Saved to {output_path}")
                results.append({'num': num, 'status': 'success', 'path': output_path})
            else:
                print(f"  ✗ No base64 image in response")
                failed.append({'num': num, 'error': 'No base64 image'})
        else:
            print(f"  ✗ API error: {response}")
            failed.append({'num': num, 'error': str(response)})
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        failed.append({'num': num, 'error': str(e)})
    
    time.sleep(0.5)  # Small delay between requests

print(f"\n=== Results ===")
print(f"Success: {len(results)}/20")
print(f"Failed: {len(failed)}/20")

if failed:
    print("\nFailed items:")
    for f in failed:
        print(f"  {f['num']}: {f['error']}")