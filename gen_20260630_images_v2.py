import json
import subprocess
import os
import time

# Load news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260630.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

output_dir = "/home/swg/.openclaw/workspace/news-blog/images"
os.makedirs(output_dir, exist_ok=True)

api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

def generate_image(news_item):
    """Generate image using CogView API via curl"""
    news_num = news_item['number']
    prompt = news_item['prompt']
    
    # Build the request payload
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    payload_str = json.dumps(payload, ensure_ascii=False)
    
    # Use curl to make the request
    cmd = [
        'curl', '-s', '-X', 'POST',
        'https://open.bigmodel.cn/api/paas/v4/chat/completions',
        '-H', f'Authorization: Bearer {api_key}',
        '-H', 'Content-Type: application/json',
        '-d', payload_str,
        '--max-time', '90'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"FAILED: {news_num} - curl error: {result.stderr}")
            return False
        
        response = json.loads(result.stdout)
        if 'choices' not in response:
            print(f"FAILED: {news_num} - No choices in response: {result.stdout[:200]}")
            return False
        
        content = response['choices'][0]['message']['content']
        
        # Extract base64 image data
        if 'data:image/png;base64,' in content:
            base64_data = content.split('data:image/png;base64,')[1]
        else:
            base64_data = content
        
        # Decode and save
        import base64 as b64
        image_data = b64.b64decode(base64_data)
        filename = f"{output_dir}/news_20260630_{news_num}.png"
        with open(filename, 'wb') as f:
            f.write(image_data)
        
        print(f"SUCCESS: {news_num} - saved to {filename}")
        return True
            
    except subprocess.TimeoutExpired:
        print(f"FAILED: {news_num} - Timeout")
        return False
    except Exception as e:
        print(f"FAILED: {news_num} - {e}")
        return False

# Generate images
for i, item in enumerate(news_data):
    print(f"[{i+1}/20] Generating {item['number']}...")
    generate_image(item)
    time.sleep(1)

print("Done!")