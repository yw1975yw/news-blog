#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
import base64
import os
import time

date_str = "2026年06月13日"
date_short = "20260613"

news_items = [
    {"num": "01", "tag": "科技", "prompt": "Astronauts in spacesuits boarding Chinese spacecraft at launchpad, rocket towering behind them against blue sky, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "02", "tag": "国际", "prompt": "World leaders at G7 summit meeting in elegant conference room with mountain view, flags of participating countries, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "03", "tag": "科技", "prompt": "Modern GPU chip close-up with glowing circuits, technology concept, blue and green neon lighting, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "04", "tag": "国际", "prompt": "Wind turbines and solar panels in green meadow landscape, European and Chinese flags together, clean energy concept, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "05", "tag": "金融", "prompt": "Bitcoin coin with golden glow, financial charts rising in background, modern trading screen atmosphere, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "06", "tag": "科技", "prompt": "Futuristic AI brain neural network visualization, glowing blue digital neurons, technology concept art, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "07", "tag": "经济", "prompt": "Cargo ships loading containers at busy modern port, China and Russia flags on shipping containers, trade concept, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "08", "tag": "国际", "prompt": "Two diplomats shaking hands in formal meeting room, US and China flags in background, diplomatic atmosphere, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "09", "tag": "科技", "prompt": "Semiconductor factory clean room with advanced chip manufacturing equipment, scientists in protective suits, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "10", "tag": "体育", "prompt": "Olympic athletes village buildings with colorful banners and Olympic rings, Paris cityscape in background, aerial view, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "11", "tag": "金融", "prompt": "Digital payment concept with glowing Chinese yuan symbol and smartphone, global connectivity visualization, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "12", "tag": "经济", "prompt": "Modern shopping mall interior with bright atmosphere, Chinese consumers browsing electronics store, retail economy concept, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "13", "tag": "社会", "prompt": "Modern coal mine control room with digital screens showing underground operations, safety monitoring concept, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "14", "tag": "科技", "prompt": "Sleek modern smartphone with professional camera lens array, elegant product photography, studio lighting, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "15", "tag": "文化", "prompt": "Elegant art museum exhibition hall with ancient Chinese artifacts in glass display cases, French palace architecture, cultural exchange atmosphere, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "16", "tag": "经济", "prompt": "Open-pit lithium mine with large excavation equipment, Australian outback landscape, mining operation concept, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "17", "tag": "社会", "prompt": "Scorching summer heat wave over Chinese cityscape, people seeking shade under trees, thermometers showing high temperature, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "18", "tag": "体育", "prompt": "World Cup soccer stadium packed with cheering fans, spectacular night game with colorful floodlights, Chinese cityscape in distance, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "19", "tag": "科技", "prompt": "Apple WWDC keynote presentation stage with glowing logo, sleek technology products displayed, developer conference atmosphere, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
    {"num": "20", "tag": "经济", "prompt": "Busy e-commerce warehouse with workers and delivery robots, delivery trucks outside, online shopping logistics concept, photorealistic, ultra detailed, 8K high resolution, no text no watermark"},
]

images_dir = "/home/swg/.openclaw/workspace/news-blog/images"
os.makedirs(images_dir, exist_ok=True)

api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

def generate_image(item):
    num = item['num']
    filename = f"news_{date_short}_{num}.png"
    output_path = os.path.join(images_dir, filename)
    prompt = item['prompt']
    
    if os.path.exists(output_path):
        print(f"skip {num} already exists")
        return True
    
    try:
        payload = {"model": "cogview-3-flash", "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            api_url, data=data,
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            image_url = content[0]['url']
            
            img_req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                img_data = img_resp.read()
                with open(output_path, 'wb') as f:
                    f.write(img_data)
        
        print(f"ok {num}")
        return True
    except Exception as e:
        print(f"fail {num}: {e}")
        return False

results = {}
for i, item in enumerate(news_items):
    success = generate_image(item)
    results[item['num']] = success
    if i < len(news_items) - 1:
        time.sleep(1.5)

success_count = sum(1 for v in results.values() if v)
print(f"Generated {success_count}/20 images")

failed = [k for k, v in results.items() if not v]
if failed:
    print(f"Retrying: {failed}")
    for num in failed:
        item = next(it for it in news_items if it['num'] == num)
        time.sleep(3)
        generate_image(item)

print("done")