#!/usr/bin/env python3
"""Generate news images for 2026年06月29日 using CogView-3-Flash API"""

import base64
import json
import os
import requests
import time

# API configuration
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

# Date
DATE = "20260629"
DISPLAY_DATE = "2026年06月29日"

# News data for 2026年06月29日
NEWS_DATA = [
    {
        "number": "01",
        "title": "全球首个量子计算云平台正式开放商用",
        "summary": "中科院量子信息实验室联合阿里云发布全球首个量子计算商用云平台，平台集成126量子比特处理器，可为金融机构、制药企业和科研机构提供量子模拟服务。量子体积达4096，错误率低于0.1%。首期开放1000个计算配额，企业用户可通过API接入，预计将加速药物研发、金融风险计算等领域突破。",
        "tag": "科技",
        "image_prompt": "A futuristic quantum computer with glowing blue circuits in a cloud computing data center, photorealistic, ultra detailed, 8K, holographic quantum bits floating above the machine"
    },
    {
        "number": "02",
        "title": "联合国大会通过全球AI监管框架公约",
        "summary": "第80届联合国大会投票通过《全球人工智能监管框架公约》，这是首个具有约束力的AI国际公约。公约设立AI安全评估机制，禁止致命性自主武器系统，并对深度伪造内容标注作出强制性规定。中国、印度和巴西作为共同提案国，呼吁建立AI发展基金帮助发展中国家提升监管能力。",
        "tag": "国际",
        "image_prompt": "United Nations General Assembly hall with delegates voting on regulations, flags of many nations displayed, photorealistic, ultra detailed, 8K, dramatic interior with golden decor"
    },
    {
        "number": "03",
        "title": "上证指数突破4500点 创2015年以来新高",
        "summary": "A股市场延续强势，上证指数大涨2.8%突破4500点关口，深成指涨3.5%，创业板指涨4.2%。两市成交额达2.8万亿元创历史天量。科技股、新能源股和消费股轮番拉升，北向资金净买入超500亿元。分析师表示政策宽松和基本面改善共振，市场有望继续震荡上行。",
        "tag": "金融",
        "image_prompt": "Stock market trading floor with massive LED screens showing stock indices rising dramatically, photorealistic, ultra detailed, 8K, traders celebrating"
    },
    {
        "number": "04",
        "title": "比亚迪第1000万辆新能源汽车正式下线",
        "summary": "比亚迪在深圳总部举行第1000万辆新能源汽车下线仪式，该车为仰望U9豪华电动跑车。从500万到1000万辆，比亚迪仅用时18个月，刷新全球新能源汽车产销纪录。王传福表示将投入1000亿元研发固态电池和智能驾驶技术，计划2027年实现固态电池车型量产。",
        "tag": "科技",
        "image_prompt": "Modern electric car factory assembly line with humanoid robots, photorealistic, ultra detailed, 8K, sleek electric vehicle rolling off production line with celebration"
    },
    {
        "number": "05",
        "title": "中国数字贸易额首超美国跃居全球第一",
        "summary": "商务部数据显示上半年中国数字贸易进出口总额达3.8万亿元，首次超越美国成为全球最大数字贸易国。跨境电商、数字服务出口和数字技术贸易均实现两位数增长。TikTok、Temu和阿里国际站位列跨境电商前三，数字支付、云服务和AI大模型出口增速超过50%。",
        "tag": "经济",
        "image_prompt": "Global digital trade network with connection lines between countries, photorealistic, ultra detailed, 8K, futuristic visualization of international e-commerce"
    },
    {
        "number": "06",
        "title": "微信鸿蒙版正式上线 全面支持原生鸿蒙应用",
        "summary": "腾讯发布微信鸿蒙版正式版，这是完全基于HarmonyOS NEXT开发的原生应用，不再兼容安卓。鸿蒙版微信在内存占用和电池续航上优化超过40%，并首发微信小店、微信直播等功能。腾讯表示鸿蒙版微信用户已突破5000万，将持续优化小程序和支付功能。",
        "tag": "科技",
        "image_prompt": "Smartphone displaying a messaging app with HarmonyOS interface, photorealistic, ultra detailed, 8K, modern tech product launch event with blue lighting"
    },
    {
        "number": "07",
        "title": "神舟二十号成功对接中国空间站",
        "summary": "神舟二十号载人飞船在酒泉卫星中心发射升空，经过6小时自主快速交会对接，成功与天宫空间站天和核心舱径向端口对接。三名航天员将在轨驻留6个月，开展空间科学实验和舱外活动。任务期间将首次使用国产星载激光通信终端，实现与地面的10Gbps高速数据传输。",
        "tag": "科技",
        "image_prompt": "Chinese spacecraft docking with space station in orbit, Earth visible in background, photorealistic, ultra detailed, 8K, dramatic space scene with solar panels"
    },
    {
        "number": "08",
        "title": "全国多地上调最低工资标准 最高涨幅达20%",
        "summary": "北京、上海、浙江等15个省市同步上调最低工资标准，平均涨幅约15%，最高涨幅达20%。北京将月最低工资调至3000元，上海为2950元，均创历史新高。人社部表示此次调整旨在保障劳动者权益，促进消费升级，预计将惠及超过5000万低收入劳动者。",
        "tag": "社会",
        "image_prompt": "Urban street scene with diverse working people, construction workers and service staff, photorealistic, ultra detailed, 8K, prosperous modern city with people going to work"
    },
    {
        "number": "09",
        "title": "中德总理会晤达成系列合作协议",
        "summary": "国务院总理在柏林与德国总理举行会谈，双方签署涵盖新能源汽车、自动驾驶、绿色氢能和文化交流的20项合作文件。德方承诺不对从中国进口电动汽车加征额外关税，中方表示将扩大从德国进口高端设备和技术。双方同意建立中德AI对话机制，深化国际热核聚变实验堆合作。",
        "tag": "国际",
        "image_prompt": "Chinese and German leaders shaking hands in formal diplomatic meeting, photorealistic, ultra detailed, 8K, formal diplomatic meeting room with delegations"
    },
    {
        "number": "10",
        "title": "《王者荣耀》国际版全球用户突破5亿",
        "summary": "腾讯游戏宣布《王者荣耀》国际版（Honor of Kings）全球注册用户突破5亿，正式超越《英雄联盟》成为全球最受欢迎的MOBA手游。国际版收入同比增长120%，在东南亚、中东和拉美市场表现尤为强劲。腾讯宣布将在洛杉矶设立游戏工作室，负责国际版IP的影视化开发。",
        "tag": "文化",
        "image_prompt": "E-sports arena with gamers playing mobile game on stage, photorealistic, ultra detailed, 8K, colorful gaming tournament with audience cheering"
    },
    {
        "number": "11",
        "title": "中国自主设计客机C919单月交付量首破10架",
        "summary": "中国商飞公布C919大型客机最新交付数据，6月单月交付量首次突破10架，累计交付量已达58架。东航、国航和南航均表示C919运营表现良好，平均客座率超过85%。中国商飞宣布启动C919增程型研发，航程将从5500公里提升至7500公里，计划2028年取证。",
        "tag": "经济",
        "image_prompt": "Chinese homemade passenger aircraft taking off from runway, photorealistic, ultra detailed, 8K, dramatic aviation scene with blue sky"
    },
    {
        "number": "12",
        "title": "蓝色起源完成首次商业空间站对接任务",
        "summary": "蓝色起源New Glenn火箭成功执行首次商业空间站对接任务，将4名私人宇航员送达轨道前沿站。任务持续10天，宇航员在轨开展微重力实验和太空 tourism体验。贝索斯宣布2027年起将推出商业空间站旅游航班，票价约3500万美元，首批预订客户已超过200人。",
        "tag": "科技",
        "image_prompt": "Commercial space station with tourists in spacesuits floating inside, photorealistic, ultra detailed, 8K, futuristic space tourism interior with Earth view"
    },
    {
        "number": "13",
        "title": "人民币跨境支付系统CIPS日交易额首破3万亿",
        "summary": "跨境银行间支付系统（CIPS）数据显示，人民币跨境支付日均交易额首次突破3万亿元，同比增长35%。参与机构覆盖109个国家和地区，人民币在全球支付占比升至8.5%。数字人民币跨境支付占比达25%，大幅提升了清算效率。中国推动的金砖国家本币结算体系已覆盖70%成员国贸易。",
        "tag": "金融",
        "image_prompt": "Global financial center with glowing trading screens showing currency symbols, photorealistic, ultra detailed, 8K, futuristic banking hall with digital displays"
    },
    {
        "number": "14",
        "title": "教育部发布AI教育规划 将在中小学全面开设AI课程",
        "summary": "教育部发布《人工智能教育发展行动计划》，要求全国中小学从2027年秋季学期起全面开设AI必修课。课程涵盖编程基础、机器学习原理和AI伦理等内容。教育部将建立AI教材审订机制，投入200亿元建设智慧校园和AI实验室，师范类大学AI师资培养规模将扩大至每年10万人。",
        "tag": "社会",
        "image_prompt": "School classroom with students learning AI and robotics, interactive smart boards, photorealistic, ultra detailed, 8K, modern educational environment with children engaged"
    },
    {
        "number": "15",
        "title": "英伟达发布下一代GPU架构 算力提升5倍",
        "summary": "英伟达在GTC大会上发布Blackwell Ultra GPU架构，H200继任者算力提升5倍达到40PFLOPS（FP8）。新架构采用Chiplet封装和HBM4内存，能效比提升3倍。黄仁勋表示该芯片将全面支持Agent AI和物理AI训练，全球八大云厂商已下单超过200亿美元。中国市场受限出口管制，但水货价格已炒至5万美元。",
        "tag": "科技",
        "image_prompt": "Next generation GPU chip on circuit board with dramatic lighting, photorealistic, ultra detailed, 8K, futuristic technology product reveal stage"
    },
    {
        "number": "16",
        "title": "中国网球公开赛决赛 中国选手首夺女单冠军",
        "summary": "中国网球公开赛女单决赛在国家网球中心落幕，22岁的中国小将郑钦文以2-1击败世界第三萨巴伦卡，首夺中网女单冠军。这是李娜之后中国选手再次捧起中网冠军奖杯。郑钦文世界排名将升至第8位，创造中国球员历史新高。现场12000名观众齐声高唱《我和我的祖国》。",
        "tag": "体育",
        "image_prompt": "Tennis champion holding trophy with confetti celebration, photorealistic, ultra detailed, 8K, crowded stadium with cheering fans"
    },
    {
        "number": "17",
        "title": "黄河古贤水利枢纽工程正式开工建设",
        "summary": "黄河古贤水利枢纽工程在陕西山西交界处正式开工，这是黄河干流又一重大控制性工程。大坝高180米，总库容380亿立方米，可将黄河下游防洪标准提升至千年一遇。工程还将改善黄河中游航运条件，年发电量达100亿度。生态环境部要求施工方全面落实黄河生态保护措施。",
        "tag": "社会",
        "image_prompt": "Large dam and reservoir under construction on a river, photorealistic, ultra detailed, 8K, massive engineering project with cranes and workers in mountainous area"
    },
    {
        "number": "18",
        "title": "苹果发布iPhone 18系列 搭载自研AI神经芯片",
        "summary": "苹果在全球开发者大会上发布iPhone 18系列，首次搭载自研AI神经处理芯片Neural A18，算力达每秒50万亿次操作。新系列全面支持离线AI助手和实时翻译，电池续航提升至30小时。苹果宣布与OpenAI合作引入ChatGPT-5能力，但中国区版本将由百度文心一言提供AI支持。",
        "tag": "科技",
        "image_prompt": "Apple iPhone launch event with dramatic product reveal, photorealistic, ultra detailed, 8K, sleek smartphone with holographic AI interface display"
    },
    {
        "number": "19",
        "title": "中巴经济走廊建设完成 贸易额突破500亿美元",
        "summary": "中巴经济走廊最后一个重点项目瓜达尔港扩建工程竣工，标志着走廊建设全面完成。走廊累计投资超过620亿美元，创造就业岗位75万个。双边贸易额突破500亿美元，巴基斯坦对华出口增长45%。双方签署走廊二期规划，重点建设产业园区和数字丝绸之路合作项目。",
        "tag": "经济",
        "image_prompt": "Modern port with container cranes and cargo ships at dusk, photorealistic, ultra detailed, 8K, busy international trade port with lights"
    },
    {
        "number": "20",
        "title": "中国科学家实现室温超导材料重大突破",
        "summary": "复旦大学团队在《自然》杂志发表论文，宣布首次实现常压室温超导，临界温度达28摄氏度。该材料采用氢化镥体系，在室温和常压下即实现零电阻特性。实验结果已通过全球10个实验室独立验证。业内认为这是百年物理学的重大里程碑，将颠覆电力传输、交通和计算行业。",
        "tag": "科技",
        "image_prompt": "Scientists in laboratory observing superconducting material with glowing effect at room temperature, photorealistic, ultra detailed, 8K, advanced physics research facility"
    }
]

