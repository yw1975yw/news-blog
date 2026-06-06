#!/usr/bin/env python3
"""Retry failed CogView-3-Flash images for 2026年06月07日."""

import json
import base64
import urllib.request
import time
import os

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
IMG_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
TODAY = "20260607"

failed_items = [
    {"number": "02", "title": "OpenAI发布GPT-5.5旗舰模型 推理能力再创新高",
     "prompt": "Futuristic AI technology presentation with glowing neural network hologram, photorealistic, ultra detailed, 8K, modern tech lab, blue ambient lighting, holographic data visualization"},
    {"number": "03", "title": "中国央行宣布定向降准0.25个百分点 支持实体经济发展",
     "prompt": "Modern central bank building with Chinese palace-style architecture, people passing by, photorealistic, ultra detailed, 8K, clear day lighting, Beijing financial district, professional photography"},
    {"number": "04", "title": "SpaceX星舰完成首次商业发射 送20颗卫星入轨",
     "prompt": "Massive rocket launching from coastal spaceport at sunrise, starship rocket with billowing steam, photorealistic, ultra detailed, 8K, cinematic wide angle, dramatic orange sky, exhaust clouds"},
    {"number": "05", "title": "全球极端高温持续 多国发出高温预警提醒居民防护",
     "prompt": "Extreme heat wave scene with cracked dry earth, thermometer showing high temperature, withered crops, photorealistic, ultra detailed, 8K, dramatic orange sunset sky, heat shimmer effect"},
    {"number": "07", "title": "中国国产大飞机C939完成首飞 挑战波音空客双寡头格局",
     "prompt": "Large modern passenger airplane taking off from airport runway into blue sky, Chinese domestic model, photorealistic, ultra detailed, 8K, white clouds, dramatic upward angle, aviation photography"},
    {"number": "10", "title": "欧洲杯揭幕战德国大胜苏格兰 东道主展现夺冠实力",
     "prompt": "European football championship opening match, packed stadium with 60000 fans, players celebrating goal, photorealistic, ultra detailed, 8K, dramatic floodlights, night match atmosphere"},
    {"number": "11", "title": "印尼火山喷发引发海啸预警 周边岛屿紧急疏散十万居民",
     "prompt": "Volcanic eruption with massive dark ash cloud rising from mountain, red lava rivers flowing, ocean waves in foreground, photorealistic, ultra detailed, 8K, dramatic stormy sky, disaster scene"},
    {"number": "13", "title": "美联储褐皮书显示美国经济韧性依旧 通胀压力仍存",
     "prompt": "US Federal Reserve building facade in Washington DC with marble steps, people walking, photorealistic, ultra detailed, 8K, bright daylight, classical American neoclassical architecture"},
    {"number": "14", "title": "国际劳工组织报告全球青年失业率创新高 呼吁政策干预",
     "prompt": "Young unemployed people waiting outside government job center, concerned expressions, urban cityscape background, photorealistic, ultra detailed, 8K, overcast day, documentary photography style"},
    {"number": "16", "title": "巴黎奥运圣火采集仪式在希腊举行 奥运进入倒计时阶段",
     "prompt": "Olympic flame ceremony at ancient Greek temple ruins, female priest in white robe lighting torch with concave mirror, photorealistic, ultra detailed, 8K, golden sunlight, classical architecture"},
    {"number": "17", "title": "丰田与清华大学成立联合研究院 押注固态电池量产",
     "prompt": "Toyota and Tsinghua University researchers in modern white laboratory working on battery technology, photorealistic, ultra detailed, 8K, clean lab environment, electric vehicle battery pack"},
    {"number": "19", "title": "阿根廷申请加入金砖国家组织 新兴市场力量持续壮大",
     "prompt": "BRICS summit meeting with flags of member nations, world leaders at conference table smiling, photorealistic, ultra detailed, 8K, formal diplomatic setting, multinational cooperation atmosphere"},
]

def generate_single(item):
    num = item["number"]
    prompt = item["prompt"]
    filename = f"news_{TODAY}_{num}.png"
    filepath = os.path.join(IMG_DIR, filename)
    
    for attempt in range(3):
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
            
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
            
            # Handle URL response
            img_url = None
            if isinstance(content, list):
                img_url = content[0].get("url") if isinstance(content[0], dict) else None
            elif isinstance(content, str) and content.startswith("http"):
                img_url = content
            
            if img_url:
                img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                    img_data = img_resp.read()
                    with open(filepath, "wb") as f:
                        f.write(img_data)
                size = os.path.getsize(filepath)
                print(f"  ✓ {filename} ({size} bytes)")
                return True
            
            print(f"  ✗ {num}: unexpected content format")
            return False
            
        except Exception as e:
            print(f"  ✗ {num} attempt {attempt+1} failed: {e}")
            time.sleep(10)  # Wait longer on rate limit
    
    return False

def main():
    print(f"Retrying {len(failed_items)} failed images...")
    success = 0
    for i, item in enumerate(failed_items):
        print(f"\n[{i+1}/{len(failed_items)}] Retrying item {item['number']}: {item['title'][:30]}...")
        if generate_single(item):
            success += 1
        time.sleep(15)  # 15 second delay between requests to avoid rate limit
    
    print(f"\n{'='*50}")
    print(f"Retry result: {success}/{len(failed_items)} succeeded")
    
    # Check all images
    existing = [f for f in os.listdir(IMG_DIR) if f.startswith(f"news_{TODAY}_")]
    print(f"Total images for {TODAY}: {len(existing)}/20")

if __name__ == "__main__":
    main()