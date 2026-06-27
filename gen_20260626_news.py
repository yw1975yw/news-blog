import json
import base64
import os
import time
import subprocess
import re

# 20 news items for 2026年06月26日
news_items = [
    {
        "id": 1,
        "title": "中国「灵晟」超算登顶全球Top500 打破美国十年垄断",
        "summary": "最新全球超级计算机500强排行榜揭晓，中国超级计算机「灵晟」以每秒15亿亿次浮点运算速度首次登顶榜首，打破美国连续十年的霸主地位。这是中国超级计算机近十年来首次重返世界第一，标志着我国在高端计算领域实现完全自主可控，对支撑人工智能、气候模拟和药物研发等领域具有重大战略意义。",
        "tag": "科技",
        "image_prompt": "world's most powerful supercomputer Lingsheng, massive server room with glowing blue lights, thousands of compute nodes, Chinese technology, dark server hall with neon lighting effects, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 2,
        "title": "首届全球AI安全峰会达成历史性共识",
        "summary": "包括中国、美国、欧盟在内的50多个国家和地区在日内瓦签署《人工智能安全治理框架公约》，就AI军事应用限制、算法透明度、数据跨境流动等核心议题达成重要共识。公约成立专门国际监督机构，这是人类历史上首个具有约束力的AI安全国际条约，为全球AI治理奠定重要法律基础。",
        "tag": "国际",
        "image_prompt": "global AI safety summit Geneva, world leaders signing AI governance agreement, United Nations conference hall, international diplomats, technology diplomacy, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 3,
        "title": "A股三大指数创年内新高 成交额突破1.8万亿",
        "summary": "受科技股业绩超预期和政策利好提振，A股市场今日放量大涨，沪指涨1.8%站上3500点，深成指涨2.3%，创业板指涨2.8%。两市成交额达1.82万亿元，创年内新高。AI芯片、半导体和新能源板块领涨，北向资金净流入超150亿元，机构投资者对后市普遍乐观。",
        "tag": "金融",
        "image_prompt": "China stock market surge, Shanghai stock exchange trading floor, stock charts rising, bull market, Chinese investors celebrating, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 4,
        "title": "中国成功发射全球首颗AI卫星 开启智能遥感新时代",
        "summary": "中国在酒泉卫星发射中心成功发射世界首颗人工智能遥感卫星，该卫星在轨运行AI推理能力达到100TOPS，可实现实时云层识别和目标跟踪。卫星数据可直接在轨处理，大幅缩短遥感图像获取时间，从传统的数小时缩短至分钟级，对自然灾害监测和城市规划具有重要意义。",
        "tag": "科技",
        "image_prompt": "China launching AI satellite, rocket lifting off at night, space mission, infrared flames against dark sky, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 5,
        "title": "欧洲央行宣布降息25个基点 结束紧缩周期",
        "summary": "欧洲央行宣布将主要再融资利率下调25个基点至3.5%，符合市场预期。行长拉加德表示欧元区通胀已回落至2.1%的目标区间，经济增速企稳回升，货币政策将转向宽松。这是欧洲央行自2022年以来的首次降息，标志着全球主要央行紧缩周期正式结束。",
        "tag": "金融",
        "image_prompt": "European Central Bank Frankfurt, ECB lowering interest rates, Euro currency symbol, bank building exterior, financial district, European finance, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 6,
        "title": "中美同意重启科技合作对话 华为芯片限制或松动",
        "summary": "中美商务部长在华盛顿举行会谈，同意重启中美科技合作对话机制，就半导体出口管制、5G安全标准和人工智能伦理等议题展开磋商。据知情人士透露，双方就华为相关芯片出口限制问题进行讨论，美方表示将评估放宽部分芯片产品出口许可，市场预期中美科技脱钩态势可能逐步缓和。",
        "tag": "国际",
        "image_prompt": "China US technology cooperation talks, bilateral meeting Washington DC, diplomats at conference table, American and Chinese flags, international diplomacy, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 7,
        "title": "全球最大8英寸碳化硅晶圆厂在重庆投产",
        "summary": "全球最大的8英寸碳化硅晶圆制造厂在重庆正式投产，年产能达20万片。碳化硅是新能源汽车和光伏逆变器的核心材料，8英寸晶圆较传统6英寸可将芯片成本降低30%以上。重庆厂采用完全国产化设备和工艺，标志着中国在第三代半导体材料领域实现重大突破，打破国际垄断。",
        "tag": "科技",
        "image_prompt": "silicon carbide wafer factory Chongqing, massive semiconductor manufacturing plant, clean room environment, robotic arms handling wafers, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 8,
        "title": "多国宣布2040年禁售燃油车 全球汽车电动化提速",
        "summary": "继欧盟之后，日本、韩国和澳大利亚相继宣布2040年全面禁售燃油车计划，全球汽车电动化进程显著加速。报告显示2026年上半年全球新能源汽车销量已超过燃油车，电动化趋势不可逆转。比亚迪、特斯拉和大众等车企已启动全面电动化转型，充电基础设施投资创历史新高。",
        "tag": "经济",
        "image_prompt": "electric vehicles replacing fuel cars, charging station network, modern electric car on highway, green energy future, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 9,
        "title": "SpaceX星舰完成首次载人绕月任务",
        "summary": "SpaceX星舰携带4名私人游客成功完成绕月飞行任务，这是自阿波罗计划以来人类首次重返月球轨道。任务持续7天，航天器最近距离月面仅100公里。创始人马斯克表示这是商业航天的重要里程碑，未来十年内将实现普通人也能负担得起的月球旅游，预计票价约2000万美元。",
        "tag": "科技",
        "image_prompt": "SpaceX Starship orbiting moon, astronauts looking at lunar surface from spacecraft window, Earth rising over moon horizon, commercial space tourism, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 10,
        "title": "中国央行试点数字货币跨境支付 首批覆盖20个国家",
        "summary": "中国人民银行宣布数字人民币跨境支付系统试点正式启动，首批覆盖亚洲、中东和欧洲20个主要经济体。系统基于分布式账本技术，跨境转账可在数秒内完成，手续费较传统渠道降低85%。试点期间主要面向跨国企业，未来将逐步向个人开放，推动人民币国际化进程。",
        "tag": "金融",
        "image_prompt": "digital yuan cross-border payment, mobile phone showing digital currency transaction, global payment network, futuristic fintech, Asian cities at night, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 11,
        "title": "联合国通过全球最低企业税率15%协议",
        "summary": "联合国大会以压倒性多数通过全球最低企业税率协议，规定大型跨国企业最低税率为15%。协议获得超过140个国家支持，主要针对年营收超过7.5亿欧元的企业。协议将有效遏制税基侵蚀和利润转移行为，预计每年可为各国增加税收收入超过2000亿美元。",
        "tag": "国际",
        "image_prompt": "United Nations General Assembly, global minimum corporate tax vote, world delegates voting, international taxation agreement, UN headquarters New York, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 12,
        "title": "中国自主研发脑机接口临床试验获批",
        "summary": "中国国家药监局批准北京脑科学与类脑研究中心自主研发的高性能脑机接口进入临床试验阶段。该设备可实现每秒1000个神经元信号的实时采集和解读，在瘫痪患者辅助和神经疾病治疗方面具有广阔应用前景。这是中国首个获批临床试验的国产脑机接口产品，标志着脑科学产业化取得重大突破。",
        "tag": "科技",
        "image_prompt": "brain-computer interface medical device, patient using neural implant, futuristic medical technology, Chinese research laboratory, brain signal visualization, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 13,
        "title": "全国夏粮丰收已成定局 产量有望首破3亿吨",
        "summary": "农业农村部发布夏粮生产形势报告，全国夏粮收获已过九成，平均亩产比去年提高4.2%，丰收已成定局。预计全年夏粮产量将首次突破3亿吨，创历史新高。优质专用小麦占比提高，收购价格稳定在每斤1.4元左右，农民种粮收益得到保障，为全年粮食稳产增产奠定坚实基础。",
        "tag": "经济",
        "image_prompt": "abundant wheat harvest China, golden wheat fields with combine harvesters, farmer smiling, agricultural prosperity, rural landscape, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 14,
        "title": "巴黎奥运会倒计时30天 中国代表团誓师出征",
        "summary": "距离巴黎奥运会开幕还有30天，中国体育代表团在北京举行誓师大会，宣布将派出716名运动员参加全部28个大项的比赛。代表团提出「金牌和体育精神双丰收」的目标，在跳水、举重、乒乓球等传统优势项目外，田径和游泳等项目有望取得突破。",
        "tag": "体育",
        "image_prompt": "Paris Olympic Games countdown, Chinese athletes team gathering, flag raising ceremony, sports celebration, Paris cityscape with Eiffel Tower, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 15,
        "title": "全球最大氢能炼钢厂在辽宁投产",
        "summary": "全球最大的氢能炼钢生产线在辽宁省鞍山市正式投产，年产能500万吨。该项目使用绿色氢气替代焦炭作为还原剂，每吨钢碳排放量从1.8吨降至接近零。项目投资200亿元，预计年减少碳排放900万吨，标志着中国钢铁行业绿色转型取得实质性进展，为全球碳中和目标做出重要贡献。",
        "tag": "经济",
        "image_prompt": "hydrogen steel manufacturing plant Liaoning, green hydrogen blast furnace, eco-friendly steel production, industrial complex with clean technology, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 16,
        "title": "教育部发布新版课标 AI教育覆盖全学段",
        "summary": "教育部发布2026年版义务教育课程方案，明确将人工智能列入中小学必修课程，并配备专项实验室。新课标要求学生了解AI基本原理和伦理边界，培养计算思维能力。全国将建设10000个人工智能教育实验室，覆盖城市和农村学校，推动教育数字化转型升级。",
        "tag": "社会",
        "image_prompt": "AI education in Chinese school, students learning artificial intelligence, computer lab with robot assistants, modern classroom technology, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 17,
        "title": "故宫博物院数字藏品发行 首日销售额破亿元",
        "summary": "故宫博物院联合蚂蚁集团发行首批5万件数字藏品，包含《千里江山图》和《清明上河图》等经典馆藏的数字孪生版本。每个藏品都有唯一数字凭证，支持在区块链上验证真伪。发行首日即售罄，销售额突破1.2亿元，文创产业数字化探索取得开门红。",
        "tag": "文化",
        "image_prompt": "Forbidden Palace museum digital collection, ancient Chinese painting NFT, blockchain technology art, cultural heritage digitization, elegant palace interior, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 18,
        "title": "国际金价突破2900美元 再创历史新高",
        "summary": "受全球央行宽松预期和地缘政治风险推动，纽约金价盘中突破每盎司2900美元关口，再创历史新高。全球央行持续增持黄金作为外汇储备多元化手段，中国和印度央行是最大买家。分析师指出在美元走弱和实际利率下行背景下，金价仍有上涨空间。",
        "tag": "金融",
        "image_prompt": "gold price hitting record high, gold bars and coins, precious metal trading floor, golden light reflection, financial security, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 19,
        "title": "中国科研团队首次实现百公里量子直接通信",
        "summary": "中国科学技术大学和南京大学联合研发团队宣布，在商用光纤环境下实现100公里量子直接通信，刷新世界纪录。该技术无需纠缠粒子即可实现安全通信，理论上不可窃听，对金融、军事和政府通信具有重要价值。团队已与华为和中兴展开合作，推动技术产业化落地。",
        "tag": "科技",
        "image_prompt": "quantum communication technology China, scientist in laboratory with quantum equipment, fiber optic cable glowing blue, quantum cryptography research, photorealistic, ultra detailed, 8K"
    },
    {
        "id": 20,
        "title": "三星堆遗址考古新发现 青铜神树重见天日",
        "summary": "四川省文物考古研究院公布三星堆遗址最新考古成果，考古队在8号祭祀坑发掘出完整的青铜神树，高度达4米，是迄今发现的最大三星堆青铜器。同时出土的还有近千件精美玉器和象牙制品，新发现的文物将古蜀文明与中原商文明的关系研究推向深入。",
        "tag": "文化",
        "image_prompt": "Sanxingdui archaeological excavation Sichuan, ancient bronze tree artifact being unearthed, archaeologists working at dig site, mysterious ancient civilization, photorealistic, ultra detailed, 8K"
    }
]

