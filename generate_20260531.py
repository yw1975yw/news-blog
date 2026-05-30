#!/usr/bin/env python3
"""Generate news for 20260531 and update index.html"""
import base64
import json
import os
import re
import subprocess
from pathlib import Path

WORKSPACE = "/home/swg/.openclaw/workspace/news-blog"
DATE_STR = "2026年05月31日"
DATE_HTML = "2026年05月31日"
DATE_FILE = "20260531"

NEWS = [
    {
        "number": "01",
        "title": "华为发布韬定律半导体新路线图 3D封装技术突破美国封锁",
        "summary": "华为在第28届国际电路与系统研讨会上正式发布韬定律半导体新路线图，通过逻辑折叠与3D堆叠封装技术突破物理极限。华为董事何庭波表示，新一代麒麟芯片将在今年秋季量产，性能提升预计超40%，美国技术封锁遭遇重大挑战。",
        "tag": "科技",
        "prompt": "A microscopic view of semiconductor chip packaging with 3D stacked layers, photorealistic, ultra detailed, 8K, deep blue and gold tones, scientific laboratory setting, glowing circuit traces, no text or watermark"
    },
    {
        "number": "02",
        "title": "OpenAI发布GPT-5.1推理模型 数学能力超越人类博士平均水平",
        "summary": "OpenAI正式发布GPT-5.1推理模型，在国际数学奥林匹克竞赛中取得满分金牌成绩，数学推理能力首次超越人类博士平均水平。该模型采用全新思维链架构，在复杂科学问题上的准确率提升至94%，引发学术界对AI通用智能的热议。",
        "tag": "科技",
        "prompt": "Abstract visualization of artificial intelligence neural network, glowing blue nodes and connections, photorealistic, ultra detailed, 8K, futuristic scientific aesthetic, no text or watermark"
    },
    {
        "number": "03",
        "title": "欧盟就AI法案补充条例达成一致 生成式AI监管框架趋于完善",
        "summary": "欧盟成员国代表就人工智能法案补充条例达成一致，明确生成式AI内容的强制标注要求和版权保护条款。新规要求月活超5000万用户的AI平台须在2027年前完成合规改造，违者最高面临全球营业额6%的罚款。",
        "tag": "国际",
        "prompt": "European parliament building with digital overlay of AI circuit patterns, photorealistic, ultra detailed, 8K, dramatic sky, Brussels cityscape, modern tech aesthetic, no text or watermark"
    },
    {
        "number": "04",
        "title": "沪深股市成交额突破4万亿元 人工智能板块连续五日涨停",
        "summary": "受DeepSeek概念股持续火热带动，沪深两市成交额再度突破4万亿元人民币大关，人工智能板块连续五个交易日出现批量涨停。机构投资者数据显示，北向资金单日净流入超300亿元，创年内新高，市场做多情绪高涨。",
        "tag": "金融",
        "prompt": "Stock market trading floor with glowing digital screens showing rising charts, photorealistic, ultra detailed, 8K, Shanghai cityscape through window, dynamic atmosphere, no text or watermark"
    },
    {
        "number": "05",
        "title": "全球最热城市排行榜再刷新 印度126城温度超45度",
        "summary": "印度多地持续遭受极端热浪侵袭，126个城市最高气温突破45摄氏度，创下有记录以来单日最多极端高温城市纪录。印度政府宣布全国进入公共卫生紧急状态，多个邦宣布学校停课，电力系统面临前所未有的考验。",
        "tag": "社会",
        "prompt": "People suffering from extreme heat in an Indian city, shaded area with traditional architecture, photorealistic, ultra detailed, 8K, harsh sunlight, dry cracked ground, no text or watermark"
    },
    {
        "number": "06",
        "title": "2026年世界杯倒计时10天 美国球迷购票数居海外首位",
        "summary": "距离2026年世界杯开幕仅剩10天，本届世界杯由美加墨三国联合举办，开幕式将在洛杉矶SoFi体育场举行。美国超越巴西和英格兰成为海外购票最多国家，赛事预计吸引超过300万现场观众，FIFA预测全球收视将超50亿人次。",
        "tag": "体育",
        "prompt": "FIFA World Cup trophy in a stadium with American flag colors, photorealistic, ultra detailed, 8K, Los Angeles skyline at sunset, celebratory atmosphere, no text or watermark"
    },
    {
        "number": "07",
        "title": "中国成功发射高分14号遥感卫星 民用星座组网完成",
        "summary": "中国在太原卫星发射中心成功发射高分14号遥感卫星，标志着中国民用遥感卫星星座组网任务全面完成。该卫星可实现全天候全球地表监测，分辨率优于0.3米，将广泛应用于国土测绘、农业估产和环境监测等领域。",
        "tag": "科技",
        "prompt": "Rocket launching from a desert launch pad at night, bright flame trail, photorealistic, ultra detailed, 8K, stars in sky, Chinese spacecraft, no text or watermark"
    },
    {
        "number": "08",
        "title": "美联储维持利率不变 全球资本流向新兴市场加速",
        "summary": "美联储宣布维持联邦基金利率目标区间在4.25%至4.5%不变，主席鲍威尔表示需更多数据确认通胀回落趋势。消息公布后，美元指数小幅回落，新兴市场货币普遍升值，跨境资本加速流入中国、印度等高增长经济体。",
        "tag": "金融",
        "prompt": "Federal Reserve building in Washington DC, photorealistic, ultra detailed, 8K, dramatic lighting, financial district skyline, no text or watermark"
    },
    {
        "number": "09",
        "title": "中国AI人才缺口达500万 高校与企业联合培养提速",
        "summary": "工信部发布的报告显示，中国人工智能领域人才缺口已扩大至500万，供需失衡日益严峻。清华大学、北京大学等20所高校与企业联合推出AI英才计划，预计每年培养10万名实战型AI工程师，以缓解产业链人才短缺问题。",
        "tag": "教育",
        "prompt": "University computer science classroom with students learning AI programming, photorealistic, ultra detailed, 8K, modern campus in Beijing, holographic displays, no text or watermark"
    },
    {
        "number": "10",
        "title": "土耳其正式加入金砖合作机制 新兴经济体版图持续扩大",
        "summary": "土耳其总统埃尔多安在金砖国家峰会上正式签署加入文件，成为金砖合作机制第十个成员国。土耳其拥有8200万人口和发达的制造业，其加入使金砖国家GDP总量占全球比重提升至37%，全球经济格局加速重塑。",
        "tag": "国际",
        "prompt": "International summit meeting with flags of multiple countries including Turkey, photorealistic, ultra detailed, 8K, grand conference hall, diplomatic atmosphere, no text or watermark"
    },
    {
        "number": "11",
        "title": "字节跳动AI教育产品全球用户突破5亿 海外市场表现亮眼",
        "summary": "字节跳动旗下AI教育平台Gauth和豆包爱学全球活跃用户突破5亿，其中海外用户占比超60%。产品采用多模态AI技术，支持100多种语言个性化辅导，在东南亚、北美市场增速超预期，成为中国教育科技出海标杆案例。",
        "tag": "科技",
        "prompt": "Students using tablet devices for AI-powered learning in a bright modern classroom, photorealistic, ultra detailed, 8K, diverse nationalities, global education scene, no text or watermark"
    },
    {
        "number": "12",
        "title": "中日韩三国领导人会谈 推动东北亚自贸区谈判重启",
        "summary": "中日韩三国领导人在东京举行会晤，就重启东北亚自由贸易区谈判达成共识。三国同意在数字贸易、绿色能源和供应链韧性等领域深化合作，并计划于年内启动首轮全面经济伙伴关系协定谈判，区域一体化进程迈出关键一步。",
        "tag": "国际",
        "prompt": "Three world leaders shaking hands in front of their national flags in Tokyo, photorealistic, ultra detailed, 8K, formal diplomatic setting, cherry blossoms, no text or watermark"
    },
    {
        "number": "13",
        "title": "中国新能源汽车5月出口超50万辆 比亚迪领跑全球市场",
        "summary": "中国汽车工业协会数据显示，5月份新能源汽车出口量首次突破50万辆大关，同比增长68%。比亚迪以18万辆出口量位居榜首，在东南亚和欧洲市场份额持续扩大，中国新能源车企正重塑全球汽车产业竞争格局。",
        "tag": "经济",
        "prompt": "Electric vehicles being loaded onto a cargo ship at a Chinese port, photorealistic, ultra detailed, 8K, industrial port setting, sunset lighting, no text or watermark"
    },
    {
        "number": "14",
        "title": "SpaceX星舰完成首次载人试飞 火星移民计划进入新阶段",
        "summary": "SpaceX宣布星舰完成首次载人亚轨道试飞，12名宇航员安全返回地球。马斯克表示，此次试飞成功验证了星舰载人能力的关键技术，下一步将在2028年执行无人火星着陆任务，正式启动火星移民计划第一阶段。",
        "tag": "科技",
        "prompt": "SpaceX Starship rocket in orbit above Earth, photorealistic, ultra detailed, 8K, astronauts inside viewing Earth through window, space station docking, no text or watermark"
    },
    {
        "number": "15",
        "title": "国际金价突破3500美元大关 央行购金潮持续",
        "summary": "受全球贸易摩擦和地缘政治风险加剧影响，国际金价首次突破3500美元每盎司整数关口。各國央行继续大幅增持黄金储备，中国央行已连续18个月增储黄金，分析人士指出，去美元化趋势和避险需求将持续支撑金价走强。",
        "tag": "金融",
        "prompt": "Golden bars stacked in a vault with dramatic lighting, photorealistic, ultra detailed, 8K, gold reflections, luxury safe, no text or watermark"
    },
    {
        "number": "16",
        "title": "香港故宫文化博物馆珍藏展出 三星堆青铜文物首次亮相",
        "summary": "香港故宫文化博物馆举办三星堆文明特展，120件距今3000至5000年的珍贵青铜文物首次在港亮相，其中包括禁止出境的青铜纵目面具。展览采用AR增强现实技术，让观众沉浸式体验古蜀文明的神秘与辉煌。",
        "tag": "文化",
        "prompt": "Ancient bronze artifacts from Sanxingdui civilization on display in a modern museum, photorealistic, ultra detailed, 8K, dramatic museum lighting, mysterious ancient Chinese artifacts, no text or watermark"
    },
    {
        "number": "17",
        "title": "北京启动自动驾驶出租车商业化运营 覆盖全城六环",
        "summary": "北京市宣布在六环内全面启动自动驾驶出租车商业化运营，超过5000辆无人驾驶出租车投入运营。乘客可通过手机APP叫车，票价与普通出租车相当，这是全球最大规模的自动驾驶商业化项目，标志着无人驾驶技术正式落地。",
        "tag": "科技",
        "prompt": "Autonomous self-driving taxi on Beijing city streets, photorealistic, ultra detailed, 8K, modern urban scenery, 6th ring road environment, no text or watermark"
    },
    {
        "number": "18",
        "title": "全球半导体设备市场规模突破2000亿美元 中国采购占四成",
        "summary": "国际半导体产业协会数据显示，全球半导体设备市场规模首次突破2000亿美元，中国采购额占比达40%。尽管受美国出口管制影响，中国半导体投资仍保持高速增长，中芯国际、华虹半导体等晶圆厂持续扩大产能。",
        "tag": "经济",
        "prompt": "Modern semiconductor fabrication factory interior with chip manufacturing equipment, photorealistic, ultra detailed, 8K, blue clean room lighting, advanced machinery, no text or watermark"
    },
    {
        "number": "19",
        "title": "上海世界移动通信大会开幕 中国移动发布6G发展白皮书",
        "summary": "2026年上海世界移动通信大会正式开幕，中国移动在会上发布6G技术发展白皮书，提出数字孪生、智慧泛在的6G愿景。华为、中兴等中国企业展示了6G原型设备，峰值速率预计达1Tbps，较5G提升100倍。",
        "tag": "科技",
        "prompt": "Telecommunications exhibition in Shanghai with 6G technology displays, photorealistic, ultra detailed, 8K, futuristic booth with holographic networks, Shanghai skyline, no text or watermark"
    },
    {
        "number": "20",
        "title": "珠穆朗玛峰登山季开启 中国一侧开放人数创新高",
        "summary": "2026年珠穆朗玛峰春季登山季正式启动，中国一侧北坡计划发放400个登山许可，创历史新高。随着高海拔氧气设备的升级和救援体系的完善，登山成功率达78%，但气象专家警告今夏厄尔尼诺现象可能带来极端天气挑战。",
        "tag": "社会",
        "prompt": "Mount Everest summit with mountaineers and Chinese flag in bright sunshine, photorealistic, ultra detailed, 8K, snow-capped Himalayan peaks, dramatic clouds below, no text or watermark"
    }
]

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


