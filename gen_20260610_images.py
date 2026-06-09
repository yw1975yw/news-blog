import base64, os, time, json, urllib.request, urllib.error

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

NEWS_DATA = [
    {"id": "01", "tag": "科技", "prompt": "Futuristic AI regulation summit, world leaders and tech executives at a grand conference hall, holographic displays showing neural networks and data streams, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "02", "tag": "科技", "prompt": "Mars rover landing on red planet surface, Chinese spacecraft Tianwen-3 touching down gracefully, solar panels deploying, Martian landscape with dust clouds, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "03", "tag": "金融", "prompt": "Wall Street stock market trading floor with digital displays showing rising stock charts, people celebrating with smartphones, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "04", "tag": "经济", "prompt": "Modern cargo train on international railway crossing mountain landscape, containers loaded with goods, Eurasian trade route, golden sunset lighting, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "05", "tag": "科技", "prompt": "Scientists in laboratory working with superconducting materials, glowing magnetic levitation effect, futuristic research facility, energy revolution concept, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "06", "tag": "体育", "prompt": "FIFA World Cup opening ceremony, colorful fireworks over massive stadium, football players from different nations, fans cheering, celebration atmosphere, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "07", "tag": "国际", "prompt": "UN peacekeeping forces patrolling peaceful border region, Mediterranean coastline, soldiers on patrol near checkpoint, Middle East peacekeeping mission, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "08", "tag": "科技", "prompt": "Electric vehicle with glowing battery pack, futuristic charging station, Chinese EV manufacturer technology, long range electric car charging, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "09", "tag": "经济", "prompt": "Busiest international shipping port at night, containers being loaded onto massive cargo ship, Chinese cross-border e-commerce goods, global logistics, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "10", "tag": "文化", "prompt": "Vibrant Chinese New Year celebration in traditional city, red lanterns, lion dance parade, people in colorful costumes celebrating, cultural heritage festival, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "11", "tag": "科技", "prompt": "Next generation GPU chip on circuit board glowing with blue light, massive data center server room background, ultra powerful graphics processor, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "12", "tag": "社会", "prompt": "Scorching summer heat wave, cracked dry earth farmland, drought affected landscape in South Asia, emergency water trucks delivering aid, extreme weather climate change, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "13", "tag": "国际", "prompt": "World leaders at G7 summit conference table, flags of seven nations, diplomatic meeting in Swiss mountain resort, international geopolitics discussion, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "14", "tag": "科技", "prompt": "Large Chinese commercial aircraft taking off from runway, aviation industry breakthrough, blue sky white clouds background, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "15", "tag": "金融", "prompt": "Bank of Japan headquarters building in Tokyo, Japanese yen banknotes and coins, monetary policy shift, financial district Tokyo, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "16", "tag": "社会", "prompt": "Majestic blue whale swimming in pristine Antarctic ocean waters, icebergs in background, marine conservation zone, environmental protection milestone, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "17", "tag": "科技", "prompt": "Quantum computer prototype in research laboratory, glowing quantum circuits and superconducting qubits, Chinese scientists celebrating breakthrough, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "18", "tag": "文化", "prompt": "Tourists visiting Eiffel Tower and Louvre Museum in Paris, crowded summer plaza, French cultural landmarks, Olympic legacy tourism boom, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "19", "tag": "科技", "prompt": "Person using AI assistant with holographic display showing multimodal AI capabilities, video and image understanding interface, next generation AI technology, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "20", "tag": "社会", "prompt": "Chinese high school students celebrating after gaokao exam, confetti and happy faces, exam venue outside scene, education milestone, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
]

def generate_image(news_id, prompt):
    output_path = f"/home/swg/.openclaw/workspace/news-blog/images/news_20260610_{news_id}.png"
    if os.path.exists(output_path):
        print(f"  [SKIP] Image {news_id} already exists")
        return True
    payload = {"model": "cogview-3-flash", "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            if "data:image/png;base64," in content:
                b64_data = content.split("data:image/png;base64,")[1]
            else:
                b64_data = content
            img_data = base64.b64decode(b64_data)
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"  [OK] Generated image {news_id}")
            return True
    except Exception as e:
        print(f"  [ERROR] Failed image {news_id}: {e}")
        return False

print("Generating news images for 2026-06-10...")
os.makedirs("/home/swg/.openclaw/workspace/news-blog/images", exist_ok=True)
results = {}
for news in NEWS_DATA:
    nid = news["id"]
    print(f"Generating image {nid}...")
    success = generate_image(nid, news["prompt"])
    results[nid] = success
    if not success:
        print(f"  Retrying image {nid}...")
        time.sleep(5)
        success = generate_image(nid, news["prompt"])
        results[nid] = success
    time.sleep(2)

ok = sum(1 for v in results.values() if v)
print(f"\nSummary: {ok}/20 success")
for nid, status in results.items():
    print(f"  {nid}: {'OK' if status else 'FAILED'}")
