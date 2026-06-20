#!/usr/bin/env python3
import json

# Load news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260621.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

news_items = data['news']
today_date = data['date']
date_short = data['date_short']
year = date_short[:4]
month = date_short[4:6]
date_formatted = f"{year}年{month}月{date_short[6:]}日"

# Read original index.html
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build new news cards HTML
new_cards = []
for item in news_items:
    card = f'''<article class="news-card" data-tag="{item["tag"]}">
    <img class="news-image" src="images/news_{date_short}_{item["number"]}.png" alt="{item["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{item["number"]}</span>
        <h3 class="news-title">{item["title"]}</h3>
        <p class="news-summary">{item["summary"]}</p>
        <div><span class="tag">{item["tag"]}</span></div>
    </div>
</article>'''
    new_cards.append(card)

new_cards_html = '\n'.join(new_cards)

# Replace title and date
html = html.replace(
    '<title>全球20条热点新闻 · 2026年06月20日 | 环球新闻</title>',
    f'<title>全球20条热点新闻 · {date_formatted} | 环球新闻</title>'
)
html = html.replace(
    '<meta name="description" content="2026年06月20日全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">',
    f'<meta name="description" content="{date_formatted}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">'
)

# Replace subtitle
html = html.replace(
    '<p class="cover-subtitle">全球20条热点新闻 · 2026年06月20日</p>',
    f'<p class="cover-subtitle">全球20条热点新闻 · {date_formatted}</p>'
)

# Replace footer date
html = html.replace(
    '<p style="margin-top:10px;font-size:0.9em;">所有新闻内容仅供参考，请以官方发布为准 · 2026年06月20日</p>',
    f'<p style="margin-top:10px;font-size:0.9em;">所有新闻内容仅供参考，请以官方发布为准 · {date_formatted}</p>'
)

# Replace news grid content (between news-grid div)
start_marker = '<div class="news-grid" id="newsGrid">'
end_marker = '</div>\n            </div>\n            <div class="comments-section">'

start_idx = html.find(start_marker) + len(start_marker)
end_idx = html.find(end_marker)

html = html[:start_idx] + '\n' + new_cards_html + '\n' + html[end_idx:]

# Write updated index.html
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Updated index.html with {len(news_items)} news items for {date_formatted}")
print(f"Date: {today_date}")