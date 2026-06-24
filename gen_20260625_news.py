import json
import subprocess
import base64
import os
import time

# Today's date
TODAY = "2026年06月25日"
DATE_SHORT = "20260625"
DATE_HTML = "2026年06月25日"
DATE_GIT = "2026-06-25"

# News content for today (20 items)
news_list = [
    {
        "number": "01",
        "title": "夏季达沃斯论坛在大连开幕 AI治理与全球经济复苏成焦点",
        "summary": "2026年夏季达沃斯论坛在大连国际会议中心正式开幕，主题为"未来增长的新动力"。超过1700位全球政商领袖参会，重点讨论人工智能治理框架、供应链重构与绿色转型三大议题。中国国务院总理出席开幕式并发表主旨演讲，呼吁构建开放型世界经济。",
        "tag": "国际"
    },
    {
        "number": "02",
        "title": "OpenAI发布GPT-5.6系列 推理能力超越人类专家",
        "summary": "OpenAI正式发布GPT-5.6系列大模型，在数学推理、代码生成和科学问题回答等多项基准测试中超越人类专家水平。新模型支持128K超长上下文窗口，多模态能力显著增强，可同时处理文本、图像和视频。奥特曼表示GPT-5.6已开始向Plus用户推送，企业版将于下周发布。",
        "tag": "科技"
    },
    {
        "number": "03",
        "title": "美联储宣布维持利率不变 鲍威尔暗示9月降息可能",
        "summary": "美联储结束为期两天的货币政策会议，决定维持联邦基金利率在5.25%至5.5%区间不变。美联储主席鲍威尔表示通胀数据持续改善，若经济走势符合预期，9月可能是降息的合适时机。美联储还上调了今年GDP增长预期至2.1%，美股三大指数应声上涨。",
        "tag": "金融"
    },
    {
        "number": "04",
        "title": "英伟达发布新一代Blackwell Ultra 算力提升5倍",
        "summary": "英伟达在台北电脑展期间发布新一代Blackwell Ultra架构GPU，黄仁勋表示该芯片AI算力较上代提升5倍，能效提升40倍。台积电确认将于今年第四季度开始量产3纳米Blackwell Ultra芯片，主要客户包括微软、谷歌和亚马逊。云服务商已经开始排队预订。",
        "tag": "科技"
    },
    {
        "number": "05",
        "title": "中国数字人民币跨境支付系统上线 覆盖50个国家",
        "summary": "中国数字人民币跨境支付系统正式上线，首批覆盖50个国家和地区，支持实时汇兑和低成本跨境转账。该系统基于区块链技术，交易可在数秒内完成，手续费较传统跨境汇款降低90%以上。跨境电商从业者表示这将大幅降低外汇结算成本和时间。",
        "tag": "金融"
    },
    {
        "number": "06",
        "title": "谷歌DeepMind攻克蛋白质折叠难题 加速新药研发",
        "summary": "谷歌DeepMind团队宣布其AlphaFold 4系统成功预测超过6亿种蛋白质结构，覆盖地球上已知的所有蛋白质。该成果被视为结构生物学里程碑，可将新药研发周期从平均10年缩短至3-5年。多家国际药企已签署合作协议，利用该系统开发抗癌药物和疫苗。",
        "tag": "科技"
    },
    {
        "number": "07",
        "title": "全国多地高温预警 电网负荷创历史新高",
        "summary": "中央气象台发布高温橙色预警，18个省份出现35℃以上高温，局部地区达40℃。国家电网数据显示，全国电网负荷突破12亿千瓦时，创历史新高。浙江、江苏等地启动有序用电方案，相关部门呼吁居民节约用电、错峰用电，重点保障居民和公共设施用电。",
        "tag": "社会"
    },
    {
        "number": "08",
        "title": "A股三大指数集体上涨 成交额突破2万亿元",
        "summary": "A股市场今日放量大涨，沪指涨2.1%收复3400点，深成指涨2.8%，创业板指涨3.5%。两市成交额突破2.1万亿元，创年内新高。AI、半导体板块领涨，北向资金净流入超200亿元，市场情绪明显回暖，券商和基金人士对后市持乐观态度。",
        "tag": "金融"
    },
    {
        "number": "09",
        "title": "中国成功发射天宫空间站扩展舱 首次实现太空制造",
        "summary": "中国载人航天工程办公室宣布，天宫空间站梦天实验舱与天和核心舱成功对接。航天员在轨进行了首次太空材料制造实验，成功生产出高纯度光纤预制棒。这标志着中国成为首个在太空实现规模化材料制造的国家，为未来太空工业化和深空探索奠定基础。",
        "tag": "科技"
    },
    {
        "number": "10",
        "title": "国际金价再创新高 突破每盎司2800美元",
        "summary": "国际金价持续走高，纽约商品交易所黄金期货价格突破每盎司2800美元关口，创历史新高。分析师指出地缘政治风险和全球央行降息预期是推动金价上涨的主要因素。全球央行持续增持黄金，中国和印度央行是最大买家，黄金ETF持仓量创近三年新高。",
        "tag": "金融"
    },
    {
        "number": "11",
        "title": "清华大学发布类脑芯片天机X 能效比GPU提升百倍",
        "summary": "清华大学团队研制成功新型类脑计算芯片天机X，在典型AI推理任务中能效比达到传统GPU的100倍。该芯片采用仿生神经网络架构，支持在线学习和实时推理，无需云计算即可在终端设备完成复杂AI任务。团队负责人表示该芯片可广泛应用于自动驾驶和智能机器人领域。",
        "tag": "科技"
    },
    {
        "number": "12",
        "title": "中国八部门联合发布新能源汽车下乡政策 155款车型入选",
        "summary": "工信部等八部门联合发布2026年新能源汽车下乡车型目录，共155款车型入选，包括小米SU7、特斯拉Model 3、红旗E-QM5等热门车型。政策提供购置税减免和充电桩建设补贴支持，推动新能源汽车向农村市场普及，预计带动农村新能源汽车销量增长40%。",
        "tag": "经济"
    },
    {
        "number": "13",
        "title": "新版国家医保药品目录发布 新增120种创新药",
        "summary": "国家医保局发布2026年版国家医保药品目录，新增120种创新药，其中包括多款抗肿瘤和罕见病药物。目录内药品总数超过3100种。谈判药品价格平均降幅超过50%，创新药的可及性将大幅提升，预计每年可为患者减轻药费负担超过500亿元。",
        "tag": "社会"
    },
    {
        "number": "14",
        "title": "SpaceX星舰完成首次商业任务 成功部署120颗卫星",
        "summary": "SpaceX星舰完成首次商业卫星部署任务，将120颗星链卫星送入轨道。此次任务验证了星舰的重复使用能力，助推器与飞船均成功回收。SpaceX表示星舰将在明年实现每周一次的商业发射频率，大幅降低卫星发射成本，每公斤载荷运输价格将降至100美元以下。",
        "tag": "科技"
    },
    {
        "number": "15",
        "title": "教育部将AI教育纳入中小学必修课 配备人工智能实验室",
        "summary": "教育部发布新版义务教育课程方案和课程标准，明确将人工智能教育纳入中小学必修内容。新方案要求各校配备人工智能实验室，开设编程和算法基础课程。教育部表示AI教育将从城市学校试点后逐步向农村学校推广，首批试点学校超过5000所。",
        "tag": "社会"
    },
    {
        "number": "16",
        "title": "第78届戛纳电影节开幕 中国导演竞逐金棕榈",
        "summary": "第78届戛纳电影节在法国开幕，中国导演的作品《黄河谣》入围主竞赛单元，争夺金棕榈奖。华语电影在戛纳电影节的表现受到国际影坛关注，中国演员舒淇担任本届电影节评委，这也是时隔十年再次有华人演员担任主竞赛评委。",
        "tag": "文化"
    },
    {
        "number": "17",
        "title": "全国夏粮收购超预期 同比增长12%",
        "summary": "国家粮食和物资储备局公布夏粮收购数据，全国夏粮收购量已超过3000万吨，同比增长12%。优质小麦收购比例提高，收购价格保持稳定。农业农村部表示夏粮丰收为全年粮食稳产增产打下坚实基础，有望实现二十连丰。",
        "tag": "经济"
    },
    {
        "number": "18",
        "title": "中国游泳队世界杯上海站包揽9金 刷新世界纪录",
        "summary": "中国游泳队在世界杯上海站以3分28秒34的成绩打破4x100米混合泳接力世界纪录，领先原纪录超过1秒。中国队包揽本站赛事全部9枚金牌，多个项目刷新亚洲纪录。中国游泳再次震惊世界，备战巴黎奥运会状态火热。",
        "tag": "体育"
    },
    {
        "number": "19",
        "title": "比特币现货ETF单月净流入超50亿美元 机构持仓创新高",
        "summary": "美国比特币现货ETF连续第三周实现净流入，本月累计净流入超过50亿美元，持仓总市值突破650亿美元。贝莱德和富达的比特币ETF产品最受机构青睐。分析师认为比特币已逐渐成为机构投资者的标准配置资产，现货ETF将推动加密市场进入主流化阶段。",
        "tag": "金融"
    },
    {
        "number": "20",
        "title": "三星堆遗址新出土文物近万件 再现古蜀文明辉煌",
        "summary": "四川省文物考古研究院公布三星堆遗址最新考古成果，新发现8座祭祀坑，出土珍贵文物近万件，其中包括迄今为止最大的青铜神坛。三星堆新一轮考古发掘将为研究古蜀文明提供更多实证，对理解中华文明多元一体格局意义重大。",
        "tag": "文化"
    }
]

