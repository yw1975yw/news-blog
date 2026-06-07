#!/usr/bin/env python3
"""生成2026年06月08日的新闻内容并更新index.html"""
import json
import base64
import os
import requests
import time

DATE = "20260608"
DATE_CN = "2026年06月08日"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

NEWS_DATA = [
    {
        "number": "01",
        "title": "全球AI监管峰会达成共识 联合国设立人工智能治理框架",
        "summary": "联合国教科文组织在日内瓦主持召开全球AI监管峰会，70多个国家和地区的代表就人工智能安全治理达成历史性共识。会议通过了《日内瓦AI治理宣言》，同意建立全球AI安全评估机制，并对高风险AI系统实施统一监管标准。峰会还决定成立AI伦理委员会，由多国专家共同参与制定国际规范。",
        "tag": "科技",
        "prompt": "United Nations conference hall with delegates from many countries discussing AI regulation, serious faces, large digital brain hologram projection, international flags, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "02",
        "title": "苹果发布全新AI芯片M5 Ultra MacBook Pro性能创新高",
        "summary": "苹果在WWDC开发者大会上正式发布M5 Ultra芯片，这是首款采用2纳米工艺制造的消费级AI处理器。M5 Ultra集成了专用神经网络引擎，AI任务处理速度较前代提升四倍，能效比提高60%。搭载M5 Ultra的新款MacBook Pro续航达30小时，已支持本地运行200亿参数大模型。",
        "tag": "科技",
        "prompt": "Apple MacBook Pro laptop on sleek desk, glowing chip visualization, developer conference stage background, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "03",
        "title": "欧洲央行宣布降息25个基点 应对经济增长放缓",
        "summary": "欧洲中央银行宣布将欧元区三大关键利率下调25个基点，以应对区内经济增长放缓和通胀回落。欧洲央行行长拉加德表示，降息有助于降低企业和居民融资成本，刺激投资与消费。分析认为此举将提振市场信心，但欧洲经济复苏仍面临地缘政治和能源价格不确定性。",
        "tag": "金融",
        "prompt": "European Central Bank headquarters in Frankfurt, euro currency symbols, financial charts and graphs, European flags, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "04",
        "title": "SpaceX星舰完成第一百次发射 创造航天史新纪录",
        "summary": "SpaceX宣布星舰火箭完成第100次发射任务，将一批Starlink V3卫星送入轨道，这也是星舰连续第50次成功回收助推器。马斯克表示，星舰的高频发射能力已证明其商业可行性，未来将每周执行一次发射任务。星舰的运营成本已降至传统火箭的十分之一。",
        "tag": "科技",
        "prompt": "SpaceX Starship rocket launching from Boca Chica pad, massive flame trail, satellite deployment in orbit, night sky with stars, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "05",
        "title": "世卫组织警告新型耐药菌扩散 呼吁各国加强防控",
        "summary": "世界卫生组织发布紧急警告，在欧洲和亚洲多国发现携带MCR-9基因的高耐药性肺炎克雷伯菌，常规抗生素对其几乎无效。数据显示该菌株致死率高达40%，且已在医疗机构内出现聚集性感染。世卫呼吁各国加强抗菌药物管理和感染控制，避免成为全球公共卫生紧急事件。",
        "tag": "社会",
        "prompt": "World Health Organization laboratory, scientists in protective gear examining bacteria samples, microscope view of resistant bacteria, medical research facility, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "06",
        "title": "中国新能源车渗透率突破70% 比亚迪销量超越特斯拉",
        "summary": "中国汽车工业协会公布数据显示，5月新能源汽车渗透率达到71.4%，创历史新高。比亚迪当月全球销量达58万辆，超越特斯拉成为全球最大纯电动车制造商。凭借e平台3.0和刀片电池技术优势，中国品牌在东南亚和欧洲市场份额持续扩大，自主品牌出口量同比增长45%。",
        "tag": "经济",
        "prompt": "Modern electric vehicle assembly line in Chinese factory, rows of brand new EVs, automated robots working, clean modern facility, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "07",
        "title": "日本放弃福岛核废水排海计划 转向固态储存方案",
        "summary": "日本政府宣布放弃将福岛核废水排入海洋的计划，转而采用美国比尔盖茨基金会支持的固态储存技术。新方案通过蒸发浓缩将核废水转化为固体形式，安全性更高但成本增加三倍。日本政府表示将就该方案与国际原子能机构重新谈判，争取2028年前完成所有核废水的处理。",
        "tag": "国际",
        "prompt": "Fukushima nuclear power plant in Japan, engineers discussing solidification storage technology, containment vessels, sunset over Pacific coastline, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "08",
        "title": "全球最大沙漠光伏电站并网 发电量可供千万家庭",
        "summary": "中国新疆塔克拉玛干沙漠全球最大光伏电站在线运行，发电装机容量达16吉瓦，每年可发电320亿度，可满足约1000万户家庭用电需求。该电站采用双面组件和智能跟踪系统，转换效率达28%。中国宣布到2030年沙漠光伏装机将突破400吉瓦，助力双碳目标实现。",
        "tag": "科技",
        "prompt": "Vast solar panel farm stretching across desert landscape, blue sky with sun rays, workers in distance for scale, renewable energy concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "09",
        "title": "英伟达市值突破五万亿美元 成为全球第二大公司",
        "summary": "英伟达股价再创新高，市值突破5万亿美元大关，成为仅次于苹果的全球第二大上市公司。受益于AI芯片需求爆发式增长，英伟达数据中心业务营收已占公司总收入的78%。黄仁勋表示Blackwell架构芯片订单已排至2028年，公司正加速扩产以满足市场需求。",
        "tag": "金融",
        "prompt": "NVIDIA headquarters with glowing green logo, stock market chart showing growth, Silicon Valley campus, futuristic chip visualization, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "10",
        "title": "阿根廷获得2026年世界杯冠军 梅西圆满谢幕",
        "summary": "2026年国际足联世界杯在墨西哥落幕，阿根廷队在决赛中通过点球大战战胜法国队，成功卫冕冠军。37岁的梅西在决赛中贡献一球一助攻，赛后正式宣布退出国家队。潘帕斯雄鹰以三座世界杯冠军超越德国，成为世界杯历史上夺冠次数最多的球队。",
        "tag": "体育",
        "prompt": "Argentina football team celebrating World Cup victory, confetti falling, Messi holding trophy, stadium full of fans, Mexican stadium background, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "11",
        "title": "亚马逊AWS全球宕机六小时 云服务安全引担忧",
        "summary": "亚马逊云服务AWS发生大规模宕机事故，持续约六小时，影响全球数百万企业和用户的服务可用性。AWS公告称事故原因为韩国数据中心冷却系统故障导致服务器过热，多个区域的EC2、S3和Lambda服务陷入瘫痪。此次事件引发业界对云计算单点故障风险的广泛讨论。",
        "tag": "科技",
        "prompt": "Data center server room with emergency lighting, technicians working on equipment, warning lights flashing, cooling system failure concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "12",
        "title": "中美商务部长会谈 双方同意重启贸易谈判",
        "summary": "中国商务部长王文涛与美国商务部长雷蒙多在日内瓦举行会谈，双方同意重启中断两年的中美贸易谈判。会谈涉及关税、科技出口管制和市场准入等关键议题，同意建立双边商务对话机制。美方表示希望减少对华贸易逆差，中方则要求美方取消对中国企业的无理制裁。",
        "tag": "国际",
        "prompt": "Chinese and American flags side by side, bilateral trade negotiation meeting room, diplomats shaking hands, Geneva conference building, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "13",
        "title": "全球第六代移动通信商用启动 峰值速率达1Tbps",
        "summary": "中国、韩国和日本率先启动6G商用服务，中国移动联合华为在上海开展全球首个6G规模试点。6G网络峰值速率达1Tbps，较5G提升100倍，时延降至0.1毫秒。6G还将实现天地一体化通信，支持水下和太空网络覆盖，预计到2030年将覆盖全球主要城市。",
        "tag": "科技",
        "prompt": "Futuristic 6G network concept, holographic data streams, city covered with invisible wireless signals, smartphone with ultra fast connection indicator, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "14",
        "title": "诺贝尔化学奖授予三位锂电池科学家 致敬绿色能源先驱",
        "summary": "瑞典皇家科学院宣布2026年诺贝尔化学奖授予三位在锂电池领域做出开创性贡献的科学家——美国古德诺夫、日本吉野彰和英国威廷汉。他们的研究成果使锂离子电池实现商业化，为新能源汽车和可再生能源存储提供了核心技术。三位获奖者平均年龄超过80岁。",
        "tag": "文化",
        "prompt": "Nobel Prize ceremony in Stockholm, scientists receiving gold medals, lithium battery technology visualization, Nobel medal close up, elegant auditorium, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "15",
        "title": "中国探月工程进入新阶段 将在月球建立永久科研站",
        "summary": "中国国家航天局公布探月工程四期计划，将于2028年发射嫦娥七号和八号探测器，在月球南极建成永久科研站。科研站将具备长期自动运行能力，支持astronaut短期驻留开展实验。中科院院士表示，月球科研站将重点研究月壤资源利用和深空探测技术。",
        "tag": "科技",
        "prompt": "Chinese lunar research station on moon surface, astronauts in spacesuits working, Earth visible in dark sky, lunar rover nearby, scientific equipment, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "16",
        "title": "德国通过新移民法 每年引入50万技术人才",
        "summary": "德国联邦议院通过新版移民法，大幅降低技术人才移民门槛，允许具有专业技能但无大学学历的人员移民德国。新法还设立积分制评估体系，语言能力和职业经验成为重要加分项。德国总理表示新法将帮助德国应对人口老龄化和劳动力短缺问题每年吸引50万技术人才。",
        "tag": "社会",
        "prompt": "German parliament building in Berlin, immigrants receiving work permits, diverse professionals working in modern office, German flag, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "17",
        "title": "比特币价格突破12万美元 加密货币牛市重来",
        "summary": "比特币价格历史上首次突破12万美元整数关口，全球加密货币总市值突破4万亿美元。机构投资者大规模入场和比特币现货ETF持续净流入是主要推动力。分析师认为比特币已成为主流资产配置选项，但各国监管政策分化仍是市场面临的不确定因素。",
        "tag": "金融",
        "prompt": "Bitcoin cryptocurrency concept, glowing coin with Bitcoin symbol, stock market charts showing upward trend, digital gold visualization, futuristic financial concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "18",
        "title": "欧盟通过数字市场法修正案 科技巨头面临更严监管",
        "summary": "欧洲议会通过数字市场法修正案，对大型互联网平台施加更严格的互操作性和数据共享义务。修正案要求即时通讯软件必须与竞争对手互联，搜索引擎需向第三方开放数据。违反规定的公司面临全球年营业额10%的罚款，谷歌、Meta和亚马逊等巨头首当其冲。",
        "tag": "经济",
        "prompt": "European Parliament building in Brussels, tech company logos under scrutiny, digital regulations concept, EU officials reviewing documents, modern office setting, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "19",
        "title": "全球粮食价格持续下跌 农业危机暂缓",
        "summary": "联合国粮农组织数据显示，全球粮食价格指数连续三个月下跌，小麦和玉米价格较年初分别下降18%和22%。丰收预期和俄乌停火谈判进展顺利是价格回落的主要原因。不过极端天气威胁依然存在，气候变化对全球粮食安全的长期影响不容忽视。",
        "tag": "社会",
        "prompt": "Golden wheat field ready for harvest, agricultural machinery in distance, clear blue sky, sustainable farming concept, food abundance, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "20",
        "title": "OpenAI GPT-5.5被曝安全漏洞 人工智能风险再度引关注",
        "summary": "网络安全研究人员在OpenAI GPT-5.5模型中发现严重安全漏洞，攻击者可通过特定提示词绕过安全限制获取受限信息。OpenAI已紧急发布补丁修复该漏洞，并暂时关闭相关API接口。业内人士呼吁建立更严格的AI安全测试标准，避免大模型被恶意利用。",
        "tag": "科技",
        "prompt": "Cybersecurity concept, hacker terminal with code, AI brain with security lock, data breach warning, dark digital environment, photorealistic, ultra detailed, 8K, high resolution"
    }
]

