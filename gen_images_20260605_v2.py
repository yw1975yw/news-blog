import subprocess
import base64
import json
import time
import os
import urllib.request
import urllib.error

news_items = [
    {"number": "01", "prompt": "Futuristic AI research laboratory with holographic displays showing neural network, scientists working, photorealistic, ultra detailed, 8K"},
    {"number": "02", "prompt": "Chinese rocket launching into blue sky with flames and smoke trail, space mission, photorealistic, ultra detailed, 8K"},
    {"number": "03", "prompt": "Federal Reserve building in Washington DC with American flag, classic architecture, photorealistic, ultra detailed, 8K"},
    {"number": "04", "prompt": "European Union flag with digital technology icons, smartphone and apps interface, photorealistic, ultra detailed, 8K"},
    {"number": "05", "prompt": "Modern Chinese shopping mall interior with shoppers and retail stores, photorealistic, ultra detailed, 8K"},
    {"number": "06", "prompt": "Apple WWDC keynote presentation stage with giant LED display showing software interface, photorealistic, ultra detailed, 8K"},
    {"number": "07", "prompt": "Olympic stadium with athletic track, Olympic rings decoration, photorealistic, ultra detailed, 8K"},
    {"number": "08", "prompt": "Electric vehicle charging station with glowing battery pack, modern technology, photorealistic, ultra detailed, 8K"},
    {"number": "09", "prompt": "International summit conference room with world leaders seated, photorealistic, ultra detailed, 8K"},
    {"number": "10", "prompt": "Advanced quantum computer in scientific laboratory with glowing circuits, photorealistic, ultra detailed, 8K"},
    {"number": "11", "prompt": "Modern tech company headquarters building exterior, glass architecture, cloud computing visualization, photorealistic, ultra detailed, 8K"},
    {"number": "12", "prompt": "Chinese high school classroom with students taking exam, invigilator walking, photorealistic, ultra detailed, 8K"},
    {"number": "13", "prompt": "Modern football stadium with referee booth and video screens, sports event, photorealistic, ultra detailed, 8K"},
    {"number": "14", "prompt": "Tesla Megafactory interior with large battery units on production line, manufacturing, photorealistic, ultra detailed, 8K"},
    {"number": "15", "prompt": "Traditional Chinese New Year celebration with red lanterns and festive decorations, photorealistic, ultra detailed, 8K"},
    {"number": "16", "prompt": "Desktop computer monitor showing modern operating system interface, keyboard and mouse, photorealistic, ultra detailed, 8K"},
    {"number": "17", "prompt": "Stock exchange trading floor with digital price displays showing upward trend, bull market, photorealistic, ultra detailed, 8K"},
    {"number": "18", "prompt": "United Nations headquarters building exterior with flags of nations, New York, photorealistic, ultra detailed, 8K"},
    {"number": "19", "prompt": "Beijing modern cityscape with tall apartment buildings and urban architecture, photorealistic, ultra detailed, 8K"},
    {"number": "20", "prompt": "Advanced semiconductor microchip under microscope showing intricate circuit patterns, technology, photorealistic, ultra detailed, 8K"},
]

api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

def download_image(url, filename):
    """Download image from URL with retry"""
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                with open(filename, 'wb') as f:
                    f.write(data)
            return True, len(data)
        except Exception as e:
            print(f"  Download attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return False, 0

for item in news_items:
    filename = f"images/news_20260605_{item['number']}.png"
    
    body = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {item['prompt']}"}]
    }
    
    cmd = f'curl -s -X POST "{url}" -H "Authorization: Bearer {api_key}" -H "Content-Type: application/json" -d \'{json.dumps(body)}\''
    
    print(f"Generating {filename}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    
    try:
        resp = json.loads(result.stdout)
        content_list = resp["choices"][0]["message"]["content"]
        
        # Handle list format with URL
        if isinstance(content_list, list):
            url_entry = content_list[0]
            if isinstance(url_entry, dict) and "url" in url_entry:
                img_url = url_entry["url"]
                print(f"  Got URL: {img_url[:80]}...")
                ok, size = download_image(img_url, filename)
                if ok:
                    print(f"  [OK] Downloaded {filename} ({size} bytes)")
                else:
                    print(f"  [ERROR] Failed to download {filename}")
            else:
                print(f"  [ERROR] Unexpected list entry: {url_entry}")
        elif isinstance(content_list, str):
            # Handle base64 format (just in case)
            if content_list.startswith("data:image"):
                b64_data = content_list.split(",")[1]
                img_data = base64.b64decode(b64_data)
                with open(filename, "wb") as f:
                    f.write(img_data)
                print(f"  [OK] Saved {filename} ({len(img_data)} bytes)")
            else:
                print(f"  [ERROR] Unexpected string content: {content_list[:100]}")
    except Exception as e:
        print(f"  [ERROR] {e}")
        print(f"  Response: {result.stdout[:500]}")
    time.sleep(2)

print("\nAll 20 images generation complete!")

# Verify files
print("\nVerifying generated files:")
for i in range(1, 21):
    num = f"{i:02d}"
    fname = f"images/news_20260605_{num}.png"
    if os.path.exists(fname):
        size = os.path.getsize(fname)
        print(f"  {fname}: {size} bytes")
    else:
        print(f"  {fname}: MISSING")