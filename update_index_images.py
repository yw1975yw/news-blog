#!/usr/bin/env python3
import re

# 读取 index.html
with open('index.html', 'r') as f:
    content = f.read()

# 找到所有 news-card 中的 <img src="images/news_default.png" ...>
# 替换为 news-generated/news_XX.png
counter = 1
def replace_default_img(m):
    global counter
    result = m.group(0).replace('images/news_default.png', f'images/news-generated/news_{counter:02d}.png')
    counter += 1
    return result

new_content = re.sub(r'<img src="images/news_default\.png"[^>]*>', replace_default_img, content)

# 统计替换了多少
original_count = len(re.findall(r'images/news_default\.png', content))
new_count = len(re.findall(r'images/news-generated/news_\d+\.png', new_content))
print(f"替换了 {original_count} -> {new_count} 张图片")

# 写回
with open('index.html', 'w') as f:
    f.write(new_content)

print("index.html 已更新")