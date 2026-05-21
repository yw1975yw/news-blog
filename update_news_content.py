#!/usr/bin/env python3
import re
from pathlib import Path

news_items = [
    ("内塔尼亚胡反对结束伊朗战争协议，特朗普为外交进程辩护", "以色列总理内塔尼亚胡强烈反对一项旨在结束与伊朗战争的协议，认为该协议让步过多。特朗普总统则为外交进程辩护，表示通过谈判施压符合美国利益。美方以重启军事打击相威胁，意在逼迫伊朗在谈判中作出实质让步，中东局势再度紧张。"),
    ("三星管理层与工会达成初步协议避免罢工", "三星电子管理层与工会代表经过多轮谈判，达成初步协议，成功避免了一场可能影响全球芯片供应的大规模罢工。协议内容包括提高工人薪酬福利、改善工作环境等措施。三星股价应声上涨，市场对芯片供应稳定的预期增强。"),
    ("特朗普结束访华，习近平邀请其9月访白宫", "美国总统特朗普结束对中国的访问，习近平主席邀请其于9月24日访问白宫。访华期间，两国签署多项贸易协议，中国承诺购买超过200架波音飞机和大量美国农产品。特朗普称此访极其积极且富有成果，中美关系有望进入新的稳定期。"),
    ("普京第25次访华，中俄关系深化引发国际关注", "俄罗斯总统普京抵达北京进行第25次访华，习近平主席举行仪式欢迎。两国元首举行会谈并共同出席中俄教育年开幕式。中俄签署多项合作协议，涉及能源、基础设施、科技等领域。中俄关系的深化引发美国和欧洲的高度关注。"),
    ("美中签署数百亿美元贸易协议，波音飞机大单受关注", "中美两国在元首峰会期间签署多项贸易协议，总价值达数百亿美元。中国承诺购买200多架波音飞机、通用电气发动机及大量美国农产品。美国贸易代表表示，预计中国将签署价值上百亿美元的美国农产品采购协议。"),
    ('特朗普警告伊朗"时钟正滴答作响"，中东战火重燃风险犹存', '美国总统特朗普在社交媒体发文警告伊朗"时钟正滴答作响"，如果不迅速行动达成协议，将遭受比之前更猛烈的打击。美方提出五项条件要求伊朗将400公斤浓缩铀交给美国，伊朗则态度强硬拒绝，军事选项再次被提上日程。'),
    ("俄乌战争接近尾声？普京暗示莫斯科或准备停火", "俄罗斯总统普京暗示俄乌战争可能正接近尾声，表示莫斯科已准备好通过谈判结束冲突。乌方对俄方表态持谨慎欢迎态度，联合国秘书长呼吁各方抓住这一机遇。战场形势仍存在不确定性，但国际社会对和平解决危机的期待上升。"),
    ("神舟二十三号载人飞行任务进行发射场演练", "神舟二十三号载人飞行任务各系统在发射场区进行全系统演练，为即将到来的发射任务做好准备。这是中国空间站建设的重要环节，航天员将在轨执行多项科学实验和技术测试任务。中国载人航天工程按计划稳步推进。"),
    ("高市早苗访问韩国，与李在明举行首脑会谈", "日本首相高市早苗访问韩国，与韩国总统李在明举行首脑会谈，双方就能源安全、经贸合作、地区局势等议题深入交换意见。这是近年来日本首相首次正式访韩，标志着韩日关系走出低谷。两国同意建立外长级定期磋商机制。"),
    ("联合国秘书长警告：封锁霍尔木兹海峡是全球性危机", "联合国秘书长访问日本时发出警告称，霍尔木兹海峡封锁正在引发全球性危机，对国际航运、能源供应和世界经济造成严重冲击。他呼吁有关方面保持克制，恢复对话以维护国际水道安全，全球供应链面临的压力持续加大。"),
    ("伊朗拒绝美方条件，核谈判陷入僵局", "伊朗方面拒绝美国提出的多项条件，包括要求伊朗将400公斤浓缩铀交给美国、仅保留一处核设施等。伊朗武装部队发言人警告，任何对伊军事行动都将导致美国遭受更猛烈的回应。伊朗认为时间在自己一边，对美态度强硬，核谈判前景不容乐观。"),
    ("美中领导人峰会讨论台湾问题，特朗普称不会为台湾出兵", "美中元首峰会上讨论了台湾议题，特朗普总统表示华盛顿与北京在台湾问题上不存在冲突，并称不会就台湾议题向习近平做出任何承诺。美国国防部消息显示，对台军售案正在审议中。台湾议题成为此次峰会的核心焦点之一。"),
    ("美国CIA局长访问古巴，讨论能源危机与人道援助", "美国中央情报局局长约翰·拉特克利夫访问古巴，与古巴官员就能源危机和人道主义援助问题举行会晤。美国国务卿卢比奥指责古巴政府在美国提出援助一事上撒谎。古巴面临日益加深的能源危机，电力供应紧张引发民众抗议。"),
    ("中国限制向美国出售关键矿产，半导体供应链博弈升级", "中国宣布限制向美国出售关键矿产，包括镓、锗等半导体制造必需材料。此举被视为对美科技封堵的反制措施，将对全球半导体产业产生深远影响。美国商务部表示正在评估供应链安全风险，呼吁盟友共同应对。"),
    ("G7财长和央行行长会议决定就AI模型风险对策汇总方策", "G7财长和央行行长会议在日本举行，决定就新型AI模型的风险管理汇总具体方策。日本政府此前已汇总高性能AI模型风险对策临时方案，获得各方积极响应。会议讨论了AI对金融稳定、就业市场的影响，同意加强跨国监管合作。"),
    ("数字人民币跨境支付服务扩展至50个国家和地区", "数字人民币国际化取得重大进展，跨境支付服务已扩展至全球50个国家和地区，覆盖亚洲、欧洲、非洲、美洲的主要经济体。跨境电商、跨境旅游、海外留学汇款等场景应用快速增长，月均交易额突破千亿元人民币。"),
    ("德国制造业PMI指数连续六个月回升，经济强劲复苏", "德国联邦统计局公布最新数据显示，制造业PMI指数已连续六个月保持在扩张区间，工业产出超出市场预期。机械设备、汽车制造、化工等支柱产业订单充足，对外贸易保持增长。分析师认为德国经济正从能源危机影响中完全恢复。"),
    ("塞尔维亚总统即将访华，推动两国全面战略伙伴关系", "应国家主席习近平邀请，塞尔维亚总统将对进行国事访问。访问期间，两国将签署涵盖经贸、基础设施、科技、文化等领域的多项合作协议。塞尔维亚是中国在中东欧地区的重要伙伴，此访将进一步深化两国传统友谊。"),
    ("美中发表AI联合声明，携手推动人工智能安全治理", "中美两国在元首峰会期间发表人工智能联合声明，就AI伦理规范、技术风险管控、跨境数据流动等核心议题达成重要共识。两国将共同推动建立全球AI治理框架，防止AI技术被滥用于军事和情报领域。此举为国际社会应对AI挑战提供重要表率。"),
    ("全球可再生能源投资首超化石能源，清洁能源时代加速到来", "国际能源署发布年度报告显示，2026年全球可再生能源投资总额首次超过化石能源投资，达到1.8万亿美元。太阳能和风能发电成本持续下降，已比化石燃料更具经济性。中国、欧盟和美国引领全球清洁能源转型，碳中和目标实现路径更加清晰。"),
]