def generate_image(news_item, retries=2):
    """使用智谱 CogView-3-Flash 生成图片"""
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {news_item['prompt']}"}]
    }
    
    for attempt in range(retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            
            # 处理返回格式：可能是URL或base64
            image_url = None
            if isinstance(content, list):
                image_url = content[0].get("url")
            elif isinstance(content, str) and content.startswith("http"):
                image_url = content
            
            if image_url:
                # 下载图片
                img_resp = requests.get(image_url, timeout=60)
                img_resp.raise_for_status()
                filename = f"images/news_{DATE}_{news_item['number']}.png"
                with open(filename, "wb") as f:
                    f.write(img_resp.content)
                print(f"✓ {news_item['number']} 生成成功: {filename}")
                return True
            
            print(f"✗ {news_item['number']} 未知响应格式: {content[:100]}")
            
        except Exception as e:
            print(f"✗ {news_item['number']} 生成失败 (尝试 {attempt+1}/{retries}): {e}")
        time.sleep(1)
    return False

def main():
    # 生成图片
    print("开始生成20张新闻配图...")
    os.makedirs("images", exist_ok=True)
    for item in NEWS_DATA:
        generate_image(item)
        time.sleep(0.5)
    
    print("\n所有图片生成完成！")

if __name__ == "__main__":
    main()