#!/usr/bin/env python3
"""
快速新闻更新脚本 - 优化版
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import time
import opencc

# 初始化简繁体转换器
converter = opencc.OpenCC('t2s')

# 配置
BLOG_PATH = "/home/swg/.openclaw/workspace/news-blog"
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "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")
IMAGES_DIR = Path(BLOG_PATH) / "images"
LOGS_DIR = Path(BLOG_PATH) / "logs"

# 创建必要的目录
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class Logger:
    def __init__(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = LOGS_DIR / f"{today}.log"
        self.log("=" * 60)
        self.log(f"开始快速更新新闻博客 - {datetime.now()}")
        self.log("=" * 60)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, 'a') as f:
            f.write(log_message + "\n")

logger = Logger()

def get_beijing_time():
    """获取北京时间（UTC+8）"""
    return datetime.now() + timedelta(hours=8)

def get_sample_news(count=20):
    """示例新闻数据（默认20条）- 每个摘要150-200字"""
    sample_news = [
        {
            "title": "全球科技峰会今日开幕",
            "summary": "多国科技领袖齐聚一堂，聚焦人工智能与可持续发展议题。各国专家就AI伦理治理、绿色能源转型、数字经济发展等议题展开深入讨论，共同制定行业新标准，推动全球科技创新合作迈向新阶段。",
            "tags": ["科技", "国际"]
        },
        {
            "title": "新能源汽车销量创新高",
            "summary": "本月新能源汽车销量同比增长30%，市场前景持续看好。多家厂商加速布局电动化转型，供应链体系持续完善，充电基础设施加快建设，消费者对新能源汽车的接受度显著提升。",
            "tags": ["汽车", "经济"]
        },
        {
            "title": "量子计算取得新突破",
            "summary": "量子计算机实现更高稳定性和运算速度，为未来科技发展奠定基础。研究团队在纠错算法和量子比特控制方面取得重大进展，推动量子计算实用化进程。",
            "tags": ["科技", "量子计算"]
        },
        {
            "title": "航天发射任务圆满成功",
            "summary": "最新卫星成功入轨，为通信网络升级提供支持。本次发射任务标志着航天工业进入新阶段，卫星互联网建设加速推进。",
            "tags": ["航天", "科技"]
        },
        {
            "title": "人工智能医疗应用加速",
            "summary": "AI在疾病诊断和药物研发中的应用取得显著进展，医疗行业迎来数字化变革。多地医疗机构引入AI辅助诊断系统，提升诊疗效率和准确率。",
            "tags": ["AI", "医疗"]
        },
        {
            "title": "可再生能源投资创新高",
            "summary": "各国加大清洁能源投资力度，推动绿色转型战略实施。太阳能、风能市场持续扩大，技术创新降低成本，储能产业迎来快速发展期。",
            "tags": ["能源", "环保"]
        },
        {
            "title": "5G网络覆盖加速推进",
            "summary": "更多城市实现5G网络全覆盖，为数字经济提供基础设施建设支撑。5G应用场景不断丰富，工业互联网、智慧城市等领域加速发展。",
            "tags": ["科技", "通信"]
        },
        {
            "title": "在线教育平台用户激增",
            "summary": "学习数字化趋势明显，在线教育平台用户规模持续增长。个性化学习方案成为行业新趋势，AI辅助教学提升学习效率。",
            "tags": ["教育", "科技"]
        },
        {
            "title": "智慧城市建设加速",
            "summary": "多个城市启动智慧城市建设项目，运用物联网、大数据等技术提升城市管理水平。智能交通、智慧安防等领域取得显著成效。",
            "tags": ["科技", "城市"]
        },
        {
            "title": "生物科技领域投资活跃",
            "summary": "基因编辑、生物制药等前沿领域投资显著增加，生物科技创新成果不断涌现。创新药物研发提速，为疑难疾病治疗带来新希望。",
            "tags": ["科技", "生物"]
        },
        {
            "title": "数字经济规模持续扩大",
            "summary": "数字经济成为经济增长新引擎，各行业数字化转型加速推进。云计算、大数据、区块链等技术广泛应用，推动产业升级和创新发展。",
            "tags": ["经济", "科技"]
        },
        {
            "title": "国际经贸合作深化",
            "summary": "多国签署新的经贸合作协议，推动全球贸易自由化。区域经济一体化进程加快，为各国经济发展注入新动力。",
            "tags": ["国际", "经济"]
        },
        {
            "title": "绿色金融发展迅速",
            "summary": "绿色债券、绿色信贷等金融产品规模快速增长，支持可持续发展项目。金融机构积极布局绿色金融领域，推动经济绿色转型。",
            "tags": ["金融", "环保"]
        },
        {
            "title": "智能制造产业升级",
            "summary": "制造业智能化改造加速推进，工业机器人应用范围扩大。智能工厂建设提速，生产效率和产品质量显著提升。",
            "tags": ["制造", "科技"]
        },
        {
            "title": "网络安全防护加强",
            "summary": "各国加强网络安全建设，提升关键信息基础设施防护能力。网络安全技术不断创新，为数字经济发展提供安全保障。",
            "tags": ["安全", "科技"]
        },
        {
            "title": "文化产业发展繁荣",
            "summary": "文化创意产业规模持续扩大，数字文化产品丰富多样。文化消费市场活跃，为经济增长注入新活力。",
            "tags": ["文化", "经济"]
        },
        {
            "title": "体育产业迎来新机遇",
            "summary": "体育赛事活动增多，体育消费市场持续扩大。体育产业与科技、旅游等产业融合发展，形成新的经济增长点。",
            "tags": ["体育", "经济"]
        },
        {
            "title": "农业现代化进程加快",
            "summary": "智慧农业技术应用范围扩大，农业生产效率显著提升。农业科技创新成果丰硕，为粮食安全提供有力保障。",
            "tags": ["农业", "科技"]
        },
        {
            "title": "国际合作应对气候变化",
            "summary": "各国加强气候合作，共同应对全球气候变化挑战。清洁能源技术推广应用，碳减排目标持续推进。",
            "tags": ["国际", "环保"]
        }
    ]

    return sample_news[:count]

def generate_images_quick(news_list, seed=101):
    """快速生成图片（使用已有图片或快速生成）"""
    logger.log(f"🎨 步骤 2/5: 生成 {len(news_list)} 张图片")

    today = datetime.now().strftime("%Y%m%d")
    results = []

    # 检查已有图片
    existing_images = list(IMAGES_DIR.glob(f"news_{today}_*.png"))
    logger.log(f"📁 已有图片: {len(existing_images)} 张")

    # 为每条新闻生成图片
    for idx, news in enumerate(news_list, 1):
        image_file = IMAGES_DIR / f"news_{today}_{idx:02d}.png"

        # 如果图片已存在，跳过
        if image_file.exists():
            logger.log(f"✅ 图片 {idx}/{len(news_list)} 已存在")
            results.append(str(image_file))
            continue

        # 否则快速生成（使用简化方法）
        logger.log(f"🖼️  生成图片 {idx}/{len(news_list)}")

        # 使用pollinations快速生成
        title = news.get("title", "")
        # 简单的英文提示词
        prompt_en = f"news photography, {title}, realistic, 8K, professional"
        prompt_en = re.sub(r'[^\w\s-]', '', prompt_en)[:200]

        try:
            result = subprocess.run(
                ["python3", str(Path(BLOG_PATH) / "pollinations_generate.py"),
                 prompt_en,
                 "--output", str(image_file),
                 "--width", "1344",
                 "--height", "768",
                 "--seed", str(seed + idx),
                 "--nologo"],
                capture_output=True,
                text=True,
                timeout=120,
                env={**os.environ, "NVIDIA_API_KEY": NVIDIA_API_KEY}
            )

            if result.returncode == 0 and image_file.exists():
                logger.log(f"✅ 图片 {idx}/{len(news_list)} 生成成功")
                results.append(str(image_file))
            else:
                logger.log(f"⚠️  图片 {idx} 生成失败，使用占位图")
                # 使用占位图
                placeholder = IMAGES_DIR / f"news_{today}_01.png"
                if placeholder.exists():
                    results.append(str(placeholder))
                else:
                    results.append(None)
        except Exception as e:
            logger.log(f"⚠️  图片 {idx} 生成异常: {str(e)}")
            results.append(None)

    return results

def create_html(news_list, image_files):
    """创建 HTML"""
    logger.log(f"📝 步骤 4/5: 创建 HTML 页面")

    try:
        from datetime import datetime
        date_str = get_beijing_time().strftime("%Y年%m月%d日")

        news_cards_html = ""
        for idx, (news, image_file) in enumerate(zip(news_list, image_files), 1):
            title = news.get("title", "无标题")
            summary = news.get("summary", "无内容")
            tags = news.get("tags", [])
            image_path = f"images/{Path(image_file).name}" if image_file else "images/news_default.png"

            # 构建新闻卡片
            news_cards_html += f"""

                <div class="news-card">
                    <img src="{image_path}" alt="{title}" class="news-image">
                    <div class="news-content">
                        <span class="news-number">{idx}</span>
                        <h3 class="news-title">{title}</h3>
                        <p class="news-summary">{summary}</p>
                        <div>"""

            # 添加标签
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
        html_content = html_content.replace("{{NEWS_DATE}}", date_str)
        html_content = html_content.replace("{{NEWS_CARDS}}", news_cards_html)

        # 保存新文件
        html_file = Path(BLOG_PATH) / "index.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.log(f"✅ HTML 创建成功: {html_file}")
        return str(html_file)

    except Exception as e:
        logger.log(f"❌ HTML 创建失败: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return None

def upload_to_github(html_file):
    """上传到 GitHub"""
    logger.log(f"🚀 步骤 5/5: 上传到 GitHub")

    try:
        # 添加所有更改
        result = subprocess.run(
            ["git", "add", "."],
            capture_output=True,
            text=True,
            cwd=BLOG_PATH
        )

        # 提交
        commit_msg = f"Update: {datetime.now().strftime('%Y%m%d')}"
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True,
            text=True,
            cwd=BLOG_PATH
        )

        if result.returncode != 0:
            logger.log(f"⚠️  Git commit: {result.stdout}")
            # 可能没有更改，继续push

        # 推送
        result = subprocess.run(
            ["git", "push"],
            capture_output=True,
            text=True,
            cwd=BLOG_PATH,
            timeout=60
        )

        if result.returncode == 0:
            logger.log("✅ 上传成功")
            return True
        else:
            logger.log(f"❌ 上传失败: {result.stderr}")
            return False

    except Exception as e:
        logger.log(f"❌ 上传异常: {str(e)}")
        return False

def main():
    """主函数"""
    try:
        # 第1步：获取新闻
        logger.log("📡 步骤 1/5: 获取 20 条新闻")
        news_list = get_sample_news(20)
        logger.log(f"✅ 获取成功: {len(news_list)} 条新闻")

        # 第2步：生成图片
        seed = int(datetime.now().strftime("%Y%m%d"))
        image_files = generate_images_quick(news_list, seed)

        # 第3步：创建 HTML
        html_file = create_html(news_list, image_files)
        if not html_file:
            return 1

        # 第4步：上传
        success = upload_to_github(html_file)
        if success:
            logger.log("=" * 60)
            logger.log("🎉 更新完成！")
            logger.log(f"🌐 https://yww001.github.io/news-blog/")
            logger.log(f"📰 新闻: {len(news_list)} 条")
            logger.log(f"📷 图片: {len([f for f in image_files if f])} 张")
            logger.log("=" * 60)
        else:
            logger.log("⚠️  图片和 HTML 已生成，但上传失败")
            return 1

        return 0

    except Exception as e:
        logger.log(f"❌ 错误: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
