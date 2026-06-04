import subprocess, json, time, urllib.request

api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

prompts = [
    ("10", "Blue glowing superconducting device in a physics laboratory, scientific research equipment, photorealistic, ultra detailed, 8K"),
    ("10", "Cryogenic chamber with superconducting circuits inside, blue LED lights, laboratory environment, photorealistic, ultra detailed, 8K"),
    ("10", "Advanced laboratory equipment with blue light emissions, scientific instruments, photorealistic, ultra detailed, 8K"),
]

for num, prompt in prompts:
    filename = f"images/news_20260605_{num}.png"
    body = {"model": "cogview-3-flash", "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]}
    cmd = f'curl -s -X POST "{url}" -H "Authorization: Bearer {api_key}" -H "Content-Type: application/json" -d \'{json.dumps(body)}\''
    print(f"Trying {filename} with prompt: {prompt[:50]}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    try:
        resp = json.loads(result.stdout)
        content_list = resp["choices"][0]["message"]["content"]
        if isinstance(content_list, list):
            url_entry = content_list[0]
            if isinstance(url_entry, dict) and "url" in url_entry:
                img_url = url_entry["url"]
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = response.read()
                    with open(filename, 'wb') as f:
                        f.write(data)
                print(f"  [OK] {filename} ({len(data)} bytes)")
                break
        print(f"  [ERROR] Failed: {result.stdout[:200]}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    time.sleep(3)
else:
    print("All attempts exhausted for image 10")