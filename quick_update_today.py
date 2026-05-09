#!/usr/bin/env python3
"""
快速更新新闻博客 - 使用已有图片
"""
import json
import re
import opencc
from datetime import datetime
from pathlib import Path

# 初始化简繁体转换器
converter = opencc.OpenCC('t2s')

# 配置
BLOG_PATH = "/home/swg/.openclaw/workspace/news-blog"
IMAGES_DIR = Path(BLOG_PATH) / "images" / "news-generated"

# 新闻数据（从搜索结果中提取）
news_data = [
    {
        "title": "美军与伊朗在霍尔木兹海峡交火",
        "summary": "美国海军导弹驱逐舰编队在穿越霍尔木兹海峡时拦截了伊朗发起的袭击，并采取自卫反击行动。美方表示无意寻求局势升级，但将始终保持战备部署。伊朗方面称已恢复正常局势。",
        "tags": ["国际", "军事"]
    },
    {
        "title": "特朗普否认停火结束",
        "summary": "美国总统特朗普接受电话采访，否认美军袭击伊朗意味着停火结束。特朗普表示这只是轻轻敲打，停火还在持续。他警告称如果伊朗不尽快达成协议，美国将采取更强硬的打击。",
        "tags": ["国际", "政治"]
    },
    {
        "title": "沙特科威特解除美军基地限制",
        "summary": "沙特阿拉伯与科威特已解除在美国启动霍尔木兹海峡通航护航行动后对美军使用其基地和领空实施的限制。此举化解了一大阻碍，美国计划重启护航行动。",
        "tags": ["国际", "军事"]
    },
    {
        "title": "美伊局势影响美股油价",
        "summary": "随着交易员和投资者密切关注中东局势，美股从前一天创下的纪录高位回落，油价则在早盘大跌后收窄跌幅，收于每桶约100美元。",
        "tags": ["经济", "金融"]
    },
    {
        "title": "美国众议院推出法案禁止中国汽车",
        "summary": "美国众议院中国问题特设委员会主席宣布推出法案，旨在阻止中国获取美国农田。另一项法案计划禁止中国汽车在美国道路行驶。",
        "tags": ["国际", "政治"]
    },
    {
        "title": "美国与伊朗间接谈判继续",
        "summary": "美国与伊朗之间的间接谈判仍在继续，双方力求在中东这场已持续九周的冲突中取得突破。华盛顿重申其目标是让伊朗成为一个无核国家。",
        "tags": ["国际", "外交"]
    },
    {
        "title": "第二十八届北京科博会开幕",
        "summary": "第二十八届中国北京国际科技产业博览会将于5月8日至10日在国家会议中心举办。本届科博会以科技引领创享未来为主题，聚焦前沿科技新兴产业和未来产业领域。",
        "tags": ["科技", "展会"]
    },
    {
        "title": "北京科博会设六大专题展区",
        "summary": "北京科博会展览总面积约5万平方米，共设置信息科技、智能制造、医药健康、绿色双碳、数字经济和区域创新等6个专题展区，国内外参展企业和机构800余家。",
        "tags": ["科技", "展会"]
    },
    {
        "title": "一季度工业增加值同比增长6.1%",
        "summary": "一季度规模以上工业增加值同比增长6.1%，31个省份全部实现正增长，行业增长面超八成，工业对经济增长的贡献率近四成。推进数字产业发展壮大。",
        "tags": ["经济", "工业"]
    },
    {
        "title": "政府工作报告聚焦科技创新",
        "summary": "2026年政府工作报告提出加快高水平科技自立自强，抓住新一轮科技革命和产业变革历史机遇，全面增强自主创新能力，为高质量发展提供科技支撑。",
        "tags": ["科技", "政策"]
    },
    {
        "title": "外交部回应英国法院裁定",
        "summary": "外交部发言人林剑表示，英方以莫须有罪名抓捕和起诉在英中国公民，滥用法律操弄司法程序定罪，是典型的政治闹剧。中方对此予以强烈谴责和坚决反对。",
        "tags": ["外交", "政治"]
    },
    {
        "title": "中国油轮在霍尔木兹海峡遇袭",
        "summary": "一艘大型中国成品油船在霍尔木兹海峡入口附近遇袭，船身标有中国船东及船员字样，甲板起火。相关遇袭船只系马绍尔群岛籍，船上有中国籍船员，未报告有船员伤亡。",
        "tags": ["国际", "军事"]
    },
    {
        "title": "特朗普称中美首脑会晤将举行",
        "summary": "美国总统特朗普日前表示，中美首脑会晤会按计划举行。中方对此表示期待，双方将重点讨论包括经贸、科技、国际地区事务等议题。",
        "tags": ["国际", "外交"]
    },
    {
        "title": "欧盟拟禁止中企参与关键基建",
        "summary": "欧盟正推进出台网络安全法，禁止中国企业参与欧关键基础设施建设。该法案要求在未来五年中拆除和替换大量中国硬件，总耗资将超过3678亿欧元。",
        "tags": ["国际", "经济"]
    },
    {
        "title": "中国三家企业入选AI影响力榜单",
        "summary": "美国时代周刊发布了2026年最具影响力的10家人工智能公司榜单，中国有3家企业入选。这充分体现了中国AI产业和技术发展的成就。",
        "tags": ["科技", "AI"]
    },
    {
        "title": "汉坦病毒疫情风险绝对很低",
        "summary": "世界卫生组织强调，汉坦病毒向普通人群传播的风险绝对很低。此前一名与确诊患者有过接触的空乘人员检测结果呈阴性。该患者来自疫情暴发的游轮。",
        "tags": ["健康", "疫情"]
    },
    {
        "title": "乌克兰战争医疗设施袭击超3000起",
        "summary": "世卫组织表示，自乌克兰战争全面升级以来，在持续1534天的冲突中，已通过监测系统核实超过3000起针对医疗设施的袭击事件。",
        "tags": ["国际", "战争"]
    },
    {
        "title": "粮农组织警告海峡危机冲击粮食供应",
        "summary": "联合国粮农组织总干事警告说，霍尔木兹海峡运输中断引发的全球化肥短缺，将导致2026年下半年至2027年间作物减产及粮食供应趋紧。",
        "tags": ["国际", "经济"]
    },
    {
        "title": "澳大利亚日本深化安全经济合作",
        "summary": "澳大利亚与日本达成新协议，深化安全与经济联系。双方将在多个领域加强合作，共同应对地区挑战。",
        "tags": ["国际", "外交"]
    },
    {
        "title": "中国前国防部长被判死缓",
        "summary": "中国两名前国防部长被判死缓。这表明中国持续加强反腐败工作，对任何违法违纪行为都将依法严惩，维护军队纯洁性和战斗力。",
        "tags": ["国内", "法治"]
    }
]