def generate_image_cogview(prompt, output_path, retry=2):
    """Generate image using CogView-3-Flash API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    for attempt in range(retry + 1):
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=120)
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0]["message"]
                content = message.get("content", [])
                
                # Content is a list with URL objects
                if isinstance(content, list) and len(content) > 0:
                    url = content[0].get("url", "")
                    if url:
                        # Download the image
                        img_response = requests.get(url, timeout=120)
                        if img_response.status_code == 200:
                            with open(output_path, 'wb') as f:
                                f.write(img_response.content)
                            print(f"✓ Saved: {output_path}")
                            return True
                
                # Check for error in response
                if "error" in result:
                    print(f"✗ API Error: {result['error']}")
                    time.sleep(2)
                    continue
                
                print(f"✗ Unexpected content format: {content}")
                
        except Exception as e:
            print(f"✗ Error generating {output_path}: {e}")
        
        if attempt < retry:
            print(f"  Retry {attempt + 1}/{retry}...")
            time.sleep(3)
    
    return False

def main():
    # Create images directory if not exists
    os.makedirs("/home/swg/.openclaw/workspace/news-blog/images", exist_ok=True)
    
    # Save news data
    news_file = f"/home/swg/.openclaw/workspace/news-blog/news_data_{DATE}.json"
    with open(news_file, 'w', encoding='utf-8') as f:
        json.dump(NEWS_DATA, f, ensure_ascii=False, indent=2)
    print(f"Saved news data: {news_file}")
    
    # Generate all images
    print(f"\nGenerating {len(NEWS_DATA)} images...")
    success_count = 0
    
    for news in NEWS_DATA:
        img_num = news["number"].zfill(2)
        output_path = f"/home/swg/.openclaw/workspace/news-blog/images/news_{DATE}_{img_num}.png"
        success = generate_image_cogview(news["image_prompt"], output_path)
        if success:
            success_count += 1
        time.sleep(2)  # Rate limiting
    
    print(f"\n✓ Generated {success_count}/{len(NEWS_DATA)} images")
    
    if success_count == len(NEWS_DATA):
        print("All images generated successfully!")
    else:
        print(f"Warning: {len(NEWS_DATA) - success_count} images failed")
    
    return success_count

if __name__ == "__main__":
    main()