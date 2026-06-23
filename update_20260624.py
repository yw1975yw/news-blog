#!/usr/bin/env python3
"""Update index.html for 2026年06月24日"""
import re

news_cards = '''<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_20260624_01.png" alt="G7峰会在意大利索伦托开幕 聚焦AI监管与气候融资" loading="lazy">
    <div class="news-content">
        <span class="news-number">01</span>
        <h3 class="news-title">G7峰会在意大利索伦托开幕 聚焦AI监管与气候融资</h3>
        <p class="news-summary">2026年G7峰会在意大利索伦托正式开幕，议题聚焦人工智能监管与气候融资。中国、美国、英国等成员国领导人出席。峰会首日就AI安全框架达成初步共识，计划建立全球AI安全合作机制。气候方面，发达国家承诺到2030年将气候融资规模扩大至2000亿美元。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_20260624_02.png" alt="中欧举行峰会 双方签署共同应对气候变化联合声明" loading="lazy">
    <div class="news-content">
        <span class="news-number">02</span>
        <h3 class="news-title">中欧举行峰会 双方签署共同应对气候变化联合声明</h3>
        <p class="news-summary">中国与欧盟领导人峰会在布鲁塞尔举行，双方签署共同应对气候变化联合声明，承诺在碳中和、绿色能源等领域深化合作。中欧班列累计开行突破10万列，贸易额再创新高。双方还就电动汽车反补贴调查达成和解协议。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_20260624_03.png" alt="苹果发布Apple Intelligence 2.0 搭载自研AI芯片M5" loading="lazy">
    <div class="news-content">
        <span class="news-number">03</span>
        <h3 class="news-title">苹果发布Apple Intelligence 2.0 搭载自研AI芯片M5</h3>
        <p class="news-summary">苹果在WWDC开发者大会上发布Apple Intelligence 2.0系统，同时推出搭载自研M5芯片的新款Mac产品。M5芯片采用3纳米工艺，AI算力提升4倍。库克表示Apple Intelligence将全面融入iOS、macOS等系统，提供更智能的个人助理体验。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_20260624_04.png" alt="谷歌发布Gemini 3.0 Ultra 号称AGI实现重大突破" loading="lazy">
    <div class="news-content">
        <span class="news-number">04</span>
        <h3 class="news-title">谷歌发布Gemini 3.0 Ultra 号称AGI实现重大突破</h3>
        <p class="news-summary">谷歌发布Gemini 3.0 Ultra版本，官方宣称在通用人工智能领域实现重大突破。新模型在复杂推理、多步骤规划等任务上表现超越现有AI系统。谷歌还宣布Gemini将整合进所有Google服务，企业版用户已超过500万。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_20260624_05.png" alt="中国成功发射天宫空间站扩展舱 首次实现太空制造" loading="lazy">
    <div class="news-content">
        <span class="news-number">05</span>
        <h3 class="news-title">中国成功发射天宫空间站扩展舱 首次实现太空制造</h3>
        <p class="news-summary">中国载人航天工程办公室宣布，天宫空间站梦天实验舱与天和核心舱成功对接。航天员在轨进行了首次太空材料制造实验，成功生产出高纯度光纤预制棒。这标志着中国成为首个在太空实现规模化材料制造的国家。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_20260624_06.png" alt="SpaceX星舰完成首次商业任务 成功部署120颗卫星" loading="lazy">
    <div class="news-content">
        <span class="news-number">06</span>
        <h3 class="news-title">SpaceX星舰完成首次商业任务 成功部署120颗卫星</h3>
        <p class="news-summary">SpaceX星舰完成首次商业卫星部署任务，将120颗星链卫星送入轨道。此次任务验证了星舰的重复使用能力助推器与飞船均成功回收。SpaceX表示星舰将在明年实现每周一次的商业发射频率，大幅降低卫星发射成本。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="金融">
    <img class="news-image" src="images/news_20260624_07.png" alt="央行降准0.5个百分点 释放长期资金约1万亿元" loading="lazy">
    <div class="news-content">
        <span class="news-number">07</span>
        <h3 class="news-title">央行降准0.5个百分点 释放长期资金约1万亿元</h3>
        <p class="news-summary">中国人民银行宣布下调金融机构存款准备金率0.5个百分点，释放长期资金约1万亿元。央行表示此举旨在保持流动性合理充裕，降低实体经济融资成本。分析师认为降准将有效支持基建投资和房地产稳定发展。</p>
        <div><span class="tag">金融</span></div>
    </div>
</article>
<article class="news-card" data-tag="金融">
    <img class="news-image" src="images/news_20260624_08.png" alt="A股三大指数集体上涨 成交额突破2万亿元" loading="lazy">
    <div class="news-content">
        <span class="news-number">08</span>
        <h3 class="news-title">A股三大指数集体上涨 成交额突破2万亿元</h3>
        <p class="news-summary">A股市场今日放量大涨，沪指涨2.1%收复3400点，深成指涨2.8%，创业板指涨3.5%。两市成交额突破2.1万亿元，创年内新高。AI、半导体板块领涨，北向资金净流入超200亿元，市场情绪明显回暖。</p>
        <div><span class="tag">金融</span></div>
    </div>
</article>
<article class="news-card" data-tag="金融">
    <img class="news-image" src="images/news_20260624_09.png" alt="国际金价再创新高 突破每盎司2800美元" loading="lazy">
    <div class="news-content">
        <span class="news-number">09</span>
        <h3 class="news-title">国际金价再创新高 突破每盎司2800美元</h3>
        <p class="news-summary">国际金价持续走高，纽约商品交易所黄金期货价格突破每盎司2800美元关口，创历史新高。分析师指出地缘政治风险和全球央行降息预期是推动金价上涨的主要因素。黄金ETF持仓量持续增加，创近三年新高。</p>
        <div><span class="tag">金融</span></div>
    </div>
</article>
<article class="news-card" data-tag="金融">
    <img class="news-image" src="images/news_20260624_10.png" alt="中国数字人民币跨境支付系统上线 覆盖50个国家" loading="lazy">
    <div class="news-content">
        <span class="news-number">10</span>
        <h3 class="news-title">中国数字人民币跨境支付系统上线 覆盖50个国家</h3>
        <p class="news-summary">中国数字人民币跨境支付系统正式上线，首批覆盖50个国家和地区，支持实时汇兑和低成本跨境转账。该系统基于区块链技术， transactions可在数秒内完成。跨境电商从业者表示这将大幅降低外汇结算成本和时间。</p>
        <div><span class="tag">金融</span></div>
    </div>
</article>
<article class="news-card" data-tag="社会">
    <img class="news-image" src="images/news_20260624_11.png" alt="全国多地高温预警 电网负荷创历史新高" loading="lazy">
    <div class="news-content">
        <span class="news-number">11</span>
        <h3 class="news-title">全国多地高温预警 电网负荷创历史新高</h3>
        <p class="news-summary">中央气象台发布高温橙色预警，18个省份出现35℃以上高温，局部地区达40℃。国家电网数据显示，全国电网负荷突破12亿千瓦时，创历史新高。浙江、江苏等地启动有序用电方案，鼓励居民节约用电和错峰用电。</p>
        <div><span class="tag">社会</span></div>
    </div>
</article>
<article class="news-card" data-tag="社会">
    <img class="news-image" src="images/news_20260624_12.png" alt="新版国家医保药品目录发布 新增120种创新药" loading="lazy">
    <div class="news-content">
        <span class="news-number">12</span>
        <h3 class="news-title">新版国家医保药品目录发布 新增120种创新药</h3>
        <p class="news-summary">国家医保局发布2026年版国家医保药品目录，新增120种创新药，其中包括多款抗肿瘤和罕见病药物。目录内药品总数超过3100种。谈判药品价格平均降幅超过50%，创新药的可及性将大幅提升。</p>
        <div><span class="tag">社会</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_20260624_13.png" alt="中国科学家首次实现百公里量子直接通信" loading="lazy">
    <div class="news-content">
        <span class="news-number">13</span>
        <h3 class="news-title">中国科学家首次实现百公里量子直接通信</h3>
        <p class="news-summary">中国科学技术大学团队首次实现100公里量子直接通信，刷新世界纪录。该技术无需密钥分发即可实现安全通信，被认为是量子通信领域的重大突破。研究成果发表在《自然》杂志上，为未来量子互联网建设奠定基础。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_20260624_14.png" alt="华为发布鸿蒙PC操作系统 打破Windows垄断格局" loading="lazy">
    <div class="news-content">
        <span class="news-number">14</span>
        <h3 class="news-title">华为发布鸿蒙PC操作系统 打破Windows垄断格局</h3>
        <p class="news-summary">华为正式发布鸿蒙PC操作系统，面向企业和消费市场。该系统支持鸿蒙生态应用无缝衔接，余承东表示已有超过1000款应用完成适配。政府机关和国有企业被鼓励优先采用国产操作系统，Windows市场份额面临挑战。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="体育">
    <img class="news-image" src="images/news_20260624_15.png" alt="巴黎奥运会在即 中国代表团备战状态良好" loading="lazy">
    <div class="news-content">
        <span class="news-number">15</span>
        <h3 class="news-title">巴黎奥运会在即 中国代表团备战状态良好</h3>
        <p class="news-summary">距离巴黎奥运会开幕还有30天，中国体育代表团已完成最后阶段集训，备战状态良好。本届奥运会中国运动员将参加30个大项的比赛，跳水、举重、乒乓球等项目依然是夺金重点。代表团规模约400人，为历届境外参赛最大规模。</p>
        <div><span class="tag">体育</span></div>
    </div>
</article>
<article class="news-card" data-tag="体育">
    <img class="news-image" src="images/news_20260624_16.png" alt="国际足联宣布2030年世界杯将由西葡摩三国联办" loading="lazy">
    <div class="news-content">
        <span class="news-number">16</span>
        <h3 class="news-title">国际足联宣布2030年世界杯将由西葡摩三国联办</h3>
        <p class="news-summary">国际足联正式宣布2030年世界杯将由西班牙、葡萄牙和摩洛哥联合举办，这也是世界杯首次跨越三个大洲。摩洛哥的拉巴特和卡萨布兰卡将承办部分比赛。三国联合举办模式旨在促进足球运动在北非地区的普及。</p>
        <div><span class="tag">体育</span></div>
    </div>
</article>
<article class="news-card" data-tag="文化">
    <img class="news-image" src="images/news_20260624_17.png" alt="秦始皇陵考古新发现 出土世界最大青铜器" loading="lazy">
    <div class="news-content">
        <span class="news-number">17</span>
        <h3 class="news-title">秦始皇陵考古新发现 出土世界最大青铜器</h3>
        <p class="news-summary">陕西省考古研究院公布秦始皇陵最新考古成果，出土一件高1.8米、重达2.3吨的青铜鼎，是目前已知世界最大的青铜器。考古学家认为这可能是秦始皇用来祭祀天地的大型礼器，对研究秦代青铜铸造技术具有重要价值。</p>
        <div><span class="tag">文化</span></div>
    </div>
</article>
<article class="news-card" data-tag="文化">
    <img class="news-image" src="images/news_20260624_18.png" alt="第78届戛纳电影节开幕 中国导演竞逐金棕榈" loading="lazy">
    <div class="news-content">
        <span class="news-number">18</span>
        <h3 class="news-title">第78届戛纳电影节开幕 中国导演竞逐金棕榈</h3>
        <p class="news-summary">第78届戛纳电影节在法国开幕，中国导演的作品《黄河谣》入围主竞赛单元，争夺金棕榈奖。华语电影在戛纳电影节的表现受到国际影坛关注。中国演员舒淇担任本届电影节评委，这也是时隔十年再次有华人演员担任主竞赛评委。</p>
        <div><span class="tag">文化</span></div>
    </div>
</article>
<article class="news-card" data-tag="社会">
    <img class="news-image" src="images/news_20260624_19.png" alt="全国外卖骑手超过700万 新就业形态持续壮大" loading="lazy">
    <div class="news-content">
        <span class="news-number">19</span>
        <h3 class="news-title">全国外卖骑手超过700万 新就业形态持续壮大</h3>
        <p class="news-summary">人力资源社会保障部发布报告显示，全国外卖骑手、网约车司机等新就业形态从业人员超过7000万，其中外卖骑手超过700万人。新业态为灵活就业提供了大量岗位，但平台企业也在完善骑手保障体系，推动职业伤害保障试点。</p>
        <div><span class="tag">社会</span></div>
    </div>
</article>
<article class="news-card" data-tag="经济">
    <img class="news-image" src="images/news_20260624_20.png" alt="全国夏粮收购超预期 同比增长12%" loading="lazy">
    <div class="news-content">
        <span class="news-number">20</span>
        <h3 class="news-title">全国夏粮收购超预期 同比增长12%</h3>
        <p class="news-summary">国家粮食和物资储备局公布夏粮收购数据，全国夏粮收购量已超过3000万吨，同比增长12%。优质小麦收购比例提高，收购价格保持稳定。农业农村部表示夏粮丰收为全年粮食稳产增产打下坚实基础。</p>
        <div><span class="tag">经济</span></div>
    </div>
</article>'''

# Read the current index.html
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the date-related elements
content = content.replace('2026年06月23日', '2026年06月24日')
content = content.replace('20260623', '20260624')

# Replace all news cards - find the news-grid section
pattern = r'<div class="news-grid" id="newsGrid">.*?</div>\s*</div>'
replacement = f'<div class="news-grid" id="newsGrid">\n{news_cards}\n</div>\n    </div>'
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write the updated index.html
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html updated successfully for 2026年06月24日")