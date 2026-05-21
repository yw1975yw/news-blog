#!/usr/bin/env python3
"""修复 index.html 的图片日期和内容更新"""
import os
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

BLOG_PATH = Path("/home/swg/.openclaw/workspace/news-blog")
IMAGES_DIR = BLOG_PATH / "images" / "news-generated"
index_file = BLOG_PATH / "index.html"

today = datetime.now(timezone(timedelta(hours=8)))
today_str = today.strftime("%Y%m%d")
date_display = today.strftime("%Y年%m月%d日")

print(f"今日日期: {date_display}")

# 读取 index.html
with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 更新封面日期
html = re.sub(
    r'<p class="cover-subtitle">全球20条热点新闻 · \d{4}年\d{2}月\d{2}日</p>',
    f'<p class="cover-subtitle">全球20条热点新闻 · {date_display}</p>',
    html
)

# 2. 更新页面标题
html = re.sub(
    r'<title>全球20条热点新闻 - \d{4}年\d{2}月\d{2}日',
    f'<title>全球20条热点新闻 - {date_display}',
    html
)

# 3. 更新 meta description
html = re.sub(
    r'<meta name="description" content="\d{4}年\d{2}月\d{2}日全球20条热点新闻',
    f'<meta name="description" content="{date_display}全球20条热点新闻',
    html
)

# 4. 更新 footer 日期
html = re.sub(
    r'所有新闻内容仅供参考，请以官方发布为准 · \d{4}年\d{2}月\d{2}日',
    f'所有新闻内容仅供参考，请以官方发布为准 · {date_display}',
    html
)

# 5. 更新新闻卡片的图片路径
# 找到 news-grid div 并替换其中的所有图片路径
# 格式: images/news-generated/news_YYYYMMDD_NN.png
# 新格式: images/news-generated/news_20260521_NN.png

def replace_image_path(match):
    old_name = match.group(1)  # e.g., "news_20260520_01"
    new_name = f"news_{today_str}_{old_name.split('_')[-1]}"  # e.g., "news_20260521_01"
    return f'src="images/news-generated/{new_name}.png"'

html = re.sub(
    r'src="images/news-generated/(news_\d{8}_\d{2})\.png"',
    replace_image_path,
    html
)

# 验证更新
old_refs = re.findall(r'news_20260520_\d{2}\.png', html)
print(f"剩余旧图片引用: {len(old_refs)}")

new_refs = re.findall(fr'news_{today_str}_\d{{2}}\.png', html)
print(f"新图片引用: {len(new_refs)}")

# 验证新闻卡片数量
card_count = html.count('class="news-card"')
print(f"新闻卡片数量: {card_count}")

# 写入
with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ index.html 已更新")

# 验证图片文件存在
missing = []
for i in range(1, 21):
    img_path = IMAGES_DIR / f"news_{today_str}_{i:02d}.png"
    if not img_path.exists():
        missing.append(f"news_{today_str}_{i:02d}.png")

if missing:
    print(f"⚠️  缺失图片: {missing[:5]}")
else:
    print(f"✅ 所有 20 张图片已就位")