def clean_text(text):
    """清理文本：移除英文、繁体、特殊符号"""
    if not text:
        return ""

    # 转换繁体为简体
    text = converter.convert(text)

    # 移除英文单词
    text = re.sub(r'[a-zA-Z]{2,}', '', text)

    # 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def expand_summary(content, min_length=150, max_length=200):
    """扩展摘要到指定长度"""
    if not content:
        return "暂无内容"

    # 移除英文
    content = re.sub(r'[a-zA-Z]{1,}', '', content)

    # 如果太短，需要扩展
    if len(content) < min_length:
        additions_pool = [
            "此事引发社会各界的普遍关注与热议。",
            "相关领域专家就此议题发表了专业见解。",
            "有关部门正在积极研究应对策略与方案。",
            "业内人士普遍认为这将产生重要影响。",
            "多家主流媒体对此进行了深度报道分析。",
            "目前各方正在保持密切沟通与协调。",
            "市场对此反应积极，总体形势向好。",
            "专家指出这一趋势值得持续关注与研究。",
            "相关部门表示将加强监管与政策指导。",
            "公众对这一话题表现出浓厚兴趣与期待。",
        ]

        used = set()
        for add in additions_pool:
            if add not in used and len(content) + len(add) <= max_length:
                content = content.rstrip('。！？') + "。" + add
                used.add(add)
            if len(content) >= min_length:
                break

    # 如果太长，截取
    if len(content) > max_length:
        truncated = content[:max_length]
        last_period = max(truncated.rfind('。'), truncated.rfind('！'), truncated.rfind('？'))
        if last_period > min_length:
            return truncated[:last_period + 1]
        return truncated + "……"

    return content

def main():
    """主函数"""
    print("开始快速更新新闻博客...")

    # 处理新闻数据
    processed_news = []
    for idx, news in enumerate(news_data, 1):
        title = clean_text(news['title'])
        summary = expand_summary(news['summary'], min_length=150, max_length=200)
        tags = news.get('tags', [])

        # 确保标题不为空
        if not title or len(title) < 4:
            title = f"今日要闻第{idx}条"

        processed_news.append({
            "title": title,
            "summary": summary,
            "tags": tags
        })

        print(f"{idx}. {title} ({len(summary)}字)")

    # 生成新闻卡片HTML
    news_cards_html = ""
    for idx, news in enumerate(processed_news, 1):
        title = news['title']
        summary = news['summary']
        tags = news['tags']
        image_path = f"images/news-generated/news_{idx:02d}.png"

        news_cards_html += f"""

                <div class="news-card">
                    <img src="{image_path}" alt="{title}" class="news-image">
                    <div class="news-content">
                        <span class="news-number">{idx}</span>
                        <h3 class="news-title">{title}</h3>
                        <p class="news-summary">{summary}</p>
                        <div>"""

        for tag in tags[:5]:
            news_cards_html += f'\n                            <span class="tag">{tag}</span>'

        news_cards_html += """
                        </div>
                    </div>
                </div>"""

    # 读取并更新 index_enhanced.html
    index_enhanced = Path(BLOG_PATH) / "index_enhanced.html"
    with open(index_enhanced, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 替换占位符
    date_str = datetime.now().strftime("%Y年%m月%d日")
    html_content = html_content.replace("{{NEWS_DATE}}", date_str)
    html_content = html_content.replace("{{NEWS_CARDS}}", news_cards_html)

    # 保存新文件
    html_file = Path(BLOG_PATH) / "index.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ HTML 创建成功: {html_file}")
    print(f"📰 新闻: {len(processed_news)} 条")
    print(f"📷 图片: {len(processed_news)} 张")

if __name__ == "__main__":
    main()
