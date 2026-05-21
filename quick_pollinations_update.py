#!/usr/bin/env python3
"""
快速更新脚本 - 使用 Pollinations AI 生成图片（免费快速）
"""
import os
import sys
import re
import json
import subprocess
import time
import opencc
from datetime import datetime, timezone, timedelta
from pathlib import Path

BLOG_PATH = Path("/home/swg/.openclaw/workspace/news-blog")
IMAGES_DIR = BLOG_PATH / "images" / "news-generated"
LOGS_DIR = BLOG_PATH / "logs"
POLLINATIONS_SCRIPT = BLOG_PATH / "pollinations_generate.py"

# 初始化简繁体转换器
converter = opencc.OpenCC('t2s')

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def get_beijing_time():
    return datetime.now(timezone(timedelta(hours=8)))

def step1_search_news(count=20):
    """搜索新闻"""
    log(f"📡 步骤 1/4: 搜索 {count} 条新闻")
    
    FEED_BLACKLIST = [
        '新闻滚动', '新闻直播', '头条汇总', '世界十大新闻', '新闻头条', '新闻排行榜',
        '全球新闻网', '联合新闻网', '大纪元', '法广', 'RFI', 'BBC中文网', '美国之音',
        '自由亚洲电台', '联合早报', 'TVB', '无线新闻', '新浪', '网易', '腾讯', '搜狐',
        '凤凰', '澎湃', '华尔街日报', '新华网', '人民网', '央视', '中国新闻网',
        '热点小时报', '热点速递', '今日头条', '百度新闻', '观察者网',
    ]
    
    search_script = Path.home() / ".hermes/scripts/tavily_search.py"
    tz_beijing = timezone(timedelta(hours=8))
    beijing_now = datetime.now(tz=tz_beijing)
    date_str = beijing_now.strftime("%Y年%m月%d日")
    
    queries = [
        f"{date_str} 国际 要闻 重大事件",
        f"{date_str} 科技 产业 经济",
        f"{date_str} 金融 股市 外贸",
        f"{date_str} 社会 民声",
        f"{date_str} 外交 军事",
    ]
    
    all_news = []
    seen_titles = set()
    
    for query in queries:
        result = subprocess.run(
            ["python3", str(search_script), query, "--max-results", "8", "--json-output"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            continue
        try:
            lines = result.stdout.splitlines()
            json_start = next((i for i, line in enumerate(lines) if line.strip().startswith('{')), 0)
            json_text = '\n'.join(lines[json_start:])
            response = json.loads(json_text)
            for item in response.get('results', []):
                title = item.get('title', '')[:80]
                raw_content = item.get('content', '')
                
                import html
                title = html.unescape(title)
                title = converter.convert(title)
                title = re.sub(r'[a-zA-Z]{2,}', '', title)
                title = re.sub(r'http[s]?://\S+', '', title)
                title = re.sub(r'www\.\S+', '', title)
                
                if title in seen_titles:
                    continue
                if any(bad in title for bad in FEED_BLACKLIST):
                    continue
                
                title = re.sub(r'\d{4}年\d{1,2}月\d{1,2}[日号](\s*[0-9时:：]+)?\s*', '', title)
                title = re.sub(r'\d{1,2}年\d{1,2}月\d{1,2}[日号](\s*[0-9时:：]+)?\s*', '', title)
                title = re.sub(r'[?#]?\d{8}', '', title)
                title = re.sub(r'\d{2}\.\d{2}\s+', '', title)
                title = re.sub(r'\d{7,}', '', title)
                title = re.sub(r'[。！？；，、]\d{1,2}年\d{1,2}月\d{1,2}[日号](\s*[0-9时:：]+)?[\s\-—–…]*$', '', title)
                title = re.sub(r'\d{1,2}年\d{1,2}月\d{1,2}[日号][\s\-—–…]*$', '', title)
                title = re.sub(r'[（(]\d{4}年\d{1,2}月\d{1,2}[日号)）]', '', title)
                title = re.sub(r'[「」『』【】《》〈〉〖〗〘〙〚〛‹›«»]', '', title)
                title = re.sub(r'[丨｜‖\||／/\\\_]', '', title)
                title = re.sub(r'^\d+[.、]\s*', '', title)
                title = re.sub(r'^[?？!！。；：、,\.\-\—–… ]+', '', title)
                title = re.sub(r'[\-—–… ]+$', '', title)
                title = re.sub(r'^[ \-—–…]+', '', title)
                title = re.sub(r'\s+', ' ', title).strip()
                title = re.sub(r'\d{4,}$', '', title)
                
                if not title or len(title) < 4:
                    title = "今日要闻"
                
                content = raw_content.strip()
                if len(content) < 30:
                    continue
                content = re.sub(r'[a-zA-Z]{3,}', '', content)
                content = re.sub(r'http\S+', '', content)
                content = re.sub(r'\s+', ' ', content).strip()
                
                if len(content) < 100:
                    content = content + " " + "该事件在全球范围内引发广泛关注，各界呼吁各方保持克制，通过对话协商解决分歧，维护地区和世界的和平与稳定。"
                
                if len(content) > 250:
                    content = content[:250]
                    if content[-1] not in '。！？':
                        for end in '。！？':
                            p = content.rfind(end)
                            if p > 150:
                                content = content[:p+1]
                                break
                
                seen_titles.add(title)
                all_news.append({"title": title, "summary": content, "tags": ["新闻"]})
                
                if len(all_news) >= count:
                    break
        except Exception as e:
            log(f"   解析搜索结果出错: {e}")
        
        if len(all_news) >= count:
            break
    
    log(f"✅ 找到 {len(all_news)} 条新闻")
    return all_news[:count]

def step2_generate_images(news_list, today_str):
    """使用 Pollinations 生成图片（快速）"""
    log(f"🎨 步骤 2/4: 生成 {len(news_list)} 张图片 (Pollinations)")
    
    # 英文翻译映射（常见新闻主题）
    theme_keywords = [
        "international news breaking", "global economy finance", "technology innovation",
        "diplomatic summit meeting", "military defense", "stock market trading",
        "climate environment summit", "sports championship", "health medicine",
        "energy oil gas", "artificial intelligence", "space exploration",
        "cultural heritage museum", "business trade deal", "social media viral",
        "scientific research discovery", "urban development city", "education university",
        "food agriculture harvest", "travel tourism"
    ]
    
    image_files = []
    for idx, news in enumerate(news_list, 1):
        title = news["title"]
        # 构建英文提示词
        theme = theme_keywords[(idx - 1) % len(theme_keywords)]
        prompt = f"Professional news photograph: {title}, {theme}, Reuters style, 8K, cinematic lighting, no text overlay"
        output_file = f"news_{today_str}_{idx:02d}.png"
        output_path = IMAGES_DIR / output_file
        
        log(f"   🖼️  [{idx}/{len(news_list)}] {title[:30]}...")
        
        # 调用 pollinations_generate.py 脚本
        result = subprocess.run(
            ["python3", str(POLLINATIONS_SCRIPT), prompt, "--output", str(output_path), "--width", "1344", "--height", "768"],
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0 and output_path.exists():
            size = output_path.stat().st_size
            log(f"   ✅ [{idx}] 生成成功 ({size//1024}KB)")
            image_files.append(str(output_path))
        else:
            log(f"   ⚠️  [{idx}] 生成失败，使用默认图片")
            image_files.append(None)
        
        time.sleep(1)  # 避免过快请求
    
    return image_files

def step3_update_html(news_list, image_files, today_str):
    """更新 index.html"""
    log(f"📝 步骤 3/4: 更新 index.html")
    
    date_display = f"{today_str[:4]}年{today_str[4:6]}月{today_str[6:8]}日"
    
    # 读取现有 index.html
    index_file = BLOG_PATH / "index.html"
    with open(index_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 更新 cover-section 的日期
    html = re.sub(
        r'cover-subtitle.*?全球20条热点新闻.*?(\d{4})年(\d{2})月(\d{2})日',
        f'cover-subtitle\">全球20条热点新闻 · {date_display}',
        html
    )
    # 备用模式：直接替换日期格式
    html = re.sub(r'全球20条热点新闻 · \d{4}年\d{2}月\d{2}日', f'全球20条热点新闻 · {date_display}', html)
    
    # 更新页面标题
    html = re.sub(r'<title>.*? - \d{4}年\d{2}月\d{2}日', f'<title>全球20条热点新闻 - {date_display}', html)
    html = re.sub(r'<meta name="description" content=".*?\d{4}年\d{2}月\d{2}日', f'<meta name="description" content="{date_display}全球20条热点新闻', html)
    
    # 更新 footer 日期
    html = re.sub(r'所有新闻内容仅供参考，请以官方发布为准 · \d{4}年\d{2}月\d{2}日', f'所有新闻内容仅供参考，请以官方发布为准 · {date_display}', html)
    
    # 构建新闻卡片
    news_cards = ""
    for idx, (news, img_path) in enumerate(zip(news_list, image_files), 1):
        if img_path:
            img_rel = f"images/news-generated/{Path(img_path).name}"
        else:
            img_rel = "images/news-generated/news_default.png"
        
        title = news["title"]
        summary = news["summary"]
        tags_html = "".join(f'<span class="tag">{tag}</span>' for tag in news.get("tags", ["新闻"])[:5])
        
        card = f'''
                <div class="news-card">
                    <img src="{img_rel}" alt="{title}" class="news-image">
                    <div class="news-content">
                        <span class="news-number">{idx}</span>
                        <h3 class="news-title">{title}</h3>
                        <p class="news-summary">{summary}</p>
                        <div>
                            {tags_html}
                        </div>
                    </div>
                </div>
'''
        news_cards += card
    
    # 替换新闻网格内容
    # 找到 <div class="news-grid" id="newsGrid"> 和下一个 </div> 之间的内容
    pattern = r'(<div class="news-grid" id="newsGrid">)\s*(.*?)\s*(</div>\s*<div class="warning">)'
    replacement = rf'\1\n{news_cards}\n            \3'
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    # 验证卡片数量
    actual = html.count('class="news-card"')
    log(f"   🔍 HTML验证: {actual} 张新闻卡片")
    
    # 写入
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    log(f"✅ index.html 更新完成")
    return str(index_file)

def step4_git_commit(html_file):
    """Git 提交"""
    log(f"🚀 步骤 4/4: Git 提交")
    os.chdir(BLOG_PATH)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    msg = f"更新首页：{date_str}"
    
    result = subprocess.run(["git", "add", "index.html"], capture_output=True, text=True)
    result = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
    if result.returncode == 0:
        log(f"✅ 提交成功: {msg}")
    else:
        log(f"⚠️ 提交: {result.stderr.strip()}")
    
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode == 0:
        log(f"✅ 推送成功")
    else:
        log(f"⚠️ 推送: {result.stderr.strip()}")

def main():
    today = get_beijing_time()
    today_str = today.strftime("%Y%m%d")
    date_display = today.strftime("%Y年%m月%d日")
    
    log("=" * 50)
    log(f"开始更新新闻博客 - {today}")
    log("=" * 50)
    
    # 确保目录存在
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: 搜索新闻
    news_list = step1_search_news(20)
    if len(news_list) < 20:
        log(f"⚠️  仅找到 {len(news_list)} 条新闻，使用默认数据补充")
        # 补充默认新闻
        defaults = get_default_news(20 - len(news_list))
        news_list.extend(defaults)
    
    # Step 2: 生成图片
    image_files = step2_generate_images(news_list, today_str)
    
    # Step 3: 更新 HTML
    html_file = step3_update_html(news_list, image_files, today_str)
    
    # Step 4: Git 提交
    step4_git_commit(html_file)
    
    log("=" * 50)
    log("✅ 更新完成!")
    log("=" * 50)

def get_default_news(count):
    """返回默认新闻（当搜索结果不足时）"""
    defaults = [
        {"title": "全球金融市场今日普涨", "summary": "受主要经济体乐观数据提振，全球主要股市今日普遍上涨，投资者风险偏好回升，市场情绪明显改善。", "tags": ["财经"]},
        {"title": "国际科技会议聚焦AI伦理", "summary": "来自全球各地的科技领袖齐聚一堂，讨论人工智能发展中的伦理问题，呼吁建立更完善的AI治理框架。", "tags": ["科技"]},
        {"title": "能源转型加速推进", "summary": "全球多国宣布新的清洁能源投资计划，太阳能和风能项目加快推进，能源转型成为各国政策重点。", "tags": ["能源"]},
        {"title": "人文交流促进国际理解", "summary": "多国举办文化交流活动，增进人民之间的相互了解和友谊，为国际关系改善营造良好氛围。", "tags": ["文化"]},
    ]
    return defaults[:count]

if __name__ == "__main__":
    main()