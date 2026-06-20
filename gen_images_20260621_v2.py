#!/usr/bin/env python3
import json
import base64
import subprocess
import os
import time
import urllib.request

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
            
            # Try to extract URL from response
            if isinstance(content, list) and len(content) > 0:
                url = content[0].get('url', '')
            elif 'url' in str(content):
                # Parse JSON with url
                resp_data = json.loads(str(content).replace("'", '"'))
                if isinstance(resp_data, list):
                    url = resp_data[0].get('url', '')
                else:
                    url = resp_data.get('url', '')
            else:
                url = None
            
            if url:
                # Download the image
                print(f"  Downloading from: {url[:60]}...")
                subprocess.run(['curl', '-s', '-o', output_path, url], timeout=60)
                
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                    print(f"  ✓ Saved to {output_path}")
                    results.append({'num': num, 'status': 'success', 'path': output_path})
                else:
                    print(f"  ✗ Download failed")
                    failed.append({'num': num, 'error': 'Download failed'})
            else:
                print(f"  ✗ No URL in response: {str(content)[:100]}")
                failed.append({'num': num, 'error': 'No URL', 'content': str(content)[:200]})
        else:
            print(f"  ✗ API error: {response}")
            failed.append({'num': num, 'error': str(response)})
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        failed.append({'num': num, 'error': str(e)})
    
    time.sleep(1)  # Small delay between requests

print(f"\n=== Results ===")
print(f"Success: {len(results)}/20")
print(f"Failed: {len(failed)}/20")

if failed:
    print("\nFailed items:")
    for f in failed:
        print(f"  {f['num']}: {f['error']}")
        if 'content' in f:
            print(f"    Content: {f['content']}")