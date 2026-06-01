#!/usr/bin/env python3
import requests, base64, json, os, time

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

news_items = [
    ("01", "Chinese astronauts entering Tiangong space station module, interior with astronauts in white spacesuits floating in microgravity, advanced control panels, photorealistic, ultra detailed, 8K"),
    ("02", "NVIDIA Blackwell Ultra GPU chip macro photography, glowing green circuit board with massive GPU die, holographic data streams, tech conference background, photorealistic, ultra detailed, 8K"),
    ("03", "China and US trade negotiators shaking hands across table with flags of both nations, Geneva conference room, warm diplomatic atmosphere, photorealistic, ultra detailed, 8K"),
    ("04", "Chinese stock market trading floor with large digital displays showing rising stock prices, bull statue foreground, investors watching screens optimistically, photorealistic, ultra detailed, 8K"),
    ("05", "Archaeologists carefully excavating ancient Sanxingdui bronze artifacts in Sichuan China, bronze masks and jade relics being unearthed, museum lighting, photorealistic, ultra detailed, 8K"),
    ("06", "Futuristic nuclear fusion power plant interior with tokamak reactor glowing blue, scientists monitoring data in control room, sci-fi energy facility, photorealistic, ultra detailed, 8K"),
    ("07", "Aerial view earthquake devastation Brazilian city, collapsed buildings rescue workers orange uniforms searching rubble, emergency helicopters overhead, photorealistic, ultra detailed, 8K"),
    ("08", "Diverse Chinese people using AI assistant apps on smartphones in modern urban setting, holographic AI brain visualization above phones, photorealistic, ultra detailed, 8K"),
    ("09", "Chinese COMAC C919 passenger aircraft flying over clouds at air show, sleek white body red accent lines, blue sky background, photorealistic, ultra detailed, 8K"),
    ("10", "WHO officials announcing pandemic end at press conference, world map background green checkmarks, relieved people traveling at airport terminal, photorealistic, ultra detailed, 8K"),
    ("11", "Bitcoin cryptocurrency gold coin glowing showing Bitcoin symbol, digital trading charts rising on multiple screens, futuristic financial district, photorealistic, ultra detailed, 8K"),
    ("12", "Massive green hydrogen production facility Xinjiang desert, large solar panels wind turbines powering electrolysis plant, white hydrogen storage tanks, photorealistic, ultra detailed, 8K"),
    ("13", "Argentina government building Buenos Aires with cranes construction, BRICS summit meeting hall with national flags, photorealistic, ultra detailed, 8K"),
    ("14", "Chinese swimmers celebrating world record victory, diving into pool burst of water, scoreboard showing new world record time, Olympic pool arena, photorealistic, ultra detailed, 8K"),
    ("15", "Huawei headquarters building with glowing AI neural network visualization, developer conference stage massive screen AI architecture, photorealistic, ultra detailed, 8K"),
    ("16", "Volcanic eruption Indonesia massive ash cloud rising, ocean waves crashing, coastal evacuation orange-suited emergency workers, photorealistic, ultra detailed, 8K"),
    ("17", "Architectural rendering three grand cultural buildings under construction in Beijing, modern skyline, cranes construction workers, photorealistic, ultra detailed, 8K"),
    ("18", "Global vaccination center in developing country, healthcare workers administering vaccines diverse population, cold chain storage containers, photorealistic, ultra detailed, 8K"),
    ("19", "Chinese scientists quantum communication laboratory with satellite dish, holographic quantum encryption visualization, Beijing cityscape, photorealistic, ultra detailed, 8K"),
    ("20", "Split scene multiple extreme weather events: North American heat wave, South Asian flooding, European drought, dramatic skies climate change, photorealistic, ultra detailed, 8K"),
]

os.makedirs('/home/swg/.openclaw/workspace/news-blog/images', exist_ok=True)

def gen(num, prompt):
    path = f'/home/swg/.openclaw/workspace/news-blog/images/news_20260601_{num}.png'
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
    time.sleep(1)

success = sum(1 for _, r in results if r)
print(f"\n=== {success}/20 ===")
for num, ok in results:
    print(f"  [{num}] {'ok' if ok else 'FAIL'}")