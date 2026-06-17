import urllib.request
import urllib.error
import json
import time
import os

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
IMAGES_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
DATE = "20260617"

news_prompts = [
    ("01", "A futuristic AI research laboratory with scientists analyzing large language model outputs on holographic displays, ultra realistic, 8K high resolution photography"),
    ("02", "World leaders sitting around a large conference table at G7 summit, flags of participating nations displayed, photorealistic news photograph style, ultra detailed"),
    ("03", "A bustling urban sky filled with various light aircraft and commercial drones flying between skyscrapers at sunset, photorealistic aerial view, 8K"),
    ("04", "A massive SpaceX rocket launching at night from a coastal spaceport, bright flame trail illuminating the sky, photorealistic, ultra detailed"),
    ("05", "US and China national flags side by side in an elegant diplomatic meeting room with technology circuit board patterns, photorealistic, ultra detailed"),
    ("06", "The European Central Bank building in Frankfurt at golden hour, financial data charts displayed on screens in foreground, photorealistic architecture photography"),
    ("07", "Apple WWDC stage with glowing AR headset devices and developers trying visionOS demos, colorful lights and modern auditorium, photorealistic event photography"),
    ("08", "International airport health screening station with medical staff in protective gear checking passengers, quarantine control zone, photorealistic news photo"),
    ("09", "A digital cryptocurrency trading screen showing Bitcoin price chart surging to new highs, glowing Bitcoin logo, financial data visualization, photorealistic"),
    ("10", "Electric vehicle charging station with sleek charging cable connecting to car, digital display showing 10 minutes charging achieving 1000km range, modern gas station, photorealistic"),
    ("11", "The United Nations headquarters building in New York, with Chinese and international officials shaking hands in front of UN logo, diplomatic setting, photorealistic"),
    ("12", "Semiconductor fabrication clean room with engineers in protective suits working on advanced chip manufacturing equipment, blue clean room lighting, photorealistic"),
    ("13", "A vibrant soccer stadium with Chinese national team in red jerseys playing against Netherlands team, crowd cheering, dramatic stadium lights at night, photorealistic sports photography"),
    ("14", "A massive cargo ship at a busy Chinese port with hundreds of new electric vehicles lined up in the cargo hold ready for export, aerial view, photorealistic"),
    ("15", "Advanced quantum computer processor suspended in a cryogenic chamber with glowing blue superconducting circuits, laboratory setting, photorealistic science photography"),
    ("16", "Citizens using portable fans and air conditioners during extreme heat wave, crowded city street with thermometers showing high temperatures, summer heat scene, photorealistic"),
    ("17", "Massive automated e-commerce logistics warehouse with delivery robots and conveyor belts sorting packages, drones flying overhead, photorealistic, ultra detailed"),
    ("18", "International conference hall with experts from many countries discussing AI safety at round table, AI neural network visualization on screens, photorealistic"),
    ("19", "Chinese internet regulation office with large digital screens showing compliance documents and platform data, serious professional atmosphere, photorealistic"),
    ("20", "Chinese high school graduates celebrating with families after receiving college entrance exam results, fireworks and confetti, joyful atmosphere, photorealistic"),
]

def generate_image(news_num, prompt, retries=2):
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method="POST"
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                # content is a list: [{'url': '...'}]
                if isinstance(content, list) and len(content) > 0:
                    img_url = content[0].get("url", "")
                elif isinstance(content, str):
                    img_url = content
                else:
                    print(f"FAIL:{news_num} unexpected content type: {type(content)}")
                    return False
                
                if not img_url:
                    print(f"FAIL:{news_num} no URL in response")
                    return False
                
                # Download the image
                img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                    img_bytes = img_resp.read()
                
                out_path = f"{IMAGES_DIR}/news_{DATE}_{news_num}.png"
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"OK:{news_num} ({len(img_bytes)} bytes)")
                return True
        except Exception as e:
            print(f"FAIL:{news_num} attempt {attempt+1}: {str(e)[:100]}")
            time.sleep(3)
    return False

for news_num, prompt in news_prompts:
    success = generate_image(news_num, prompt)
    if not success:
        print(f"  -> Retrying {news_num}...")
        generate_image(news_num, prompt, retries=2)
    time.sleep(1)

print("DONE")