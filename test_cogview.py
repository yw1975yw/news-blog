#!/usr/bin/env python3
"""Test CogView-3-Flash API with a single image."""

import json
import base64
import urllib.request
import time
import os

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

prompt = "A futuristic technology conference stage with a giant holographic display showing neural network visualization, photorealistic, ultra detailed, 8K, high resolution, dramatic lighting, tech keynote setting"

print("Testing CogView-3-Flash API...")
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

start = time.time()
try:
    with urllib.request.urlopen(req, timeout=90) as resp:
        elapsed = time.time() - start
        result = json.loads(resp.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"]
        print(f"Response received in {elapsed:.1f}s")
        print(f"Content length: {len(content)}")
        print(f"Content preview: {content[:200]}")
        
        # Extract base64
        if "data:image" in content:
            b64_data = content.split("data:image/png;base64,")[1]
        else:
            b64_data = content
        
        img_data = base64.b64decode(b64_data)
        output_path = "/home/swg/.openclaw/workspace/news-blog/images/test_cogview.png"
        with open(output_path, "wb") as f:
            f.write(img_data)
        print(f"Saved to: {output_path}, size: {len(img_data)} bytes")
except Exception as e:
    elapsed = time.time() - start
    print(f"Failed after {elapsed:.1f}s: {e}")