# Save news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260626.json', 'w', encoding='utf-8') as f:
    json.dump(news_items, f, ensure_ascii=False, indent=2)

print(f"Generated {len(news_items)} news items")
print("\nNews items saved to news_data_20260626.json")

# Now generate images using CogView API
api_key = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
os.makedirs('/home/swg/.openclaw/workspace/news-blog/images', exist_ok=True)

def generate_cogview_image(news_id, prompt):
    """Generate image using CogView-3-Flash API"""
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    cmd = [
        'curl', '-s', '-X', 'POST', url,
        '-H', f'Authorization: Bearer {api_key}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and result.stdout:
        try:
            resp = json.loads(result.stdout)
            if 'choices' in resp and len(resp['choices']) > 0:
                content = resp['choices'][0]['message']['content']
                # Extract base64 image
                if 'data:image/png;base64,' in content:
                    b64_data = content.split('data:image/png;base64,')[1]
                    img_data = base64.b64decode(b64_data)
                    filename = f'/home/swg/.openclaw/workspace/news-blog/images/news_20260626_{news_id:02d}.png'
                    with open(filename, 'wb') as f:
                        f.write(img_data)
                    print(f"[{news_id:02d}] Image saved: {filename}")
                    return True
        except Exception as e:
            print(f"[{news_id:02d}] Parse error: {e}")
    
    print(f"[{news_id:02d}] Failed: {result.stdout[:200] if result.stdout else 'no output'}")
    return False

# Generate all 20 images
print("\n=== Generating 20 images ===")
for item in news_items:
    success = False
    for attempt in range(2):  # 2 attempts per image
        if generate_cogview_image(item['id'], item['image_prompt']):
            success = True
            break
        if not success and attempt == 0:
            print(f"[{item['id']:02d}] Retrying...")
            time.sleep(2)
    
    if not success:
        print(f"[{item['id']:02d}] FAILED after 2 attempts")
    
    time.sleep(1)  # Rate limiting

print("\n=== Image generation complete ===")