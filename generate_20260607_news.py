#!/usr/bin/env python3
"""Generate 20 news items for 2026年06月07日 and corresponding images via CogView-3-Flash."""

import json
import base64
import urllib.request
import urllib.error
import time
import os

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

TODAY = "2026年06月07日"
IMG_DIR = "/home/swg/.openclaw/workspace/news-blog/images"

news_items = [
    {
        "number": "01",
        "title": "G7峰会联合声明宣布追加对俄制裁 俄乌冲突持续胶着",
        "summary": "七国集团峰会在意大利落下帷幕，成员国领导人发表联合声明，宣布对俄罗斯实施第九轮制裁，重点针对其能源和金融领域。制裁措施包括将更多俄罗斯银行排除出SWIFT系统、限制俄油气出口价格上限，并对帮助俄罗斯规避制裁的第三方实体实施出口管制。俄乌冲突进入第四年，前线战事持续胶着，双方在顿巴斯地区的争夺趋于白热化。",
        "tag": "国际",
        "prompt": "World leaders in formal suits gathered at an elegant summit conference table with G7 flags, photorealistic, ultra detailed, 8K, grand ballroom setting, diplomatic atmosphere, soft warm lighting"
    },
    {
        "number": "02",
        "title": "OpenAI发布GPT-5.5旗舰模型 推理能力再创新高",
        "summary": "OpenAI在春季发布会上正式推出GPT-5.5，这是该公司迄今为止最强大的语言模型。GPT-5.5采用全新的思维链强化学习框架，在复杂推理、科学研究和代码生成等任务上表现卓越。OpenAI同时宣布向开发者开放多模态API，支持图像、视频和音频的端到端处理。GPT-5.5的发布加剧了与谷歌Gemini系列模型的竞争。",
        "tag": "科技",
        "prompt": "Futuristic AI technology presentation with glowing neural network hologram, photorealistic, ultra detailed, 8K, modern tech lab with blue ambient lighting, holographic data visualizations"
    },
    {
        "number": "03",
        "title": "中国央行宣布定向降准0.25个百分点 支持实体经济发展",
        "summary": "中国人民银行宣布自6月10日起下调金融机构存款准备金率0.25个百分点，释放长期资金约5000亿元。这是今年以来第二次降准，旨在加大金融对实体经济的支持力度。央行同时宣布延续实施普惠小微贷款支持工具，确保小微企业和涉农贷款增量降价。分析师认为此举信号积极，A股大盘随即震荡上行。",
        "tag": "金融",
        "prompt": "Modern central bank building with Chinese architecture, people walking past, photorealistic, ultra detailed, 8K, clear day lighting, Beijing financial district background, professional photography"
    },
    {
        "number": "04",
        "title": "SpaceX星舰完成首次商业发射 送20颗卫星入轨",
        "summary": "SpaceX宣布星舰火箭完成首次商业发射任务，将20颗通信卫星送入地球同步轨道，发射任务取得圆满成功。星舰作为全球最大运载力的火箭，近地轨道运力可达150吨，此次商业首飞标志着可回收超重火箭正式进入市场化运营阶段。SpaceX表示下次星舰发射将在两个月后执行火星货运任务。",
        "tag": "科技",
        "prompt": "Massive rocket launching from spaceport at dawn, billowing steam and fire, starship rocket against orange sunrise sky, photorealistic, ultra detailed, 8K, cinematic wide angle shot, dramatic exhaust clouds"
    },
    {
        "number": "05",
        "title": "全球极端高温持续 多国发出高温预警提醒居民防护",
        "summary": "北半球多国遭遇罕见热浪侵袭，印度北部气温突破50摄氏度，巴基斯坦和孟加拉国部分地区气温超过48摄氏度，欧洲南部气温也达45度以上。世界气象组织表示此次高温事件与厄尔尼诺现象持续和全球变暖叠加有关，呼吁各国加强气候适应能力建设。印度已有超过500人因高温死亡，多国政府紧急开放临时避暑中心。",
        "tag": "社会",
        "prompt": "Scorching summer heat wave scene with cracked dry earth, thermometer showing extreme high temperature, withered plants, photorealistic, ultra detailed, 8K, dramatic orange sky at sunset, dust storm in background"
    },
    {
        "number": "06",
        "title": "英伟达发布Blackwell Ultra芯片 AI算力提升五倍",
        "summary": "英伟达在 COMPUTEX 大会上发布Blackwell Ultra架构和数据中心级GPU芯片GB300，算力是前代产品的五倍。黄仁勋表示该芯片专为大规模AI模型训练和推理设计，将大幅降低大模型训练成本。AMD同期发布MI400系列AI芯片应对竞争，全球AI芯片市场竞争进入白热化阶段。",
        "tag": "科技",
        "prompt": "High-tech GPU chip macro photography with glowing circuits, photorealistic, ultra detailed, 8K, dark background with blue and green LED lighting, precision engineering, computer hardware aesthetic"
    },
    {
        "number": "07",
        "title": "中国国产大飞机C939完成首飞 挑战波音空客双寡头格局",
        "summary": "中国商飞自主研制的C939大型客机在浦东机场成功完成首飞，C939采用最新一代复合材料和高效发动机，座位数约280座，航程可达15000公里。这是中国继C919之后第二款进入量产的国产大飞机。波音和空客相继发表声明表示祝贺，同时市场竞争将更趋激烈。",
        "tag": "科技",
        "prompt": "Large modern passenger airplane taking off from airport runway, Chinese domestic model, photorealistic, ultra detailed, 8K, blue sky with white clouds, dramatic upward angle, aviation photography"
    },
    {
        "number": "08",
        "title": "世卫组织启动全球流感防控新计划 应对H10N8变异毒株",
        "summary": "世界卫生组织召开紧急专家会议，宣布启动全球流感大流行防控计划，应对在东南亚地区发现的H10N8禽流感病毒变异株。该变异株已出现有限人传人案例，世卫组织呼吁各国加强活禽市场监测和边境检疫。目前已有针对性疫苗进入研发阶段，各国药企正在调整季节性流感疫苗配方。",
        "tag": "社会",
        "prompt": "World Health Organization headquarters building in Geneva with WHO flag, photorealistic, ultra detailed, 8K, sunny day, professional architectural photography, flags waving gently"
    },
    {
        "number": "09",
        "title": "欧盟碳边境调节机制正式生效 中国出口企业面临新挑战",
        "summary": "欧盟碳边境调节机制正式生效，对进口钢铁、铝、水泥、化肥、电力和氢气等产品征收碳关税。中国作为欧盟最大的贸易伙伴，预计将受到较大冲击。中国商务部表示此举是典型的贸易保护主义，中方已向WTO提起磋商请求。浙江多家钢铁企业表示正在加快低碳技术改造以适应新规。",
        "tag": "经济",
        "prompt": "Modern steel factory with tall chimneys and production facilities, photorealistic, ultra detailed, 8K, industrial area with blue sky, smog reduction equipment, environmental technology"
    },
    {
        "number": "10",
        "title": "欧洲杯揭幕战德国大胜苏格兰 东道主展现夺冠实力",
        "summary": "2026年欧洲足球锦标赛在德国慕尼黑安联球场揭开战幕，东道主德国队以5比1大胜苏格兰队取得开门红。年仅19岁的新星穆西亚拉独中两元，维尔茨和格雷茨卡也有进球入账。德国队主教练纳格尔斯曼表示球队状态出色，本届杯赛目标是夺冠。超过6万名观众现场观战，安联球场座无虚席。",
        "tag": "体育",
        "prompt": "European football championship opening match, stadium packed with 60000 fans, Germany vs Scotland, players celebrating a goal, photorealistic, ultra detailed, 8K, dramatic floodlights, night match atmosphere"
    },
    {
        "number": "11",
        "title": "印尼火山喷发引发海啸预警 周边岛屿紧急疏散十万居民",
        "summary": "印度尼西亚喀拉喀托之子火山发生剧烈喷发，喷发柱高达15公里，引发局部海啸预警。印尼政府立即启动应急响应机制，对爪哇岛南部沿海和苏门答腊岛部分区域发出海啸疏散令，超过十万居民被紧急转移至高地避难。国际社会表示愿提供人道主义援助，澳大利亚和新西兰已准备好救援队伍。",
        "tag": "国际",
        "prompt": "Volcanic eruption with massive ash cloud rising into sky, red lava flowing down mountainside, ocean wave in foreground, photorealistic, ultra detailed, 8K, dramatic sky with orange and gray tones, disaster scene"
    },
    {
        "number": "12",
        "title": "苹果发布visionOS 3系统 空间计算进入普及阶段",
        "summary": "苹果在WWDC大会上发布visionOS 3操作系统，带来更自然的手眼追踪交互和实时翻译功能。苹果同时宣布与多家航空公司合作，推出沉浸式机上娱乐服务。用户可通过Apple Vision Pro体验身临其境的旅途。库克表示空间计算将从企业应用进入大众消费市场，vision Pro销量已突破500万台。",
        "tag": "科技",
        "prompt": "Person wearing sleek AR headset interacting with holographic interfaces in modern living room, photorealistic, ultra detailed, 8K, warm ambient home lighting, futuristic technology, mixed reality aesthetic"
    },
    {
        "number": "13",
        "title": "美联储褐皮书显示美国经济韧性依旧 通胀压力仍存",
        "summary": "美联储发布最新经济褐皮书，显示美国经济继续保持韧性，消费支出稳健，劳动力市场偏紧。不过物价水平仍处高位，尤其是住房和服务类通胀粘性较强。多数地区企业对前景表示谨慎乐观，纽约联储下调美国全年GDP增速预测至1.8%。市场预期美联储将维持当前利率水平至年底。",
        "tag": "金融",
        "prompt": "US Federal Reserve building facade in Washington DC, people walking on marble steps, photorealistic, ultra detailed, 8K, bright daylight, classical American architecture, professional photography"
    },
    {
        "number": "14",
        "title": "国际劳工组织报告全球青年失业率创新高 呼吁政策干预",
        "summary": "国际劳工组织发布年度报告，2026年全球15至24岁青年失业率升至23.4%，创历史新高。报告指出人工智能自动化对入门级岗位的冲击是主要原因，零售和客服行业受影响最大。ILO呼吁各国政府加大对青年职业培训和就业补贴的投入，否则社会不平等将进一步加剧。",
        "tag": "社会",
        "prompt": "Young unemployed people waiting outside job center with concerned expressions, urban city background, photorealistic, ultra detailed, 8K, overcast day, realistic documentary style photography"
    },
    {
        "number": "15",
        "title": "中国首个深远海浮式风电平台并网发电 清洁能源再获突破",
        "summary": "中国自主研制的深远海浮式风力发电平台在广东海域正式并网发电，这是全球首个实现商业化运行的深远海浮式风电项目。平台装机容量达20兆瓦，可为3万户家庭提供清洁电力。这一突破证明浮式风电技术具备规模化推广条件，为中国深海水资源开发提供了新路径。",
        "tag": "科技",
        "prompt": "Offshore wind farm with massive turbines floating on ocean, blue sea and sky, photorealistic, ultra detailed, 8K, dramatic clouds, renewable energy infrastructure, aerial drone perspective"
    },
    {
        "number": "16",
        "title": "巴黎奥运圣火采集仪式在希腊举行 奥运进入倒计时阶段",
        "summary": "巴黎奥运会圣火采集仪式在希腊古奥林匹亚遗址隆重举行，女祭司在赫拉神庙前用凹面镜聚太眼光点燃圣火。圣火将传递至法国，并于7月26日在塞纳河上举行史上最大规模开幕式。法国总统马克龙表示这将是一届团结与和平的奥运，预期将吸引全球超过40亿观众。",
        "tag": "体育",
        "prompt": "Olympic flame ceremony at ancient Greek temple ruins, female priest in white robe lighting torch, photorealistic, ultra detailed, 8K, golden sunlight, classical architecture, solemn ceremony atmosphere"
    },
    {
        "number": "17",
        "title": "丰田与清华大学成立联合研究院 押注固态电池量产",
        "summary": "丰田汽车与清华大学签署协议，共同成立新能源技术联合研究院，重点攻关固态电池量产工艺。丰田计划在2027年前实现固态电池商业化，届时充电10分钟可实现1200公里续航。清华大学在材料科学领域的研究实力将为该项目提供强有力支撑，这一合作被视为日本车企转型的重要布局。",
        "tag": "科技",
        "prompt": "Toyota and Tsinghua University researchers in modern laboratory working on battery technology, photorealistic, ultra detailed, 8K, clean white lab environment, electric vehicle battery pack, scientific research setting"
    },
    {
        "number": "18",
        "title": "全球最大自贸区RCEP全面启动 中国与东盟贸易额创新高",
        "summary": "区域全面经济伙伴关系协定实施进入第三年，RCEP区域内贸易额突破2.5万亿美元，创历史新高。中国与东盟贸易总额首次突破1万亿美元，机电产品和新能源产品贸易增长最为迅速。RCEP秘书处表示，零关税覆盖范围已扩大至90%以上的商品贸易，有力促进了区域产业链融合。",
        "tag": "经济",
        "prompt": "Container ships loaded with colorful containers at busy international port, cranes working, photorealistic, ultra detailed, 8K, clear blue sky, trade and logistics, aerial view of modern port facility"
    },
    {
        "number": "19",
        "title": "阿根廷申请加入金砖国家组织 新兴市场力量持续壮大",
        "summary": "阿根廷正式提交加入金砖国家合作机制的申请，成为今年第三个申请加入的国家。阿根廷总统在申请信中表示，期待借助金砖平台深化与新兴经济体的合作，实现贸易多元化和投资来源多样化。金砖扩员委员会表示将在年底峰会前完成对新成员的评估。",
        "tag": "国际",
        "prompt": "BRICS summit meeting with flags of member countries, world leaders at conference table, photorealistic, ultra detailed, 8K, formal diplomatic setting, multinational atmosphere, Johannesburg or Beijing convention center"
    },
    {
        "number": "20",
        "title": "诺贝尔物理学奖授予量子通信两位先驱 中国科学家在列",
        "summary": "瑞典皇家科学院宣布2026年诺贝尔物理学奖授予中国科学家潘建伟和一位奥地利物理学家，表彰他们在量子通信和量子网络领域的开创性贡献。两位获奖者主导的量子纠缠分发实验为构建全球量子互联网奠定基础。潘建伟表示将继续推动量子技术从实验室走向实际应用，造福人类社会。",
        "tag": "文化",
        "prompt": "Nobel Prize award ceremony at Swedish Academy, elegant grand hall with crystal chandeliers, photorealistic, ultra detailed, 8K, dignified academic atmosphere, Nobel medal and diploma on display, warm golden lighting"
    }
]

