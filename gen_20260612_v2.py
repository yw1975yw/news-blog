import base64, os, time, json, subprocess, re

DATE = "20260612"
DATE_CN = "2026年06月12日"

NEWS_DATA = [
    {"id": "01", "tag": "科技", "title": "神舟二十号载人飞船成功发射 三名航天员入驻空间站", "summary": "今日上午，长征二号F运载火箭在酒泉卫星发射中心点火升空，搭载神舟二十号载人飞船进入预定轨道。飞船载着三名航天员，计划与天宫空间站完成自主交会对接，随后开展为期六个月的太空科学实验和技术验证任务。此次任务将重点实施空间站舱外设备安装与维护，以及多模态生物打印等前沿实验。", "prompt": "Chinese rocket launching from desert launchpad at sunrise, Long March rocket blazing into blue sky with bright flames, space station orbiting above Earth atmosphere, astronauts in space suits inside spacecraft, photorealistic, ultra detailed, 8K, high resolution, cinematic lighting, no text, no watermark"},
    {"id": "02", "tag": "国际", "title": "北约峰会闭幕 发表联合宣言强化集体防御承诺", "summary": "北约峰会在布鲁塞尔落下帷幕，成员国领导人发表联合宣言，承诺将国防支出提升至GDP的2.5%以上，并成立新的混合战争应对中心。宣言首次明确将太空列为作战领域，允许成员国在遭受网络攻击时启动集体防御条款。", "prompt": "NATO summit meeting in Brussels grand hall, world leaders and ministers seated around large conference table with NATO flags, military alliance ceremony, diplomatic handshake, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "03", "tag": "金融", "title": "比特币突破12万美元关口 加密市场迎来新一轮牛市", "summary": "比特币价格在今日亚洲交易时段突破12万美元大关，创下历史新高，涨幅超过15%。以太坊、Solana等主流加密货币同步上涨，整个加密货币市值单日增长超过5000亿美元。分析师认为，现货比特币ETF持续获得机构资金流入，以及即将到来的比特币减半效应是本轮上涨的主要推动力。", "prompt": "Bitcoin cryptocurrency surging dramatically, golden Bitcoin coin glowing on digital stock market screen showing rising charts, crypto trading visualization, gold bars background, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "04", "tag": "经济", "title": "中国发布一季度GDP同比增长5.4% 经济延续回升态势", "summary": "国家统计局发布数据显示，一季度中国国内生产总值同比增长5.4%，增速比去年四季度加快0.2个百分点。消费对经济增长的贡献率超过65%，新能源汽车、锂电池、光伏产品出口继续保持高速增长。", "prompt": "Modern Chinese city skyline at sunrise with glass skyscrapers reflecting golden light, people commuting in business district, economic growth concept with rising chart overlay, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "05", "tag": "科技", "title": "华为发布鸿蒙PC操作系统 打破Windows与macOS双寡头格局", "summary": "华为今日在深圳举行发布会，正式推出鸿蒙PC操作系统，面向企业级和个人用户。这意味着鸿蒙系统已覆盖手机、平板、可穿戴设备及PC全场景。鸿蒙PC版采用微内核架构，支持与手机、平板的无缝协同，首批合作OEM厂商包括联想、戴尔、惠普等主流PC品牌。", "prompt": "Sleek modern laptop computer on minimalist white desk, Huawei product glowing screen showing harmonyOS interface, Chinese tech aesthetic, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "06", "tag": "体育", "title": "全运会网球决赛落幕 郑钦文逆转夺冠成就三冠王", "summary": "第十五届全国运动会网球项目女子单打决赛在西安奥体中心落幕。头号种子郑钦文在先失一盘的不利局面下，以2比1逆转击败江苏选手王欣瑜，夺得个人第三枚全运会金牌。", "prompt": "Tennis champion holding golden trophy on center court, confetti falling, crowd cheering enthusiastically, professional tennis stadium atmosphere, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "07", "tag": "国际", "title": "伊朗与沙特签署历史性和解协议 恢复中断八年的外交关系", "summary": "伊朗与沙特阿拉伯在巴格达签署和解协议，正式恢复自2016年断绝的外交关系。协议涵盖安全合作、能源政策和朝觐安排等多项内容。联合国秘书长对此表示欢迎，认为这将为中东地区和平与稳定开辟新前景。", "prompt": "Middle East diplomatic ceremony, Saudi and Iranian officials shaking hands warmly, diplomatic flags of both nations displayed, peace agreement signing in ornate hall, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "08", "tag": "科技", "title": "小米汽车月交付量首破3万辆 超级工厂产能提速", "summary": "小米汽车公布最新交付数据，5月份单月交付量达到30165辆，首次突破3万辆大关。其中小米SU7 Pro版占比超过60%，成为销量主力。超级工厂二期工程已投入使用，年产能提升至30万辆，预计年内将推出搭载城市NOA功能的新款SUV车型。", "prompt": "Modern electric car factory production line with robotic arms assembling vehicles, Xiaomi SU7 electric car on assembly line, automated manufacturing facility with clean high-tech environment, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "09", "tag": "经济", "title": "广交会累计成交额突破500亿美元 新能源产品占比超四成", "summary": "第138届广交会在广州闭幕，累计实现成交额517亿美元，同比增长8.3%。新能源电动汽车、光伏组件、储能系统等绿色产品成交占比达到42%，创历史新高。一带一路沿线国家采购商数量增长20%，成为最大采购群体。", "prompt": "Massive exhibition trade hall with diverse products on display, international buyers negotiating at booth, Chinese export goods containers at port, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "10", "tag": "文化", "title": "故宫博物院获赠明代珍贵书画 填补数十年学术研究空白", "summary": "故宫博物院举行捐赠仪式，接受收藏家詹氏家族捐赠的37件明代珍贵书画，其中包括唐寅、仇英等大师的未公开作品。这批文物填补了明代中后期绘画研究的多个空白，对研究明代社会生活具有重要价值。", "prompt": "Palace Museum Beijing with traditional Chinese architecture, ancient Ming dynasty calligraphy scrolls and paintings displayed in elegant gallery, cultural artifacts under soft lighting, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "11", "tag": "科技", "title": "字节跳动发布豆包大模型3.0 多模态能力对标GPT-5", "summary": "字节跳动正式发布豆包大模型3.0版本，在视觉-语言模型基准测试中超越GPT-4V，与GPT-5持平。新版本支持128K token上下文窗口，可一次性分析整部电影并回答复杂问题。豆包3.0还具备实时语音克隆和个性化数字人创建能力，已向企业用户开放API调用。", "prompt": "Futuristic AI interface with holographic display showing multimodal AI capabilities, ByteDance/TikTok tech aesthetic, neural network visualization, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "12", "tag": "社会", "title": "南方多省暴雨引发洪涝灾害 各地全力开展抢险救援", "summary": "受强对流天气影响，广东、广西、江西等省份出现大范围暴雨，部分河流水位超警戒线。广东韶关、清远等地出现严重内涝，受灾人口超过200万。应急管理部启动三级应急响应，调派消防救援力量和橡皮艇等装备前往灾区。", "prompt": "Flood disaster emergency rescue scene, rescue boats saving people from floodwaters in southern China city, firefighters in rescue operations, heavy rain and rising water levels, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "13", "tag": "国际", "title": "中美商务部长通话 同意建立出口管制对话机制", "summary": "中国商务部部长应约与美国商务部长通话，双方就出口管制、半导体供应链等议题交换意见。两國同意建立出口管制对话机制，定期就相关政策进行沟通。中国向WTO提起诉讼，指控美国芯片法案违反国际贸易规则，但双方表示将通过对话协商解决分歧。", "prompt": "US and China flags at bilateral diplomatic meeting, trade negotiators in professional setting, international commerce concept, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "14", "tag": "科技", "title": "中国成功研发16T大容量固态硬盘 填补国内高端存储空白", "summary": "长江存储宣布成功研发全球首款16TB消费级PCIe 5.0固态硬盘，顺序读取速度达到14GB/s，采用Xtacking 4.0架构。该产品将于下月开始量产供货，首批主要面向数据中心和AI训练服务器市场。", "prompt": "Large capacity SSD solid state drive with glowing blue LED lighting, detailed circuit board closeup, Chinese semiconductor technology, data storage concept, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "15", "tag": "金融", "title": "人民币跨境支付系统CIPS单日交易额突破3万亿元 创新纪录", "summary": "跨境银行间支付系统（CIPS）公布数据，单日交易额首次突破3万亿元人民币，同比增长35%。美元在跨境结算中的占比首次降至50%以下，人民币、欧元、英镑等多元化趋势明显。人民币跨境支付便利化政策持续显效，覆盖全球100多个国家和地区的千家金融机构。", "prompt": "Global financial transaction system visualization, multiple currency exchange rates on screen, international banking network, RMB symbol with world map, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "16", "tag": "社会", "title": "全国养老机构床位数突破900万张 银发经济规模超5万亿", "summary": "民政部发布养老服务发展报告，全国各类养老机构床位总数达到903万张，较五年前增长42%。65岁以上老年人口抚养比持续上升，银发经济市场规模突破5万亿元，智能养老产品和适老化改造成为投资热点。", "prompt": "Modern elderly care facility interior with warm lighting, elderly people enjoying activities and social interaction, caring professional staff, comfortable senior living environment, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "17", "tag": "科技", "title": "腾讯发布混元大模型SOTA版本 中文理解能力全球第一", "summary": "腾讯发布混元大模型最新版本，在MMLU、CMMLU等权威评测中均位列全球第一，中文理解与生成能力显著超越GPT-4。混元SOTA采用稀疏MoE架构，推理效率提升3倍，已在微信、QQ等超级APP中灰度上线。", "prompt": "Tencent headquarters building in Shenzhen, AI language model visualization with Chinese characters floating in digital space, futuristic data streams and neural networks, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "18", "tag": "文化", "title": "三星堆遗址新发掘再获重大发现 出土文物超过两千件", "summary": "三星堆遗址考古工作取得新进展，考古队在祭祀坑区发现距今约3200年的完整青铜神坛以及大量玉器、金器。新发掘文物总数超过两千件，包括一件刻有神秘符号的青铜器，被专家推测为古蜀王国最高等级祭祀器物。", "prompt": "Archaeological excavation site in Sichuan China, ancient bronze artifacts carefully being unearthed by archaeologists wearing white gloves, Sanxingdui mysterious bronze面具, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "19", "tag": "科技", "title": "百度萝卜快跑实现L4级自动驾驶商业化 覆盖十城", "summary": "百度宣布其自动驾驶出行服务平台萝卜快跑已在全国10座城市实现L4级完全无人驾驶商业运营，累计服务乘客突破500万人次。每辆运营车辆取消方向盘和刹车踏板，由5G云代驾中心远程监控。", "prompt": "Futuristic autonomous robotaxi self-driving car driving on city street at night, no driver visible inside vehicle, city lights reflecting on sleek car body, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
    {"id": "20", "tag": "社会", "title": "全国结婚登记数止跌回升 年轻人倾向简约婚礼新风尚", "summary": "民政部公布婚姻登记数据，今年前五个月全国结婚登记对数达到392万对，同比增长12.6%，扭转了连续多年下降趋势。年轻人更倾向于简约婚礼，旅行结婚、目的地婚礼占比提升至35%。婚庆消费平均支出下降18%，但珠宝首饰和海外蜜月旅行消费逆势增长。", "prompt": "Modern elegant Chinese wedding ceremony, young couple in stylish wedding attire, simple beautiful venue with floral decorations, romantic atmosphere, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"},
]

def generate_image(news_id, prompt):
    output_path = f"/home/swg/.openclaw/workspace/news-blog/images/news_{DATE}_{news_id}.png"
    if os.path.exists(output_path):
        print(f"  [SKIP] Image {news_id} already exists")
        return True
    escaped_prompt = prompt.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
    curl_cmd = [
        "curl", "-s", "-X", "POST",
        "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "-H", f"Authorization: Bearer 88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB",
        "-H", "Content-Type: application/json",
        "-d", f'{{"model":"cogview-3-flash","messages":[{{"role":"user","content":"Image prompt: {escaped_prompt}"}}]}}'
    ]
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"  [ERROR] curl failed for {news_id}: {result.stderr}")
            return False
        resp = json.loads(result.stdout)
        # Response format: choices[0].message.content is a list with {url: "..."}
        content_list = resp.get("choices", [{}])[0].get("message", {}).get("content", [])
        if isinstance(content_list, list) and len(content_list) > 0:
            img_url = content_list[0].get("url", "")
        else:
            print(f"  [ERROR] Unexpected response format for {news_id}")
            return False
        # Download image
        dl_cmd = ["curl", "-s", "-o", output_path, img_url]
        dl_result = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=60)
        if dl_result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"  [OK] Generated image {news_id}")
            return True
        else:
            print(f"  [ERROR] Download failed for {news_id}")
            return False
    except Exception as e:
        print(f"  [ERROR] Failed image {news_id}: {e}")
        return False

os.makedirs("/home/swg/.openclaw/workspace/news-blog/images", exist_ok=True)
results = {}
for news in NEWS_DATA:
    nid = news["id"]
    print(f"Generating image {nid}: {news['title'][:30]}...")
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

all_cards = "\n                ".join([build_news_card(n) for n in NEWS_DATA])

index_path = "/home/swg/.openclaw/workspace/news-blog/index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("2026年06月11日", DATE_CN)
html = html.replace("全球20条热点新闻 · 2026年06月11日", f"全球20条热点新闻 · {DATE_CN}")

grid_pattern = re.compile(r'(<div class="news-grid" id="newsGrid">)\s*.*?(</div>\s*<div class="comments-section">)', re.DOTALL)
html = grid_pattern.sub(f'\\1\n                {all_cards}\n            </div>\n            <div class="comments-section">', html)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"index.html updated successfully!")