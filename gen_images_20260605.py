import subprocess
import base64
import json
import time
import os

news_items = [
    {"number": "01", "prompt": "A scientist working at a futuristic AI research lab, holographic displays showing neural network architecture, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "02", "prompt": "Chinese Long March rocket launching into blue sky with flames and smoke, space mission, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "03", "prompt": "Federal Reserve building in Washington DC with American flag, financial district, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "04", "prompt": "European Union flag with digital technology symbols, smartphone and apps, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "05", "prompt": "Busy Chinese shopping mall with shoppers, retail stores, consumers, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "06", "prompt": "Apple WWDC keynote stage with giant display showing iOS interface, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "07", "prompt": "Paris Olympics 2026 stadium with athletes, Olympic rings, French flag decorations, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "08", "prompt": "Electric vehicle charging station with glowing battery, fast charging technology, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "09", "prompt": "G7 world leaders meeting at summit, international conference, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "10", "prompt": "Quantum computer in laboratory with glowing blue circuits, scientific research, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "11", "prompt": "Modern tech company headquarters building with cloud computing visualization, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "12", "prompt": "Chinese high school exam hall, students taking test, invigilators, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "13", "prompt": "Football stadium VAR video assistant referee booth with screens, World Cup match, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "14", "prompt": "Tesla Megafactory large energy storage batteries on production line, manufacturing, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "15", "prompt": "Chinese Spring Festival celebration with red lanterns, fireworks at night, traditional cultural festival, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "16", "prompt": "Desktop computer running HarmonyOS operating system interface, modern office setup, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "17", "prompt": "Shanghai Stock Exchange trading floor with digital displays showing stock prices rising, bull market, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "18", "prompt": "United Nations headquarters building in New York with flags of nations, international organization, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "19", "prompt": "Beijing cityscape with modern apartment buildings and real estate, urban housing, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
    {"number": "20", "prompt": "Semiconductor chip under electron microscope showing 3nm transistor architecture, computer processor technology, photorealistic, ultra detailed, 8K, high resolution, no text watermark"},
]

api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

for item in news_items:
    filename = f"images/news_20260605_{item['number']}.png"
    if os.path.exists(filename):
        print(f"[SKIP] {filename} already exists")
        continue
    
    body = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {item['prompt']}"}]
    }
    
    cmd = f'curl -s -X POST "{url}" -H "Authorization: Bearer {api_key}" -H "Content-Type: application/json" -d \'{json.dumps(body)}\''
    
    print(f"Generating {filename}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    
    try:
        resp = json.loads(result.stdout)
        content = resp["choices"][0]["message"]["content"]
        if content.startswith("data:image/png;base64,"):
            b64_data = content.split(",")[1]
            img_data = base64.b64decode(b64_data)
            with open(filename, "wb") as f:
                f.write(img_data)
            print(f"  [OK] Saved {filename} ({len(img_data)} bytes)")
        else:
            print(f"  [ERROR] Unexpected content format: {content[:200]}")
    except Exception as e:
        print(f"  [ERROR] {e}")
        print(f"  Response: {result.stdout[:500]}")
    time.sleep(2)

print("\nAll 20 images generation complete!")