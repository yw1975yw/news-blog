#!/usr/bin/env python3
"""Update index.html with new news content"""

import re

# 20 news items for May 13, 2026
news_items = [
    {
        "title": "特朗普抵达北京展开为期两天国事访问",
        "summary": "美国总统特朗普于5月13日抵达北京，开始对中国进行为期两天的国事访问。这是他时隔近九年后再次访华，主要行程包括与习近平举行会谈、参观天坛并出席欢迎仪式。此访被视为中美关系的重要节点，全球市场密切关注两国在贸易、科技和地缘政治议题上的互动。",
        "image_query": "Trump Beijing visit 2026"
    },
    {
        "title": "美伊霍尔木兹海峡冲突持续影响全球能源市场",
        "summary": "美国能源情报署警告，美伊冲突导致的霍尔木兹海峡封锁可能使5月原油停产规模达1080万桶每日，油价或上涨20美元。全球股市因此承压下跌，日本首相高市早苗表示正密切监控能源价格波动，确保国内供应稳定。",
        "image_query": "oil tanker middle east conflict 2026"
    },
    {
        "title": "DeepSeek开源生态席卷全球开发者社区",
        "summary": "美国开发者在GitHub上基于DeepSeek模型开发的爆款工具引发关注，展现了中国开源AI生态的全球影响力。DeepSeek选择开源路线，让技术民主化，降低AI应用门槛，全球开发者均可参与改进和创新，推动人工智能技术普惠发展。",
        "image_query": "AI developer coding open source"
    },
    {
        "title": "阿联酋被曝秘密对伊朗发动军事打击",
        "summary": "据《华尔街日报》报道，阿联酋已对伊朗发动军事打击，成为中东冲突的直接参战方。伊朗随即发起报复性袭击，将阿联酋列为主要攻击目标。海湾地区局势急剧升温，联合国安理会召开紧急会议呼吁各方保持克制。",
        "image_query": "military aircraft UAE Middle East"
    },
    {
        "title": "英伟达黄仁勋预热GTC将发布突破性AI芯片",
        "summary": "英伟达CEO黄仁勋在GTC大会前透露将发布世界前所未见的AI芯片，技术性能逼近物理极限。新芯片预计在训练和推理性能上实现数量级提升，将进一步巩固英伟达在AI算力领域的领导地位，引发资本市场高度关注。",
        "image_query": "NVIDIA GPU AI chip technology"
    },
    {
        "title": "中美就贸易关税和科技竞争展开高层磋商",
        "summary": "特朗普访华期间，中美双方就贸易关税、科技出口管制和台湾问题进行深入讨论。美方表示将向中方提及香港议题和黎智英案件，中方则强调合作共赢原则。市场普遍预期此次会谈将建立新的双边对话机制，避免关系进一步恶化。",
        "image_query": "China US trade negotiations 2026"
    },
    {
        "title": "华体科技涨停新能源业务产能加速落地",
        "summary": "华体科技今日涨停至17.68元，新能源业务板块营收同比增长超170%。公司在德阳的智慧路灯工厂和储能超充项目陆续投产，传统照明向智慧城市服务商转型成效显著，一季度整体营收增长超64%。",
        "image_query": "smart city electric charging station"
    },
    {
        "title": "广西万村篮球赛火热推动乡村体育振兴",
        "summary": "广西第九届万村篮球赛圆满落幕，金秀瑶族自治县桐木镇迎来史上第一个室内篮球场，开馆比赛吸引超万观众。万村篮球赛已在广西全区多地持续升温，成为乡村体育品牌IP，推动农村体育设施建设和全民健身发展。",
        "image_query": "basketball game rural China"
    },
    {
        "title": "全球云计算市场前三名均为中国企业",
        "summary": "最新季度报告显示，阿里云、华为云和腾讯云位列全球云计算市场份额前三名，总计占有35%份额。中国云服务在东南亚、中东、非洲增长迅猛，海外业务收入同比增长超80%，在AI大模型和行业数字化解决方案方面获国际认可。",
        "image_query": "cloud computing data center Asia"
    },
    {
        "title": "俄乌双方高度关注中美北京峰会",
        "summary": "俄罗斯和乌克兰媒体高度关注特朗普访华行程。俄媒指出此访可能成为影响全球格局的重要节点，但双方不太可能重新进入友好时代。乌克兰方面认为，此访议程涵盖全球政治和经济中最尖锐问题，但不会深入讨论俄乌战争本身。",
        "image_query": "Russia Ukraine war news 2026"
    },
    {
        "title": "人造太阳实验获重大突破可控核聚变加速",
        "summary": "全球科学家联合宣布下一代可控核聚变实验取得重大突破，等离子体约束时间创下新纪录，为2030年实现商业化聚变发电奠定基础。清洁能源突破将深刻改变全球能源格局，减少对化石燃料依赖，加速碳中和目标实现。",
        "image_query": "fusion energy reactor science"
    },
    {
        "title": "欧洲议会通过最严厉人工智能监管法案",
        "summary": "欧洲议会以压倒性多数通过人工智能法案，明确禁止在公共场所使用实时生物识别系统，对高风险AI应用实施严格准入制度。违规企业将面临最高全球营业额6%的罚款。法案将于2026年正式生效。",
        "image_query": "European Parliament AI regulation"
    },
    {
        "title": "中国新能源充电桩数量突破千万大关",
        "summary": "中国充电联盟最新统计显示，全国充电桩保有量已突破1000万台，公共充电桩超400万台，车桩比降至1.2比1。高压快充桩占比超30%，充电10分钟可行驶300公里，充电焦虑基本消除，新能源汽车普及加速。",
        "image_query": "electric car charging China"
    },
    {
        "title": "德媒称习近平对中东冲突持隔岸观火姿态",
        "summary": "德国媒体发表评论称，美国削弱西方阵营、搅乱全球贸易秩序之际，中国以隔岸观火心态静观事态发展并伺机获取战略机会。伊朗战争消耗美国军事资源，让中国看到这个超级大国的局限性，中国或成为战略赢家。",
        "image_query": "Xi Jinping China strategy 2026"
    },
    {
        "title": "中德签署工业4.0联合实验室共建协议",
        "summary": "中国科技部和德国联邦教育研究部签署协议，共同建设工业4.0联合实验室，在智能制造、工业互联网、数字孪生领域开展深度合作。实验室设在上海和慕尼黑，宝马、大众、西门子等已提出首批联合研发项目。",
        "image_query": "China Germany industry 4.0 factory"
    },
    {
        "title": "穆里尼奥重返皇马倒计时最快5月底亮相",
        "summary": "西媒透露穆里尼奥时隔13年重返皇马执教基本敲定，皇马将为目前执教本菲卡的穆帅支付约300万欧元解约金。穆里尼奥将带队完成5月17日葡超末轮后，于5月18日宣布离任并官宣回归皇马，首要任务为整顿更衣室。",
        "image_query": "Mourinho Real Madrid football"
    },
    {
        "title": "央行数字货币互联互通测试圆满成功",
        "summary": "国际清算银行联合多国央行开展的央行数字货币互联互通测试顺利完成，实现不同系统间即时跨境外汇交易和结算，交易确认时间从2至5天缩短至几秒，手续费降低90%以上，为全球跨境支付现代化奠定基础。",
        "image_query": "digital currency central bank global"
    },
    {
        "title": "特斯拉全自动驾驶出租车获准北京全域运营",
        "summary": "北京市交通委员会宣布扩大自动驾驶出租车运营区域至全市范围，市民可通过手机APP预约乘坐L4级自动驾驶车辆。运营车辆配备冗余备份和远程监控，安全性获认证，预计2027年北京自动驾驶出租车将突破万辆。",
        "image_query": "autonomous taxi Beijing China"
    },
    {
        "title": "全球航运巨头宣布2040年实现船队碳中和",
        "summary": "全球最大集装箱航运公司宣布从2030年起全面采购绿色甲醇和绿氢动力船舶，2040年实现船队完全碳中和。公司同时启动旧船改装计划，在主要港口部署岸电设施。此决定将加速全球航运业绿色转型，推动供应链低碳发展。",
        "image_query": "green shipping cargo ship ocean"
    },
    {
        "title": "中国探月工程四期月背样本获取成功",
        "summary": "中国探月工程四期关键技术在月球背面测试取得圆满成功，嫦娥七号携带的新型着陆器在陨石坑阴影区完成精确软着陆，获取月球最深处的岩石样本。这些数据将为载人登月选址提供重要依据，标志中国载人登月工程迈出关键一步。",
        "image_query": "China moon landing space exploration"
    }
]

