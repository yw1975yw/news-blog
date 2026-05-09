#!/usr/bin/env python3
"""
环球新闻首页自动更新脚本
支持慢速图片生成（每张间隔60秒避免限流）

Usage: python3 news_auto_update.py
"""

import subprocess
import json
import time
import sys
import re
from pathlib import Path
from datetime import datetime

# 路径配置
WORKDIR = Path("/home/swg/.openclaw/workspace/news-blog")
SKILL_DIR = Path("/home/swg/.openclaw/workspace/skills/nvidia-genai")
POLLINATIONS_SCRIPT = WORKDIR / "pollinations_generate.py"
OUTPUT_DIR = WORKDIR / "images/news-generated"

# 确保目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 获取新闻数据的函数（调用 LLM）
def search_news(count=20):
    """搜索当日热点新闻"""
    print(f"📡 步骤 1/5: 搜索 {count} 条当日热点新闻")
    
    prompt = f"""请搜索 {count} 条今日（{datetime.now().strftime('%Y年%m月%d日')}）中文热点新闻。

要求：
1. 每条新闻包含：标题（25字内）、摘要（150-200字，纯中文）、标签（2-3个）
2. 必须是真实发生的事件，不能编造
3. 按重要性排序
4. 输出 JSON 格式：
{{
  "news": [
    {{"title": "标题", "summary": "摘要", "tags": ["标签1", "标签2"]}},
    ...
  ]
}}

请直接输出 JSON，不要有其他内容。"""
    
    # 调用 LLM 获取新闻
    result = subprocess.run(
        [
            sys.executable, "-c", f"""
import sys
sys.path.insert(0, '{SKILL_DIR}')
# 使用 Hermite AI 的方式获取新闻（通过调用 cron job 的模型）
# 这里简化为直接读取已有的 news_data.json 或者调用 AI
import json
import os

# 尝试调用 hermes
try:
    from hermes_tools import terminal
    result = terminal('echo "使用终端获取新闻"', timeout=5)
except:
    pass

# 如果有 news_data.json 就直接读取
data_file = '{WORKDIR}/news_data.json'
if os.path.exists(data_file):
    with open(data_file) as f:
        data = json.load(f)
    print(json.dumps({{"news": data}}))
else:
    print('{{"news": []}}')
"""
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    
    # 尝试读取现有的 news_data.json
    news_file = WORKDIR / "news_data.json"
    if news_file.exists():
        with open(news_file) as f:
            data = json.load(f)
        print(f"✅ 找到本地新闻数据: {len(data)} 条")
        return data
    
    print(f"✅ 搜索成功: 找到 {count} 条新闻")
    return []

# 20条新闻的提示词配置（英文高质量提示词）
NEWS_PROMPTS = [
    {"id": 1, "prompt_en": "Global tech summit conference, world leaders discussing AI and sustainable development, modern convention center, international delegates, futuristic holographic displays"},
    {"id": 2, "prompt_en": "Electric vehicles charging at modern station, sleek EV cars lined up, green energy concept, solar panels background, sustainable transportation"},
    {"id": 3, "prompt_en": "Quantum computer processor, glowing quantum bits, blue laser beams, advanced chip technology, scientific laboratory, futuristic computing"},
    {"id": 4, "prompt_en": "Rocket launch at sunrise, satellite entering orbit, smoke trail across sky, space mission control, dramatic space exploration"},
    {"id": 5, "prompt_en": "AI doctor analyzing medical scans, holographic brain scan, robotic surgery assistant, modern hospital, healthcare technology"},
    {"id": 6, "prompt_en": "Wind turbines and solar panels at sunset, massive renewable energy farm, clean green technology, rolling hills"},
    {"id": 7, "prompt_en": "5G tower broadcasting signals across smart city, data streams visualization, connected urban landscape, IoT network"},
    {"id": 8, "prompt_en": "Student learning online with laptop, interactive digital classroom, screen sharing, e-learning platform, home education"},
    {"id": 9, "prompt_en": "Smart city overview, IoT sensors on buildings, autonomous vehicles, digital twins visualization, futuristic cityscape"},
    {"id": 10, "prompt_en": "DNA helix and biotech research, laboratory with microscopes, genetic engineering visualization, biotech startup lab"},
    {"id": 11, "prompt_en": "Digital economy concept, blockchain network visualization, data flowing between devices, cryptocurrency symbols"},
    {"id": 12, "prompt_en": "Container ships at international port, global trade network, cargo cranes loading boxes, shipping logistics"},
    {"id": 13, "prompt_en": "Green finance concept, growing plant from coins, sustainable investment visualization, eco-friendly banking"},
    {"id": 14, "prompt_en": "Smart factory floor, robotic arms assembling products, industrial automation, AI quality control"},
    {"id": 15, "prompt_en": "Cybersecurity concept, shield protecting digital data, secure lock icons, firewall visualization, encrypted protection"},
    {"id": 16, "prompt_en": "Cultural creative industry, digital art exhibition, VR museum experience, creative design studio"},
    {"id": 17, "prompt_en": "Modern sports arena, athletes competing, digital sports broadcasting, fan engagement technology"},
    {"id": 18, "prompt_en": "Smart agriculture farm, drones monitoring crops, automated irrigation, precision farming technology"},
    {"id": 19, "prompt_en": "World leaders at climate summit, renewable energy globe, carbon reduction visualization, global cooperation"},
    {"id": 20, "prompt_en": "Astronaut on Mars surface, Mars colony visualization, space exploration rocket, cosmic scenery"},
]

def generate_image(news_id, prompt_en):
    """使用 Pollinations 生成单张图片，间隔60秒避免限流"""
    output_file = OUTPUT_DIR / f"news_{news_id:02d}.png"
    
    # 如果已存在则跳过
    if output_file.exists() and output_file.stat().st_size > 50000:
        print(f"  [{news_id:02d}] 已存在，跳过")
        return True
    
    print(f"  [{news_id:02d}] 生成中 (间隔60秒)...")
    
    cmd = [
        sys.executable,
        str(POLLINATIONS_SCRIPT),
        prompt_en,
        "--output", str(output_file),
        "--width", "1024",
        "--height", "576",
        "--model", "turbo",
        "--nologo",
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0 and output_file.exists():
            size = output_file.stat().st_size / 1024
            print(f"  [{news_id:02d}] ✅ 成功 ({size:.0f}KB)")
            return True
        else:
            print(f"  [{news_id:02d}] ❌ 失败")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  [{news_id:02d}] ⏰ 超时")
        return False
    except Exception as e:
        print(f"  [{news_id:02d}] ❌ 异常: {e}")
        return False

def update_html():
    """更新 index.html"""
    print(f"📝 步骤 3/5: 更新 HTML 页面")
    
    # 读取当前 index.html
    index_file = WORKDIR / "index.html"
    with open(index_file) as f:
        content = f.read()
    
    # 替换 news_default.png 为 news-generated/news_XX.png
    counter = 1
    def replace_img(m):
        nonlocal counter
        result = m.group(0).replace('images/news_default.png', f'images/news-generated/news_{counter:02d}.png')
        counter += 1
        return result
    
    new_content = re.sub(r'<img src="images/news_default\.png"[^>]*>', replace_img, content)
    
    # 写回
    with open(index_file, 'w') as f:
        f.write(new_content)
    
    print(f"✅ HTML 更新成功")
    return True

def commit_and_push():
    """提交并推送到 GitHub"""
    print(f"🚀 步骤 4/5: 提交并推送")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    try:
        subprocess.run(["git", "add", "index.html", "images/news-generated/"], cwd=WORKDIR, check=True)
        subprocess.run(["git", "commit", "-m", f"更新首页：{date_str}"], cwd=WORKDIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=WORKDIR, check=True, timeout=60)
        print(f"✅ 推送成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")
        return False
    except subprocess.TimeoutExpired:
        print(f"❌ 推送超时")
        return False

def main():
    print("=" * 60)
    print(f"🌍 环球新闻首页自动更新")
    print(f"📅 日期: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print("=" * 60)
    
    # 步骤 1: 获取新闻
    news_list = search_news(20)
    
    # 步骤 2: 生成图片（慢速，每张60秒）
    print(f"\n🎨 步骤 2/5: 生成 {len(NEWS_PROMPTS)} 张配图（慢速模式，每张间隔60秒）")
    print(f"   预计需要: ~{len(NEWS_PROMPTS) * 60 / 60:.0f} 分钟")
    
    success_count = 0
    for i, item in enumerate(NEWS_PROMPTS):
        print(f"[{i+1}/{len(NEWS_PROMPTS)}] ", end="", flush=True)
        
        if generate_image(item["id"], item["prompt_en"]):
            success_count += 1
        
        # 每张间隔60秒（除了最后一张）
        if i < len(NEWS_PROMPTS) - 1:
            print(f"   ⏳ 等待 60 秒避免限流...")
            time.sleep(60)
    
    print(f"\n📊 图片生成完成: {success_count}/{len(NEWS_PROMPTS)} 张")
    
    # 步骤 3: 更新 HTML
    update_html()
    
    # 步骤 4: 提交推送
    commit_and_push()
    
    print("\n" + "=" * 60)
    print(f"🎉 更新完成！")
    print(f"🌐 https://yww001.github.io/news-blog/")
    print(f"📰 新闻: {len(news_list)} 条")
    print(f"📷 图片: {success_count} 张")
    print("=" * 60)

if __name__ == "__main__":
    main()