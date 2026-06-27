#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import time

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
IMG_DIR = "/home/swg/.openclaw/workspace/news-blog/images"

def generate_image(num, prompt):
    """Generate a single image"""
    output = f"{IMG_DIR}/news_20260628_{num}.png"
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    data = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            img_url = result["choices"][0]["message"]["content"][0]["url"]
            
            # Download the image
            img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(img_req, timeout=30) as img_response:
                with open(output, "wb") as f:
                    f.write(img_response.read())
            
            print(f"Image {num} saved: {output}")
            return True
            
    except Exception as e:
        print(f"Image {num} failed: {e}")
        return False

# Retry failed images
failed = [("02", "World leaders at an international summit conference hall, flags of BRICS nations displayed, photorealistic, ultra detailed, 8K, diplomatic meeting with elegant interior design"),
          ("13", "Digital payment concept with Chinese yuan symbol and smartphone payment interface, photorealistic, ultra detailed, 8K, futuristic financial technology visualization")]

for num, prompt in failed:
    print(f"Retrying image {num}...")
    generate_image(num, prompt)
    time.sleep(2)

# Verify
import os
import glob
images = sorted(glob.glob(f"{IMG_DIR}/news_20260628_*.png"))
print(f"\nTotal images: {len(images)}")
for img in images:
    print(f"  {os.path.basename(img)}")