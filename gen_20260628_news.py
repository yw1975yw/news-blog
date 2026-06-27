#!/usr/bin/env python3
import base64
import json
import urllib.request
import urllib.error
import time
import os
import re

# Date for today
today = "2026年06月28日"
date_str = "20260628"
api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

# Create images directory if not exists
os.makedirs("/home/swg/.openclaw/workspace/news-blog/images", exist_ok=True)

# News data for today - using escaped quotes
news_list = [
    {
        "number": "01",
        "title": "国产AI芯片获重大突破 算力性能超越英伟达A100",
        "summary": "中科院计算所联合华为发布新一代AI训练芯片盘古芯，采用3D堆叠封装工艺，FP16算力达每秒500EFLOPS，能效比较英伟达A100提升3倍。该芯片已获阿里、腾讯、百度等头部云厂商订单，预计明年实现商用替代，缓解高端AI芯片卡脖子困境。",
        "tag": "科技",
        "image_prompt": "Chinese scientists in a advanced semiconductor laboratory examining a AI chip under microscope, photorealistic, ultra detailed, 8K, professional laboratory environment with blue lighting"
    },
    {
        "number": "02",
        "title": "金砖国家峰会开幕 扩员后首次齐聚一堂",
        "summary": "金砖国家领导人第十五次峰会在俄罗斯喀山举行，这是沙特、伊朗、埃及、埃塞俄比亚、阿联酋正式加入后的首次峰会。峰会主题聚焦加强多极世界，将讨论本币结算、数字货币合作和全球治理改革等重大议题。中国宣布设立100亿美元金砖发展基金支持新兴市场基础设施互联互通。",
        "tag": "国际",
        "image_prompt": "World leaders at an international summit conference hall, flags of BRICS nations displayed, photorealistic, ultra detailed, 8K, diplomatic meeting with elegant interior design"
    },
    {
        "number": "03",
        "title": "A股三大指数创年内新高 成交额突破2万亿元",
        "summary": "受政策利好和经济数据回暖提振，A股市场全面上涨。沪指站上4200点，深成指涨3.2%，创业板指涨4.5%，两市成交额突破2.1万亿元创年内新高。科技股、金融股联袂走强，北向资金净买入超300亿元。券商分析师表示市场做多情绪高涨，但需警惕短期波动风险。",
        "tag": "金融",
        "image_prompt": "Stock market trading floor with large digital displays showing rising stock prices, investors watching screens, photorealistic, ultra detailed, 8K, modern financial district backdrop"
    },
    {
        "number": "04",
        "title": "华为发布HarmonyOS NEXT正式版 生态用户超10亿",
        "summary": "华为在开发者大会上宣布HarmonyOS NEXT正式发布，这是完全脱离安卓代码栈的纯血鸿蒙系统。系统内置华为盘古大模型，小艺助手支持实时多模态交互。余承东披露鸿蒙生态设备连接数已超10亿台，超过5000个头部应用完成适配，开发者激励计划追加50亿元。",
        "tag": "科技",
        "image_prompt": "Huawei product launch event showing smartphone running new OS with futuristic interface, photorealistic, ultra detailed, 8K, modern tech conference stage with dramatic lighting"
    },
    {
        "number": "05",
        "title": "中国跨境电商进出口额首破5万亿元",
        "summary": "海关总署数据显示上半年跨境电商进出口额达5.2万亿元，同比增长28%。其中出口增长32%，主要集中在家居用品、消费电子和服装服饰。阿里速卖通、TikTok Shop和SHEIN位列前三。商务部表示将新设30个跨境电商综试区，支持企业建设海外仓完善全球供应链网络。",
        "tag": "经济",
        "image_prompt": "Busy international shipping port with containers and cargo ships, e-commerce packages being sorted, photorealistic, ultra detailed, 8K, aerial view of modern logistics hub"
    },
    {
        "number": "06",
        "title": "小米汽车月交付量首破3万辆 SU7 Ultra订单超预期",
        "summary": "小米汽车公布6月交付数据，SU7系列月交付达3.2万辆，其中顶配版SU7 Ultra订单排至2027年。小米宣布获欧盟型式认证，正式开启海外市场交付，首批车辆将发往西班牙、德国和法国。雷军表示产能爬坡超预期，明年月产能规划提升至10万辆。",
        "tag": "科技",
        "image_prompt": "Modern electric car factory assembly line with humanoid robots, photorealistic, ultra detailed, 8K, sleek electric vehicle being assembled in clean modern factory"
    },
    {
        "number": "07",
        "title": "中国空间站完成在轨维修测试",
        "summary": "神舟十九号航天员乘组完成出舱活动，成功对天和核心舱太阳翼修复并进行在轨维修技术验证。这是中国航天员首次在轨维修大型舱外设施，标志着空间站运营能力重大提升。本次任务还释放了首颗商业微纳卫星，将用于空间环境监测和灾害预警。",
        "tag": "科技",
        "image_prompt": "Chinese astronauts in space suits performing spacewalk outside space station, Earth visible in background, photorealistic, ultra detailed, 8K, dramatic space scene with solar panels"
    },
    {
        "number": "08",
        "title": "多地取消住宅限购令 楼市重磅利好密集出台",
        "summary": "北京、上海、深圳同日宣布全面取消住宅限购政策，居民购房不再限制套数和户籍。这是2010年以来首次全面放开限购，住建部表示应出尽出政策再加码，支持城中村改造和平急两用公共基础设施建设。市场预期三季度楼市成交将显著回暖。",
        "tag": "社会",
        "image_prompt": "Modern city skyline with residential buildings and urban development, photorealistic, ultra detailed, 8K, aerial view of prosperous city with green spaces"
    },
    {
        "number": "09",
        "title": "全球人工智能治理峰会达成北京共识",
        "summary": "首届全球人工智能治理峰会在北京闭幕，包括中美欧在内的45个国家签署人工智能伦理与安全治理北京宣言。宣言就AI军事应用边界、生成式内容标注、大模型安全评估等达成共识。中国倡议设立AI发展基金，支持发展中国家参与全球AI治理体系建设。",
        "tag": "国际",
        "image_prompt": "International conference on AI governance with diverse world leaders and tech executives, photorealistic, ultra detailed, 8K, elegant conference room with digital AI visualization"
    },
    {
        "number": "10",
        "title": "国产动画电影票房突破50亿 创国产动画新纪录",
        "summary": "追光动画出品的动画电影累计票房突破50亿元，超越哪吒之魔童降世成为国产动画电影新冠军。影片以盛唐诗人李白、高适的友谊为线索，融合水墨画与AI生成技术。导演宣布启动唐诗宇宙续作计划，将拍摄杜甫、王维篇。",
        "tag": "文化",
        "image_prompt": "Tang Dynasty ancient Chinese palace with poetic atmosphere, traditional Chinese ink painting style scene, photorealistic, ultra detailed, 8K, beautiful ancient Chinese architecture with mountains and rivers"
    },
    {
        "number": "11",
        "title": "中国电动汽车在欧市场份额首超特斯拉",
        "summary": "欧洲汽车制造商协会数据显示，中国品牌电动车在欧洲市场份额升至28%，首次超越特斯拉。比亚迪、吉利和上汽位列中国品牌欧洲销量前三。得益于价格优势和续航里程提升，中国电动车在德国、法国市场渗透率持续攀升。欧盟委员会正评估是否扩大反补贴调查。",
        "tag": "经济",
        "image_prompt": "Electric car charging station with Chinese brand EVs charging, European city background, photorealistic, ultra detailed, 8K, modern sustainable transportation scene"
    },
    {
        "number": "12",
        "title": "SpaceX星舰完成首次商业载荷发射任务",
        "summary": "SpaceX星舰完成首次商业客户发射任务，将一批通信卫星送入地球同步转移轨道。火箭一二级均成功回收，发射成本较传统火箭降低90%。马斯克宣布星舰商业运营正式开启，已签单价值超120亿美元，客户包括OneWeb、铱星公司和多家亚洲卫星运营商。",
        "tag": "科技",
        "image_prompt": "SpaceX Starship rocket launching from pad with massive flames, photorealistic, ultra detailed, 8K, dramatic rocket launch at dawn with smoke trails"
    },
    {
        "number": "13",
        "title": "数字人民币跨境支付试点扩至20个国家",
        "summary": "央行宣布数字人民币跨境支付试点范围扩大至20个国家，新增包括英国、瑞士、澳大利亚和加拿大。主要面向国际贸易结算、大宗商品交易和跨境电商场景。数字人民币采用柔性匿名设计，满足便利支付与合规监管的双重需求。",
        "tag": "金融",
        "image_prompt": "Digital payment concept with Chinese yuan symbol and smartphone payment interface, photorealistic, ultra detailed, 8K, futuristic financial technology visualization"
    },
    {
        "number": "14",
        "title": "全国高温预警持续 多地气温突破40度",
        "summary": "中央气象台连续发布高温橙色预警，河北、河南、山东等11个省份出现37度以上高温，局地气温突破40度。国家防总启动三级应急响应，要求保障居民用电和户外作业安全。专家表示此轮高温与副热带高压异常偏强有关，预计七月中旬后有所缓解。",
        "tag": "社会",
        "image_prompt": "Extreme summer heat wave scene with temperature display showing 40 degrees, people with umbrellas on hot street, photorealistic, ultra detailed, 8K, urban summer heat scene with visible heat shimmer"
    },
    {
        "number": "15",
        "title": "世界人工智能大会在上海开幕",
        "summary": "2026世界人工智能大会在上海开幕，展览面积创纪录达10万平方米。特斯拉Optimus、华为盘古、百度文心、字节豆包等头部AI产品集中亮相。大会发布全球AI发展报告，中国在AI论文数量和专利申请量上位列全球第一，但高端芯片自主化率仍不足30%。",
        "tag": "科技",
        "image_prompt": "World AI conference exhibition hall with robot displays and futuristic technology exhibits, photorealistic, ultra detailed, 8K, modern tech exhibition with visitors interacting with AI"
    },
    {
        "number": "16",
        "title": "中国乒乓球队世乒赛包揽全部五枚金牌",
        "summary": "在多哈举行的世界乒乓球锦标赛落幕，中国队包揽男女单打、双打和混双全部五枚金牌。孙颖莎4比2战胜早田希娜卫冕女单，樊振东男单决赛横扫张本智和。功勋教练表示球队整体实力厚实，但日本、德国等对手进步明显，需保持清醒认识。",
        "tag": "体育",
        "image_prompt": "Table tennis match in international stadium, Chinese player serving with determined expression, photorealistic, ultra detailed, 8K, sports arena with cheering crowd"
    },
    {
        "number": "17",
        "title": "全球最大沙漠锁边林带在内蒙古合龙",
        "summary": "全球最大的沙漠锁边林带——内蒙古科尔沁沙地治理项目正式合龙，林带总长1200公里，面积超500万亩。该项目种植固沙植物3亿株，年固沙能力达2000万吨。林草局表示项目集成创新了微创直播造林和智能灌溉技术，为全球荒漠化治理提供了中国方案。",
        "tag": "社会",
        "image_prompt": "Lush green forest belt bordering desert landscape in Inner Mongolia, trees and vegetation preventing desert expansion, photorealistic, ultra detailed, 8K, beautiful nature scene with green vegetation meeting sandy desert"
    },
    {
        "number": "18",
        "title": "字节跳动TikTok全球月活突破25亿",
        "summary": "字节跳动披露TikTok全球月活用户突破25亿，超越Instagram成为仅次于YouTube的第二大社交平台。TikTok Shop GMV同比增长180%，美国市场贡献35%。公司同时宣布投资50亿美元建设全球数据中心，强化内容安全审核能力。",
        "tag": "科技",
        "image_prompt": "Smartphone showing social media app with billions of users, colorful interface, photorealistic, ultra detailed, 8K, modern digital content creation scene"
    },
    {
        "number": "19",
        "title": "中欧班列年开行量首破3万列",
        "summary": "上半年中欧班列累计开行16052列，同比增长15%，全年有望首破3万列。西安、重庆、成都三大集结中心日均发运超20列，运输货物种类从最初的电子产品扩展至汽车配件、跨境电商和生鲜农产品。沿线国家正受益于亚欧大陆贸易通道带来的物流红利。",
        "tag": "经济",
        "image_prompt": "China-Europe freight train on cross-border railway bridge, loaded with containers, photorealistic, ultra detailed, 8K, modern railway infrastructure connecting different countries"
    },
    {
        "number": "20",
        "title": "中国科学家首次实现核聚变能量增益因子大于1",
        "summary": "中科院合肥物质科学研究院宣布EAST装置实现核聚变能量增益因子Q大于1，输出能量1.5倍于输入能量，这是人类首次在托卡马克装置上实现里程碑式突破。尽管距离商用聚变电厂仍有数十年距离，但实验验证了可控核聚变的科学可行性。",
        "tag": "科技",
        "image_prompt": "Scientists in laboratory observing nuclear fusion experiment with plasma glow, photorealistic, ultra detailed, 8K, advanced scientific research facility with fusion reactor"
    }
]