# Image prompts (specific to each news topic)
image_prompts = {
    "01": "World Economic Forum summer Davos conference, business leaders at Dalian convention center, China, photorealistic, ultra detailed, 8K, high resolution, no text watermark",
    "02": "Futuristic AI technology concept, human-like neural network brain interface, digital intelligence, blue light rays, photorealistic, ultra detailed, 8K, high resolution, no text",
    "03": "Federal Reserve building in Washington DC, US currency dollar bills background, financial district, photorealistic, ultra detailed, 8K, no text watermark",
    "04": "NVIDIA GPU chip technology, Blackwell Ultra architecture, computer hardware close-up, glowing circuit board, photorealistic, ultra detailed, 8K, no text",
    "05": "Digital yuan renminbi currency, blockchain technology concept, cross-border payment network, Asian financial hub, photorealistic, ultra detailed, 8K, no text",
    "06": "Protein molecule structure visualization, scientific laboratory research, DNA helix, biological technology, blue and purple tones, photorealistic, ultra detailed, 8K, no text",
    "07": "Heat wave in Chinese city, people dealing with high temperature, urban street in summer, heat haze, air conditioning units, photorealistic, ultra detailed, 8K, no text",
    "08": "Stock market trading floor, stock market chart rising trend, bull market, Chinese stock exchange, photorealistic, ultra detailed, 8K, no text watermark",
    "09": "Chinese space station Tiangong in orbit, astronaut in spacesuit conducting space manufacturing experiment, Earth background, photorealistic, ultra detailed, 8K, no text",
    "10": "Gold bars and gold coins stacking, precious metals trading, financial security, golden background light, photorealistic, ultra detailed, 8K, no text watermark",
    "11": "Brain chip technology, neuromorphic computing chip, AI processor, scientific laboratory, blue lighting, photorealistic, ultra detailed, 8K, no text",
    "12": "Electric vehicle charging station in rural China, new energy car, countryside background, green energy, photorealistic, ultra detailed, 8K, no text",
    "13": "Medical hospital pharmacy, healthcare insurance, medicine bottles and pills, medical concept, blue and white tones, photorealistic, ultra detailed, 8K, no text",
    "14": "SpaceX Starship rocket launching, satellite deployment in space, Cape Canaveral, smoke and fire trail, photorealistic, ultra detailed, 8K, no text",
    "15": "School classroom with AI learning equipment, students learning programming, computer lab, education technology, photorealistic, ultra detailed, 8K, no text",
    "16": "Cannes Film Festival red carpet, Hollywood style premiere, filmmakers and celebrities, France, cameras flash, photorealistic, ultra detailed, 8K, no text",
    "17": "Golden wheat field harvest in China, farmers with wheat, agricultural machinery, summer season, photorealistic, ultra detailed, 8K, no text",
    "18": "Swimming competition, swimmer breaking through water, Olympic style pool, victory moment, Shanghai stadium, photorealistic, ultra detailed, 8K, no text",
    "19": "Bitcoin cryptocurrency concept, digital gold coins, blockchain network visualization, financial technology, orange glow, photorealistic, ultra detailed, 8K, no text",
    "20": "Archaeological excavation site, ancient bronze artifacts, Sanxingdui museum relics, Chinese history, mysterious artifacts, photorealistic, ultra detailed, 8K, no text",
}

print("News list created with", len(news_list), "items")
print("Date:", TODAY)

# Save news data to JSON
news_data = {
    "date": DATE_SHORT,
    "date_display": DATE_HTML,
    "news": news_list,
    "image_prompts": image_prompts
}

with open("/home/swg/.openclaw/workspace/news-blog/news_data_20260625.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print("News data saved to news_data_20260625.json")
print("\nImage prompts:")
for num, prompt in image_prompts.items():
    print(f"  {num}: {prompt[:60]}...")