#!/usr/bin/env python3
import urllib.request
import urllib.parse
import urllib.error
import os
import time
import json

# Image queries for each news item
image_queries = [
    "Trump Beijing visit 2026 diplomatic meeting",
    "oil tanker Persian Gulf middle east conflict",
    "AI developer coding open source technology",
    "UAE military aircraft middle east war",
    "NVIDIA GPU AI chip technology GTC",
    "China US trade negotiations diplomacy",
    "smart city electric charging station green",
    "basketball game rural village China sports",
    "cloud computing data center Asia technology",
    "Russia Ukraine war conflict news 2026",
    "fusion energy reactor science laboratory",
    "European Parliament AI regulation law",
    "electric car charging station China",
    "China strategy middle east diplomacy",
    "China Germany factory industry 4.0 manufacturing",
    "Mourinho Real Madrid football coach",
    "digital currency central bank global finance",
    "autonomous taxi Beijing China technology",
    "green cargo ship ocean shipping",
    "China moon landing space exploration"
]

output_dir = "/home/swg/.openclaw/workspace/news-blog/images/news-generated"
os.makedirs(output_dir, exist_ok=True)

def download_image(query, filename, retry=2):
    """Download image from Pollinations API"""
    encoded_query = urllib.parse.quote(query)
    url = f"https://image.pollinations.ai/prompt/{encoded_query}?width=800&height=600&nologo=true"
    
    filepath = os.path.join(output_dir, filename)
    
    for attempt in range(retry):
        try:
            print(f"Downloading: {filename} (attempt {attempt+1})")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=90) as response:
                with open(filepath, 'wb') as f:
                    f.write(response.read())
            print(f"  Success: {filename}")
            return True
        except Exception as e:
            print(f"  Failed {filename} (attempt {attempt+1}): {e}")
            if attempt < retry - 1:
                time.sleep(3)
    
    print(f"  ERROR: Failed to download {filename} after {retry} attempts")
    return False

# Download all 20 images
results = []
for i, query in enumerate(image_queries, 1):
    filename = f"news_{i:02d}.png"
    success = download_image(query, filename)
    results.append((filename, success))
    time.sleep(2)  # Rate limiting

# Save results
with open(os.path.join(output_dir, "generation_result.json"), "w") as f:
    json.dump(results, f, indent=2)

print("\n=== Download Results ===")
success_count = sum(1 for _, s in results if s)
print(f"Success: {success_count}/{len(results)}")