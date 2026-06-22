#!/usr/bin/env python3
"""Generate 20 news images using CogView-3-Flash API for 2026年06月23日"""
import subprocess
import json
import os
import time
import urllib.request

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

news_data = [
    {"id": "01", "title": "夏季达沃斯论坛在大连开幕 聚焦规模化创新与全球合作", "tag": "国际",
     "prompt": "A grand international conference venue in Dalian China with modern architecture and thousands of delegates from 90 countries photorealistic ultra detailed 8K"},
    {"id": "02", "title": "美伊在瑞士日内瓦重启核谈判 霍尔木兹海峡局势紧张", "tag": "国际",
     "prompt": "Diplomatic meeting in Geneva Switzerland US and Iranian negotiators at conference table with international flags photorealistic ultra detailed 8K"},
    {"id": "03", "title": "字节跳动火山引擎FORCE大会开幕 发布AI全家桶新品", "tag": "科技",
     "prompt": "Tech conference keynote stage with massive LED screen showing AI technology visualizations Chinese tech company branding photorealistic ultra detailed 8K"},
    {"id": "04", "title": "DeepSeek完成510亿元融资 估值突破1500亿元", "tag": "科技",
     "prompt": "Modern AI startup office interior with holographic data displays showing neural networks Chinese engineers collaborating photorealistic ultra detailed 8K"},
    {"id": "05", "title": "英伟达成全球市值最高公司 黄仁勋发布新一代Blackwell架构", "tag": "科技",
     "prompt": "NVIDIA CEO presenting at massive tech keynote with futuristic GPU chip displayed on stage dramatic stage lighting photorealistic ultra detailed 8K"},
    {"id": "06", "title": "特斯拉Optimus机器人量产版亮相 售价2万美元起", "tag": "科技",
     "prompt": "Humanoid robot standing in modern factory performing precise assembly tasks on automotive parts photorealistic ultra detailed 8K"},
    {"id": "07", "title": "清华大学发布类脑芯片天机X 能效比GPU提升百倍", "tag": "科技",
     "prompt": "Researchers in Tsinghua University laboratory examining novel brain inspired computer chip under microscope photorealistic ultra detailed 8K"},
    {"id": "08", "title": "OpenAI发布GPT-5.6系列 推理能力超越人类专家", "tag": "科技",
     "prompt": "OpenAI headquarters with holographic AI brain visualization ChatGPT interface showing complex reasoning tasks photorealistic ultra detailed 8K"},
    {"id": "09", "title": "中国八部门联合发布新能源汽车下乡政策 155款车型入选", "tag": "经济",
     "prompt": "Electric vehicles charging at rural Chinese village charging station farmers examining new energy cars solar powered infrastructure photorealistic ultra detailed 8K"},
    {"id": "10", "title": "国务院出台31条措施促进民营经济发展 聚焦融资与市场准入", "tag": "经济",
     "prompt": "Chinese government building in Beijing with national flag business leaders entering for policy meeting modern financial district photorealistic ultra detailed 8K"},
    {"id": "11", "title": "美联储宣布维持利率不变 鲍威尔暗示9月降息可能", "tag": "金融",
     "prompt": "Federal Reserve building in Washington DC Federal Reserve chair at press conference podium charts showing interest rate projections photorealistic ultra detailed 8K"},
    {"id": "12", "title": "比特币现货ETF单月净流入超50亿美元 机构持仓创新高", "tag": "金融",
     "prompt": "Bitcoin symbol with upward trending charts institutional investors in modern office cryptocurrency trading screens photorealistic ultra detailed 8K"},
    {"id": "13", "title": "国际油价持续下跌 布伦特原油跌破75美元关口", "tag": "金融",
     "prompt": "Oil tanker ship at sea during sunset oil price drop displayed on financial trading screens global economy visualization photorealistic ultra detailed 8K"},
    {"id": "14", "title": "阿里巴巴季度营收2650亿元 AI云业务增长超50%", "tag": "金融",
     "prompt": "Alibaba Group headquarters in Hangzhou impressive skyscraper complex data visualization screens showing revenue growth photorealistic ultra detailed 8K"},
    {"id": "15", "title": "三星堆遗址新出土文物近万件 再现古蜀文明辉煌", "tag": "文化",
     "prompt": "Archaeological site excavation in Sichuan ancient bronze artifacts carefully unearthed mysterious Sanxingdui masks on display photorealistic ultra detailed 8K"},
    {"id": "16", "title": "中国动漫长安三万里全球票房突破50亿元", "tag": "文化",
     "prompt": "Chinese animated movie poster featuring Tang Dynasty poets in traditional Chinese painting style theater entrance movie audience photorealistic ultra detailed 8K"},
    {"id": "17", "title": "中国游泳队世界杯上海站包揽9金 覃海洋刷新世界纪录", "tag": "体育",
     "prompt": "Chinese swimmers celebrating at Shanghai World Aquatics Championships gold medals ceremony national flag rising photorealistic ultra detailed 8K"},
    {"id": "18", "title": "英民调显示王室支持率跌至33年最低 仅三成民众支持君主制", "tag": "国际",
     "prompt": "Buckingham Palace in London with British flags British royal family crest gray London sky photorealistic ultra detailed 8K"},
    {"id": "19", "title": "全国铁路暑运启动 预计发送旅客8.6亿人次", "tag": "社会",
     "prompt": "Massive Chinese high speed railway station crowded with summer travelers bullet trains on platforms families with luggage photorealistic ultra detailed 8K"},
    {"id": "20", "title": "教育部将AI教育纳入中小学必修课 配备人工智能实验室", "tag": "社会",
     "prompt": "Chinese students in modern AI classroom interacting with robots and holographic displays programming lessons futuristic educational environment photorealistic ultra detailed 8K"}
]

def generate_image(news_item, retry=False):
    """Generate a single image using CogView-3-Flash API"""
    prompt = news_item["prompt"]
    news_id = news_item["id"]
    output_path = f"/home/swg/.openclaw/workspace/news-blog/images/news_20260623_{news_id}.png"
    
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
            return False
        
        content = resp["choices"][0]["message"]["content"]
        # Content is a list of objects with url field
        if isinstance(content, list) and len(content) > 0:
            url = content[0].get("url", "")
            if url:
                # Download the image
                subprocess.run([
                    "curl", "-s", "-o", output_path, url
                ], timeout=30)
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                    print(f"[{news_id}] SUCCESS: Saved to {output_path}")
                    return True
                else:
                    print(f"[{news_id}] ERROR: Download failed")
                    return False
        
        print(f"[{news_id}] ERROR: Unexpected content format")
        return False
    except json.JSONDecodeError as e:
        print(f"[{news_id}] ERROR: JSON decode failed - {e}")
        return False
    except Exception as e:
        print(f"[{news_id}] ERROR: {e}")
        return False

def main():
    print(f"Generating 20 images for 2026年06月23日...")
    print("=" * 60)
    
    success_count = 0
    failed = []
    
    for item in news_data:
        news_id = item["id"]
        print(f"\n[{news_id}/20] {item['title']}")
        
        output_path = f"/home/swg/.openclaw/workspace/news-blog/images/news_20260623_{news_id}.png"
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"[{news_id}] Already exists, skipping")
            success_count += 1
            continue
        
        success = generate_image(item)
        if success:
            success_count += 1
        else:
            failed.append(item)
        
        time.sleep(0.5)
    
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
            time.sleep(1)
        
        if failed:
            print(f"\nStill {len(failed)} failed: {[f['id'] for f in failed]}")
    
    print(f"\nFINAL: {success_count}/20 images ready")

if __name__ == "__main__":
    main()