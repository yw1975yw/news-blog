#!/usr/bin/env python3
"""Generate news images for 2026年06月19日 using CogView-3-Flash API"""
import subprocess
import base64
import os
import json
import time

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

news_items = [
    {
        "id": "01",
        "title": "美伊和平协议今日正式签署 中东局势迎来转机",
        "summary": "美国与伊朗两国代表在瑞士日内瓦举行仪式，正式签署和平协议，结束长达数年的核争端。协议内容包括伊朗削减核计划换取制裁解除，双方还同意在能源、反恐等领域展开合作。特朗普总统特别致谢习近平主席和普京总统在幕后斡旋中的关键作用，该协议被视为中东地区数十年来的重要外交突破。",
        "tag": "国际",
        "prompt": "Diplomatic ceremony signing historic peace agreement between United States and Iran in Geneva Switzerland, elegant conference room with两国国旗, diplomats shaking hands, formal atmosphere, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "02",
        "title": "世界杯淘汰赛：葡萄牙3-1淘汰英格兰晋级八强",
        "summary": "2026年世界杯又一场重磅对决在迈阿密硬石体育场打响，葡萄牙队以3-1战胜英格兰，强势晋级八强。葡萄牙当家球星C罗在第34分钟头球破门，下半场又送出两次助攻，当选全场最佳球员。英格兰队长凯恩在第72分钟点球扳回一城，但最终无力回天。八强战中葡萄牙将遭遇法国。",
        "tag": "体育",
        "prompt": "Football World Cup knockout match stadium atmosphere, Portuguese player celebrating goal with arms raised, crowd cheering, dramatic stadium lights, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "03",
        "title": "中国发布《新一代人工智能法》草案 明确治理框架",
        "summary": "全国人大常委会发布《新一代人工智能法》草案并公开征求意见，草案共8章120条，涵盖AI研发、应用、监管和法律责任等内容。草案要求大模型提供商进行安全评估，对深度合成技术实行标识制度，并设立人工智能安全委员会。业内人士认为草案总体有利于行业健康发展。",
        "tag": "科技",
        "prompt": "Chinese legislative building with digital AI data streams and neural network visualization, futuristic technology concept, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "04",
        "title": "英伟达Q2财报超预期 AI芯片需求持续强劲",
        "summary": "英伟达公布截至今年7月的季度财报，总营收达到320亿美元，同比增长125%，远超市场预期。数据中心业务营收增长180%至285亿美元，其中H200和Blackwell架构芯片供不应求。黄仁勋表示AI算力需求已进入爆发期，未来几年将持续扩大投资。公司股价在盘后交易中上涨8%。",
        "tag": "科技",
        "prompt": "NVIDIA headquarters building with glowing green logo, futuristic chip visualization, data center servers with blue LED lights, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "05",
        "title": "德国经济部长：欧洲经济正在温和复苏",
        "summary": "德国联邦经济部长哈贝克表示，欧洲经济正呈现温和复苏态势，制造业PMI已连续三个月回升，出口数据好于预期。欧盟委员会将欧元区今年经济增长预测上调至1.5%，德国经济预计增长1.2%。能源价格回落和通胀压力缓解是主要积极因素，但货币政策走向仍存在不确定性。",
        "tag": "经济",
        "prompt": "European cityscape with factory smokestacks and wind turbines, green energy and industrial revival concept, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "06",
        "title": "联合国气候变化基金承诺增加200亿美元",
        "summary": "联合国气候大会在纽约闭幕，与会各国代表同意将气候变化基金规模扩大至200亿美元，帮助发展中国家应对气候挑战。主要出资方美国、欧盟和中国均宣布了新的出资承诺。大会还通过了一项关于减少甲烷排放的自愿承诺，覆盖全球80%的甲烷排放源。",
        "tag": "国际",
        "prompt": "United Nations headquarters building with green environmental symbol, global climate conference delegates, world globe visualization, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "07",
        "title": "日本央行维持宽松政策 下调今年通胀预期",
        "summary": "日本央行宣布维持负利率政策和收益率曲线控制政策不变，同时将2026财年通胀预期从2.1%下调至1.6%。日本央行行长植田和男表示，物价上涨动力仍不足，需要继续维持超宽松货币政策。日元对美元汇率跌至158:1，创年内新低，出口企业受益但消费者信心受挫。",
        "tag": "金融",
        "prompt": "Bank of Japan building in Tokyo with traditional architecture, yen currency symbols, financial district, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "08",
        "title": "全球最大IPO！SpaceX公开募股估值达3500亿美元",
        "summary": "太空探索技术公司SpaceX正式启动首次公开募股，估值高达3500亿美元，成为有史以来最大规模IPO。SpaceX将发行价值120亿美元的新股，所得资金将用于星舰项目研发和卫星互联网业务扩张。分析师预计SpaceX上市将引发新一轮太空经济投资热潮。",
        "tag": "金融",
        "prompt": "SpaceX rocket launching into space with stars background, futuristic space exploration concept, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "09",
        "title": "世卫组织：全球新冠疫情已彻底结束",
        "summary": "世界卫生组织总干事谭德塞宣布，全球新冠疫情已彻底结束，大流行应急状态正式解除。谭德塞表示，全球疫苗接种率达到78%，病毒变异趋于温和，新一代广谱疫苗普及是关键因素。各国开始陆续取消入境限制和口罩令，旅游和航空业迎来全面复苏。",
        "tag": "社会",
        "prompt": "WHO World Health Organization headquarters in Geneva, happy diverse people celebrating end of pandemic, global health victory, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "10",
        "title": "印度宣布1000亿美元可再生能源投资计划",
        "summary": "印度政府宣布将在未来五年内投资1000亿美元发展可再生能源，目标是将可再生能源装机容量提升至500吉瓦。主要投资方向包括光伏、风电和绿氢产业。印度总理莫迪表示，印度将成为全球清洁能源制造中心，并承诺到2070年实现碳中和。",
        "tag": "经济",
        "prompt": "India landscape with massive solar farm and wind turbines, green energy revolution, farmers working near renewable energy, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "11",
        "title": "马克龙与习近平会晤 呼吁欧洲战略自主",
        "summary": "法国总统马克龙在巴黎爱丽舍宫与中国国家主席习近平举行会谈，双方就中欧关系、乌克兰危机等议题深入交换意见。马克龙呼吁欧洲加快战略自主步伐，减少对任何单一大国的依赖。两国领导人还宣布签署一系列经贸合作协议，涉及航空、可再生能源和金融领域。",
        "tag": "国际",
        "prompt": "Elysee Palace in Paris, French and Chinese presidents in formal meeting, diplomatic ceremony with两国国旗, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "12",
        "title": "中国科学家研发新型AI算法 癌症诊断准确率达98%",
        "summary": "中国科学院深圳先进技术研究院宣布，其团队研发的新型AI癌症诊断系统在临床试验中取得突破，对早期肺癌、乳腺癌和结直肠癌的诊断准确率达到98%。该系统可在10秒内完成影像分析，并标注疑似病变区域。研究成果已发表于国际顶级医学期刊《柳叶刀·肿瘤学》。",
        "tag": "科技",
        "prompt": "Chinese scientists in modern laboratory analyzing medical imaging with AI, cancer diagnosis technology, precision medicine, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "13",
        "title": "阿根廷获IMF新贷款援助 经济改革加速",
        "summary": "国际货币基金组织批准向阿根廷提供150亿美元贷款援助，支持该国经济改革计划。阿根廷政府承诺加快财政整顿、推进能源改革并改善央行独立性。受此消息提振，阿根廷比索汇率升值3%，阿根廷十年期国债收益率下降50个基点。",
        "tag": "经济",
        "prompt": "Buenos Aires cityscape with Argentine flag, IMF headquarters background, financial district, economic growth concept, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "14",
        "title": "2028年洛杉矶奥运会筹备工作正式启动",
        "summary": "洛杉矶奥运会组委会召开发布会，公布2028年夏季奥运会筹备计划和场馆改造方案。本届奥运会将充分利用现有设施，强调可持续性和科技感。开闭幕式将在洛杉矶纪念体育场举行，新建的奥运村可容纳2万名运动员。门票销售将于2027年初启动。",
        "tag": "体育",
        "prompt": "Los Angeles city skyline with Hollywood sign, Olympic rings symbol, futuristic stadium design, 2028 Olympics preparation, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "15",
        "title": "荷兰ASML向中国出口部分先进光刻机",
        "summary": "荷兰光刻机巨头ASML宣布，已获得政府许可向中国出口部分中端光刻机设备。此批设备主要用于28纳米及以上制程的芯片制造，不包含最先进的EUV光刻机。ASML表示中国市场需求依然强劲，这一决定有助于公司维持全球运营效率。消息公布后ASML股价上涨4%。",
        "tag": "科技",
        "prompt": "ASML semiconductor factory in Netherlands, advanced lithography machine inside clean room, microchip manufacturing, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "16",
        "title": "全球云计算市场竞争加剧 阿里云份额突破10%",
        "summary": "市场研究机构IDC最新报告显示，全球云计算市场规模已达6000亿美元，阿里云市场份额突破10%，位居全球第三。AWS和微软Azure仍以32%和23%的份额领先，但阿里云在东南亚和中东地区增长迅速。AI大模型训练需求成为云市场增长的主要驱动力。",
        "tag": "科技",
        "prompt": "Data center server room with blue lighting, cloud computing infrastructure, global network connectivity, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "17",
        "title": "中国人民银行宣布降准0.5个百分点",
        "summary": "中国人民银行宣布，从6月20日起下调金融机构存款准备金率0.5个百分点，释放长期资金约1万亿元。央行表示此举旨在加大对实体经济的支持力度，降低企业融资成本。分析人士预计此举将利好股市和债市，LPR报价利率有望在7月进一步下调。",
        "tag": "金融",
        "prompt": "People's Bank of China headquarters in Beijing with yuan currency symbol, financial center, monetary policy concept, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "18",
        "title": "欧洲多国遭热浪袭击 法国气温达45℃",
        "summary": "极端热浪席卷欧洲西南部，法国、西班牙和意大利多地气温突破45摄氏度，造成严重干旱和山火风险。法国政府发布最高级别红色预警，禁止部分地区户外作业。高温还导致电力需求激增，法国不得不重启部分燃煤电厂以保障供电。",
        "tag": "社会",
        "prompt": "European city in extreme heat wave, thermometer showing high temperature 45 degrees, dry cracked earth, heat haze over urban area, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "19",
        "title": "俄罗斯与乌克兰交换战俘 双方各释放50人",
        "summary": "俄罗斯与乌克兰在第三方调解下完成新一轮战俘交换，双方各释放50名被俘人员。这是自冲突爆发以来规模最大的一次战俘交换行动。卡塔尔和土耳其提供了调停支持，联合国对此表示欢迎。交换行动在白俄罗斯边境地区进行。",
        "tag": "国际",
        "prompt": "Ukraine Russia prisoner exchange at border crossing, Red Cross workers assisting, diplomatic humanitarian operation, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    },
    {
        "id": "20",
        "title": "UNESCO将中国丹霞地貌列入世界遗产候选名单",
        "summary": "联合国教科文组织宣布，中国贵州赤水丹霞地貌正式列入世界遗产候选名单，进入最终冲刺阶段。赤水丹霞总面积超过1300平方公里，是全球保存最完好、最具观赏性的丹霞地貌之一。此前中国已有十余处丹霞地貌被列入世界遗产。",
        "tag": "文化",
        "prompt": "China Danxia landform with spectacular red cliffs and canyons, UNESCO World Heritage candidate, natural landscape with lush vegetation, photorealistic, ultra detailed, 8K, high resolution, no text no watermark"
    }
]

def generate_image_cogview(prompt_text, output_path):
    """Generate image using CogView-3-Flash API"""
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt_text}"}]
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    cmd = [
        "curl", "-s", "-X", "POST", API_URL,
        "-H", f"Authorization: Bearer {API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    if result.returncode != 0:
        print(f"Curl failed: {result.stderr}")
        return False
    
    try:
        data = json.loads(result.stdout)
        content = data["choices"][0]["message"]["content"]
        # Extract base64 after "data:image/png;base64,"
        if "base64," in content:
            b64_data = content.split("base64,")[1]
        else:
            b64_data = content
        
        image_data = base64.b64decode(b64_data)
        with open(output_path, "wb") as f:
            f.write(image_data)
        print(f"✓ Saved {output_path}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        print(f"Response: {result.stdout[:500]}")
        return False

def main():
    date_str = "20260619"
    workdir = "/home/swg/.openclaw/workspace/news-blog"
    images_dir = os.path.join(workdir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Save news data
    with open(os.path.join(workdir, "news_data_20260619.json"), "w", encoding="utf-8") as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    
    # Generate images
    success_count = 0
    for i, item in enumerate(news_items):
        img_path = os.path.join(images_dir, f"news_{date_str}_{item['id']}.png")
        print(f"[{i+1}/20] Generating {item['id']}: {item['title'][:30]}...")
        
        for attempt in range(2):
            if generate_image_cogview(item["prompt"], img_path):
                success_count += 1
                break
            else:
                print(f"  Retry {attempt+1}/2...")
                time.sleep(2)
        
        time.sleep(1)  # Rate limiting
    
    print(f"\nDone: {success_count}/20 images generated")
    
    # Save news items for HTML update
    with open("/tmp/news_items_20260619.json", "w") as f:
        json.dump(news_items, f, ensure_ascii=False)

if __name__ == "__main__":
    main()