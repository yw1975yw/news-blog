#!/usr/bin/env python3
import requests, base64, json, os, time

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

news_items = [
    ("01", "A futuristic technology conference stage with a giant holographic display showing neural network visualization, photorealistic, ultra detailed, 8K, high resolution, dramatic lighting, tech keynote setting"),
    ("02", "Rocket launching from coastal spaceport at sunset with billowing smoke and bright flame exhaust, cargo spacecraft in flight against blue sky, photorealistic, ultra detailed, 8K, cinematic composition"),
    ("03", "European Parliament building in Brussels illuminated at night with EU flags, photorealistic, ultra detailed, 8K, evening atmosphere with lamp posts, architectural photography"),
    ("04", "Financial trading screens showing cryptocurrency price charts with glowing charts and upward trend, modern trading floor, photorealistic, ultra detailed, 8K, dramatic lighting with blue and green colors"),
    ("05", "Modern cargo port with container ships at dock, crane operations loading colorful shipping containers, industrial harbor scene, photorealistic, ultra detailed, 8K, golden hour lighting"),
    ("06", "Advanced humanoid robot in modern factory environment performing precise assembly task, photorealistic, ultra detailed, 8K, clean white factory interior with robotic arm, cinematic lighting"),
    ("07", "World leaders at G7 summit meeting in elegant conference room with international flags, photorealistic, ultra detailed, 8K, diplomatic atmosphere with formal table setting"),
    ("08", "Delivery drones flying in urban sky over modern Chinese city skyline at dusk, photorealistic, ultra detailed, 8K, sunset atmosphere with buildings and flying quadcopters carrying packages"),
    ("09", "NVIDIA headquarters building with sleek modern architecture, stock market display showing upward arrow, photorealistic, ultra detailed, 8K, corporate campus in Silicon Valley, dramatic sky"),
    ("10", "Wimbledon tennis championships grass court with players in action, Centre Court at sunset, photorealistic, ultra detailed, 8K, lush green grass, British summer atmosphere, dramatic clouds"),
    ("11", "Ancient Chinese palace museum interior with digital holographic projections of traditional Chinese paintings, visitors experiencing VR exhibition, photorealistic, ultra detailed, 8K, cultural heritage site"),
    ("12", "Elderly people in China happily receiving pension benefits at modern bank service counter, photorealistic, ultra detailed, 8K, warm lighting, social security service hall with friendly staff"),
    ("13", "Meta logo illuminated on modern office building exterior at night, technology campus atmosphere, photorealistic, ultra detailed, 8K, blue and purple neon lighting, digital atmosphere"),
    ("14", "Three world leaders shaking hands at diplomatic summit meeting in Seoul, international flags in background, photorealistic, ultra detailed, 8K, formal diplomatic setting, warm handshake moment"),
    ("15", "Modern electric vehicle charging station with sleek car at charging point in Chinese urban environment, photorealistic, ultra detailed, 8K, clean modern setting with green energy concept"),
    ("16", "Shanghai financial district skyline with Pudong towers at night reflected in river, photorealistic, ultra detailed, 8K, dramatic skyline with illuminated buildings, Huangpu River scene"),
    ("17", "Scientific research laboratory with researcher examining papers and laptop showing rejection notice, photorealistic, ultra detailed, 8K, academic office setting with books and scientific equipment"),
    ("18", "International summit meeting with diverse world leaders from BRICS countries, flags of participating nations, photorealistic, ultra detailed, 8K, diplomatic conference hall with global leaders"),
    ("19", "Modern AI research laboratory interior with scientists working at computers analyzing neural network data on large displays, photorealistic, ultra detailed, 8K, clean high-tech research environment"),
    ("20", "Chinese scientists in quantum computing laboratory with advanced quantum hardware and optical instruments, photorealistic, ultra detailed, 8K, high-tech research facility with blue laser beams, futuristic atmosphere"),
]

os.makedirs('/home/swg/.openclaw/workspace/news-blog/images', exist_ok=True)

def gen(num, prompt):
    path = f'/home/swg/.openclaw/workspace/news-blog/images/news_20260604_{num}.png'
    if os.path.exists(path):
        print(f"[{num}] exists skip")
        return True
    try:
        resp = requests.post(API_URL, json={"model":"cogview-3-flash","messages":[{"role":"user","content":f"Image prompt: {prompt}"}]}, headers={"Authorization":f"Bearer {API_KEY}","Content-Type":"application/json"}, timeout=120)
        data = resp.json()
        content_list = data['choices'][0]['message']['content']
        img_url = content_list[0]['url']
        img_resp = requests.get(img_url, timeout=60)
        with open(path, 'wb') as f:
            f.write(img_resp.content)
        print(f"[{num}] OK ({len(img_resp.content)} bytes)")
        return True
    except Exception as e:
        print(f"[{num}] ERR: {e}")
        return False

results = []
for num, prompt in news_items:
    r = gen(num, prompt)
    results.append((num, r))
    time.sleep(2)

success = sum(1 for _, r in results if r)
print(f"\n=== {success}/20 ===")
for num, ok in results:
    print(f"  [{num}] {'ok' if ok else 'FAIL'}")
