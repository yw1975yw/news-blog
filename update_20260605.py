import re

date_display = "2026年06月05日"
date_short = "2026年06月04日"

news_items = [
    {
        "number": "01", "tag": "科技",
        "title": "OpenAI发布GPT-5.6正式版 上下文窗口达到150万tokens",
        "summary": "OpenAI在旧金山召开春季发布会，正式发布GPT-5.6正式版模型。该版本支持高达150万token的超长上下文窗口，可一次性处理约100万字的中文文本。在多项基准测试中，GPT-5.6在数学推理、代码生成和多轮对话一致性方面刷新世界纪录。OpenAI同时宣布GPT-5.6将向Plus用户全面开放，企业版支持私有化部署。",
        "image": "images/news_20260605_01.png"
    },
    {
        "number": "02", "tag": "科技",
        "title": "神舟二十号载人飞船发射取得圆满成功 三名航天员顺利进入空间站",
        "summary": "北京时间2026年6月5日上午，神舟二十号载人飞船在酒泉卫星发射中心由长征二号F遥二十一运载火箭成功发射。飞船搭载三名航天员，与中国空间站成功完成自主交会对接。三名航天员将在空间站开展为期六个月的科学实验、技术试验和出舱活动，此次任务是中国空间站应用与发展阶段的第五次载人飞行。",
        "image": "images/news_20260605_02.png"
    },
    {
        "number": "03", "tag": "金融",
        "title": "美联储宣布维持利率不变 暗示下半年或降息两次",
        "summary": "美国联邦储备委员会宣布维持联邦基金利率在5.25%至5.5%不变，符合市场预期。美联储主席鲍威尔在新闻发布会上表示，美国经济整体保持韧性，但通胀率持续回落为货币政策调整提供了空间。点阵图显示多数官员支持2026年下半年降息两次。消息公布后，美股三大指数集体上涨，纳斯达克指数涨幅超过2%。",
        "image": "images/news_20260605_03.png"
    },
    {
        "number": "04", "tag": "国际",
        "title": "欧盟就数字市场法案执法达成协议 苹果开放侧载功能",
        "summary": "欧盟委员会与苹果公司达成协议，苹果将在iOS系统中正式支持侧载应用安装，这是欧盟数字市场法案的重要里程碑。根据协议，欧盟用户可以从经认证的应用商店或直接下载安装第三方应用，苹果将收取适度安全费用。欧盟委员会表示这将促进应用市场的公平竞争，为消费者提供更多选择。",
        "image": "images/news_20260605_04.png"
    },
    {
        "number": "05", "tag": "经济",
        "title": "中国5月CPI同比上涨0.3% 消费市场持续回暖",
        "summary": "国家统计局发布5月份居民消费价格指数，CPI同比上涨0.3%，涨幅比上月扩大0.1个百分点。其中食品价格上涨0.2%，非食品价格上涨0.3%。受五一假期带动，酒店住宿、旅游和餐饮消费大幅增长。分析认为消费市场延续恢复态势，下半年有望进一步提升。",
        "image": "images/news_20260605_05.png"
    },
    {
        "number": "06", "tag": "科技",
        "title": "苹果全球开发者大会开幕 发布iOS 20和Vision Pro 2",
        "summary": "苹果全球开发者大会在Cupertino举行，发布iOS 20操作系统和Vision Pro 2头显设备。iOS 20引入AI驱动的Siri 2.0，支持跨应用任务规划和实时翻译。Vision Pro 2重量减轻30%，电池续航提升至6小时，售价降至2499美元。苹果还宣布将ChatGPT深度整合至全系统，全球超过20亿台iOS设备将获得AI能力升级。",
        "image": "images/news_20260605_06.png"
    },
    {
        "number": "07", "tag": "体育",
        "title": "巴黎奥运会倒计时30天 法国启动史上最大规模安保行动",
        "summary": "距离2026年巴黎奥运会开幕还有30天，法国政府启动史上最大规模安保行动，超过10万名军警将参与奥运会安保工作。巴黎奥组委公布开幕式流程，运动员将乘船沿塞纳河巡游，预计全球超过10亿观众通过电视直播观看。本届奥运会共设35个场馆，目前所有场馆建设已全部完工。",
        "image": "images/news_20260605_07.png"
    },
    {
        "number": "08", "tag": "科技",
        "title": "丰田固态电池量产获突破 充电10分钟续航1200公里",
        "summary": "丰田汽车宣布固态电池量产技术取得重大突破，新型固态电池充电10分钟可实现1200公里续航，循环寿命超过2000次。丰田计划2027年在旗下车型上搭载固态电池，首批受益车型为电动轿车和SUV。业内分析认为固态电池的商业化将加速电动汽车替代燃油车的进程。",
        "image": "images/news_20260605_08.png"
    },
    {
        "number": "09", "tag": "国际",
        "title": "G7峰会联合声明宣布将向发展中国家提供5000亿美元气候援助",
        "summary": "七国集团峰会在意大利召开，峰会联合声明宣布2026年至2030年将向发展中国家提供5000亿美元气候援助资金，用于支持清洁能源转型和应对气候变化。援助资金将主要来自公共资金和多边开发银行，同时鼓励私人资本参与。发展中国家对此表示欢迎，但呼吁资金分配更加透明公正。",
        "image": "images/news_20260605_09.png"
    },
    {
        "number": "10", "tag": "科技",
        "title": "中国科学家成功研发16位量子计算机 量子计算进入实用阶段",
        "summary": "中国科学技术大学宣布成功研发16位超导量子计算机\"九章三号\"，在特定数学问题求解上比超级计算机快1亿亿倍。该量子计算机已接入国家超算互联网，向科研机构开放使用。潘建伟院士表示这是量子计算从实验室走向实用化的关键一步，未来三年内有望在药物研发、金融建模等领域产生实际应用价值。",
        "image": "images/news_20260605_10.png"
    },
    {
        "number": "11", "tag": "经济",
        "title": "阿里巴巴发布财报 淘天集团收入增长18%超预期",
        "summary": "阿里巴巴发布2026财年第四季度财报，淘天集团收入同比增长18%至1200亿元人民币，主要得益于AI驱动的个性化推荐提升转化率和客单价。阿里云收入增长15%，通义千问大模型已接入超过50万企业用户。阿里巴巴CEO吴泽明表示，AI正在深度改造电商和云计算业务，将持续加大投入。",
        "image": "images/news_20260605_11.png"
    },
    {
        "number": "12", "tag": "社会",
        "title": "全国高考今日开考 1342万名考生走进考场",
        "summary": "2026年全国普通高校招生考试今日开考，全国共有1342万名考生报名参加，同比增长4.3%。北京、上海等大城市首次采用AI智能监考系统，通过人脸识别和行为分析有效防范作弊。各省市派出监考人员超过100万人，确保高考公平公正。考试成绩将于6月25日公布，志愿填报时间为6月28日至7月5日。",
        "image": "images/news_20260605_12.png"
    },
    {
        "number": "13", "tag": "体育",
        "title": "国际足联宣布2026年世界杯VAR系统升级 增加人工智能辅助裁判",
        "summary": "国际足联宣布2026年世界杯将启用升级版VAR系统，引入人工智能辅助裁判技术。该系统可在0.3秒内完成越位判定，并将判罚依据实时呈现在球场大屏上。每场比赛配置7名官员，包括主裁判、助理裁判和视频助理裁判。国际足联表示新技术将大幅减少争议判罚，提升比赛流畅性和公正性。",
        "image": "images/news_20260605_13.png"
    },
    {
        "number": "14", "tag": "经济",
        "title": "特斯拉上海储能超级工厂投产 年产能达40GWh",
        "summary": "特斯拉上海储能超级工厂正式投产，这是特斯拉在美国以外建设的首个储能电池生产基地。工厂年产能规划40GWh，主要生产Megapack大型储能电池，产品将供应亚太市场。上海市委书记陈吉宁出席投产仪式，特斯拉CEO马斯克通过视频表示上海工厂是特斯拉全球布局的关键一环。",
        "image": "images/news_20260605_14.png"
    },
    {
        "number": "15", "tag": "文化",
        "title": "联合国教科文组织将春节列入人类非物质文化遗产代表作名录",
        "summary": "联合国教科文组织保护非物质文化遗产政府间委员会通过评审，正式将春节列入人类非物质文化遗产代表作名录。春节是中华民族最重要的传统节日，已在全球200多个国家和地区受到庆祝。教科文组织表示春节体现了家庭团聚、文化传承和多元价值，是全人类的共同文化遗产。",
        "image": "images/news_20260605_15.png"
    },
    {
        "number": "16", "tag": "科技",
        "title": "华为发布鸿蒙PC操作系统 打破Windows和macOS垄断格局",
        "summary": "华为正式发布鸿蒙PC操作系统，面向企业和个人用户推出商用版本。鸿蒙PC支持与手机、平板、智能汽车的无缝协同，可实现跨设备文件拖拽和应用续接。首批搭载鸿蒙PC的设备包括联想、惠普和清华同方等品牌机型。业内分析认为这将打破Windows和macOS在PC市场的双寡头格局。",
        "image": "images/news_20260605_16.png"
    },
    {
        "number": "17", "tag": "金融",
        "title": "A股三大指数集体收涨 沪指重返3500点",
        "summary": "A股市场今日强势反弹，上证综指上涨2.1%收报3512点，深证成指上涨2.8%，创业板指上涨3.5%。北向资金净流入超过200亿元，创年内单日新高。券商板块集体涨停，保险、银行和消费电子板块涨幅居前。分析师认为政策暖风频吹和企业盈利改善共振，推动市场做多情绪升温。",
        "image": "images/news_20260605_17.png"
    },
    {
        "number": "18", "tag": "国际",
        "title": "中国成功当选联合国人权理事会成员 任期2027-2029年",
        "summary": "第79届联合国大会投票选举联合国人权理事会新成员，中国以压倒性多数票成功当选，任期为2027年至2029年。中国常驻联合国代表表示，中国当选体现了国际社会对人权发展道路的支持，中国将继续积极参与人权理事会工作，推动构建人类命运共同体。",
        "image": "images/news_20260605_18.png"
    },
    {
        "number": "19", "tag": "社会",
        "title": "北京二手房成交量创历史新高 单月突破3万套",
        "summary": "北京市住建委公布数据，5月份二手房成交量突破3万套，创历史单月新高，成交金额超过1500亿元。受益于存量房贷利率下调和限购政策优化，市场活跃度显著提升。业内预计6月份成交将继续保持高位，房价整体保持平稳，部分核心区域小幅上涨。",
        "image": "images/news_20260605_19.png"
    },
    {
        "number": "20", "tag": "科技",
        "title": "三星电子发布首款3nm自研芯片 挑战苹果M系列性能",
        "summary": "三星电子发布首款3nm工艺自研PC处理器Exynos 2500，性能测试结果全面超越苹果M4芯片。三星同时推出搭载该芯片的Galaxy Book笔记本电脑，厚度仅11毫米，续航达18小时。三星芯片部门负责人表示，Exynos 2500将向其他PC厂商供货，有望改写笔记本电脑处理器市场格局。",
        "image": "images/news_20260605_20.png"
    },
]

