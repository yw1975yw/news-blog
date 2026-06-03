#!/usr/bin/env python3
"""Generate 20 news items for 2026年06月04日 and corresponding images via CogView-3-Flash."""

import json
import base64
import urllib.request
import urllib.error
import time
import os
import re

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

TODAY = "2026年06月04日"
IMG_DIR = "/home/swg/.openclaw/workspace/news-blog/images"

news_items = [
    {
        "number": "01",
        "title": "谷歌发布Gemini Ultra 2.0 多模态能力全面超越GPT-5",
        "summary": "谷歌在年度I/O大会上正式发布Gemini Ultra 2.0，该模型在图像理解、视频推理和3D建模等多项测试中刷新世界纪录。支持1000万token超长上下文窗口，可一次性解析整部高清电影。谷歌同时宣布将Gemini集成至Android 16操作系统，全球超过30亿台设备将率先获得AI能力升级。",
        "tag": "科技",
        "prompt": "A futuristic technology conference stage with a giant holographic display showing neural network visualization, photorealistic, ultra detailed, 8K, high resolution, dramatic lighting, tech keynote setting"
    },
    {
        "number": "02",
        "title": "中国成功发射天舟九号货运飞船 空间站物资补给到位",
        "summary": "中国在文昌航天发射场使用长征七号运载火箭成功发射天舟九号货运飞船，为中国空间站运送超过7吨物资，包括航天员生活用品、科学实验设备和舱外作业工具。此次任务是空间站进入应用与发展阶段后的第三次货运补给，进一步保障在轨航天员的长期驻留需求。",
        "tag": "科技",
        "prompt": "Rocket launching from coastal spaceport at sunset with billowing smoke and bright flame exhaust, cargo spacecraft in flight against blue sky, photorealistic, ultra detailed, 8K, cinematic composition"
    },
    {
        "number": "03",
        "title": "欧盟通过《人工智能责任指令》  AI服务商需承担算法损害责任",
        "summary": "欧洲议会以压倒性多数通过《人工智能责任指令》，规定AI服务提供商须对算法决策造成的公民伤害承担严格责任。指令要求所有在欧盟运营的AI系统必须保留训练数据日志并接受监管机构审查，违规最高罚款可达全球年营业额的6%。",
        "tag": "国际",
        "prompt": "European Parliament building in Brussels illuminated at night with EU flags, photorealistic, ultra detailed, 8K, evening atmosphere with lamp posts, architectural photography"
    },
    {
        "number": "04",
        "title": "比特币重返10万美元关口 加密货币市场迎来新一轮牛市",
        "summary": "比特币价格再度突破10万美元心理大关，创下历史新高，主要受美国比特币现货ETF持续净流入和机构配置增加推动。以太坊同步上涨突破3500美元，整个加密货币市场总市值重返4万亿美元。监管机构提示短期波动风险，投资者应理性看待行情。",
        "tag": "金融",
        "prompt": "Financial trading screens showing cryptocurrency price charts with glowing charts and upward trend, modern trading floor, photorealistic, ultra detailed, 8K, dramatic lighting with blue and green colors"
    },
    {
        "number": "05",
        "title": "中国5月出口同比增长12.6%  新能源汽车和光伏产品领跑",
        "summary": "海关总署公布5月外贸数据，以美元计出口同比增长12.6%，增速较上月加快3个百分点。新能源汽车、锂电池和光伏组件三大类产品合计出口增长超过40%，成为拉动出口的主要引擎。分析指出全球绿色能源转型为中国制造业提供了广阔市场空间。",
        "tag": "经济",
        "prompt": "Modern cargo port with container ships at dock, crane operations loading colorful shipping containers, industrial harbor scene, photorealistic, ultra detailed, 8K, golden hour lighting"
    },
    {
        "number": "06",
        "title": "波士顿动力发布Atlas机器人商业版 工厂自动化进入新阶段",
        "summary": "波士顿动力正式发布Atlas机器人商业版本，售价约20万美元，首批1000台已获得汽车制造和物流企业订单。该机器人具备全身协调运动能力，可完成复杂装配任务，号称全球首款实现规模化商用的全尺寸人形机器人。",
        "tag": "科技",
        "prompt": "Advanced humanoid robot in modern factory environment performing precise assembly task, photorealistic, ultra detailed, 8K, clean white factory interior with robotic arm, cinematic lighting"
    },
    {
        "number": "07",
        "title": "G7峰会就碳边境调节机制达成一致 钢铁铝业面临新贸易规则",
        "summary": "七国集团峰会在加拿大召开，与会国就碳边境调节机制实施细则达成共识，将于2027年起对高碳进口商品征收碳关税。钢铁、铝业和水泥等行业将首先受到冲击，发展中国家呼吁给予更长适应期。",
        "tag": "国际",
        "prompt": "World leaders at G7 summit meeting in elegant conference room with international flags, photorealistic, ultra detailed, 8K, diplomatic atmosphere with formal table setting"
    },
    {
        "number": "08",
        "title": "中国多省份推进无人机配送商业化 深圳上空现外卖无人机机群",
        "summary": "深圳、北京和上海等城市同步推进无人机配送商业化试点，美团和顺丰的无人机配送网络已覆盖主要商圈。用户通过APP下单后可选择无人机配送，30分钟内送达，配送费用与普通快递持平。专家认为无人机配送将成为即时零售的重要补充。",
        "tag": "社会",
        "prompt": "Delivery drones flying in urban sky over modern Chinese city skyline at dusk, photorealistic, ultra detailed, 8K, sunset atmosphere with buildings and flying quadcopters carrying packages"
    },
    {
        "number": "09",
        "title": "英伟达市值突破4万亿美元 成为全球第二大上市公司",
        "summary": "英伟达股价再创新高，市值突破4万亿美元，超越苹果成为全球第二大上市公司。数据中心业务收入同比增长超过200%，Blackwell架构GPU供不应求。黄仁勋表示AI基础设施投资热潮将持续至少五年，公司正加速扩大产能以满足市场需求。",
        "tag": "金融",
        "prompt": "NVIDIA headquarters building with sleek modern architecture, stock market display showing upward arrow, photorealistic, ultra detailed, 8K, corporate campus in Silicon Valley, dramatic sky"
    },
    {
        "number": "10",
        "title": "2026年温布尔登网球锦标赛抽签揭晓 中国金花冲击冠军",
        "summary": "温布尔登网球锦标赛在伦敦举行抽签仪式，中国选手郑钦文作为女单四号种子镇守下半区，首轮对阵法国选手帕里。王曦雨和袁悦也进入正赛签表，中国金花首次有三人同时以种子身份出战大满贯正赛。",
        "tag": "体育",
        "prompt": "Wimbledon tennis championships grass court with players in action, Centre Court at sunset, photorealistic, ultra detailed, 8K, lush green grass, British summer atmosphere, dramatic clouds"
    },
    {
        "number": "11",
        "title": "故宫博物院联合腾讯推出数字汴京展  VR技术再现清明上河图",
        "summary": "故宫博物院与腾讯联合发布"数字汴京"沉浸展，运用VR和体积视频技术将北宋张择端《清明上河图》以数字孪生形式重现。观众可化身画中人物，穿行于汴京城的大街小巷，体验千年之前宋代市井生活。这是数字文旅融合的里程碑式作品。",
        "tag": "文化",
        "prompt": "Ancient Chinese palace museum interior with digital holographic projections of traditional Chinese paintings, visitors experiencing VR exhibition, photorealistic, ultra detailed, 8K, cultural heritage site"
    },
    {
        "number": "12",
        "title": "全国基本养老保险基金委托投资规模突破3万亿元",
        "summary": "人社部宣布全国基本养老保险基金委托投资规模已达3.2万亿元，年化投资收益率约5.8%。基金主要配置于国债、银行存款和指数基金，风险敞口控制在安全区间。人社部表示将稳步推进基金投资市场化运作，确保待遇按时足额发放。",
        "tag": "社会",
        "prompt": "Elderly people in China happily receiving pension benefits at modern bank service counter, photorealistic, ultra detailed, 8K, warm lighting, social security service hall with friendly staff"
    },
    {
        "number": "13",
        "title": "Meta发布Llama 4开源大模型 性能逼近闭源顶级模型",
        "summary": "Meta正式发布Llama 4系列开源大模型，其中旗舰版本在MMLU和HumanEval等基准测试中与GPT-5 Turbo基本持平。Meta宣布Llama 4将完全开源并允许商业免费使用，业界认为这将动摇闭源模型的市场主导地位，推动AI技术普惠化进程。",
        "tag": "科技",
        "prompt": "Meta logo illuminated on modern office building exterior at night, technology campus atmosphere, photorealistic, ultra detailed, 8K, blue and purple neon lighting, digital atmosphere"
    },
    {
        "number": "14",
        "title": "中日韩领导人会议重启 三国同意建立自贸区早期收获安排",
        "summary": "中断三年的中日韩领导人会议在首尔重启，三国发表联合声明，同意启动建立自贸区的早期收获安排，涵盖农产品关税削减和制造业供应链便利化。韩国总统主持会议，中国国务院总理和日本首相出席，三方还就朝鲜半岛局势交换意见。",
        "tag": "国际",
        "prompt": "Three world leaders shaking hands at diplomatic summit meeting in Seoul, international flags in background, photorealistic, ultra detailed, 8K, formal diplomatic setting, warm handshake moment"
    },
    {
        "number": "15",
        "title": "小米汽车月交付量突破3万辆  SU10系列推动新能源下沉市场",
        "summary": "小米汽车公布5月交付数据，SU7和SU10系列合计交付3.2万辆，环比增长35%。其中SU10起售价14.99万元，瞄准二三线城市家庭用户，订单排期已至2027年。小米汽车正加速扩产，北京工厂第二条产线即将投产，年产能有望达30万辆。",
        "tag": "社会",
        "prompt": "Modern electric vehicle charging station with sleek小米car at charging point in Chinese urban environment, photorealistic, ultra detailed, 8K, clean modern setting with green energy concept"
    },
    {
        "number": "16",
        "title": "上海原油期货主力合约成交量创新高 亚太原油定价权持续增强",
        "summary": "上海原油期货主力合约单日成交突破200万手，创品种上市以来新高，持仓量达80万手。境外投资者交易占比升至32%，人民币原油期货的亚太基准价功能持续强化。业内外人士指出上海原油期货正成为亚太地区原油贸易的重要参考。",
        "tag": "金融",
        "prompt": "Shanghai financial district skyline with Pudong towers at night reflected in river, photorealistic, ultra detailed, 8K, dramatic skyline with illuminated buildings, Huangpu River scene"
    },
    {
        "number": "17",
        "title": "国际期刊撤稿数量创历史新高  科研诚信问题引发广泛关注",
        "summary": "全球学术出版联盟报告显示，2025年全球期刊撤稿数量超过1.2万篇，创历史新高，其中约70%涉及图片造假和数据篡改。多国科研管理机构联合推出"科研诚信2026行动计划"，建立全球论文造假黑名单数据库，对违规科研人员实施跨机构联合惩戒。",
        "tag": "社会",
        "prompt": "Scientific research laboratory with researcher examining papers and laptop showing rejection notice, photorealistic, ultra detailed, 8K, academic office setting with books and scientific equipment"
    },
    {
        "number": "18",
        "title": "阿根廷成为金砖国家正式成员 南南合作开启新篇章",
        "summary": "金砖国家宣布阿根廷正式完成入盟程序，成为该组织第十个成员。阿根廷总统米莱表示加入金砖是外交多元化战略的重要组成，将深化与亚非拉伙伴的经贸合作。金砖国家GDP总量在全球占比升至38%，对现行国际经济秩序的影响力进一步扩大。",
        "tag": "国际",
        "prompt": "International summit meeting with diverse world leaders from BRICS countries, flags of participating nations, photorealistic, ultra detailed, 8K, diplomatic conference hall with global leaders"
    },
    {
        "number": "19",
        "title": "OpenAI员工联合创始人家属成立新AI实验室 专注AI安全研究",
        "summary": "多位OpenAI前员工和创始人家属联合宣布成立非营利AI研究实验室Nexus AI，初始融资10亿美元，致力于AGI安全和对齐研究。实验室承诺所有研究成果完全开源，并建立独立伦理委员会监督研究方向，号称打造AI时代的"红灯笼"安全防线。",
        "tag": "科技",
        "prompt": "Modern AI research laboratory interior with scientists working at computers analyzing neural network data on large displays, photorealistic, ultra detailed, 8K, clean high-tech research environment"
    },
    {
        "number": "20",
        "title": "中国科学家实现量子加密通信产业化 京沪干线和城市网络同步启用",
        "summary": "中国科学技术大学和国盾量子联合宣布，量子加密通信正式实现产业化，北京至上海量子保密通信干线投入运营，同时北京、合肥等10个城市量子城域网全面启用。量子密钥分发速率提升10倍，可为金融、政务和军事通信提供理论上不可破解的加密保障。",
        "tag": "科技",
        "prompt": "Chinese scientists in quantum computing laboratory with advanced quantum hardware and optical instruments, photorealistic, ultra detailed, 8K, high-tech research facility with blue laser beams, futuristic atmosphere"
    }
]

