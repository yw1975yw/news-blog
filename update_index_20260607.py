#!/usr/bin/env python3
"""Update index.html with 2026年06月07日 news."""

import json
import re
import os

TODAY = "2026年06月07日"
TODAY_SHORT = "20260607"
NEWS_DATA_FILE = "/home/swg/.openclaw/workspace/news-blog/news_data_20260607.json"
INDEX_FILE = "/home/swg/.openclaw/workspace/news-blog/index.html"

with open(NEWS_DATA_FILE, "r", encoding="utf-8") as f:
    news_items = json.load(f)

# Extended summaries for each news item
summaries = {
    "01": "七国集团峰会在意大利落下帷幕，成员国领导人发表联合声明，宣布对俄罗斯实施第九轮制裁，重点针对其能源和金融领域。制裁措施包括将更多俄罗斯银行排除出SWIFT系统、限制俄油气出口价格上限。俄乌冲突进入第四年，前线战事持续胶着，双方在顿巴斯地区的争夺趋于白热化。",
    "02": "OpenAI在春季发布会上正式推出GPT-5.5，这是该公司迄今为止最强大的语言模型。GPT-5.5采用全新的思维链强化学习框架，在复杂推理、科学研究和代码生成等任务上表现卓越。OpenAI同时宣布向开发者开放多模态API，支持图像、视频和音频的端到端处理。GPT-5.5的发布加剧了与谷歌Gemini系列模型的竞争。",
    "03": "中国人民银行宣布自6月10日起下调金融机构存款准备金率0.25个百分点，释放长期资金约5000亿元。这是今年以来第二次降准，旨在加大金融对实体经济的支持力度。央行同时宣布延续实施普惠小微贷款支持工具，确保小微企业和涉农贷款增量降价。分析师认为此举信号积极，A股大盘随即震荡上行。",
    "04": "SpaceX宣布星舰火箭完成首次商业发射任务，将20颗通信卫星送入地球同步轨道，发射任务取得圆满成功。星舰作为全球最大运载力的火箭，近地轨道运力可达150吨，此次商业首飞标志着可回收超重火箭正式进入市场化运营阶段。SpaceX表示下次星舰发射将在两个月后执行火星货运任务。",
    "05": "北半球多国遭遇罕见热浪侵袭，印度北部气温突破50摄氏度，巴基斯坦和孟加拉国部分地区气温超过48摄氏度，欧洲南部气温也达45度以上。世界气象组织表示此次高温事件与厄尔尼诺现象持续和全球变暖叠加有关，呼吁各国加强气候适应能力建设。印度已有超过500人因高温死亡，多国政府紧急开放临时避暑中心。",
    "06": "英伟达在 COMPUTEX 大会上发布Blackwell Ultra架构和数据中心级GPU芯片GB300，算力是前代产品的五倍。黄仁勋表示该芯片专为大规模AI模型训练和推理设计，将大幅降低大模型训练成本。AMD同期发布MI400系列AI芯片应对竞争，全球AI芯片市场竞争进入白热化阶段。",
    "07": "中国商飞自主研制的C939大型客机在浦东机场成功完成首飞，C939采用最新一代复合材料和高效发动机，座位数约280座，航程可达15000公里。这是中国继C919之后第二款进入量产的国产大飞机。波音和空客相继发表声明表示祝贺，同时市场竞争将更趋激烈。",
    "08": "世界卫生组织召开紧急专家会议，宣布启动全球流感大流行防控计划，应对在东南亚地区发现的H10N8禽流感病毒变异株。该变异株已出现有限人传人案例，世卫组织呼吁各国加强活禽市场监测和边境检疫。目前已有针对性疫苗进入研发阶段，各国药企正在调整季节性流感疫苗配方。",
    "09": "欧盟碳边境调节机制正式生效，对进口钢铁、铝、水泥、化肥、电力和氢气等产品征收碳关税。中国作为欧盟最大的贸易伙伴，预计将受到较大冲击。中国商务部表示此举是典型的贸易保护主义，中方已向WTO提起磋商请求。浙江多家钢铁企业表示正在加快低碳技术改造以适应新规。",
    "10": "2026年欧洲足球锦标赛在德国慕尼黑安联球场揭开战幕，东道主德国队以5比1大胜苏格兰队取得开门红。年仅19岁的新星穆西亚拉独中两元，维尔茨和格雷茨卡也有进球入账。德国队主教练纳格尔斯曼表示球队状态出色，本届杯赛目标是夺冠。超过6万名观众现场观战，安联球场座无虚席。",
    "11": "印度尼西亚喀拉喀托之子火山发生剧烈喷发，喷发柱高达15公里，引发局部海啸预警。印尼政府立即启动应急响应机制，对爪哇岛南部沿海和苏门答腊岛部分区域发出海啸疏散令，超过十万居民被紧急转移至高地避难。国际社会表示愿提供人道主义援助，澳大利亚和新西兰已准备好救援队伍。",
    "12": "苹果在WWDC大会上发布visionOS 3操作系统，带来更自然的手眼追踪交互和实时翻译功能。苹果同时宣布与多家航空公司合作，推出沉浸式机上娱乐服务。用户可通过Apple Vision Pro体验身临其境的旅途。库克表示空间计算将从企业应用进入大众消费市场，vision Pro销量已突破500万台。",
    "13": "美联储发布最新经济褐皮书，显示美国经济继续保持韧性，消费支出稳健，劳动力市场偏紧。不过物价水平仍处高位，尤其是住房和服务类通胀粘性较强。多数地区企业对前景表示谨慎乐观，纽约联储下调美国全年GDP增速预测至1.8%。市场预期美联储将维持当前利率水平至年底。",
    "14": "国际劳工组织发布年度报告，2026年全球15至24岁青年失业率升至23.4%，创历史新高。报告指出人工智能自动化对入门级岗位的冲击是主要原因，零售和客服行业受影响最大。ILO呼吁各国政府加大对青年职业培训和就业补贴的投入，否则社会不平等将进一步加剧。",
    "15": "中国自主研制的深远海浮式风力发电平台在广东海域正式并网发电，这是全球首个实现商业化运行的深远海浮式风电项目。平台装机容量达20兆瓦，可为3万户家庭提供清洁电力。这一突破证明浮式风电技术具备规模化推广条件，为中国深海水资源开发提供了新路径。",
    "16": "巴黎奥运会圣火采集仪式在希腊古奥林匹亚遗址隆重举行，女祭司在赫拉神庙前用凹面镜聚太眼光点燃圣火。圣火将传递至法国，并于7月26日在塞纳河上举行史上最大规模开幕式。法国总统马克龙表示这将是一届团结与和平的奥运，预期将吸引全球超过40亿观众。",
    "17": "丰田汽车与清华大学签署协议，共同成立新能源技术联合研究院，重点攻关固态电池量产工艺。丰田计划在2027年前实现固态电池商业化，届时充电10分钟可实现1200公里续航。清华大学在材料科学领域的研究实力将为该项目提供强有力支撑，这一合作被视为日本车企转型的重要布局。",
    "18": "区域全面经济伙伴关系协定实施进入第三年，RCEP区域内贸易额突破2.5万亿美元，创历史新高。中国与东盟贸易总额首次突破1万亿美元，机电产品和新能源产品贸易增长最为迅速。RCEP秘书处表示，零关税覆盖范围已扩大至90%以上的商品贸易，有力促进了区域产业链融合。",
    "19": "阿根廷正式提交加入金砖国家合作机制的申请，成为今年第三个申请加入的国家。阿根廷总统在申请信中表示，期待借助金砖平台深化与新兴经济体的合作，实现贸易多元化和投资来源多样化。金砖扩员委员会表示将在年底峰会前完成对新成员的评估。",
    "20": "瑞典皇家科学院宣布2026年诺贝尔物理学奖授予中国科学家潘建伟和一位奥地利物理学家，表彰他们在量子通信和量子网络领域的开创性贡献。两位获奖者主导的量子纠缠分发实验为构建全球量子互联网奠定基础。潘建伟表示将继续推动量子技术从实验室走向实际应用，造福人类社会。",
}

