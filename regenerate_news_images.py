#!/usr/bin/env python3
"""
重新生成新闻配图 - 基于实际新闻内容
"""

import subprocess
import time
import sys
from pathlib import Path
from PIL import Image

from datetime import datetime, timezone, timedelta

tz_beijing = timezone(timedelta(hours=8))
today = datetime.now(tz=tz_beijing).strftime("%Y%m%d")

SKILL_DIR = Path("/home/swg/.openclaw/workspace/skills/nvidia-genai")
POLLINATIONS_SCRIPT = Path("/home/swg/.openclaw/workspace/news-blog/pollinations_generate.py")
OUTPUT_DIR = Path("/home/swg/.openclaw/workspace/news-blog/images/news-generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 实际20条新闻 - 从 index.html 获取
NEWS_IMAGES = [
    {"id": 1, "title": "美军与伊朗在霍尔木兹海峡交火", "prompt_en": "Military naval battle at strategic sea strait, warships exchanging fire, smoke and explosions at sea, military conflict scene, dramatic ocean waves, armed vessels confrontational"},
    {"id": 2, "title": "特朗普否认停火结束", "prompt_en": "Former US president speaking at press conference, denying ceasefire end, serious expression, media cameras, political statement, dramatic lighting"},
    {"id": 3, "title": "沙特科威特解除美军基地限制", "prompt_en": "US military base in Middle East desert, military aircraft on runway, US soldiers, Arabian desert landscape, military installation, strategic partnership"},
    {"id": 4, "title": "美伊局势影响美股油价", "prompt_en": "Stock market trading floor with declining graphs, oil barrel price chart, economic crisis concept, traders looking worried, oil refinery background, financial turbulence"},
    {"id": 5, "title": "美国众议院推出法案禁止中国汽车", "prompt_en": "US Capitol building, congressional chamber, politicians voting, Chinese electric vehicles blocked at border, legislative process, government policy"},
    {"id": 6, "title": "美国与伊朗间接谈判继续", "prompt_en": "Diplomatic negotiation table, US and Iran flags, mediators in middle, serious diplomatic discussion, international diplomacy, negotiation room"},
    {"id": 7, "title": "第二十八届北京科博会开幕", "prompt_en": "International technology expo in Beijing, grand exhibition hall, tech companies booths, futuristic displays, Beijing skyline background, technology exhibition"},
    {"id": 8, "title": "北京科博会设六大专题展区", "prompt_en": "Large tech exhibition with multiple themed zones, visitors walking through booths, holographic displays, various technology showcases, organized exhibition floor"},
    {"id": 9, "title": "一季度工业增加值同比增长6.1%", "prompt_en": "Modern factory with industrial robots, manufacturing data charts showing growth, industrial production increase, automation assembly line, economic growth visualization"},
    {"id": 10, "title": "政府工作报告聚焦科技创新", "prompt_en": "Government building with Chinese flag, officials presenting work report, technology innovation themes displayed, policy presentation scene, official ceremony"},
    {"id": 11, "title": "国防部宣布军事技术突破", "prompt_en": "Advanced military technology displayed, stealth fighter jet, missile defense system, defense exhibition, breakthrough technology showcase, military modernization"},
    {"id": 12, "title": "中美经贸高层会谈启动", "prompt_en": "US and China flags side by side, trade negotiation table, economic ministers meeting, bilateral trade discussion, international trade talks"},
    {"id": 13, "title": "欧盟对华投资再创新高", "prompt_en": "European Union headquarters in Brussels, investment growth chart, European and Chinese business leaders shaking hands, trade partnership, investment cooperation"},
    {"id": 14, "title": "全球AI监管框架加速形成", "prompt_en": "AI robot with regulation shield, global network of connected devices, AI governance concept, international standards organization, digital regulation"},
    {"id": 15, "title": "量子通信试验卫星发射成功", "prompt_en": "Quantum satellite launching on rocket, space mission at night, quantum communication waves visualization, satellite in orbit, space exploration technology"},
    {"id": 16, "title": "深海油气勘探取得重大发现", "prompt_en": "Deep sea oil rig platform, underwater oil reservoir visualization, offshore drilling in ocean, energy exploration, deep sea equipment, oil discovery"},
    {"id": 17, "title": "国际刑事法院发布调查令", "prompt_en": "International criminal court building in The Hague, legal scales of justice, court documents, international law enforcement, judicial proceedings"},
    {"id": 18, "title": "全球半导体产能持续扩张", "prompt_en": "Semiconductor chip factory interior, clean room with workers in suits, silicon wafer production, chip manufacturing, high-tech electronics"},
    {"id": 19, "title": "联合国安理会召开紧急会议", "prompt_en": "UN Security Council chamber, diplomats from different nations, emergency meeting in session, international conflict discussion, UN headquarters"},
    {"id": 20, "title": "国际能源署发布展望报告", "prompt_en": "International Energy Agency headquarters, global energy outlook report, world map with energy infrastructure, renewable and fossil energy visualization, energy policy report"},
]

def generate_with_pollinations(news_id, prompt_en, title):
    """使用 Pollinations 生成图片"""
    output_file = OUTPUT_DIR / f"news_{today}_{news_id:02d}.png"
    
    print(f"[{news_id:02d}] 重新生成: {title}")
    print(f"     Prompt: {prompt_en[:60]}...")
    
    cmd = [
        "python3",
        str(POLLINATIONS_SCRIPT),
        prompt_en,
        "--output", str(output_file),
        "--width", "800",
        "--height", "450",
        "--model", "turbo",
        "--nologo",
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
        )
        
        if result.returncode == 0 and output_file.exists():
            size = output_file.stat().st_size / 1024
            print(f"  ✅ 成功 ({size:.0f}KB)")
            
            # 验证是真正的 PNG
            try:
                with Image.open(output_file) as img:
                    if img.format != 'PNG' or img.mode not in ('RGB', 'RGBA'):
                        print(f"  ⚠️ 格式验证失败: {img.format} {img.mode}")
                        return False
            except Exception as e:
                print(f"  ⚠️ 图片验证失败: {e}")
                return False
            
            return True
        else:
            print(f"  ❌ 失败: {result.stderr[:200] if result.stderr else 'Unknown error'}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ❌ 超时")
        return False
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        return False

if __name__ == "__main__":
    print(f"开始重新生成 {len(NEWS_IMAGES)} 张新闻配图...")
    print(f"每张间隔 60 秒避免限流，总耗时约 {len(NEWS_IMAGES)} 分钟\n")
    
    success = 0
    failed = []
    
    for i, news in enumerate(NEWS_IMAGES):
        print(f"[{i+1}/{len(NEWS_IMAGES)}]")
        if generate_with_pollinations(news["id"], news["prompt_en"], news["title"]):
            success += 1
        else:
            failed.append(news["id"])
        
        # 每张间隔60秒避免限流
        if i < len(NEWS_IMAGES) - 1:
            print(f"  等待 60 秒...")
            time.sleep(60)
    
    print(f"\n完成！成功 {success}/{len(NEWS_IMAGES)}")
    if failed:
        print(f"失败: {failed}")