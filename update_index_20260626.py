#!/usr/bin/env python3
import json

with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260626.json', 'r', encoding='utf-8') as f:
    news_items = json.load(f)

# Read current index.html
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update date in title and meta
html = html.replace('2026年06月25日', '2026年06月26日')

# Build new news cards HTML
new_cards = ''
for item in news_items:
    news_id = f"{item['id']:02d}"
    card = f'''<article class="news-card" data-tag="{item['tag']}">
    <img class="news-image" src="images/news_20260626_{news_id}.png" alt="{item['title']}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{news_id}</span>
        <h3 class="news-title">{item['title']}</h3>
        <p class="news-summary">{item['summary']}</p>
        <div><span class="tag">{item['tag']}</span></div>
    </div>
</article>'''
    new_cards += card + '\n'

# Find and replace the news grid content
import re

# Find the news grid section
pattern = r'<div class="news-grid" id="newsGrid">.*?</div>\s*</div>\s*<div class="comments-section">'
replacement = f'<div class="news-grid" id="newsGrid">\n{new_cards}</div>\n    </div>\n    <div class="comments-section">'

html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Write updated index.html
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated successfully!")
print(f"Updated {len(news_items)} news cards")