#!/usr/bin/env python3
"""Generate 20 news images using CogView-3-Flash API for 2026年06月24日"""
import subprocess
import json
import os
import time
import base64

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

news_data = [
    {"id": "01", "title": "G7峰会在意大利索伦托开幕 聚焦AI监管与气候融资", "tag": "国际",
     "prompt": "G7 summit conference venue in Sorrento Italy Mediterranean coastal hotel with world leaders meeting photorealistic ultra detailed 8K"},
    {"id": "02", "title": "中欧举行峰会 双方签署共同应对气候变化联合声明", "tag": "国际",
     "prompt": "China EU summit meeting in Brussels elegant conference hall with Chinese and European flags bilateral talks photorealistic ultra detailed 8K"},
    {"id": "03", "title": "苹果发布Apple Intelligence 2.0 搭载自研AI芯片M5", "tag": "科技",
     "prompt": "Apple keynote event at Apple Park new iPhone and AI chip M5 revealed dramatic stage lighting photorealistic ultra detailed 8K"},
    {"id": "04", "title": "谷歌发布Gemini 3.0 Ultra 号称AGI实现重大突破", "tag": "科技",
     "prompt": "Google headquarters in Mountain View Gemini AI brain visualization conference keynote photorealistic ultra detailed 8K"},
    {"id": "05", "title": "中国成功发射天宫空间站扩展舱 首次实现太空制造", "tag": "科技",
     "prompt": "Chinese space station Tiangong in orbit with new expanded module astronauts performing spacewalk photorealistic ultra detailed 8K"},
    {"id": "06", "title": "SpaceX星舰完成首次商业任务 成功部署120颗卫星", "tag": "科技",
     "prompt": "SpaceX Starship launching from Boca Chica Texas rocket trail at sunset satellite deployment in space photorealistic ultra detailed 8K"},
    {"id": "07", "title": "央行降准0.5个百分点 释放长期资金约1万亿元", "tag": "金融",
     "prompt": "People's Bank of China headquarters in Beijing central bank governor press conference monetary policy announcement photorealistic ultra detailed 8K"},
    {"id": "08", "title": "A股三大指数集体上涨 成交额突破2万亿元", "tag": "金融",
     "prompt": "Shanghai Stock Exchange trading floor with stock tickers rising bullish market sentiment investors celebrating photorealistic ultra detailed 8K"},
    {"id": "09", "title": "国际金价再创新高 突破每盎司2800美元", "tag": "金融",
     "prompt": "Gold bars and gold coins arranged in vault gold price chart hitting new highs trading screens photorealistic ultra detailed 8K"},
    {"id": "10", "title": "中国数字人民币跨境支付系统上线 覆盖50个国家", "tag": "金融",
     "prompt": "Digital yuan cross-border payment system interface globe showing international transactions Chinese payment technology photorealistic ultra detailed 8K"},
    {"id": "11", "title": "全国多地高温预警 电网负荷创历史新高", "tag": "社会",
     "prompt": "Heat wave in Chinese city power transmission towers high voltage lines workers in protective gear maintenance photorealistic ultra detailed 8K"},
    {"id": "12", "title": "新版国家医保药品目录发布 新增120种创新药", "tag": "社会",
     "prompt": "Modern Chinese hospital pharmacy with new medicines on shelves doctors consulting patients medical insurance cards photorealistic ultra detailed 8K"},
    {"id": "13", "title": "中国科学家首次实现百公里量子直接通信", "tag": "科技",
     "prompt": "Chinese scientists in quantum communication laboratory optical table with quantum entanglement equipment university campus photorealistic ultra detailed 8K"},
    {"id": "14", "title": "华为发布鸿蒙PC操作系统 打破Windows垄断格局", "tag": "科技",
     "prompt": "Huawei product launch event new HarmonyOS PC laptop revealed stage with tech enthusiasts audience photorealistic ultra detailed 8K"},
    {"id": "15", "title": "巴黎奥运会在即 中国代表团备战状态良好", "tag": "体育",
     "prompt": "Chinese athletes training for Paris Olympics swimming gymnastics athletics preparation sports center photorealistic ultra detailed 8K"},
    {"id": "16", "title": "国际足联宣布2030年世界杯将由西葡摩三国联办", "tag": "体育",
     "prompt": "FIFA headquarters in Zurich World Cup trophy celebration three countries Spain Portugal Morocco flags photorealistic ultra detailed 8K"},
    {"id": "17", "title": "秦始皇陵考古新发现 出土世界最大青铜器", "tag": "文化",
     "prompt": "Terracotta Army pit excavation at Qin Shi Huang Mausoleum massive bronze artifact being carefully preserved photorealistic ultra detailed 8K"},
    {"id": "18", "title": "第78届戛纳电影节开幕 中国导演竞逐金棕榈", "tag": "文化",
     "prompt": "Cannes Film Festival red carpet glamour Cannes France film premiere celebrities on red carpet photorealistic ultra detailed 8K"},
    {"id": "19", "title": "全国外卖骑手超过700万 新就业形态持续壮大", "tag": "社会",
     "prompt": "Chinese food delivery riders on electric bikes in busy city intersection delivery bags loading onto motorcycles photorealistic ultra detailed 8K"},
    {"id": "20", "title": "全国夏粮收购超预期 同比增长12%", "tag": "经济",
     "prompt": "Chinese summer wheat harvest golden wheat fields combine harvesters rural China grain silos storage photorealistic ultra detailed 8K"}
]

