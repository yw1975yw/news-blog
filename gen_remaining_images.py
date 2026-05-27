#!/usr/bin/env python3
"""Generate missing news images for May 26, 2026"""

import os
import urllib.parse
import requests
import time

workdir = "/home/swg/.openclaw/workspace/news-blog"
images_dir = os.path.join(workdir, "images")
os.makedirs(images_dir, exist_ok=True)

prompts = {
    5: "Global cross-border digital payment system, smartphone with currency symbols worldwide, fintech concept, realistic photography 8K",
    6: "NASA Mars probe rocket launching from Cape Canaveral, space exploration, dramatic sky, realistic photography 8K",
    7: "Quantum computing cloud platform, data center with blue lighting, cryogenic cooling, futuristic technology, realistic photography 8K",
    8: "ASEAN summit meeting, Southeast Asian leaders signing digital economy agreement, Jakarta conference, diplomatic, realistic photography 8K",
    9: "Chinese super camera with high resolution lens, billion pixel optical equipment research lab, scientific, realistic photography 8K",
    10: "Ocean plastic cleanup autonomous boat collecting waste from Pacific Ocean, environmental protection, realistic photography 8K",
    11: "Room temperature superconductor material research, laboratory with advanced physics equipment, scientific breakthrough, realistic photography 8K",
    12: "World's longest undersea high speed rail tunnel construction, Japanese engineering project, marine construction, realistic photography 8K",
    13: "International Space Station orbital platform, astronauts conducting life extension upgrade, space station exterior, realistic photography 8K",
    14: "Global digital identity authentication system, biometric security technology, blockchain verification, futuristic, realistic photography 8K",
    15: "Amazon rainforest restoration project, reforestation workers planting trees, carbon sink verification, environmental, realistic photography 8K",
    16: "Brain computer interface technology, blind patient with visual cortex implant, medical breakthrough, neuroscience, realistic photography 8K",
    17: "Blockchain carbon trading platform, cryptocurrency exchange interface, environmental finance technology, realistic photography 8K",
    18: "Antarctic research station under aurora, scientists studying ancient microbial life in ice, polar exploration, realistic photography 8K",
    19: "Global 5G network coverage concept, smartphone signal towers worldwide connection, telecommunications network, realistic photography 8K",
    20: "International Maghreb Canal project, North Africa engineering blueprint, Mediterranean Atlantic connection, realistic photography 8K",
}

def download_image(num, prompt):
    filename = os.path.join(images_dir, f"news_20260526_{num:02d}.png")
    if os.path.exists(filename):
        print(f"Image {num} already exists, skipping")
        return True
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=800&nologo=true"
    
    print(f"Generating image {num}: {prompt[:50]}...")
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200 and len(response.content) > 10000:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  Saved: {filename} ({len(response.content)} bytes)")
            return True
        else:
            print(f"  Failed: status={response.status_code}, size={len(response.content)}")
            return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

success_count = 0
for num, prompt in sorted(prompts.items()):
    if download_image(num, prompt):
        success_count += 1
    time.sleep(2)  # be nice to the server

print(f"\nGenerated {success_count}/{len(prompts)} images")