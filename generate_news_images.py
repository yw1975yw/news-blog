#!/usr/bin/env python3
"""
为环球新闻首页生成20张配图
使用 Pollinations AI，每张图间隔60秒避免限流

Usage:
    python3 generate_news_images.py
"""

import json
import time
import sys
from pathlib import Path

# 添加 nvidia-genai skill 路径
sys.path.insert(0, '/home/swg/.openclaw/workspace/skills/nvidia-genai')
from pollinations_generate import generate_image

NEWS_BLOG_DIR = Path('/home/swg/.openclaw/workspace/news-blog')
IMAGES_DIR = NEWS_BLOG_DIR / 'images'
NEWS_DATA = NEWS_BLOG_DIR / 'news_data.json'

# 新闻标题到提示词的映射（英文，因为 Pollinations 对英文支持更好）
PROMPTS = {
    1: "A bull statue on a stock exchange floor, Asian financial district background, green arrows showing growth, modern skyscraper skyline, professional photography, 16:9",
    2: "Chinese government building with flags, trade barriers concept, shipping containers, international commerce, serious atmosphere, 16:9",
    3: "Data visualization screens showing cybersecurity, digital infrastructure, binary code background, warning symbols, futuristic technology, 16:9",
    4: "Technology innovation concept, semiconductor chips on world map, Chinese research lab, blue technology aesthetic, 16:9",
    5: "Persian Gulf strait map, oil tankers, geopolitical tension, economic charts, blue ocean water, 16:9",
    6: "Taiwan strait map with military vessels, geopolitical tension, Asian Pacific region, serious news atmosphere, 16:9",
    7: "High-quality development conference, Chinese economic forum, business leaders meeting, professional setting, 16:9",
    8: "Multiple government departments united for tech innovation, scientists in lab, breakthrough research, blue background, 16:9",
    9: "China five-year plan roadmap, technology superpower concept, satellite and AI imagery, strategic planning, 16:9",
    10: "High-tech development achievement, smartphone and chip technology, Chinese innovation, modern factory, 16:9",
    11: "Semiconductor factory clean room, chip manufacturing, Silicon wafer production, technological precision, 16:9",
    12: "AI chips competition, neural network visualization, tech giants rivalry, futuristic circuit board, 16:9",
    13: "Deep learning AI model visualization, semiconductor stock market surge, trading screens showing growth, 16:9",
    14: "AI chip design system concept, automated design tools, computer circuitry, innovative technology, 16:9",
    15: "Tech stock market analysis, PCB circuit boards, growth charts, technology sector performance, 16:9",
    16: "AI artificial intelligence era, semiconductor revolution, digital transformation, futuristic technology, 16:9",
    17: "Applied Materials company logo with stock growth chart, semiconductor equipment, dramatic price increase, 16:9",
    18: "Semiconductor equipment manufacturing, precision machinery, historical opportunity concept, industrial technology, 16:9",
    19: "South Korea semiconductor export growth, memory chips and data centers, dramatic increase visualization, 16:9",
    20: "Chinese domestic semiconductor chip production, self-sufficient technology, national champions, innovation, 16:9",
}

def main():
    # 确保图片目录存在
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    # 读取新闻数据
    with open(NEWS_DATA) as f:
        news_list = json.load(f)
    
    print(f"📰 共 {len(news_list)} 条新闻，开始生成配图...")
    print(f"⏱️  每张图间隔 60 秒避免限流，预计需要 ~{len(news_list)} 分钟")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    for i, news in enumerate(news_list):
        idx = i + 1
        title = news.get('title', f'News {idx}')
        output_file = IMAGES_DIR / f"news_{idx:02d}.png"
        
        prompt = PROMPTS.get(idx, f"Breaking news, {title}, professional journalism, 16:9")
        
        print(f"\n[{idx}/20] {title[:40]}...")
        print(f"   提示词: {prompt[:50]}...")
        
        try:
            success = generate_image(
                prompt=prompt,
                output_path=str(output_file),
                width=1344,
                height=756,  # 16:9
                seed=idx * 100,  # 每条新闻不同 seed
                nologo=True
            )
            
            if success:
                success_count += 1
                print(f"   ✅ 已保存: {output_file}")
            else:
                fail_count += 1
                print(f"   ❌ 生成失败")
        
        except Exception as e:
            fail_count += 1
            print(f"   ❌ 错误: {e}")
        
        # 每张图间隔 60 秒（除了最后一张）
        if idx < 20:
            print(f"   ⏳ 等待 60 秒避免限流...")
            time.sleep(60)
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！成功 {success_count} 张，失败 {fail_count} 张")
    
    if success_count > 0:
        print(f"\n📁 图片位置: {IMAGES_DIR}")
        for i in range(1, 21):
            p = IMAGES_DIR / f"news_{i:02d}.png"
            if p.exists():
                size_kb = p.stat().st_size / 1024
                print(f"   {i:02d}. {p.name} ({size_kb:.0f} KB)")

if __name__ == "__main__":
    main()