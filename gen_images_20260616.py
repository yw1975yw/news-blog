#!/usr/bin/env python3
"""Generate news images using CogView-3-Flash API"""

import json
import base64
import urllib.request
import time
import os
import ssl

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
IMAGES_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
DATE_ID = "20260616"

# News items
NEWS_ITEMS = [
    {"number": "01", "prompt": "A scientist in a modern AI research lab, examining holographic neural network displays showing GPT model architecture, photorealistic, ultra detailed, 8K, high resolution, cinematic lighting"},
    {"number": "02", "prompt": "World leaders at G7 summit in Taormina Sicily, elegant conference hall with Mediterranean view, photorealistic, ultra detailed, 8K, high resolution, news photography style"},
    {"number": "03", "prompt": "Federal Reserve building in Washington DC, traders watching stock market screens, photorealistic, ultra detailed, 8K, high resolution, financial district atmosphere"},
    {"number": "04", "prompt": "SpaceX Starship spacecraft docking with lunar orbital station, Earth visible in background, photorealistic, ultra detailed, 8K, high resolution, space exploration atmosphere"},
    {"number": "05", "prompt": "Chinese and American flags side by side, diplomatic meeting room, photorealistic, ultra detailed, 8K, high resolution, formal international summit setting"},
    {"number": "06", "prompt": "Electric vehicles and batteries at EU port, carbon border adjustment signage, photorealistic, ultra detailed, 8K, high resolution, industrial trade scene"},
    {"number": "07", "prompt": "Google Android 16 launch event, holographic smartphone displays, photorealistic, ultra detailed, 8K, high resolution, tech conference atmosphere"},
    {"number": "08", "prompt": "Peace talks in Ankara Turkey, diplomats shaking hands, UN flag visible, photorealistic, ultra detailed, 8K, high resolution, diplomatic summit setting"},
    {"number": "09", "prompt": "Cryptocurrency trading screens showing Bitcoin price crash, traders concerned, photorealistic, ultra detailed, 8K, high resolution, financial trading floor"},
    {"number": "10", "prompt": "High-tech job fair with AI engineers, competitive salary displays, photorealistic, ultra detailed, 8K, high resolution, professional recruiting event"},
    {"number": "11", "prompt": "Microsoft quantum computer chip Majorana 1, scientist in lab coat examining processor, photorealistic, ultra detailed, 8K, high resolution, cutting-edge technology"},
    {"number": "12", "prompt": "Chinese consumers shopping at modern mall, retail stores bustling, photorealistic, ultra detailed, 8K, high resolution, urban commercial district"},
    {"number": "13", "prompt": "Japanese families with children in Tokyo park, cherry blossoms, urban setting, photorealistic, ultra detailed, 8K, high resolution, demographic challenges"},
    {"number": "14", "prompt": "New York Stock Exchange trading floor, bull statue, digital displays showing record highs, photorealistic, ultra detailed, 8K, high resolution, financial district"},
    {"number": "15", "prompt": "Epic sci-fi movie poster with astronauts near Jupiter, Chinese film production, photorealistic, ultra detailed, 8K, high resolution, cinematic poster art"},
    {"number": "16", "prompt": "FIFA World Cup trophy ceremony, fans celebrating, stadium packed, photorealistic, ultra detailed, 8K, high resolution, soccer championship atmosphere"},
    {"number": "17", "prompt": "Indian Prime Minister meeting EU leaders, green energy hydrogen plant background, photorealistic, ultra detailed, 8K, high resolution, diplomatic summit"},
    {"number": "18", "prompt": "Stanford University campus, AI research papers and data visualization, photorealistic, ultra detailed, 8K, high resolution, academic research setting"},
    {"number": "19", "prompt": "Heavy rainfall flooding in urban city, emergency responders with rescue boats, photorealistic, ultra detailed, 8K, high resolution, dramatic weather event"},
    {"number": "20", "prompt": "Electric vehicles charging station with modern design, multiple EVs charging, photorealistic, ultra detailed, 8K, high resolution, sustainable transportation"},
]

def generate_image(news_num, prompt, retry=2):
    """Generate image using CogView-3-Flash API"""
    filename = f"news_{DATE_ID}_{news_num}.png"
    filepath = os.path.join(IMAGES_DIR, filename)
    
    # Skip if already exists
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"[{news_num}] Already exists: {filename}")
        return True, filename
    
    for attempt in range(retry + 1):
        try:
            data = json.dumps({
                "model": "cogview-3-flash",
                "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
            }, ensure_ascii=False).encode("utf-8")
            
            req = urllib.request.Request(
                API_URL,
                data=data,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                
                # Parse response - might be URL or base64
                image_url = None
                if isinstance(content, list):
                    image_url = content[0].get("url") if isinstance(content[0], dict) else None
                elif isinstance(content, str):
                    if "http" in content:
                        if "data:image" in content:
                            # base64
                            b64_data = content.split("data:image/png;base64,")[1] if "data:image/png;base64," in content else content
                            img_data = base64.b64decode(b64_data)
                            with open(filepath, "wb") as f:
                                f.write(img_data)
                            print(f"[{news_num}] Generated (base64): {filename}")
                            return True, filename
                        else:
                            image_url = content
                
                if image_url:
                    # Download from URL
                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                    
                    with urllib.request.urlopen(image_url, timeout=60, context=ssl_context) as img_resp:
                        img_data = img_resp.read()
                        with open(filepath, "wb") as f:
                            f.write(img_data)
                    print(f"[{news_num}] Generated (URL): {filename}")
                    return True, filename
                
                print(f"[{news_num}] Unknown response format: {str(content)[:100]}")
                return False, filename
                
        except Exception as e:
            print(f"[{news_num}] Attempt {attempt+1} failed: {e}")
            if attempt < retry:
                time.sleep(2)
    
    print(f"[{news_num}] FAILED after {retry+1} attempts")
    return False, filename

# Generate all images
print(f"Generating {len(NEWS_ITEMS)} images for {DATE_ID}...")
print("=" * 50)

results = []
for i, item in enumerate(NEWS_ITEMS):
    print(f"\n[{i+1}/{len(NEWS_ITEMS)}] Processing {item['number']}...")
    success, filename = generate_image(item['number'], item['prompt'])
    results.append({'number': item['number'], 'success': success, 'filename': filename})
    time.sleep(1)  # Rate limiting

# Summary
success_count = sum(1 for r in results if r['success'])
failed = [r for r in results if not r['success']]

print("\n" + "=" * 50)
print(f"Generation Complete: {success_count}/20 successful")
if failed:
    print("Failed items:", [f['number'] for f in failed])
else:
    print("All images generated successfully!")

# Verify files exist
print("\nVerifying generated files...")
for i in range(1, 21):
    num = f"{i:02d}"
    filepath = os.path.join(IMAGES_DIR, f"news_{DATE_ID}_{num}.png")
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  [{num}] OK ({size:,} bytes)")
    else:
        print(f"  [{num}] MISSING")