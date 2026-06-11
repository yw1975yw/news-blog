import base64, os, time, json, urllib.request, urllib.error, re

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

DATE = "20260612"
DATE_CN = "2026年06月12日"

NEWS_DATA = [
    {
        "id": "01", "tag": "科技",
        "title": "神舟二十号载人飞船成功发射 三名航天员入驻空间站",
        "summary": "今日上午，长征二号F运载火箭在酒泉卫星发射中心点火升空，搭载神舟二十号载人飞船进入预定轨道。飞船载着三名航天员，计划与天宫空间站完成自主交会对接，随后开展为期六个月的太空科学实验和技术验证任务。此次任务将重点实施空间站舱外设备安装与维护，以及多模态生物打印等前沿实验。",
        "prompt": "Chinese manned spacecraft launching from desert launchpad, rocket blazing into blue sky with flames, space station orbiting above Earth, astronauts in space suits, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "02", "tag": "国际",
        "title": "北约峰会闭幕 发表联合宣言强化集体防御承诺",
        "summary": "北约峰会在布鲁塞尔落下帷幕，成员国领导人发表联合宣言，承诺将国防支出提升至GDP的2.5%以上，并成立新的混合战争应对中心。宣言首次明确将太空列为作战领域，允许成员国在遭受网络攻击时启动集体防御条款。美国总统在记者会上表示，北约比以往任何时候都更加团结。",
        "prompt": "NATO summit meeting in Brussels, world leaders around conference table with flags, military alliance ceremony, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "03", "tag": "金融",
        "title": "比特币突破12万美元关口 加密市场迎来新一轮牛市",
        "summary": "比特币价格在今日亚洲交易时段突破12万美元大关，创下历史新高，涨幅超过15%。以太坊、Solana等主流加密货币同步上涨，整个加密货币市值单日增长超过5000亿美元。分析师认为，现货比特币ETF持续获得机构资金流入，以及即将到来的比特币减半效应是本轮上涨的主要推动力。",
        "prompt": "Bitcoin cryptocurrency surge, golden Bitcoin coin with rising chart, digital gold bars, cryptocurrency trading screen, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "04", "tag": "经济",
        "title": "中国发布一季度GDP同比增长5.4% 经济延续回升态势",
        "summary": "国家统计局发布数据显示，一季度中国国内生产总值同比增长5.4%，增速比去年四季度加快0.2个百分点。消费对经济增长的贡献率超过65%，新能源汽车、锂电池、光伏产品出口继续保持高速增长。经济学家表示，装备制造业和数字经济成为拉动增长的主要引擎。",
        "prompt": "Modern Chinese city skyline at sunrise with economic growth chart overlay, people walking in business district, prosperity concept, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "05", "tag": "科技",
        "title": "华为发布鸿蒙PC操作系统 打破Windows与macOS双寡头格局",
        "summary": "华为今日在深圳举行发布会，正式推出鸿蒙PC操作系统，面向企业级和个人用户。这意味着鸿蒙系统已覆盖手机、平板、可穿戴设备及PC全场景。余承东表示，鸿蒙PC版采用微内核架构，支持与手机、平板的无缝协同，首批合作OEM厂商包括联想、戴尔、惠普等主流PC品牌。",
        "prompt": "Modern computer running new operating system, Chinese tech company logo, sleek laptop on minimalist desk, futuristic interface, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "06", "tag": "体育",
        "title": "全运会网球决赛落幕 郑钦文逆转夺冠成就三冠王",
        "summary": "第十五届全国运动会网球项目女子单打决赛在西安奥体中心落幕。头号种子郑钦文在先失一盘的不利局面下，以2比1逆转击败江苏选手王欣瑜，夺得个人第三枚全运会金牌。郑钦文赛后表示，很高兴能在主场观众面前展现最佳状态，感谢团队的支持与付出。",
        "prompt": "Tennis champion celebrating with trophy on court, confetti and crowd cheering, professional tennis match atmosphere, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "07", "tag": "国际",
        "title": "伊朗与沙特签署历史性和解协议 恢复中断八年的外交关系",
        "summary": "伊朗与沙特阿拉伯在巴格达签署和解协议，正式恢复自2016年断绝的外交关系。协议涵盖安全合作、能源政策和朝觐安排等多项内容。伊拉克总理作为调解方出席签字仪式，联合国秘书长对此表示欢迎，认为这将为中东地区和平与稳定开辟新前景。",
        "prompt": "Middle East diplomatic ceremony, Saudi and Iranian officials shaking hands, diplomatic flags, peace agreement signing, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "08", "tag": "科技",
        "title": "小米汽车月交付量首破3万辆 超级工厂产能提速",
        "summary": "小米汽车公布最新交付数据，5月份单月交付量达到30165辆，首次突破3万辆大关。其中小米SU7 Pro版占比超过60%，成为销量主力。小米集团总裁卢伟冰表示，超级工厂二期工程已投入使用，年产能提升至30万辆，预计年内将推出搭载城市NOA功能的新款SUV车型。",
        "prompt": "Modern electric car factory production line, robot arms assembling vehicles, Chinese EV manufacturer facility, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "09", "tag": "经济",
        "title": "广交会累计成交额突破500亿美元 新能源产品占比超四成",
        "summary": "第138届中国进出口商品交易会（广交会）在广州闭幕，累计实现成交额517亿美元，同比增长8.3%。新能源电动汽车、光伏组件、储能系统等绿色产品成交占比达到42%，创历史新高。一带一路沿线国家采购商数量增长20%，成为最大采购群体。",
        "prompt": "Massive trade expo exhibition hall, diverse products display, international business negotiations, Chinese export goods, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "10", "tag": "文化",
        "title": "故宫博物院获赠明代珍贵书画 填补数十年学术研究空白",
        "summary": "故宫博物院举行捐赠仪式，接受收藏家詹氏家族捐赠的37件明代珍贵书画，其中包括唐寅、仇英等大师的未公开作品。故宫博物院院长表示，这批文物填补了明代中后期绘画研究的多个空白，对研究明代社会生活具有重要价值。故宫将在明年举办特展向公众展示这批藏品。",
        "prompt": "Palace Museum Beijing, ancient Chinese calligraphy scrolls and paintings in exhibition hall, Ming dynasty cultural artifacts, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "11", "tag": "科技",
        "title": "字节跳动发布豆包大模型3.0 多模态能力对标GPT-5",
        "summary": "字节跳动正式发布豆包大模型3.0版本，在视觉-语言模型基准测试中超越GPT-4V，与GPT-5持平。新版本支持128K token上下文窗口，可一次性分析整部电影并回答复杂问题。豆包3.0还具备实时语音克隆和个性化数字人创建能力，已向企业用户开放API调用。",
        "prompt": "AI language model interface with holographic display, Chinese tech company headquarters, multimodal AI capabilities visualization, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "12", "tag": "社会",
        "title": "南方多省暴雨引发洪涝灾害 各地全力开展抢险救援",
        "summary": "受强对流天气影响，广东、广西、江西等省份出现大范围暴雨，部分河流水位超警戒线。广东韶关、清远等地出现严重内涝，受灾人口超过200万。应急管理部启动三级应急响应，调派消防救援力量和橡皮艇等装备前往灾区，全力转移被困群众。",
        "prompt": "Flood disaster rescue scene, rescue boats saving people from floodwaters, emergency response in southern China city, rain and rising water levels, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "13", "tag": "国际",
        "title": "中美商务部长通话 同意建立出口管制对话机制",
        "summary": "中国商务部部长应约与美国商务部长通话，双方就出口管制、半导体供应链等议题交换意见。两國同意建立出口管制对话机制，定期就相关政策进行沟通。同日，中国向WTO提起诉讼，指控美国芯片法案违反国际贸易规则，但双方表示将通过对话协商解决分歧。",
        "prompt": "US and China flags at diplomatic meeting, trade negotiators at conference table, bilateral relations concept, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "14", "tag": "科技",
        "title": "中国成功研发16T大容量固态硬盘 填补国内高端存储空白",
        "summary": "长江存储宣布成功研发全球首款16TB消费级PCIe 5.0固态硬盘，顺序读取速度达到14GB/s，采用Xtacking 4.0架构。该产品将于下月开始量产供货，首批主要面向数据中心和AI训练服务器市场。国产替代进程加速，有望打破三星、SK海力士等厂商在高端存储市场的垄断。",
        "prompt": "Large capacity SSD solid state drive with glowing circuitry, Chinese semiconductor factory, high speed storage technology, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "15", "tag": "金融",
        "title": "人民币跨境支付系统CIPS单日交易额突破3万亿元 创新纪录",
        "summary": "跨境银行间支付系统（CIPS）公布数据，单日交易额首次突破3万亿元人民币，同比增长35%。美元在跨境结算中的占比首次降至50%以下，人民币、欧元、英镑等多元化趋势明显。人民币跨境支付便利化政策持续显效，覆盖全球100多个国家和地区的千家金融机构。",
        "prompt": "International financial transaction screen showing RMB and multi-currency exchange rates, global payment system visualization, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "16", "tag": "社会",
        "title": "全国养老机构床位数突破900万张 银发经济规模超5万亿",
        "summary": "民政部发布养老服务发展报告，全国各类养老机构床位总数达到903万张，较五年前增长42%。65岁以上老年人口抚养比持续上升，银发经济市场规模突破5万亿元，智能养老产品和适老化改造成为投资热点。多个城市出台政策鼓励家庭养老床位建设。",
        "prompt": "Modern elderly care facility interior, elderly people enjoying activities, caring staff, senior living community, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "17", "tag": "科技",
        "title": "腾讯发布混元大模型SOTA版本 中文理解能力全球第一",
        "summary": "腾讯发布混元大模型最新版本，在MMLU、CMMLU等权威评测中均位列全球第一，中文理解与生成能力显著超越GPT-4。混元SOTA采用稀疏MoE架构，推理效率提升3倍，已在微信、QQ等超级APP中灰度上线。腾讯云同步推出模型精调平台，支持企业私有化部署。",
        "prompt": "Tencent tech headquarters, AI language model visualization with Chinese characters, futuristic data streams, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "18", "tag": "文化",
        "title": "三星堆遗址新发掘再获重大发现 出土文物超过两千件",
        "summary": "三星堆遗址考古工作取得新进展，考古队在祭祀坑区发现距今约3200年的完整青铜神坛以及大量玉器、金器。新发掘文物总数超过两千件，包括一件刻有神秘符号的青铜器，被专家推测为古蜀王国最高等级祭祀器物。三星堆博物馆将于明年建成开放，届时将展出这批最新出土文物。",
        "prompt": "Ancient archaeological excavation site in China, bronze artifacts being unearthed, archaeologists working at dig site, Sanxingdui cultural relics, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "19", "tag": "科技",
        "title": "百度萝卜快跑实现L4级自动驾驶商业化 覆盖十城",
        "summary": "百度宣布其自动驾驶出行服务平台萝卜快跑已在全国10座城市实现L4级完全无人驾驶商业运营，累计服务乘客突破500万人次。每辆运营车辆取消方向盘和刹车踏板，由5G云代驾中心远程监控。百度表示，每辆萝卜快跑日均订单量已超过传统网约车，单车毛利率转正。",
        "prompt": "Autonomous robotaxi driving on city street, no driver in vehicle, futuristic self-driving car, Chinese city environment, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "id": "20", "tag": "社会",
        "title": "全国结婚登记数止跌回升 年轻人倾向简约婚礼新风尚",
        "summary": "民政部公布婚姻登记数据，今年前五个月全国结婚登记对数达到392万对，同比增长12.6%，扭转了连续多年下降趋势。调查显示，年轻人更倾向于简约婚礼，旅行结婚、目的地婚礼占比提升至35%。婚庆消费平均支出下降18%，但珠宝首饰和海外蜜月旅行消费逆势增长。",
        "prompt": "Modern Chinese wedding ceremony, young couple at simple elegant wedding venue, wedding registration office, romantic celebration, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
]

def generate_image(news_id, prompt):
    output_path = f"/home/swg/.openclaw/workspace/news-blog/images/news_{DATE}_{news_id}.png"
    if os.path.exists(output_path):
        print(f"  [SKIP] Image {news_id} already exists")
        return True
    payload = {"model": "cogview-3-flash", "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            if "data:image/png;base64," in content:
                b64_data = content.split("data:image/png;base64,")[1]
            else:
                b64_data = content
            img_data = base64.b64decode(b64_data)
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"  [OK] Generated image {news_id}")
            return True
    except Exception as e:
        print(f"  [ERROR] Failed image {news_id}: {e}")
        return False

def build_news_card(news):
    nid = news["id"]
    return f'''<article class="news-card" data-tag="{news["tag"]}">
                    <img class="news-image" src="images/news_{DATE}_{nid}.png" alt="{news["title"]}" loading="lazy">
                    <div class="news-content">
                        <span class="news-number">{nid}</span>
                        <h3 class="news-title">{news["title"]}</h3>
                        <p class="news-summary">{news["summary"]}</p>
                        <div>
                            <span class="tag">{news["tag"]}</span>
                        </div>
                    </div>
                </article>'''

print(f"Generating news images for {DATE_CN}...")
os.makedirs("/home/swg/.openclaw/workspace/news-blog/images", exist_ok=True)
results = {}
for news in NEWS_DATA:
    nid = news["id"]
    print(f"Generating image {nid}...")
    success = generate_image(nid, news["prompt"])
    results[nid] = success
    if not success:
        print(f"  Retrying image {nid}...")
        time.sleep(5)
        success = generate_image(nid, news["prompt"])
        results[nid] = success
    time.sleep(2)

ok = sum(1 for v in results.values() if v)
print(f"\nImage Summary: {ok}/20 success")

# Build all news cards
all_cards = "\n                ".join([build_news_card(n) for n in NEWS_DATA])

# Update index.html
index_path = "/home/swg/.openclaw/workspace/news-blog/index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace date in title and cover
html = html.replace("2026年06月11日", DATE_CN)
html = html.replace("全球20条热点新闻 · 2026年06月11日", f"全球20条热点新闻 · {DATE_CN}")

# Replace news grid content
grid_pattern = re.compile(r'(<div class="news-grid" id="newsGrid">)\s*.*?(</div>\s*<div class="comments-section">)', re.DOTALL)
html = grid_pattern.sub(f'\\1\n                {all_cards}\n            </div>\n            <div class="comments-section">', html)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nindex.html updated successfully!")
print(f"Next steps: git add, commit, push")