def generate_image(prompt, output_path, retry=True):
    """Generate image via CogView-3-Flash API."""
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}, photorealistic, ultra detailed, 8K, high resolution"}]
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            
            # Extract base64 image data
            if "data:image/png;base64," in content:
                b64_data = content.split("data:image/png;base64,")[1]
            elif "data:image/jpeg;base64," in content:
                b64_data = content.split("data:image/jpeg;base64,")[1]
            else:
                b64_data = content
            
            img_data = base64.b64decode(b64_data)
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"  [OK] {output_path}")
            return True
    except Exception as e:
        print(f"  [ERROR] {output_path}: {e}")
        if retry:
            print(f"  [RETRY] Retrying {output_path}...")
            time.sleep(3)
            return generate_image(prompt, output_path, retry=False)
        return False

# Create output dir
os.makedirs(IMG_DIR, exist_ok=True)

# Generate all 20 images
print(f"Generating images for {TODAY}...")
results = []
for i, item in enumerate(news_items):
    num = item["number"]
    img_path = f"{IMG_DIR}/news_20260604_{num}.png"
    print(f"[{i+1}/20] Generating news_{num}...")
    ok = generate_image(item["prompt"], img_path)
    results.append((item, img_path, ok))
    time.sleep(1)  # Rate limit protection

print("\nGeneration complete:")
for item, path, ok in results:
    status = "✓" if ok else "✗"
    print(f"  {status} news_{item['number']}: {item['title']}")

failed = [(item, path) for item, path, ok in results if not ok]
if failed:
    print(f"\nFailed: {len(failed)} images")
    for item, path in failed:
        print(f"  - {item['title']}")
else:
    print("\nAll 20 images generated successfully!")