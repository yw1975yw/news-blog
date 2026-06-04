import subprocess, base64, json, time, os, urllib.request

api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

def gen_and_download(prompt, filename):
    body = {"model": "cogview-3-flash", "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]}
    cmd = f'curl -s -X POST "{url}" -H "Authorization: Bearer {api_key}" -H "Content-Type: application/json" -d \'{json.dumps(body)}\''
    print(f"Retrying {filename}...")
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
                return True
        print(f"  [ERROR] Unexpected: {result.stdout[:300]}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    return False

# Retry 10 and 11 with new prompts
gen_and_download("Glowing blue quantum computing device in a modern research lab, photorealistic, ultra detailed, 8K", "images/news_20260605_10.png")
time.sleep(3)
gen_and_download("Modern tech company tower building with glass facade and blue sky, photorealistic, ultra detailed, 8K", "images/news_20260605_11.png")