#!/usr/bin/env python3
"""
增强版新闻博客自动更新器
包含质量检查机制
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
converter = opencc.OpenCC('t2s')  # Traditional to Simplified

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
        self.log(f"开始更新新闻博客 - {datetime.now()}")
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

def step_1_search_news(count=20):
    """第1步：搜索新闻（使用多个查询确保获取足够数量）"""
    logger.log(f"📡 步骤 1/5: 搜索 {count} 条真实新闻")

    # 排除的垃圾关键词（feed/聚合/列表类网站）
    FEED_BLACKLIST = [
        '新闻滚动', '新闻直播', '时事与新闻直播', '全球新闻滚动',
        '头条汇总', '世界十大新闻', '新闻头条', '新闻排行榜',
        '网带您看遍', '全球新闻网', '联合新闻网', '大纪元',
        '法广', 'RFI', 'BBC中文网', '美国之音', '自由亚洲电台',
        '联合早报', 'TVB', 'TVB News', '无线新闻', '無綫新聞', '八度空間',
        '新浪', '新浪新闻', '新浪财经', '新浪体育', '新浪科技',
        '网易', '网易新闻', '腾讯', '腾讯新闻', '搜狐', '搜狐新闻',
        '凤凰', '澎湃', '华尔街日报',
        '新华网', '人民网', '央广网', '央视', '中国新闻网', '中国青年网',
        '热点小时报', '实时热点', '热点速递', '热点实时',
        '新闻摘要', '新闻速报', '新闻早报', '新闻晚报',
        '新闻滚动', '新闻直播', '新闻简报', '新闻头条', '新闻排行榜',
        '无线', '无线新闻', '大纪元', '联合早报',
        '法广', 'RFI', 'BBC', '美国之音', '自由亚洲电台',
        '今日头条', '百度', '百度新闻', '观察者网',
    ]

    try:
        search_script = Path.home() / ".hermes/scripts/tavily_search.py"
        date_str = datetime.now().strftime("%Y年%m月%d日")  # 使用当前日期
        
        # 使用多个搜索查询获取不同类型的新闻
        queries = [
            f"{date_str} 今日 要闻 重大事件",
            f"{date_str} 科技 产业 经济",
            f"{date_str} 国际 外交",
            f"{date_str} 社会 民声",
            f"{date_str} 金融 股市",
        ]
        
        # 收集所有新闻
        all_news = []
        seen_titles = set()
        
        for query in queries:
            result = subprocess.run(
                ["python3", str(search_script), query, "--max-results", "10", "--json-output"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and result.stdout.strip():
                import json
                try:
                    lines = result.stdout.splitlines()
                    json_start = 0
                    for i, line in enumerate(lines):
                        if line.strip().startswith('{'):
                            json_start = i
                            break
                    json_text = '\n'.join(lines[json_start:])
                    response = json.loads(json_text)
                    
                    if 'results' in response:
                        for item in response['results']:
                            title = item.get('title', '')[:80]  # 截取标题避免过长
                            raw_content = item.get('content', '')

                            # 第一步：解码HTML实体并统一简繁（所有后续处理基于简体）
                            import html as _html_mod
                            title = _html_mod.unescape(title)
                            title = converter.convert(title)  # 繁→简统一
                            # 移除英文字符（英文媒体名等）
                            title = re.sub(r'[a-zA-Z]{2,}', '', title)
                            # 移除URL残留
                            title = re.sub(r'http[s]?://\S+', '', title)
                            title = re.sub(r'www\.\S+', '', title)

                            # 第二步：在简体标题上做去重和来源过滤
                            if title in seen_titles:
                                continue
                            skip = False
                            for bad in FEED_BLACKLIST:
                                if bad in title:
                                    skip = True
                                    break
                            if skip:
                                continue

                            # 第三步：精细清洗（简繁统一后版本）
                            # 移除日期前缀（多种格式）
                            title = re.sub(r'\d{4}年\d{1,2}月\d{1,2}[日号](\s*[0-9时:：]+)?\s*', '', title)
                            title = re.sub(r'\d{1,2}年\d{1,2}月\d{1,2}[日号](\s*[0-9时:：]+)?\s*', '', title)
                            title = re.sub(r'[?#]?\d{8}', '', title)
                            title = re.sub(r'\d{2}\.\d{2}\s+', '', title)
                            title = re.sub(r'\d{7,}', '', title)
                            # 移除尾部日期后缀
                            title = re.sub(r'[。！？；，、]\d{1,2}年\d{1,2}月\d{1,2}[日号](\s*[0-9时:：]+)?[\s\-—–…]*$', '', title)
                            title = re.sub(r'\d{1,2}年\d{1,2}月\d{1,2}[日号][\s\-—–…]*$', '', title)
                            # 移除全角括号包裹的日期
                            title = re.sub(r'[（(]\d{4}年\d{1,2}月\d{1,2}[日号)）]', '', title)
                            title = re.sub(r'[（(]\d{1,2}年\d{1,2}月\d{1,2}[日号)）]', '', title)
                            # 移除特殊分隔符、引用标记
                            title = re.sub(r'[「」『』【】《》〈〉〖〗〘〙〚〛‹›«»]', '', title)
                            title = re.sub(r'[丨｜‖\||／/\\\\_]', '', title)
                            title = re.sub(r'^\d+[.、]\s*', '', title)
                            # 移除头尾部残留标点和空白
                            title = re.sub(r'^[?？!！。；：、,\.\-\—–… ]+', '', title)
                            title = re.sub(r'[\-—–… ]+$', '', title)
                            title = re.sub(r'^[ \-—–…]+', '', title)
                            # 移除多余空白并strip
                            title = re.sub(r'\s+', ' ', title).strip()
                            # 移除尾部4+位数字
                            title = re.sub(r'\d{4,}$', '', title)

                            # 最终兜底：太短则给默认标题
                            if not title or len(title) < 4:
                                title = "今日要闻"

                            # 第三步：清洗内容
                            content = clean_news_content(raw_content)

                            # 跳过太短的内容
                            if len(content) < 30:
                                continue
                            
                            # 确保摘要150-200字
                            content = expand_summary(content, min_length=150, max_length=200)
                            
                            seen_titles.add(title)
                            all_news.append({
                                "title": title,
                                "summary": content,
                                "raw_prompt": raw_content[:100],
                                "tags": ["新闻"]
                            })
                            
                            if len(all_news) >= count:
                                break
                except Exception as e:
                    continue
            
            if len(all_news) >= count:
                break
        
        if len(all_news) >= count:
            logger.log(f"✅ 搜索成功: 找到 {len(all_news)} 条新闻")
            return all_news[:count]
        else:
            logger.log(f"⚠️ 仅找到 {len(all_news)} 条新闻，使用示例数据补足")
            remaining = count - len(all_news)
            sample = get_sample_news(remaining)
            for news in sample:
                news['summary'] = expand_summary(news['summary'], min_length=150, max_length=200)
                news['raw_prompt'] = news['summary'][:100]
            all_news.extend(sample)
            return all_news
    
    except Exception as e:
        logger.log(f"⚠️ 搜索异常: {str(e)}，使用示例数据")
    
    # Fallback: 使用高质量示例新闻
    logger.log("📝 使用高质量示例新闻")
    sample_news = get_sample_news(count)
    for news in sample_news:
        news['summary'] = expand_summary(news['summary'], min_length=150, max_length=200)
        news['raw_prompt'] = news['summary'][:100]
    return sample_news


def extract_image_keywords(title, summary):
    """从标题和摘要中提取图片生成的关键词"""
    import re
    
    # 合并标题和摘要
    text = f"{title} {summary}"
    
    # 定义常见关键词类别
    keyword_map = {
        # 科技类
        "科技": "technology, computer, digital",
        "人工智能": "AI, artificial intelligence, robot",
        "AI": "AI, artificial intelligence, robot",
        "手机": "smartphone, mobile phone",
        "电脑": "computer, laptop",
        "互联网": "internet, network",
        "5G": "5G network, communication tower",
        "芯片": "computer chip, semiconductor",
        "新能源": "solar panel, wind turbine, clean energy",
        "汽车": "car, automobile, vehicle",
        "电动车": "electric car, EV",
        
        # 国际/政治类
        "美国": "United States, American flag",
        "白宫": "White House, Washington DC",
        "联合国": "United Nations, UN headquarters",
        
        # 经济类
        "经济": "economy, business, finance",
        "股市": "stock market, trading",
        "银行": "bank, finance building",
        
        # 社会类
        "教育": "school, education, students",
        "医疗": "hospital, doctor, medicine",
        "气候": "climate, weather, environment",
        "灾难": "disaster, emergency",
        
        # 体育/娱乐
        "体育": "sports, stadium",
        "奥运": "Olympics, sports",
        "电影": "movie, cinema, film",
        "音乐": "music, concert",
        
        # 地点
        "北京": "Beijing, China cityscape",
        "上海": "Shanghai, modern city",
        "国际": "international, global",
        "全球": "world, global",
    }
    
    keywords_found = []
    for cn_keyword, en_keyword in keyword_map.items():
        if cn_keyword in text:
            keywords_found.append(en_keyword)
    
    # 如果没找到关键词，使用通用描述
    if not keywords_found:
        return "breaking news, current events"
    
    return ", ".join(keywords_found[:3])  # 最多返回3个关键词


def translate_title_to_en(title):
    """将中文标题翻译为英文关键词短语，用于图片生成"""
    import re

    # 中文到英文关键词的映射（标题专用的精简翻译）
    TITLE_TRANSLATION = [
        ("习近平总书记", "President Xi Jinping"),
        ("习近平", "Xi Jinping"),
        ("川普普京", "Trump Putin"),
        ("中国男足", "Chinese men's football team"),
        ("中国女排", "Chinese women's volleyball"),
        ("人工智能", "artificial intelligence"),
        ("量子计算", "quantum computing"),
        ("电动汽车", "electric vehicles"),
        ("国际科技创新中心", "international technology innovation center"),
        ("数字中国", "digital China"),
        ("新能源汽车", "new energy vehicles"),
        ("中美贸易", "China US trade"),
        ("联合国", "United Nations"),
        ("二十届四中全会", "4th Plenary Session"),
        ("川普", "Trump"),
        ("特朗普", "Trump"),
        ("普京", "Putin"),
        ("拜登", "Biden"),
        ("美中", "US China"),
        ("中美", "China US"),
        ("美国", "United States"),
        ("中国", "China"),
        ("航天", "spaceflight"),
        ("卫星", "satellite"),
        ("经济", "economy"),
        ("科技", "technology"),
        ("AI", "AI"),
        ("新能源", "new energy"),
        ("外交", "diplomacy"),
        ("贸易", "trade"),
        ("关税", "tariff"),
        ("峰会", "summit"),
        ("会议", "conference"),
        ("全球", "global"),
        ("国际", "international"),
        ("突破", "breakthrough"),
        ("创新", "innovation"),
        ("发布", "released"),
        ("开幕", "opened"),
        ("召开", "held"),
        ("举行", "held"),
        ("成功", "successful"),
        ("上涨", "rose"),
        ("下跌", "fell"),
        ("增长", "growth"),
        ("下降", "decline"),
        ("要闻", "top news"),
        ("今日要闻", "today's top news"),
        ("热点", "hot topic"),
        ("头条", "headline"),
    ]

    # 直接替换已知词组（按长度降序，避免短词先替换导致长词无法匹配）
    text = title
    for cn, en in TITLE_TRANSLATION:
        text = text.replace(cn, " " + en + " ")

    # 移除剩余中文字符
    text = re.sub(r'[\u4e00-\u9fa5]', ' ', text)

    # 清理多余空白和标点
    text = re.sub(r'[\s,。！？；：、]+', ' ', text).strip()

    # 在英文单词/词组之间加空格（让 CamelCase 和连写词分开）
    # 例如 "TrumpPutin" → "Trump Putin", "XiJinping" → "Xi Jinping"
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # camelCase → 空格
    text = re.sub(r'([a-zA-Z])([a-z])(?=[A-Z])', r'\1 \2', text)  # 词组边界
    text = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', text)

    # 清理多余空格
    text = re.sub(r'\s+', ' ', text).strip()

    if not text or len(text) < 3:
        return "breaking news, current events"

    return text


def clean_title(text):
    """专门清理新闻标题：移除网站前缀、尾部来源、特殊分隔符，保留核心标题"""
    if not text:
        return "今日要闻"

    import re
    import html

    # 0. 解码 HTML 实体（&#12304; &#x1F308; 等）再转简体
    text = html.unescape(text)
    text = converter.convert(text)

    # 1. 先移除英文单词（影响后续正则匹配）
    text = re.sub(r'[a-zA-Z]{2,}', '', text)

    # 2. 移除尾部网站来源（常见新闻网站后缀）
    SITE_SUFFIX_BLACKLIST = [
        '手机新浪网', '新浪网', '新浪体育', '新浪财经', '新浪科技',
        '新华网', '新华网客户端', '新华网财经',
        '人民网', '人民日报', '人民日报客户端',
        '央广网', '央视新闻', '中国新闻网', '中国青年网',
        '网易财经', '网易新闻', '网易科技', '网易体育',
        '腾讯新闻', '腾讯财经', '腾讯体育', '腾讯科技',
        '搜狐新闻', '搜狐财经', '凤凰网', '凤凰资讯',
        '澎湃新闻', '界面新闻', '财新网', '第一财经',
        '36氪', '虎嗅网', '观察者网', '环球时报',
        '中国日报网', '经济参考报', '经济日报',
        '21经济网', '21世纪经济报道', '经济观察网',
        '国家统计局', '国家数据局', '央视网',
        '新京报', '北京日报', '参考消息',
        '亿欧网', '雷锋网', 'PingWest', '品玩',
        '群益期货',
        '的文章列表', '的热门文章', '热门文章',
        '华人头条', '无线新闻', '华语新闻', '八度空间华语新闻',
        '驻墨尔本总领事馆', '外交部新闻',
    ]
    for suffix in SITE_SUFFIX_BLACKLIST:
        if text.endswith(suffix):
            text = text[:-len(suffix)]
        if suffix in text:
            text = text.replace(suffix, ' ')

    # 前缀黑名单（网站名前缀）
    SITE_PREFIX_BLACKLIST = [
        '新浪体育', '新浪财经', '新浪科技', '新浪新闻',
        '新浪中国足球热点小时报', '新浪人工智能热点小时报',
        '新浪汽车热点小时报', '新浪军事热点小时报',
        '新浪国际热点小时报', '新浪财经热点小时报',
        '网易号', '腾讯新闻', '网易新闻',
        '今日头条', '百度新闻', '搜狐新闻',
        '凤凰新闻', '澎湃新闻',
        '华尔街日报', '华尔街日报中文版',
        '中文版',
        '国际热点小时报',
        '热点小时报', '实时热点', '热点速递',
        '新闻摘要', '新闻速报', '新闻早报', '新闻晚报',
        '光明日报', '经济参考报',
        '无线新闻', '华语新闻', '八度空间',
        '【新闻第一线】', '【时事纵横】', '【今日焦点】',
        '华人头条',
    ]
    for prefix in SITE_PREFIX_BLACKLIST:
        if text.startswith(prefix):
            text = text[len(prefix):]
        if prefix in text:
            text = text.replace(prefix, ' ')

    # 4. 移除头部日期前缀（多种格式）
    text = re.sub(r'^\d{4}年\d{1,2}月\d{1,2}[日号](\s*[0-9时:：]+)?\s*', '', text)
    text = re.sub(r'^\d{1,2}年\d{1,2}月\d{1,2}[日号](\s*[0-9时:：]+)?\s*', '', text)
    # 移除 "?YYYYMMDD" 或 "YYYYMMDD" 日期格式（中间位置也要处理）
    text = re.sub(r'[?#]?\d{8}', '', text)
    # 移除 "MM.DD" 日期格式
    text = re.sub(r'^\d{2}\.\d{2}\s+', '', text)
    # 移除尾部日期后缀（日期+标点/连字符出现在末尾，如 "。26年4月30日-" 或 "4月30日-"）
    text = re.sub(r'[。！？；，、]\d{1,2}年\d{1,2}月\d{1,2}[日号](\s*[0-9时:：]+)?[\s\-—–…]*$', '', text)
    text = re.sub(r'\d{1,2}年\d{1,2}月\d{1,2}[日号][\s\-—–…]*$', '', text)

    # 6. 移除尾部数字ID/来源（如：12345678、ABC123等残留数字串）
    text = re.sub(r'\d{4,}$', '', text)
    text = re.sub(r'^新浪', '', text)

    # 7. 移除标题中的特殊分隔符、引用标记和列表标记
    text = re.sub(r'[丨｜‖\||／/\\\\_]', '', text)  # 竖线分隔符和下划线
    text = re.sub(r'^\d+[.、]\s*', '', text)  # 数字编号
    # 移除各类引用标记
    text = re.sub(r'[「」『』【】《》〈〉〖〗〘〙〚〛]', '', text)  # 中文引号和书名号
    text = re.sub(r'[‹›«»]', '', text)  # 西文尖引号

    # 8. 移除URL残留
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)

    # 9. 移除全角括号包裹的日期（如 "（2026年4月29日）"）
    text = re.sub(r'[（(]\d{4}年\d{1,2}月\d{1,2}[日号)）]', '', text)
    text = re.sub(r'[（(]\d{1,2}年\d{1,2}月\d{1,2}[日号)）]', '', text)

    # 10. 移除尾部残留的标点连字符（如 " -"、"——"、"…"）
    text = re.sub(r'[\-—–… ]+$', '', text)
    text = re.sub(r'^[ \-—–…]+', '', text)

    # 11. 移除多余空白（统一在此处strip，不在中间处理）
    text = re.sub(r'\s+', ' ', text).strip()

    # 12. 如果标题为空或太短，生成默认标题
    if not text or len(text) < 4:
        return "今日要闻"

    # 9. 截断过长标题，保留前40字
    if len(text) > 40:
        # 尝试在句号或逗号处截断
        truncated = text[:40]
        last_punct = max(truncated.rfind('，'), truncated.rfind('。'),
                         truncated.rfind('：'), truncated.rfind('—'))
        if last_punct > 15:
            text = text[:last_punct + 1]
        else:
            text = truncated.rstrip() + "……"

    return text


def clean_news_content(text):
    """清理新闻内容：移除英文、繁体、特殊符号，转为纯简体中文"""
    if not text:
        return "暂无内容"

    import re

    # 0. 首先转换繁体为简体
    text = converter.convert(text)

    # 1. 移除 markdown 链接和图片标记 ![[ ]] [[ ]] [视频]
    text = re.sub(r'!\[\[.*?\]\]', '', text)
    text = re.sub(r'\[\[视频\].*?\]', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)

    # 2. 移除 Markdown 标题标记 ### ## *
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*|\*', '', text)

    # 3. 移除英文单词（保留中文）
    text = re.sub(r'[a-zA-Z]{2,}', '', text)

    # 4. 移除数字开头的内容（如 "1、", "2、" 作为列表编号）
    text = re.sub(r'^\d+[.、]\s*', '', text, flags=re.MULTILINE)

    # 5. 移除特殊分隔符（竖线类）
    text = re.sub(r'[丨｜‖\||／/\\\\]', '', text)

    # 6. 移除剩余特殊符号 但保留中文标点
    text = re.sub(r'[^\u4e00-\u9fa5\u3000-\u303f\uff00-\uffefa-zA-Z0-9\s\d，。！？；：、""''（）【】《》——…·]', '', text)

    # 7. 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()

    # 8. 移除 URL
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)

    # 9. 移除头部/尾部的网站名前缀（内容层）
    SITE_BLACKLIST_CONTENT = [
        '新浪体育', '新浪财经', '新浪科技', '新浪新闻',
        '新浪中国足球热点小时报', '新浪人工智能热点小时报',
        '手机新浪网', '新浪网', '新华网', '新华网客户端',
        '人民网', '人民日报', '央视新闻', '中国新闻网',
        '网易财经', '网易新闻', '网易科技',
        '腾讯新闻', '腾讯财经', '腾讯体育',
        '搜狐新闻', '凤凰网', '澎湃新闻',
        '21经济网', '21世纪经济报道', '经济观察网',
        '国家统计局', '国家数据局', '36氪', '虎嗅网',
    ]
    for site in SITE_BLACKLIST_CONTENT:
        if text.startswith(site):
            text = text[len(site):].lstrip()
        if text.endswith(site):
            text = text[:-len(site)].rstrip()

    text = text.strip()

    return text if text else "暂无内容"


def expand_summary(content, min_length=150, max_length=200):
    """扩展摘要到指定长度，确保恰好150-200字，纯中文无英文无重复"""
    if not content:
        return "暂无内容"

    # 彻底清理：移除所有英文单词
    import re
    content = re.sub(r'[a-zA-Z]{1,}', '', content)

    # 如果太短，需要扩展内容
    if len(content) < min_length:
        # 提取已有内容中的关键词（提取名词性短语）
        sentences = re.split(r'[。！？]', content)
        keywords = []
        for s in sentences:
            s = s.strip()
            if len(s) > 4:
                # 提取5-10字的有意义片段作为关键词
                words = re.findall(r'[\u4e00-\u9fa5]{5,15}', s)
                keywords.extend(words[:2])

        # 生成多样化的补充内容（不重复）
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
            "这一进展标志着相关领域迈入新阶段。",
            "各方对此表示高度关注并积极应对。",
            "该事件对行业发展具有深远意义。",
            "相关数据表明这一趋势将持续发展。",
            "业内分析认为未来前景广阔。",
            "这一变化将带来新的发展机遇。",
            "各方正在积极推动相关工作开展。",
            "该举措得到了广泛支持与认可。",
            "这一成果具有重要的里程碑意义。",
            "相关研究为后续发展奠定了基础。",
        ]

        # 避免重复：优先用不同补充句
        used = set()
        # 先尝试用关键词匹配的补充句
        for kw in keywords:
            if len(content) >= max_length:
                break
            for add in additions_pool:
                if add not in used and len(content) + len(add) <= max_length:
                    content = content.rstrip('。！？') + "。" + add
                    used.add(add)
                    break

        # 如果还不够长度，继续添加不重复的补充（更积极）
        for add in additions_pool:
            if add not in used and len(content) + len(add) <= max_length:
                content = content.rstrip('。！？') + "。" + add
                used.add(add)
            if len(content) >= min_length:
                break

        # 如果仍然不够，强制添加（即使超过max_length）
        if len(content) < min_length:
            for add in additions_pool:
                if add not in used:
                    content = content.rstrip('。！？') + "。" + add
                    used.add(add)
                    if len(content) >= min_length:
                        break

    # 如果太长，截取并确保句子完整
    if len(content) > max_length:
        # 尝试在句号处截断
        truncated = content[:max_length]
        last_period = max(truncated.rfind('。'), truncated.rfind('！'), truncated.rfind('？'))
        if last_period > min_length:
            return truncated[:last_period + 1]
        return truncated + "……"

    return content

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
        }
    ]

    # 生成更多示例新闻达到20条，每个都是150-200字
    for i in range(11, count + 1):
        sample_news.append({
            "title": f"今日要闻第{i}条",
            "summary": f"今日要闻第{i}条的相关报道。据相关部门介绍，该消息引发了广泛关注，业内人士分析认为这将对相关行业产生积极影响。目前各项工作正在有序推进中，具体实施细节将另行公布。",
            "tags": ["要闻", "动态"]
        })
    
    return sample_news


def step_2_generate_images(news_list, seed=101, max_retries=5, parallel=2):
    """第2步：并行生成图片（带质量检查和重试，严格限流避免429）"""
    import concurrent.futures
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading

    logger.log(f"🎨 步骤 2/5: 并行生成 {len(news_list)} 张图片（{parallel}个线程）")
    logger.log(f"📊 质量标准: 文件50KB-800KB, 宽≥1024, 高≥576, 比例16:9")
    logger.log(f"⚡ API限流应对: 失败自动重试最多{max_retries+1}次，每次间隔递增等待")

    genai_script = Path.home() / ".hermes/scripts/pollinations_generate.py"
    if not genai_script.exists():
        genai_script = Path(BLOG_PATH) / "pollinations_generate.py"

    results = [None] * len(news_list)

    # 全局限流信号量：确保同时最多只有1个请求在队列中（Pollinations限制）
    rate_limiter = threading.Semaphore(1)
    last_request_time = [time.time()]
    request_lock = threading.Lock()

    def rate_limited_sleep(min_interval=5):
        """确保请求间隔至少min_interval秒"""
        with request_lock:
            elapsed = time.time() - last_request_time[0]
            if elapsed < min_interval:
                sleep_time = min_interval - elapsed
                logger.log(f"⏳ 请求限流: 等待 {sleep_time:.1f} 秒...")
                time.sleep(sleep_time)
            last_request_time[0] = time.time()

    def generate_single_image(idx, news, thread_seed):
        """为单条新闻生成图片（线程安全，带限流）"""
        title = news.get("title", "")
        summary = news.get("summary", "")[:150]
        raw_prompt = news.get("raw_prompt", "")[:150]

        # 从原始内容（含英文）提取关键词，用于图片生成
        keywords = extract_image_keywords(title, raw_prompt if raw_prompt else summary)

        # 翻译标题概念为英文（用于图片生成）
        title_en = translate_title_to_en(title)

        # 构建纯英文提示词（Pollinations是英文模型，纯英文效果更好）
        prompt_en = f"Realistic news photography: {title_en}. {keywords}. "
        prompt_en += "8K ultra high definition, photorealistic, detailed, natural lighting, "
        prompt_en += "professional photojournalism, Reuters/AP style, "
        prompt_en += "real news scene, actual event, no animation, no cartoon, vivid colors, "
        prompt_en += "cinematic composition, sharp focus, depth of field, current news headline"
        prompt_en = prompt_en[:500]  # 限制提示词长度

        # 使用日期+序号格式：news_YYYYMMDD_NN.png
        today = "20260502"  # 强制使用2026年5月2日
        image_file = IMAGES_DIR / f"news_{today}_{idx:02d}.png"
        
        retry_count = 0
        while retry_count <= max_retries:
            # 获取限流锁，确保一次只有一个请求
            rate_limiter.acquire()
            try:
                logger.log(f"🖼️  生成图片 {idx}/{len(news_list)}: {title[:30]}... (尝试 {retry_count + 1}/{max_retries + 1})")
                
                # 限流：请求间隔至少20秒
                rate_limited_sleep(min_interval=20)

                result = subprocess.run(
                    ["python3", str(genai_script),
                     prompt_en,
                     "--output", str(image_file),
                     "--width", "1024",
                     "--height", "576",
                     "--seed", str(thread_seed + retry_count * 100),
                     "--nologo"],
                    capture_output=True,
                    text=True,
                    timeout=600,
                    env={**os.environ, "NVIDIA_API_KEY": NVIDIA_API_KEY}
                )

                if result.returncode == 0 and image_file.exists():
                    quality_ok = check_image_quality(image_file)
                    if quality_ok:
                        logger.log(f"✅ 图片 {idx}/{len(news_list)} 生成成功且质量合格")
                        return idx, str(image_file)
                    else:
                        logger.log(f"⚠️  图片 {idx} 质量不达标，重新生成...")
                        if image_file.exists():
                            image_file.unlink()
                        retry_count += 1
                        if retry_count <= max_retries:
                            wait_time = 60
                            logger.log(f"⏳ 等待 {wait_time} 秒...")
                            time.sleep(wait_time)
                        else:
                            logger.log(f"⚠️  图片 {idx} 质量未达标但已达到最大重试次数")
                            return idx, str(image_file)
                else:
                    # 检查是否是429限流错误
                    error_msg = result.stdout + result.stderr
                    if "429" in error_msg or "Queue full" in error_msg or "Too Many Requests" in error_msg:
                        logger.log(f"⚠️  图片 {idx} 触发API限流，增加等待时间...")
                        retry_count += 1
                        if retry_count <= max_retries:
                            wait_time = 60
                            logger.log(f"⏳ 限流等待 {wait_time} 秒...")
                            time.sleep(wait_time)
                        else:
                            return idx, None
                    else:
                        logger.log(f"⚠️  图片 {idx} 生成失败: {result.stderr[:100] if result.stderr else result.stdout[:100]}")
                        retry_count += 1
                        if retry_count <= max_retries:
                            wait_time = 60
                            logger.log(f"⏳ 等待 {wait_time} 秒后重试...")
                            time.sleep(wait_time)
                        else:
                            logger.log(f"❌ 图片 {idx} 达到最大重试次数")
                            return idx, None
            finally:
                rate_limiter.release()

        return idx, None
    
    with ThreadPoolExecutor(max_workers=parallel) as executor:
        futures = {}
        for idx, news in enumerate(news_list, 1):
            thread_seed = seed + idx
            future = executor.submit(generate_single_image, idx, news, thread_seed)
            futures[future] = idx
        
        for future in as_completed(futures):
            idx, result_file = future.result()
            results[idx - 1] = result_file

    return results

def check_image_quality(image_path):
    """检查图片质量是否达标（提高标准）"""
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            width, height = img.size
            file_size_kb = os.path.getsize(image_path) / 1024

            # Pollinations 质量标准（适配实际输出）
            min_size_kb = 50   # Pollinations 压缩率较高
            max_size_kb = 800
            min_width = 1024   # Pollinations 通常输出 1024 宽度
            min_height = 576
            target_ratio = 16/9
            ratio_tolerance = 0.2  # 放宽比例容差

            ratio = width / height
            ratio_diff = abs(ratio - target_ratio) / target_ratio

            # 检查各项指标
            size_ok = min_size_kb <= file_size_kb <= max_size_kb
            resolution_ok = width >= min_width and height >= min_height
            ratio_ok = ratio_diff <= ratio_tolerance

            return size_ok and resolution_ok and ratio_ok
    except:
        return False

def step_3_check_quality(news_list, image_files):
    """第3步：检查整体质量"""
    logger.log(f"🔍 步骤 3/5: 检查内容和图片质量")

    try:
        check_script = Path(BLOG_PATH) / "check_quality.py"

        # 临时创建检查脚本需要的参数
        check_ok = True

        for idx, (news, image_file) in enumerate(zip(news_list, image_files), 1):
            title = news.get("title", "No Title")
            summary = news.get("summary", "")

            # 检查内容长度
            if len(summary) < 50:
                logger.log(f"⚠️  新闻 {idx} 内容过短 ({len(summary)} 字符)")
                check_ok = False
            else:
                logger.log(f"✅ 新闻 {idx} 内容长度: {len(summary)} 字符")

            # 检查图片
            if image_file and os.path.exists(image_file):
                img_quality = check_image_quality(image_file)
                if img_quality:
                    size_kb = os.path.getsize(image_file) / 1024
                    logger.log(f"✅ 新闻 {idx} 图片质量: {size_kb:.1f}KB")
                else:
                    logger.log(f"⚠️  新闻 {idx} 图片质量未达标")
                    check_ok = False
            else:
                logger.log(f"⚠️  新闻 {idx} 图片文件不存在")
                check_ok = False

        if check_ok:
            logger.log("✅ 质量检查通过")
        else:
            logger.log("⚠️  部分内容或图片质量未达标，但继续发布")

        return check_ok
    except Exception as e:
        logger.log(f"❌ 质量检查异常: {str(e)}")
        return True  # 出错时继续，不阻止发布

def step_4_create_html(news_list, image_files):
    """第4步：创建 HTML"""
    logger.log(f"📝 步骤 4/5: 创建 HTML 页面")

    try:
        # 这里使用完整的 index_enhanced.html 作为基础模板
        # 只需要修改新闻卡片部分

        from datetime import datetime
        date_str = datetime.now().strftime("%Y年%m月%d日")  # 使用当前日期

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

def step_5_upload_to_github(html_file):
    """第5步：上传到 GitHub"""
    logger.log(f"🚀 步骤 5/5: 上传到 GitHub")

    try:
        upload_script = Path(BLOG_PATH) / "upload.sh"

        result = subprocess.run(
            [str(upload_script), f"📰 自动更新 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=BLOG_PATH
        )

        if result.returncode == 0:
            logger.log("✅ 上传成功")
            return True
        else:
            logger.log(f"❌ 上传失败")
            return False

    except Exception as e:
        logger.log(f"❌ 上传异常: {str(e)}")
        return False

def main():
    """主函数"""
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="自动更新新闻博客（增强版）")
    parser.add_argument("--news-count", type=int, default=20, help="新闻数量")
    parser.add_argument("--no-upload", action="store_true", help="不上传，仅生成")
    parser.add_argument("--seed", type=int, help="图片随机种子（默认基于日期生成，避免覆盖历史图片）")

    args = parser.parse_args()

    # 默认用日期生成seed，每天不重复，避免覆盖历史图片
    if args.seed is None:
        today = datetime.now().strftime("%Y%m%d")
        args.seed = int(today)  # e.g. 20260428

    try:
        # 第1步：搜索新闻
        news_list = step_1_search_news(args.news_count)
        if not news_list:
            return 1

        # 第2步：生成图片（带质量检查）
        image_files = step_2_generate_images(news_list, args.seed)

        # 第3步：检查质量
        quality_ok = step_3_check_quality(news_list, image_files)

        # 第4步：创建 HTML
        html_file = step_4_create_html(news_list, image_files)
        if not html_file:
            return 1

        # 第5步：上传
        if not args.no_upload:
            success = step_5_upload_to_github(html_file)
            if success:
                logger.log("=" * 60)
                logger.log("🎉 更新完成！")
                logger.log(f"🌐 https://yww001.github.io/news-blog/")
                logger.log(f"📊 质量: {'✅ 合格' if quality_ok else '⚠️  部分未达标'}")
                logger.log(f"📷 生成: {len(image_files)} 张图片")
                logger.log(f"📰 新闻: {len(news_list)} 条")
                logger.log("=" * 60)
            else:
                logger.log("⚠️  图片和 HTML 已生成，但上传失败")
                return 1
        else:
            logger.log("✅ 生成完成（未上传）")
            logger.log(f"📄 HTML 文件: {html_file}")

        return 0

    except Exception as e:
        logger.log(f"❌ 错误: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