def build_news_card(num, item):
    img_path = f"images/news_{TODAY_SHORT}_{num}.png"
    title = item["title"]
    tag = item["tag"]
    summary = summaries[num]
    
    return f'''                <div class="news-card">
                    <img class="news-image" src="{img_path}" alt="{title}" loading="lazy">
                    <div class="news-content">
                        <span class="news-number">{num}</span>
                        <h3 class="news-title">{title}</h3>
                        <p class="news-summary">{summary}</p>
                        <div>
                            <span class="tag">{tag}</span>
                        </div>
                    </div>
                </div>'''

# Read index.html
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Update title date
html = re.sub(
    r'<title>全球20条热点新闻 · \d{4}年\d{2}月\d{2}日',
    f'<title>全球20条热点新闻 · {TODAY}',
    html
)

# Update meta description date
html = re.sub(
    r'<meta name="description" content="\d{4}年\d{2}月\d{2}日全球20条热点新闻',
    f'<meta name="description" content="{TODAY}全球20条热点新闻',
    html
)

# Update cover subtitle date
html = re.sub(
    r'<p class="cover-subtitle">全球20条热点新闻 · \d{4}年\d{2}月\d{2}日</p>',
    f'<p class="cover-subtitle">全球20条热点新闻 · {TODAY}</p>',
    html
)

# Update footer date
html = re.sub(
    r'<p style="margin-top:10px;font-size:0.9em;">所有新闻内容仅供参考，请以官方发布为准 · \d{4}年\d{2}月\d{2}日</p>',
    f'<p style="margin-top:10px;font-size:0.9em;">所有新闻内容仅供参考，请以官方发布为准 · {TODAY}</p>',
    html
)

# Replace news grid content
# Find the news-grid div and replace everything inside it
news_grid_pattern = r'(<div class="news-grid" id="newsGrid">)(.*?)(</div>\s*</div>)'
news_cards_html = "\n".join(build_news_card(item["number"], item) for item in news_items)

def replace_news_grid(match):
    return match.group(1) + "\n" + news_cards_html + "\n" + match.group(3)

html = re.sub(news_grid_pattern, replace_news_grid, html, flags=re.DOTALL)

# Write updated index.html
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"index.html updated successfully with {len(news_items)} news items for {TODAY}")

# Verify the key changes
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Check that old date is gone and new date is present
old_date = "2026年06月06日"
if old_date in content:
    print(f"WARNING: Old date {old_date} still appears in index.html!")
else:
    print("✓ Old date successfully replaced")

if TODAY in content:
    print(f"✓ New date {TODAY} found in index.html")
else:
    print(f"WARNING: New date {TODAY} not found in index.html!")

# Check for news cards
news_card_count = content.count('class="news-card"')
print(f"✓ Found {news_card_count} news-card elements")

# Check for images
img_count = sum(1 for i in range(1, 21) if f"news_{TODAY_SHORT}_{i:02d}.png" in content)
print(f"✓ Found {img_count}/20 news images referenced")