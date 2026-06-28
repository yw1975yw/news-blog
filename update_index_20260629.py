#!/usr/bin/env python3
"""Update index.html with news for 2026年06月29日"""

import json
import re

DATE = "20260629"
DISPLAY_DATE = "2026年06月29日"

# Read news data
with open(f"/home/swg/.openclaw/workspace/news-blog/news_data_{DATE}.json", 'r', encoding='utf-8') as f:
    news_data = json.load(f)

# Read index.html
with open("/home/swg/.openclaw/workspace/news-blog/index.html", 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace title date
html = re.sub(r'<title>.*?环球新闻</title>', f'<title>{DISPLAY_DATE} 环球新闻</title>', html)

# 2. Replace meta description date
html = re.sub(r'<meta name="description" content=".*?">', 
              f'<meta name="description" content="{DISPLAY_DATE}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">', html)

# 3. Replace cover subtitle
html = re.sub(r'<p class="cover-subtitle">.*?</p>', 
              f'<p class="cover-subtitle">全球20条热点新闻 · {DISPLAY_DATE}</p>', html)

# 4. Find and replace the news grid content
# Pattern to match the news-grid div content (from <div class="news-grid" id="newsGrid"> to </div>)
# We need to replace all 20 news cards

news_cards = ""
for news in news_data:
    img_num = news["number"].zfill(2)
    card = f'''<article class="news-card" data-tag="{news["tag"]}">
    <img class="news-image" src="images/news_{DATE}_{img_num}.png" alt="{news["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{news["number"]}</span>
        <h3 class="news-title">{news["title"]}</h3>
        <p class="news-summary">{news["summary"]}</p>
        <div><span class="tag">{news["tag"]}</span></div>
    </div>
</article>
'''
    news_cards += card

# Find the news-grid section and replace it
pattern = r'<div class="news-grid" id="newsGrid">.*?</div>\s*</div>\s*</article>'
replacement = f'<div class="news-grid" id="newsGrid">\n{news_cards}</div>\n        </div>'
html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Write updated index.html
with open("/home/swg/.openclaw/workspace/news-blog/index.html", 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ Updated index.html with {len(news_data)} news cards for {DISPLAY_DATE}")