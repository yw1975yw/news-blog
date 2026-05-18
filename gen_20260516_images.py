#!/usr/bin/env python3
"""
为20260516新闻生成20张高清写实配图
"""
import urllib.request
import urllib.parse
import os
import time
import json
from datetime import datetime, timezone, timedelta

tz_beijing = timezone(timedelta(hours=8))
today = datetime.now(tz=tz_beijing).strftime("%Y%m%d")

OUTPUT_DIR = "/home/swg/.openclaw/workspace/news-blog/images/news-generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 20260516新闻配图prompt（按顺序）
NEWS_PROMPTS = [
    ("01", "Xi Jinping and Trump meeting at Great Hall of the People Beijing, bilateral summit diplomatic talks, Chinese and American flags, official government ceremony, realistic news photography, photojournalism style"),
    ("02", "President Putin visiting China, Kremlin palace architecture background, China-Russia bilateral meeting, diplomatic handshake, realistic news photography, Kremlin press photo style"),
    ("03", "US Secretary of State Rubio visiting China, diplomatic meeting with Chinese Foreign Minister, official reception, US China diplomatic relations, news photojournalism"),
    ("04", "Chinese AI technology DeepSeek, large language model interface on computer screen, Chinese tech company office, artificial intelligence research, realistic tech photography"),
    ("05", "Beijing-Shanghai high-speed railway G-train at railway station, Chinese high-speed rail, ticket counter display showing price increase, realistic transportation photography"),
    ("06", "Evergrande Group founder Xu Jiayin trial at Shenzhen court, court building exterior, Chinese real estate scandal, financial crime news photography"),
    ("07", "International Museum Day celebration in China, crowded museum interior with ancient artifacts, visitors viewing Chinese cultural relics, National Museum China, cultural photography"),
    ("08", "Heavy rainfall and flooding in central eastern China, flooded streets, people with umbrellas, storm weather, heavy rain on city, realistic weather news photography"),
    ("09", "Liberia foreign minister visiting China, diplomatic meeting with Chinese officials, China Africa cooperation, Beijing diplomatic venue, official news photography"),
    ("10", "Solomon Islands new prime minister election, Pacific island nation parliament building, Oceania political news, South Pacific island scenery, realistic documentary photography"),
    ("11", "Chinese stock market A-shares trading floor, stock exchange LED board showing rising numbers, bull market rally, tech stocks up, financial news photography"),
    ("12", "Deepwater oil gas equipment manufacturing facility in China, offshore oil platform, deep sea oil drilling equipment, industrial manufacturing, realistic industrial photography"),
    ("13", "OpenAI CEO Sam Altman testifying before US Congress, Senate hearing room, tech regulation, AI company investigation, US Capitol building, news photography"),
    ("14", "China Tianzhou-10 cargo spacecraft launch, rocket launching at Wenchang spaceport, Long March rocket space launch, Chinese space station, realistic space photography"),
    ("15", "Chinese smart appliance brand Dreame signing Cristiano Ronaldo as brand ambassador, product launch event, famous football star, brand endorsement deal, celebrity photography"),
    ("16", "Memory chip semiconductor factory clean room, chip manufacturing in China, AI server memory chips, tech industry production line, realistic industrial photography"),
    ("17", "Chinese fintech company stock market surge, Tonghuashun financial app on phone, stock trading app interface, fintech mobile application, financial technology photography"),
    ("18", "Samsung Electronics withdrawing from Chinese home appliance market, empty electronics store shelf, Korean company exit from China, retail store closing, realistic retail photography"),
    ("19", "Hong Kong embodied AI industry summit, tech conference in Hong Kong, robotics and AI research presentations, Hong Kong convention center, tech industry photography"),
    ("20", "Chinese tech stocks bull market, AI computing power demand, fund manager analyzing stock data, financial district office, stock market investment, realistic financial photography"),
]

def generate_image(idx, prompt_text):
    """使用 Pollinations 生成高清图片"""
    filename = f"news_20260516_{idx}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    encoded_prompt = urllib.parse.quote(prompt_text)
    # 高清参数：1024x576 (16:9), 高质量
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&model=flux"
    
    print(f"[{idx}] 生成中: {prompt_text[:60]}...")
    
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=180) as response:
                data = response.read()
            
            with open(filepath, 'wb') as f:
                f.write(data)
            
            size = os.path.getsize(filepath) / 1024
            print(f"  ✅ [{idx}] 成功 ({size:.0f}KB) - {filename}")
            return True
        except Exception as e:
            print(f"  ❌ [{idx}] 失败 (attempt {attempt+1}): {e}")
            if attempt < 2:
                time.sleep(15)
    
    print(f"  ❌ [{idx}] 最终失败")
    return False

if __name__ == "__main__":
    print(f"开始生成 20260516 新闻配图，共{len(NEWS_PROMPTS)}张")
    print(f"每张间隔60秒避免限流，预计耗时约{len(NEWS_PROMPTS)}分钟\n")
    
    success = 0
    failed = []
    
    for i, (idx, prompt) in enumerate(NEWS_PROMPTS):
        print(f"[{i+1}/{len(NEWS_PROMPTS)}]")
        if generate_image(idx, prompt):
            success += 1
        else:
            failed.append(idx)
        
        # 每张间隔60秒（限流保护）
        if i < len(NEWS_PROMPTS) - 1:
            print(f"  等待 60 秒...")
            time.sleep(60)
    
    print(f"\n完成！成功 {success}/{len(NEWS_PROMPTS)}")
    if failed:
        print(f"失败: {failed}")
    
    # 保存结果
    result = {
        "date": "20260516",
        "total": len(NEWS_PROMPTS),
        "success": success,
        "failed": failed
    }
    with open(os.path.join(OUTPUT_DIR, "gen_20260516_result.json"), "w") as f:
        json.dump(result, f, indent=2)