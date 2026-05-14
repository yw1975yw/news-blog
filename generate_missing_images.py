#!/usr/bin/env python3
import urllib.request
import urllib.parse
import os
import time
import json

# Image queries - only the ones still needing update (05, 12-20)
# Based on file timestamps, news_01-04,06-11 are new; 05,12-20 need updating
pending_images = {
    5: "green shipping cargo ship clean energy ocean",
    12: "European Parliament AI regulation technology",
    13: "electric car charging station China",
    14: "China diplomacy middle east strategy",
    15: "China Germany factory smart manufacturing",
    16: "Mourinho football coach Real Madrid",
    17: "digital currency blockchain financial technology",
    18: "autonomous taxi self-driving Beijing",
    19: "green shipping container ship ocean ecology",
    20: "space rocket launch moon mission China"
}

output_dir = "/home/swg/.openclaw/workspace/news-blog/images/news-generated"

def download_image(query, filename, retry=2):
    encoded_query = urllib.parse.quote(query)
    url = f"https://image.pollinations.ai/prompt/{encoded_query}?width=800&height=600&nologo=true"
    filepath = os.path.join(output_dir, filename)
    
    for attempt in range(retry):
        try:
            print(f"Downloading: {filename}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120) as response:
                with open(filepath, 'wb') as f:
                    f.write(response.read())
            print(f"  Success: {filename}")
            return True
        except Exception as e:
            print(f"  Failed (attempt {attempt+1}): {e}")
            if attempt < retry - 1:
                time.sleep(3)
    return False

results = {}
for i, query in pending_images.items():
    filename = f"news_{i:02d}.png"
    success = download_image(query, filename)
    results[filename] = success
    time.sleep(2)

# Save results
with open(os.path.join(output_dir, "generation_result2.json"), "w") as f:
    json.dump(results, f, indent=2)

print(f"\nResults: {sum(results.values())}/{len(results)} successful")