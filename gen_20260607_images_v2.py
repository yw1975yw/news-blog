#!/usr/bin/env python3
"""Generate 20 news images for 2026年06月07日 using CogView-3-Flash API."""

import json
import base64
import urllib.request
import time
import os
import concurrent.futures

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
IMG_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
TODAY = "20260607"

news_items = [
    {"number": "01", "tag": "国际", "title": "G7峰会联合声明宣布追加对俄制裁 俄乌冲突持续胶着",
     "prompt": "World leaders in formal suits at G7 summit conference table with flags, photorealistic, ultra detailed, 8K, elegant ballroom, diplomatic atmosphere, soft warm lighting"},
    {"number": "02", "tag": "科技", "title": "OpenAI发布GPT-5.5旗舰模型 推理能力再创新高",
     "prompt": "Futuristic AI technology presentation with glowing neural network hologram, photorealistic, ultra detailed, 8K, modern tech lab, blue ambient lighting, holographic data visualization"},
    {"number": "03", "tag": "金融", "title": "中国央行宣布定向降准0.25个百分点 支持实体经济发展",
     "prompt": "Modern central bank building with Chinese palace-style architecture, people passing by, photorealistic, ultra detailed, 8K, clear day lighting, Beijing financial district, professional photography"},
    {"number": "04", "tag": "科技", "title": "SpaceX星舰完成首次商业发射 送20颗卫星入轨",
     "prompt": "Massive rocket launching from coastal spaceport at sunrise, starship rocket with billowing steam, photorealistic, ultra detailed, 8K, cinematic wide angle, dramatic orange sky, exhaust clouds"},
    {"number": "05", "tag": "社会", "title": "全球极端高温持续 多国发出高温预警提醒居民防护",
     "prompt": "Extreme heat wave scene with cracked dry earth, thermometer showing high temperature, withered crops, photorealistic, ultra detailed, 8K, dramatic orange sunset sky, heat shimmer effect"},
    {"number": "06", "tag": "科技", "title": "英伟达发布Blackwell Ultra芯片 AI算力提升五倍",
     "prompt": "High-tech GPU chip close-up with glowing circuits and LEDs, photorealistic, ultra detailed, 8K, dark background with blue green lighting, precision engineering, computer hardware aesthetic"},
    {"number": "07", "tag": "科技", "title": "中国国产大飞机C939完成首飞 挑战波音空客双寡头格局",
     "prompt": "Large modern passenger airplane taking off from airport runway into blue sky, Chinese domestic model, photorealistic, ultra detailed, 8K, white clouds, dramatic upward angle, aviation photography"},
    {"number": "08", "tag": "社会", "title": "世卫组织启动全球流感防控新计划 应对H10N8变异毒株",
     "prompt": "World Health Organization headquarters building in Geneva with WHO flag, photorealistic, ultra detailed, 8K, sunny day, elegant architectural photography, flags waving gently"},
    {"number": "09", "tag": "经济", "title": "欧盟碳边境调节机制正式生效 中国出口企业面临新挑战",
     "prompt": "Modern steel factory with tall chimneys and industrial facilities, photorealistic, ultra detailed, 8K, industrial area with blue sky, environmental protection equipment, clean production"},
    {"number": "10", "tag": "体育", "title": "欧洲杯揭幕战德国大胜苏格兰 东道主展现夺冠实力",
     "prompt": "European football championship opening match, packed stadium with 60000 fans, players celebrating goal, photorealistic, ultra detailed, 8K, dramatic floodlights, night match atmosphere"},
    {"number": "11", "tag": "国际", "title": "印尼火山喷发引发海啸预警 周边岛屿紧急疏散十万居民",
     "prompt": "Volcanic eruption with massive dark ash cloud rising from mountain, red lava rivers flowing, ocean waves in foreground, photorealistic, ultra detailed, 8K, dramatic stormy sky, disaster scene"},
    {"number": "12", "tag": "科技", "title": "苹果发布visionOS 3系统 空间计算进入普及阶段",
     "prompt": "Person wearing sleek AR headset in modern living room, interacting with holographic interfaces, photorealistic, ultra detailed, 8K, warm ambient home lighting, futuristic mixed reality"},
    {"number": "13", "tag": "金融", "title": "美联储褐皮书显示美国经济韧性依旧 通胀压力仍存",
     "prompt": "US Federal Reserve building facade in Washington DC with marble steps, people walking, photorealistic, ultra detailed, 8K, bright daylight, classical American neoclassical architecture"},
    {"number": "14", "tag": "社会", "title": "国际劳工组织报告全球青年失业率创新高 呼吁政策干预",
     "prompt": "Young unemployed people waiting outside government job center, concerned expressions, urban cityscape background, photorealistic, ultra detailed, 8K, overcast day, documentary photography style"},
    {"number": "15", "tag": "科技", "title": "中国首个深远海浮式风电平台并网发电 清洁能源再获突破",
     "prompt": "Offshore wind farm with massive turbines floating on ocean waves, blue sea and sky, photorealistic, ultra detailed, 8K, dramatic clouds, renewable energy, aerial drone perspective view"},
    {"number": "16", "tag": "体育", "title": "巴黎奥运圣火采集仪式在希腊举行 奥运进入倒计时阶段",
     "prompt": "Olympic flame ceremony at ancient Greek temple ruins, female priest in white robe lighting torch with concave mirror, photorealistic, ultra detailed, 8K, golden sunlight, classical architecture"},
    {"number": "17", "tag": "科技", "title": "丰田与清华大学成立联合研究院 押注固态电池量产",
     "prompt": "Toyota and Tsinghua University researchers in modern white laboratory working on battery technology, photorealistic, ultra detailed, 8K, clean lab environment, electric vehicle battery pack"},
    {"number": "18", "tag": "经济", "title": "全球最大自贸区RCEP全面启动 中国与东盟贸易额创新高",
     "prompt": "Container ships loaded with colorful shipping containers at busy international port, giant cranes working, photorealistic, ultra detailed, 8K, clear blue sky, trade logistics, aerial port view"},
    {"number": "19", "tag": "国际", "title": "阿根廷申请加入金砖国家组织 新兴市场力量持续壮大",
     "prompt": "BRICS summit meeting with flags of member nations, world leaders at conference table smiling, photorealistic, ultra detailed, 8K, formal diplomatic setting, multinational cooperation atmosphere"},
    {"number": "20", "tag": "文化", "title": "诺贝尔物理学奖授予量子通信两位先驱 中国科学家在列",
     "prompt": "Nobel Prize award ceremony at Swedish Academy, elegant grand hall with crystal chandeliers and golden decorations, photorealistic, ultra detailed, 8K, dignified academic atmosphere, warm lighting"},
]

