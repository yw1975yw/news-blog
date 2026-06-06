#!/usr/bin/env python3
"""Generate images for 2026年06月07日 using Pollinations AI (fast and reliable)."""

import json
import urllib.request
import urllib.parse
import os
import time
import concurrent.futures

API_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
TODAY = "20260607"

news_items = [
    {"number": "01", "title": "G7峰会联合声明宣布追加对俄制裁 俄乌冲突持续胶着",
     "prompt": "World leaders in formal suits at G7 summit conference table with flags, photorealistic, ultra detailed, 8K, elegant ballroom, diplomatic atmosphere, soft warm lighting"},
    {"number": "02", "title": "OpenAI发布GPT-5.5旗舰模型 推理能力再创新高",
     "prompt": "Futuristic AI technology presentation with glowing neural network hologram, photorealistic, ultra detailed, 8K, modern tech lab, blue ambient lighting, holographic data"},
    {"number": "03", "title": "中国央行宣布定向降准0.25个百分点 支持实体经济发展",
     "prompt": "Modern central bank building with Chinese architecture, photorealistic, ultra detailed, 8K, clear day lighting, Beijing financial district, professional photography"},
    {"number": "04", "title": "SpaceX星舰完成首次商业发射 送20颗卫星入轨",
     "prompt": "Massive rocket launching from spaceport at dawn, starship rocket, photorealistic, ultra detailed, 8K, cinematic wide angle, dramatic exhaust clouds, orange sunrise sky"},
    {"number": "05", "title": "全球极端高温持续 多国发出高温预警提醒居民防护",
     "prompt": "Scorching summer heat wave scene, cracked dry earth, extreme high temperature, withered plants, photorealistic, ultra detailed, 8K, dramatic orange sunset, dust storm"},
    {"number": "06", "title": "英伟达发布Blackwell Ultra芯片 AI算力提升五倍",
     "prompt": "High-tech GPU chip macro photography with glowing circuits, photorealistic, ultra detailed, 8K, dark background, blue green LED lighting, precision engineering"},
    {"number": "07", "title": "中国国产大飞机C939完成首飞 挑战波音空客双寡头格局",
     "prompt": "Large modern passenger airplane taking off from runway, Chinese domestic model, photorealistic, ultra detailed, 8K, blue sky white clouds, dramatic upward angle, aviation photography"},
    {"number": "08", "title": "世卫组织启动全球流感防控新计划 应对H10N8变异毒株",
     "prompt": "World Health Organization Geneva headquarters with WHO flag, photorealistic, ultra detailed, 8K, sunny day, classical architectural photography, flags waving"},
    {"number": "09", "title": "欧盟碳边境调节机制正式生效 中国出口企业面临新挑战",
     "prompt": "Modern steel factory with tall chimneys, production facilities, photorealistic, ultra detailed, 8K, industrial area, blue sky, environmental technology, clean production"},
    {"number": "10", "title": "欧洲杯揭幕战德国大胜苏格兰 东道主展现夺冠实力",
     "prompt": "European football championship opening match, stadium packed with 60000 fans, Germany vs Scotland, players celebrating goal, photorealistic, ultra detailed, 8K, floodlights, night match"},
    {"number": "11", "title": "印尼火山喷发引发海啸预警 周边岛屿紧急疏散十万居民",
     "prompt": "Volcanic eruption with massive ash cloud rising, red lava flowing down mountain, ocean wave, photorealistic, ultra detailed, 8K, dramatic sky, orange gray tones, disaster"},
    {"number": "12", "title": "苹果发布visionOS 3系统 空间计算进入普及阶段",
     "prompt": "Person wearing AR headset interacting with holographic interfaces in modern living room, photorealistic, ultra detailed, 8K, warm home lighting, futuristic mixed reality"},
    {"number": "13", "title": "美联储褐皮书显示美国经济韧性依旧 通胀压力仍存",
     "prompt": "US Federal Reserve building facade Washington DC, people walking on marble steps, photorealistic, ultra detailed, 8K, bright daylight, classical American architecture"},
    {"number": "14", "title": "国际劳工组织报告全球青年失业率创新高 呼吁政策干预",
     "prompt": "Young unemployed people waiting outside job center, concerned expressions, urban city background, photorealistic, ultra detailed, 8K, overcast day, documentary style"},
    {"number": "15", "title": "中国首个深远海浮式风电平台并网发电 清洁能源再获突破",
     "prompt": "Offshore wind farm with massive turbines floating on ocean, blue sea and sky, photorealistic, ultra detailed, 8K, dramatic clouds, renewable energy, aerial drone perspective"},
    {"number": "16", "title": "巴黎奥运圣火采集仪式在希腊举行 奥运进入倒计时阶段",
     "prompt": "Olympic flame ceremony at ancient Greek temple ruins, female priest in white robe lighting torch, photorealistic, ultra detailed, 8K, golden sunlight, classical architecture"},
    {"number": "17", "title": "丰田与清华大学成立联合研究院 押注固态电池量产",
     "prompt": "Toyota and Tsinghua University researchers in modern laboratory working on battery technology, photorealistic, ultra detailed, 8K, clean white lab, electric vehicle battery"},
    {"number": "18", "title": "全球最大自贸区RCEP全面启动 中国与东盟贸易额创新高",
     "prompt": "Container ships loaded with colorful containers at busy international port, cranes working, photorealistic, ultra detailed, 8K, blue sky, trade logistics, aerial port view"},
    {"number": "19", "title": "阿根廷申请加入金砖国家组织 新兴市场力量持续壮大",
     "prompt": "BRICS summit meeting with flags of member countries, world leaders at conference table, photorealistic, ultra detailed, 8K, formal diplomatic setting, multinational cooperation"},
    {"number": "20", "title": "诺贝尔物理学奖授予量子通信两位先驱 中国科学家在列",
     "prompt": "Nobel Prize award ceremony at Swedish Academy, elegant grand hall with crystal chandeliers, photorealistic, ultra detailed, 8K, dignified academic atmosphere, warm golden lighting"},
]

def download_image(item):
    num = item["number"]
    prompt = item["prompt"]
    filename = f"news_{TODAY}_{num}.png"
    filepath = os.path.join(API_DIR, filename)
    
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=800&height=600&nologo=true&model=flux"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
            with open(filepath, 'wb') as f:
                f.write(data)
        size = os.path.getsize(filepath)
        print(f"  ✓ {filename} ({size} bytes)")
        return (num, True, filepath)
    except Exception as e:
        print(f"  ✗ {num} failed: {e}")
        return (num, False, None)

def main():
    os.makedirs(API_DIR, exist_ok=True)
    
    print("Generating 20 news images via Pollinations...")
    
    # Run in parallel batches of 5
    results = []
    for i in range(0, 20, 5):
        batch = news_items[i:i+5]
        print(f"\nBatch {i//5 + 1}/4: items {i+1}-{i+len(batch)}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
            batch_results = list(ex.map(download_image, batch))
        results.extend(batch_results)
        time.sleep(2)  # Small delay between batches
    
    success = sum(1 for _, ok, _ in results if ok)
    print(f"\n{'='*50}")
    print(f"Image generation: {success}/20 succeeded")
    
    # Save news data
    news_data_path = os.path.join(os.path.dirname(API_DIR), "news_data_20260607.json")
    with open(news_data_path, "w", encoding="utf-8") as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    print(f"News data saved to: {news_data_path}")

if __name__ == "__main__":
    main()