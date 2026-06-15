#!/usr/bin/env python3
"""Update index.html with new news content"""
import re

# Read the current file
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new news items
news_items = [
    {"number": "01", "tag": "科技", "title": "OpenAI发布GPT-5.5多模态模型 推理能力再度刷新人类极限", "summary": "OpenAI在旧金山发布GPT-5.5多模态大模型，该模型在科学推理、医学诊断和复杂数学证明等基准测试中大幅超越人类专家平均水平。GPT-5.5支持文本、图像、视频、音频和3D模型的统一处理，上下文窗口扩展至500万tokens。OpenAI同时发布企业版ChatGPT Enterprise 3.0，将向全球财富500强企业优先部署。英伟达表示下一代Blackwell Ultra GPU已针对GPT-5.5优化。", "image": "news_20260616_01.png"},
    {"number": "02", "tag": "国际", "title": "G7峰会在意大利陶尔米纳闭幕 达成AI全球治理框架协议", "summary": "七国集团峰会在意大利西西里岛陶尔米纳闭幕，美国总统特朗普首次出席G7会议引发广泛关注。峰会达成AI全球治理框架协议，同意建立跨国AI安全评估机制，并对超过1000亿参数的大模型实施联合监管。欧盟呼吁建立AI发展基金，帮助发展中国家应对AI带来的就业冲击。峰会还讨论了贸易体系改革和气候变化融资等议题。", "image": "news_20260616_02.png"},
    {"number": "03", "tag": "金融", "title": "美联储维持利率不变 但暗示最快9月启动降息", "summary": "美联储宣布维持联邦基金利率目标区间在5.25%至5.5%不变，符合市场预期。美联储主席鲍威尔表示通胀率已接近2%目标，但就业市场仍需观察，暗示最快可能在9月会议启动降息。美联储同时公布缩表继续推进，每月国债缩减规模维持在600亿美元。美股三大指数小幅收涨，纳斯达克指数上涨0.6%。", "image": "news_20260616_03.png"},
    {"number": "04", "tag": "科技", "title": "SpaceX星舰完成第三次载人任务 成功着陆月球轨道站", "summary": "SpaceX星舰完成第三次载人任务，成功与国际月球轨道站对接。四名宇航员将在轨道站驻留30天，进行月球表面远程探测实验。此次任务是阿尔忒弥斯计划的重要组成部分，为2028年载人登月任务进行最后准备。SpaceX同时宣布星舰货运版本已获得NASA合同，将承担地月物流运输任务。", "image": "news_20260616_04.png"},
    {"number": "05", "tag": "国际", "title": "中美重启经贸谈判 双方在华盛顿举行高层对话", "summary": "中美两国代表在华盛顿举行高层经贸对话，重启自2025年底中断的双边贸易谈判。双方就关税、科技制裁和投资限制等议题深入交换意见。据知情人士透露，双方可能在近期达成一项阶段性协议，涉及恢复部分商品正常贸易和科技产品出口许可。中国商务部表示对话具有建设性，双方同意继续保持沟通。", "image": "news_20260616_05.png"},
    {"number": "06", "tag": "经济", "title": "欧盟碳边境调节机制扩大范围 覆盖新能源汽车和电池", "summary": "欧盟委员会宣布碳边境调节机制（CBAM）扩大范围，新增新能源汽车和动力电池两大行业。欧盟进口商需为来自未实施严格碳定价国家的商品购买碳排放证书。德国汽车制造商协会表示反对，认为这可能引发贸易摩擦。中国新能源汽车企业已在欧洲建立本地化生产体系以规避关税。", "image": "news_20260616_06.png"},
    {"number": "07", "tag": "科技", "title": "谷歌发布Android 16操作系统 深度整合Gemini AI助手", "summary": "谷歌在全球开发者大会上发布Android 16操作系统，深度整合Gemini AI助手，提供前所未有的智能体验。新系统支持设备端大模型运行，用户可在离线状态下使用AI翻译、图像生成和文档摘要等功能。Android 16还引入隐私沙盒2.0，大幅限制应用追踪用户行为。谷歌同时发布Pixel 10系列手机，搭载自研Tensor G5芯片。", "image": "news_20260616_07.png"},
    {"number": "08", "tag": "国际", "title": "俄乌和平谈判取得进展 双方就停火协议框架达成共识", "summary": "俄罗斯与乌克兰代表团在土耳其安卡拉的和平谈判取得重要进展，双方就停火协议框架大部分条款达成共识。谈判在联合国和土耳其共同斡旋下进行，重点讨论了停火监督机制、战俘交换程序和部分地区撤军安排。美国和欧盟对谈判进展表示欢迎，但提醒各方保持谨慎，最终协议仍需双方议会批准。", "image": "news_20260616_08.png"},
    {"number": "09", "tag": "金融", "title": "比特币价格跌至9万美元 加密货币市场经历大幅回调", "summary": "比特币价格在全球监管收紧和机构获利了结的压力下跌至9万美元，较今年高点回落超过30%。加密货币总市值缩水至3.5万亿美元，以太坊同步下跌。美国证券交易委员会对多家交易所展开调查，要求提供用户资产安全保障措施。分析师认为短期波动不改长期趋势，机构投资者仍在逢低买入。", "image": "news_20260616_09.png"},
    {"number": "10", "tag": "社会", "title": "全球AI工程师平均年薪突破60万美元 人才争夺白热化", "summary": "猎头公司最新报告显示，全球AI和大模型领域高级人才薪酬再创新高，具备多模态模型训练经验的工程师年薪普遍超过60万美元，顶尖科学家年薪可达500万美元以上。谷歌、微软和Meta为争夺顶级AI人才展开激烈竞价，签署即用奖金屡创新高。中国科技企业在硅谷的研发中心持续扩张，争夺全球AI人才。", "image": "news_20260616_10.png"},
    {"number": "11", "tag": "科技", "title": "微软发布量子芯片Majorana 1 量子计算实用化进程加速", "summary": "微软发布Majorana 1量子计算芯片，这是全球首款基于马约拉纳费米子的商业量子处理器。微软表示该芯片实现了量子纠错的重大突破，错误率较传统量子计算机降低100倍。Majorana 1可在常温下运行，无需昂贵稀释制冷设备。微软宣布与多家金融机构和制药公司合作，探索量子计算实际应用场景。", "image": "news_20260616_11.png"},
    {"number": "12", "tag": "经济", "title": "中国5月CPI同比上涨0.3% 消费市场温和复苏", "summary": "中国国家统计局公布5月居民消费价格指数（CPI）同比上涨0.3%，涨幅较上月扩大0.1个百分点。食品价格小幅下降，服务价格上涨0.5%成为主要支撑。5月社会消费品零售总额同比增长3.1%，消费市场延续复苏态势。分析认为居民消费信心仍需进一步提振，财政政策有望继续发力。", "image": "news_20260616_12.png"},
    {"number": "13", "tag": "社会", "title": "日本少子化问题持续加剧 政府推出史上最强生育补贴", "summary": "日本厚生劳动省公布最新人口数据，全国新生儿人数连续第10年创历史新低。日本政府宣布将推出史上最强生育补贴政策，育儿家庭每月可获10万日元补助，孩子入园费用全免，多子女家庭购房最高补贴500万日元。人口学家警告即使政策力度空前，生育率反弹仍需至少5至10年观察期。", "image": "news_20260616_13.png"},
    {"number": "14", "tag": "金融", "title": "纳斯达克指数突破20000点 科技股领涨全球股市", "summary": "受AI板块业绩超预期提振，纳斯达克综合指数首次突破20000点整数关口，创历史新高。英伟达、苹果和微软等科技巨头股价集体走高，带动全球科技股上涨。欧洲斯托克50指数上涨0.8%，日经225指数上涨1.1%。资金持续流入科技主题ETF，新兴市场股市净流入超过50亿美元。", "image": "news_20260616_14.png"},
    {"number": "15", "tag": "文化", "title": "国产科幻大片《星际探索》票房突破8亿美元 好莱坞竞争加剧", "summary": "中国科幻大片《星际探索》全球票房突破8亿美元，超越《流浪地球3》成为最卖座的中国科幻电影。该片讲述人类首次载人登陆木星的壮举，特效制作水准比肩好莱坞一线大片。影片在北美和欧洲市场表现超出预期，IMAX银幕占比超过40%。中国科幻电影工业体系日趋成熟，引发国际电影界广泛关注。", "image": "news_20260616_15.png"},
    {"number": "16", "tag": "体育", "title": "2026年世界杯开幕倒计时30天 美国筹备史上最盛大足球盛会", "summary": "2026年世界杯开幕倒计时30天，这是首次由美国、加拿大和墨西哥三国联合举办的世界杯。48支球队将在16个主办城市角逐大力神杯，赛事总投入超过200亿美元。开幕式将在纽约大都会球场举行，预计吸引超过10万现场观众。中国男足将首次亮相世界杯决赛圈，首场小组赛对阵荷兰。", "image": "news_20260616_16.png"},
    {"number": "17", "tag": "国际", "title": "印度总理莫迪访问欧盟 签署绿色氢能合作协议", "summary": "印度总理莫迪访问比利时布鲁塞尔，与欧盟委员会主席签署绿色氢能全面合作协议。欧盟将在未来10年向印度提供200亿欧元投资，用于建设绿色氢能生产和出口基地。作为交换，印度将向欧洲出口低成本绿色氢气，帮助欧盟实现能源转型目标。这一合作被视为印欧关系的重大突破，也对全球能源格局产生深远影响。", "image": "news_20260616_17.png"},
    {"number": "18", "tag": "科技", "title": "斯坦福AI报告更新 中国AI论文数量连续三年全球第一", "summary": "斯坦福大学人类中心人工智能研究所更新2026年AI指数报告，中国在AI学术论文数量和质量方面连续第三年领跑全球。中国2025年AI论文发表量超过38万篇，占全球总量42%以上，高被引论文数量较2020年增长350%。美国在AI芯片算力和创业投资方面仍占优势，中国在AI应用落地方面进展迅速。", "image": "news_20260616_18.png"},
    {"number": "19", "tag": "社会", "title": "华北地区遭遇强降雨 国家防总启动三级应急响应", "summary": "受副热带高压影响，华北地区遭遇大范围强降雨，局部地区降雨量突破历史极值。国家防汛抗旱总指挥部启动三级应急响应，要求各地做好城市内涝防范和山洪灾害预警。北京市出动超过2万名排水工人和应急救援人员，重点保障地铁和地下空间安全。气象部门提醒未来三天华北地区仍有强降雨，公众需注意防范。", "image": "news_20260616_19.png"},
    {"number": "20", "tag": "经济", "title": "全球电动汽车渗透率突破50% 中国市场新能源车占比超80%", "summary": "国际能源署发布全球电动汽车市场报告，今年上半年全球电动汽车销量突破1800万辆，渗透率首次突破50%大关。中国市场新能源汽车渗透率高达80%，比亚迪以月销80万辆的成绩稳居全球第一。欧洲市场增速放缓，特斯拉在欧洲市场份额持续下滑。动力电池技术迭代加速，固态电池开始批量装车。", "image": "news_20260616_20.png"},
]