def generate_cogview_image(item):
    """Generate image via CogView-3-Flash API. Returns (number, success, filepath)."""
    num = item["number"]
    prompt = item["prompt"]
    filename = f"news_{TODAY}_{num}.png"
    filepath = os.path.join(IMG_DIR, filename)
    
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"  ✓ {filename} already exists, skipping")
        return (num, True, filepath)
    
    for attempt in range(2):
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
            
            # Handle URL response (list format)
            img_url = None
            if isinstance(content, list):
                img_url = content[0].get("url") if isinstance(content[0], dict) else None
            elif isinstance(content, str):
                if content.startswith("http"):
                    img_url = content
                elif "data:image" in content:
                    b64 = content.split("base64,")[-1]
                    img_data = base64.b64decode(b64)
                    with open(filepath, "wb") as f:
                        f.write(img_data)
                    size = os.path.getsize(filepath)
                    print(f"  ✓ {filename} ({size} bytes)")
                    return (num, True, filepath)
            
            if img_url:
                # Download from URL
                img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                    img_data = img_resp.read()
                    with open(filepath, "wb") as f:
                        f.write(img_data)
                size = os.path.getsize(filepath)
                print(f"  ✓ {filename} ({size} bytes, URL)")
                return (num, True, filepath)
            
            print(f"  ✗ {num}: unexpected content format: {str(content)[:100]}")
            
        except Exception as e:
            print(f"  ✗ {num} attempt {attempt+1} failed: {e}")
            time.sleep(5)
    
    return (num, False, None)

def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    
    print(f"Generating 20 news images for {TODAY} via CogView-3-Flash...")
    
    # Run in parallel batches of 3 (to avoid overwhelming the API)
    all_results = []
    for i in range(0, 20, 3):
        batch = news_items[i:i+3]
        print(f"\nBatch {i//3 + 1}/7: items {i+1}-{i+len(batch)}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            batch_results = list(ex.map(generate_cogview_image, batch))
        all_results.extend(batch_results)
        time.sleep(3)
    
    success = sum(1 for _, ok, _ in all_results if ok)
    print(f"\n{'='*50}")
    print(f"Image generation: {success}/20 succeeded")
    
    failed = [num for num, ok, _ in all_results if not ok]
    if failed:
        print(f"Failed items: {failed}")
    
    # Save news data
    news_data_path = os.path.join(os.path.dirname(IMG_DIR), "news_data_20260607.json")
    with open(news_data_path, "w", encoding="utf-8") as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    print(f"News data saved to: {news_data_path}")

if __name__ == "__main__":
    main()