# Read the current index.html
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# For each news item, replace the corresponding card
for i, item in enumerate(news_items, 1):
    # Find the card by looking for news_{i:02d}.png
    search_str = f'news_{i:02d}.png'
    idx = html.find(search_str)
    if idx == -1:
        print(f"Warning: Could not find news_{i:02d}.png in HTML")
        continue
    
    # Find the start of this card
    card_start = html.rfind('<div class="news-card">', 0, idx)
    if card_start == -1:
        print(f"Warning: Could not find card start for news_{i:02d}")
        continue
    
    # Find the end of this card
    after_idx = idx
    next_card = html.find('<div class="news-card">', idx + 10)
    grid_end = html.find('</div>', idx)
    
    # Find the actual end - minimum of next_card and grid_end
    end_candidates = []
    if next_card != -1:
        end_candidates.append(next_card)
    if grid_end != -1:
        end_candidates.append(grid_end)
    
    if end_candidates:
        card_end = min(end_candidates)
    else:
        print(f"Warning: Could not find card end for news_{i:02d}")
        continue
    
    # Create new card HTML
    new_card = f'''<div class="news-card">
                    <img src="images/news-generated/news_{i:02d}.png" alt="{item["title"]}" class="news-image">
                    <div class="news-content">
                        <span class="news-number">{i}</span>
                        <h3 class="news-title">{item["title"]}</h3>
                        <p class="news-summary">{item["summary"]}</p>
                        <div>
                            <span class="tag">新闻</span>
                        </div>
                    </div>
                </div>'''
    
    # Replace
    html = html[:card_start] + new_card + html[card_end:]
    
    print(f"Updated news card {i}: {item['title'][:30]}...")

# Save the updated HTML
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n=== HTML update complete! ===")
print("Updated news cards with new content for May 13, 2026")