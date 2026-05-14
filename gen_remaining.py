#!/usr/bin/env python3
import urllib.request
import urllib.parse
import os
import time

pending = {
    15: "China Germany factory smart manufacturing industry 4.0",
    16: "Mourinho football coach celebration Real Madrid",
    17: "digital currency blockchain banking financial",
    18: "autonomous taxi self-driving car Beijing city",
    19: "green shipping container ship clean ocean transport",
    20: "China lunar spacecraft moon mission space"
}

output_dir = "/home/swg/.openclaw/workspace/news-blog/images/news-generated"

for i, query in pending.items():
    filename = f"news_{i:02d}.png"
    encoded_query = urllib.parse.quote(query)
    url = f"https://image.pollinations.ai/prompt/{encoded_query}?width=800&height=600&nologo=true"
    filepath = os.path.join(output_dir, filename)
    
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=120) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        print(f"  Success!")
    except Exception as e:
        print(f"  Error: {e}")
    
    time.sleep(2)

print("Done!")