def generate_image(news_item, retry=False):
    """Generate a single image using CogView-3-Flash API"""
    prompt = news_item["prompt"]
    news_id = news_item["id"]
    output_path = f"/home/swg/.openclaw/workspace/news-blog/images/news_20260624_{news_id}.png"
    
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    result = subprocess.run([
        "curl", "-s", "-X", "POST",
        "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ], capture_output=True, text=True, timeout=60)
    
    if result.returncode != 0:
        print(f"[{news_id}] ERROR: curl failed")
        return False
    
    try:
        resp = json.loads(result.stdout)
        if "error" in resp:
            print(f"[{news_id}] ERROR: API error - {resp['error']}")
            return False
        if "choices" not in resp or len(resp["choices"]) == 0:
            print(f"[{news_id}] ERROR: No choices in response")
            print(f"Response: {result.stdout[:200]}")
            return False
        
        content = resp["choices"][0]["message"]["content"]
        
        # Handle base64 format: "data:image/png;base64,XXXXX"
        if isinstance(content, str) and content.startswith("data:image"):
            b64_data = content.split(",", 1)[1]
            img_data = base64.b64decode(b64_data)
            with open(output_path, "wb") as f:
                f.write(img_data)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                print(f"[{news_id}] SUCCESS: Saved base64 to {output_path}")
                return True
            else:
                print(f"[{news_id}] ERROR: Save failed")
                return False
        
        # Handle URL list format: [{"url": "https://..."}]
        if isinstance(content, list) and len(content) > 0:
            url = content[0].get("url", "")
            if url:
                subprocess.run([
                    "curl", "-s", "-o", output_path, url
                ], timeout=30)
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                    print(f"[{news_id}] SUCCESS: Downloaded from URL to {output_path}")
                    return True
                else:
                    print(f"[{news_id}] ERROR: Download failed")
                    return False
        
        print(f"[{news_id}] ERROR: Unexpected content format")
        print(f"Content type: {type(content)}, preview: {str(content)[:100]}")
        return False
    except json.JSONDecodeError as e:
        print(f"[{news_id}] ERROR: JSON decode failed - {e}")
        print(f"Response: {result.stdout[:200]}")
        return False
    except Exception as e:
        print(f"[{news_id}] ERROR: {e}")
        return False

def main():
    print(f"Generating 20 images for 2026年06月24日...")
    print("=" * 60)
    
    success_count = 0
    failed = []
    
    for item in news_data:
        news_id = item["id"]
        print(f"\n[{news_id}/20] {item['title']}")
        
        output_path = f"/home/swg/.openclaw/workspace/news-blog/images/news_20260624_{news_id}.png"
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"[{news_id}] Already exists, skipping")
            success_count += 1
            continue
        
        success = generate_image(item)
        if success:
            success_count += 1
        else:
            failed.append(item)
        
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"First pass: {success_count}/20 generated")
    
    if failed:
        print(f"\nRetrying {len(failed)} failed images...")
        for item in failed:
            news_id = item["id"]
            print(f"[{news_id}] RETRY: {item['title']}")
            success = generate_image(item, retry=True)
            if success:
                success_count += 1
                failed.remove(item)
            time.sleep(2)
        
        if failed:
            print(f"\nStill {len(failed)} failed: {[f['id'] for f in failed]}")
    
    print(f"\nFINAL: {success_count}/20 images ready")

if __name__ == "__main__":
    main()