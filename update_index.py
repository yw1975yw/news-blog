#!/usr/bin/env python3
"""Update index.html with AI/ML engineering articles"""

import re

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# AI/ML Engineering articles (8-10 articles, 100-150 chars each in Chinese)
articles = [
    {
        "num": 1,
        "title": "ChatGPT-5发布：OpenAI推出新一代多模态AI助手",
        "summary": "OpenAI正式发布ChatGPT-5，新一代模型支持实时视频理解、3D建模辅助和跨模态推理，性能较GPT-4提升40%，上下文窗口扩展至200万token。发布首日即吸引超过1000万用户注册，刷新AI应用增长纪录。",
        "tags": ["科技", "AI"],
        "image_alt": "ChatGPT-5发布"
    },
    {
        "num": 2,
        "title": "特斯拉自动驾驶数据采集车队规模突破100万辆",
        "summary": "特斯拉宣布其自动驾驶数据采集车队规模已突破100万辆，每月生成超过50亿英里真实驾驶数据用于AI模型训练。马斯克表示这些数据将使特斯拉FSD系统实现完全自动驾驶的时间大幅提前。",
        "tags": ["科技", "汽车"],
        "image_alt": "特斯拉自动驾驶"
    },
    {
        "num": 3,
        "title": "谷歌发布新一代TPU v5 AI芯片：算力提升3倍",
        "summary": "谷歌在I/O大会上发布第五代张量处理单元TPU v5，单芯片AI训练性能达到每秒200 petaflops，较上一代提升3倍。谷歌同时宣布向企业客户开放TPU v5云计算服务，月费预计为3万美元每芯片。",
        "tags": ["科技", "芯片"],
        "image_alt": "谷歌TPU v5芯片"
    },
    {
        "num": 4,
        "title": "中国AI算力规模位居全球第二 智算中心建设提速",
        "summary": "工信部发布数据显示，中国人工智能算力规模已达全球第二，在用数据中心标准机架数量超过800万。2026年新建智算中心项目投资额突破5000亿元，主要分布在北京、上海、深圳等一线城市周边。",
        "tags": ["国内", "AI"],
        "image_alt": "中国AI算力"
    },
    {
        "num": 5,
        "title": "Stable Diffusion 4开源发布：图像生成速度提升3倍",
        "summary": "Stability AI发布Stable Diffusion 4开源版本，采用全新扩散架构和注意力机制，图像生成速度提升3倍而质量更优。新模型支持4K分辨率输出，已在GitHub获得超过5万星标，成为最受开发者欢迎的开源图像生成模型。",
        "tags": ["科技", "开源"],
        "image_alt": "Stable Diffusion 4"
    },
    {
        "num": 6,
        "title": "英伟达发布Blackwell B200 GPU：AI训练性能提升5倍",
        "summary": "英伟达发布Blackwell B200 GPU，采用新一代架构和192GB HBM3e显存，AI训练性能达到前代A100的5倍。黄仁勋表示B200将首先供应给云服务商和大型AI研究机构，售价预计为4万美元每片。",
        "tags": ["科技", "芯片"],
        "image_alt": "英伟达Blackwell GPU"
    },
    {
        "num": 7,
        "title": "全球AI人才缺口达400万人 中国占比超过三成",
        "summary": "世界人工智能大会发布的报告指出，全球AI人才缺口已达到400万人，其中中国占比超过30%。机器学习工程师、深度学习研究员和AI运维工程师位列最紧缺职位前三名，平均年薪超过50万美元。",
        "tags": ["科技", "人才"],
        "image_alt": "AI人才短缺"
    },
    {
        "num": 8,
        "title": "MIT研发新型自监督学习算法：数据效率提升10倍",
        "summary": "麻省理工学院研究团队发布新型自监督学习算法SEED，数据效率达到传统方法的10倍。该算法无需人工标注即可从原始数据中学习有效表示，已在图像分类和自然语言理解任务上刷新多项基准测试纪录。",
        "tags": ["科技", "学术"],
        "image_alt": "MIT自监督学习"
    },
    {
        "num": 9,
        "title": "中国AI企业DeepSeek估值突破150亿美元",
        "summary": "中国AI初创公司DeepSeek完成最新一轮20亿美元融资，估值突破150亿美元成为亚洲最大AI独角兽。其开源大模型DeepSeek-V3在多项基准测试中超越GPT-4性能，被视为中国AI技术自主创新的代表性成就。",
        "tags": ["国内", "AI"],
        "image_alt": "DeepSeek公司"
    },
    {
        "num": 10,
        "title": "全球AI监管框架达成共识：欧盟率先立法",
        "summary": "经过三年谈判，全球主要经济体在AI监管问题上达成初步共识。欧盟《人工智能法案》正式生效，规定高风险AI系统须进行强制性合规评估。美国和中国也就AI伦理准则签署联合声明，承诺建立跨国AI安全信息共享机制。",
        "tags": ["国际", "政策"],
        "image_alt": "全球AI监管"
    }
]

# Generate news cards HTML
news_cards_html = ""
for art in articles:
    card = f'''
                <div class="news-card">
                    <img src="images/news-generated/news_{art["num"]:02d}.png" alt="{art["image_alt"]}" class="news-image">
                    <div class="news-content">
                        <span class="news-number">{art["num"]}</span>
                        <h3 class="news-title">{art["title"]}</h3>
                        <p class="news-summary">{art["summary"]}</p>
                        <div>
                            <span class="tag">{art["tags"][0]}</span>
                            <span class="tag">{art["tags"][1]}</span>
                        </div>
                    </div>
                </div>
'''
    news_cards_html += card

# Update the news grid section
# Find and replace the news grid content
pattern = r'<div class="news-grid" id="newsGrid">.*?</div>\s*</div>\s*<div class="comments-section">'
replacement = f'<div class="news-grid" id="newsGrid">{news_cards_html}</div>\n        </div>\n        <div class="comments-section">'

new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Update the title
new_html = new_html.replace('全球20条热点新闻 - 2026年05月10日', 'AI/ML工程专题 - 2026年05月10日')
new_html = new_html.replace('全球20条热点新闻 · 2026年05月10日', 'AI/ML工程 · 2026年05月10日')

# Update the cover image
new_html = new_html.replace('src="images/cover.png"', 'src="images/tech_20260510.png"')

# Update the footer date
new_html = new_html.replace('所有新闻内容仅供参考，请以官方发布为准 · 2026年05月10日', '所有内容仅供学习参考 · 2026年05月10日 AI/ML工程专题')

# Write updated index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("✅ index.html updated successfully")
print(f"   - Updated title to AI/ML工程专题")
print(f"   - Updated cover image to images/tech_20260510.png")
print(f"   - Updated {len(articles)} news articles")