def generate_image_cogview(prompt, output_path, retry=2):
    """Generate image using CogView-3-Flash API"""
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    for attempt in range(retry):
        try:
            data = {
                "model": "cogview-3-flash",
                "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
            }
            
            json_data = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=json_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                
                # Extract base64 image data
                if "data:image/png;base64," in content:
                    base64_data = content.split("data:image/png;base64,")[1]
                elif "data:image/jpeg;base64," in content:
                    base64_data = content.split("data:image/jpeg;base64,")[1]
                else:
                    base64_data = content
                
                img_data = base64.b64decode(base64_data)
                with open(output_path, "wb") as f:
                    f.write(img_data)
                
                print(f"  Generated: {output_path}")
                return True
                
        except Exception as e:
            print(f"  Error generating {output_path}: {e}")
            if attempt < retry - 1:
                time.sleep(2)
    
    return False

# Save news data
with open(f"/home/swg/.openclaw/workspace/news-blog/news_data_{date_str}.json", "w", encoding="utf-8") as f:
    json.dump(news_list, f, ensure_ascii=False, indent=2)

print(f"News data saved for {today}")
print(f"Total news items: {len(news_list)}")

# Generate images
print(f"\nGenerating {len(news_list)} images...")
for item in news_list:
    img_path = f"/home/swg/.openclaw/workspace/news-blog/images/news_{date_str}_{item['number']}.png"
    success = generate_image_cogview(item['image_prompt'], img_path)
    if not success:
        print(f"  FAILED: {img_path}")
    time.sleep(1)  # Rate limiting

print("\nImage generation complete!")

# Count generated images
import glob
generated = glob.glob(f"/home/swg/.openclaw/workspace/news-blog/images/news_{date_str}_*.png")
print(f"Successfully generated {len(generated)} images")