# Read existing index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update page title and meta
html = html.replace("2026年06月04日", "2026年06月05日")

# Also update date in subtitle (cover-overlay)
html = re.sub(r'全球20条热点新闻 · 2026年06月0\d日', f'全球20条热点新闻 · {date_display}', html)

# Update footer date
html = re.sub(r'所有新闻内容仅供参考，请以官方发布为准 · 2026年06月0\d日', f'所有新闻内容仅供参考，请以官方发布为准 · {date_display}', html)

# Build new news cards HTML
new_cards = ""
for item in news_items:
    card = f'''                <div class="news-card">
                    <img class="news-image" src="{item["image"]}" alt="{item["title"]}" loading="lazy">
                    <div class="news-content">
                        <span class="news-number">{item["number"]}</span>
                        <h3 class="news-title">{item["title"]}</h3>
                        <p class="news-summary">{item["summary"]}</p>
                        <div>
                            <span class="tag">{item["tag"]}</span>
                        </div>
                    </div>
                </div>
'''
    new_cards += card

# Replace news grid content
# Find the news-grid div and replace its contents
pattern = r'(<div class="news-grid" id="newsGrid">).*?(</div>\s*</div>\s*<div class="comments-section">)'
replacement = f'<div class="news-grid" id="newsGrid">\n{new_cards}\n                </div>\n            </div>\n            <div class="comments-section">'
html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Write updated index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated successfully!")
print(f"Date: {date_display}")
print(f"News items: {len(news_items)}")