def generate_image_cogview(news_item):
    """Generate image using CogView-3-Flash API"""
    import urllib.request
    import urllib.parse

    prompt = news_item["prompt"]
    number = news_item["number"]
    output_path = f"{WORKSPACE}/images/news_{DATE_FILE}_{number}.png"

    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            # Content is a list: [{"url": "https://..."}]
            content_list = result["choices"][0]["message"]["content"]
            if isinstance(content_list, list) and len(content_list) > 0:
                img_url = content_list[0].get("url", "")
            else:
                img_url = str(content_list)

        # Download the image
        with urllib.request.urlopen(img_url, timeout=60) as img_resp:
            img_data = img_resp.read()

        with open(output_path, "wb") as f:
            f.write(img_data)
        print(f"  [OK] Image {number} saved: {output_path}")
        return True
    except Exception as e:
        print(f"  [FAIL] Image {number} error: {e}")
        return False


def main():
    os.chdir(WORKSPACE)
    print(f"\n=== Generating news for {DATE_STR} ===\n")

    # Step 1: Generate images
    print("Step 1: Generating 20 images via CogView-3-Flash...")
    success_count = 0
    for i, news in enumerate(NEWS):
        print(f"  [{i+1}/20] News {news['number']}: {news['title'][:25]}...")
        for attempt in range(2):
            if generate_image_cogview(news):
                success_count += 1
                break
        if i < len(NEWS) - 1:
            import time
            time.sleep(1)

    print(f"\n  Images generated: {success_count}/20")

    # Step 2: Update index.html
    print("\nStep 2: Updating index.html...")
    with open(f"{WORKSPACE}/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Update title
    html_content = re.sub(
        r"<title>.*?\| 环球新闻</title>",
        f"<title>全球20条热点新闻 - {DATE_HTML} | 环球新闻</title>",
        html_content
    )
    # Update meta description
    html_content = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{DATE_HTML}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">',
        html_content
    )
    # Update cover subtitle
    html_content = re.sub(
        r"全球20条热点新闻 . \d{4}年\d{2}月\d{2}日",
        f"全球20条热点新闻 \u00b7 {DATE_HTML}",
        html_content
    )
    # Update footer date
    html_content = re.sub(
        r"所有新闻内容仅供参考，请以官方发布为准 . \d{4}年\d{2}月\d{2}日",
        f"所有新闻内容仅供参考，请以官方发布为准 \u00b7 {DATE_HTML}",
        html_content
    )

    # Build news card HTML
    news_cards = ""
    for news in NEWS:
        card = f'''<div class="news-card">
                    <img class="news-image" src="images/news_{DATE_FILE}_{news["number"]}.png" alt="{news["title"]}" loading="lazy">
                    <div class="news-content">
                        <span class="news-number">{news["number"]}</span>
                        <h3 class="news-title">{news["title"]}</h3>
                        <p class="news-summary">{news["summary"]}</p>
                        <div>
                            <span class="tag">{news["tag"]}</span>
                        </div>
                    </div>
                </div>'''
        news_cards += card + "\n                "

    # Replace the news grid content
    pattern = r'<div class="news-grid" id="newsGrid">.*?</div>\s+</div>\s+<div class="comments-section">'
    replacement = f'<div class="news-grid" id="newsGrid">\n                {news_cards}</div>\n            </div>\n            <div class="comments-section">'
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

    with open(f"{WORKSPACE}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("  [OK] index.html updated")

    # Step 3: Git push
    print("\nStep 3: Pushing to GitHub...")
    try:
        subprocess.run(
            ["bash", "-c", f"git add index.html images/news_{DATE_FILE}_*.png"],
            cwd=WORKSPACE, check=True
        )
        commit_msg = f"Update: {DATE_FILE}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=WORKSPACE, check=True)
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = "ssh -i ~/.ssh/id_ed25519"
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=WORKSPACE, env=env, capture_output=True, text=True
        )
        if result.returncode == 0:
            print("  [OK] Pushed to GitHub successfully")
        else:
            print(f"  [FAIL] Push failed: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"  [FAIL] Git error: {e}")


if __name__ == "__main__":
    main()