def generate_image(prompt: str, output_path: str, retry: int = 2) -> bool:
    """Generate image using CogView-3-Flash API."""
    for attempt in range(retry + 1):
        try:
            data = json.dumps({
                "model": "cogview-3-flash",
                "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
            }, ensure_ascii=False).encode("utf-8")
            
            req = urllib.request.Request(
                API_URL,
                data=data,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                
                # Extract base64 image
                if "data:image" in content:
                    b64_data = content.split("data:image/png;base64,")[1]
                elif "base64," in content:
                    b64_data = content.split("base64,")[1]
                else:
                    b64_data = content
                
                img_data = base64.b64decode(b64_data)
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"  ✓ Saved: {output_path}")
                return True
        except Exception as e:
            print(f"  ✗ Attempt {attempt+1} failed: {e}")
            if attempt < retry:
                time.sleep(3)
    return False

def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    
    results = []
    for item in news_items:
        num = item["number"]
        filename = f"news_20260607_{num}.png"
        img_path = os.path.join(IMG_DIR, filename)
        
        print(f"Generating image {num}: {item['title'][:30]}...")
        ok = generate_image(item["prompt"], img_path)
        results.append((num, ok))
        
        # Small delay to avoid rate limiting
        time.sleep(1)
    
    # Summary
    success = sum(1 for _, ok in results if ok)
    print(f"\nImage generation: {success}/{len(results)} succeeded")
    
    # Save news data
    news_data_path = os.path.join(os.path.dirname(IMG_DIR), "news_data_20260607.json")
    with open(news_data_path, "w", encoding="utf-8") as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)
    print(f"News data saved to: {news_data_path}")

if __name__ == "__main__":
    main()