BLOG_PATH = Path("/home/swg/.openclaw/workspace/news-blog")
index_file = BLOG_PATH / "index.html"
html = index_file.read_text(encoding="utf-8")

today_str = "20260521"
news_cards_html = ""
for idx, (title, summary) in enumerate(news_items, 1):
    img_src = f"images/news-generated/news_{today_str}_{idx:02d}.png"
    news_cards_html += f"""
                <div class="news-card">
                    <img src="{img_src}" alt="{title}" class="news-image">
                    <div class="news-content">
                        <span class="news-number">{idx}</span>
                        <h3 class="news-title">{title}</h3>
                        <p class="news-summary">{summary}</p>
                        <div>
                            <span class="tag">新闻</span>
                        </div>
                    </div>
                </div>
"""

start_marker = '<div class="news-grid" id="newsGrid">'
end_marker = '</div>\n            <div class="warning">'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx == -1:
    print(f"ERROR: start marker not found")
    exit(1)

if end_idx == -1:
    print(f"ERROR: end marker not found")
    # Try alternate end marker
    alt_end = '</div>\n        </div>\n        <div class="comments-section">'
    end_idx_alt = html.find(alt_end)
    if end_idx_alt != -1:
        end_idx = end_idx_alt + len('</div>\n        </div>\n        <div class="comments-section">') - len('<div class="comments-section">')
        end_marker = '</div>\n        <div class="comments-section">'
    else:
        print(f"ERROR: end marker not found either")
        exit(1)

end_idx += len(end_marker)
new_html = html[:start_idx] + start_marker + '\n' + news_cards_html + '\n            ' + end_marker + html[end_idx:]

actual_cards = new_html.count('class="news-card"')
print(f"Found {actual_cards} news cards")

index_file.write_text(new_html, encoding="utf-8")
print("Written successfully")

# Verify
verify = index_file.read_text(encoding="utf-8")
verify_count = verify.count('class="news-card"')
print(f"Verified: {verify_count} news cards in file")

first_card_idx = verify.find('class="news-card"')
snippet = verify[first_card_idx:first_card_idx+300]
print(f"First card snippet: {snippet[:150]}")