# Build the new news grid HTML
new_news_grid = '            <div class="news-grid" id="newsGrid">\n'

for item in news_items:
    new_news_grid += f'''                <article class="news-card" data-tag="{item['tag']}">
                    <img class="news-image" src="images/{item['image']}" alt="{item['title']}" loading="lazy">
                    <div class="news-content">
                        <span class="news-number">{item['number']}</span>
                        <h3 class="news-title">{item['title']}</h3>
                        <p class="news-summary">{item['summary']}</p>
                        <div><span class="tag">{item['tag']}</span></div>
                    </div>
                </article>
'''

new_news_grid += '            </div>'

# Find and replace the news-grid section
start_marker = '<div class="news-grid" id="newsGrid">'
start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: Could not find news-grid start marker")
    exit(1)

# Find where news-grid closes
search_from = start_idx + len(start_marker)
end_idx = content.find('\n            </div>', search_from)
if end_idx == -1:
    print("ERROR: Could not find news-grid end marker")
    exit(1)
end_idx += len('\n            </div>')

old_news_grid = content[start_idx:end_idx]

# Verify old content
old_card_count = old_news_grid.count('<article class="news-card"')
print(f"Found {old_card_count} existing news cards")

# Replace
new_content = content[:start_idx] + new_news_grid + content[end_idx:]

# Verify new content
new_card_count = new_content.count('<article class="news-card"')
print(f"New content has {new_card_count} news cards")

# Write back
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("index.html updated successfully")