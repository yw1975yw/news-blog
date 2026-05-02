#!/bin/bash
# 晚上存档脚本 - 将今日新闻存档到历史
# 时间：UTC 0:00 (北京时间 08:00)
# 用途：将首页新闻存档到历史页面

set -e

REPO_DIR="/home/swg/.openclaw/workspace/news-blog"

# 获取今天的日期（动态）
TODAY_STR=$(date '+%Y年%m月%d日')
TODAY_FILE=$(date '+%Y%m%d')
CURRENT_DATE=$(date '+%Y-%m-%d')
YEAR=$(date '+%Y')
MONTH=$(date '+%m')

# 获取上个月的最后一天（作为模板）
PREV_YEAR=$(date -d "last month" '+%Y')
PREV_MONTH=$(date -d "last month" '+%m')
PREV_MONTH_DISPLAY=$(date -d "last month" '+%-m')  # 去掉前导零

# 获取上个月的天数（使用date命令计算）
PREV_MONTH_DAYS=$(date -d "$(date +%Y-%m-01) -1 day" '+%d')

# 构建模板文件名
SOURCE_DATE="${PREV_YEAR}${PREV_MONTH}${PREV_MONTH_DAYS}"
SOURCE_DATE_STR="${PREV_YEAR}年${PREV_MONTH_DISPLAY}月${PREV_MONTH_DAYS}日"

echo "========================================"
echo "晚上存档任务启动 - $CURRENT_DATE"
echo "========================================"
echo "📅 存档日期：$TODAY_STR"
echo "📁 文件名：$TODAY_FILE.html"
echo "📋 模板：$SOURCE_DATE.html（上个月最后一天）"
echo "📂 目录：history/$YEAR/$MONTH/"
echo ""

cd $REPO_DIR

# 步骤1：创建目录结构
echo "📝 步骤1：创建目录结构..."
mkdir -p "history/$YEAR/$MONTH"
mkdir -p "images/$YEAR/$MONTH"
echo "✅ 已创建目录：history/$YEAR/$MONTH/"
echo "✅ 已创建目录：images/$YEAR/$MONTH/"
echo ""

# 步骤2：拷贝模板文件
echo "📝 步骤2：拷贝模板文件..."
if [ ! -f "history/$PREV_YEAR/$PREV_MONTH/$SOURCE_DATE.html" ]; then
    echo "❌ 错误：找不到模板文件 history/$PREV_YEAR/$PREV_MONTH/$SOURCE_DATE.html"
    exit 1
fi
cp "history/$PREV_YEAR/$PREV_MONTH/$SOURCE_DATE.html" "history/$YEAR/$MONTH/$TODAY_FILE.html"
echo "✅ 已拷贝：history/$PREV_YEAR/$PREV_MONTH/$SOURCE_DATE.html → history/$YEAR/$MONTH/$TODAY_FILE.html"
echo ""

# 步骤3：替换日期和修复导航链接
echo "📝 步骤3：替换日期和修复导航链接..."
sed -i "s/$SOURCE_DATE_STR/$TODAY_STR/g" "history/$YEAR/$MONTH/$TODAY_FILE.html"
sed -i "s/images\\/$SOURCE_DATE\\//images\\/$YEAR\\/$MONTH\\/$TODAY_FILE\\//g" "history/$YEAR/$MONTH/$TODAY_FILE.html"

# 修复导航链接：将相对路径改为正确的路径
sed -i 's|<a href="index.html"|<a href="../../../index.html"|g' "history/$YEAR/$MONTH/$TODAY_FILE.html"
sed -i 's|<a href="about.html"|<a href="../../../about.html"|g' "history/$YEAR/$MONTH/$TODAY_FILE.html"
sed -i 's|<a href="contact.html"|<a href="../../../contact.html"|g' "history/$YEAR/$MONTH/$TODAY_FILE.html"
sed -i 's|<a href="history.html"|<a href="../../../history.html"|g' "history/$YEAR/$MONTH/$TODAY_FILE.html"
sed -i 's|<a href="rss.xml"|<a href="../../../rss.xml"|g' "history/$YEAR/$MONTH/$TODAY_FILE.html"

echo "✅ 已将所有 $SOURCE_DATE_STR 替换为 $TODAY_STR"
echo "✅ 已将图片路径从 images/$TODAY_FILE/ 改为 images/$YEAR/$MONTH/$TODAY_FILE/"
echo "✅ 已修复导航链接路径"
echo ""

# 步骤4：从首页提取新闻并替换
echo "📝 步骤4：从首页提取新闻内容并替换..."

python3 << PYTHON_EOF
import re

# 从bash获取变量
today_file = "$TODAY_FILE"
year = "$YEAR"
month = "$MONTH"

# 读取首页
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
except:
    print("❌ 错误：无法读取首页 index.html")
    exit(1)

# 读取目标历史文件
try:
    with open(f"history/{year}/{month}/{today_file}.html", 'r', encoding='utf-8') as f:
        history_content = f.read()
except:
    print(f"❌ 错误：无法读取历史文件 history/{year}/{month}/{today_file}.html")
    exit(1)

# 从首页提取新闻网格内容
start = index_content.find('<div class="news-grid" id="newsGrid">')
if start != -1:
    depth = 1
    pos = start + len('<div class="news-grid" id="newsGrid">')
    while depth > 0 and pos < len(index_content):
        next_open = index_content.find('<div', pos)
        next_close = index_content.find('</div>', pos)
        
        if next_close == -1:
            break
        
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                end = next_close + 6
                news_grid = index_content[start:end]
                break
            pos = next_close + 6

# 提取每个news-card
card_pattern = r'<div class="news-card">(.*?)</div>\s*</div>'
cards = re.findall(card_pattern, news_grid, re.DOTALL)

# 提取每个article
article_pattern = r'<article class="news-card"[^>]*>(.*?)</article>'
articles = re.findall(article_pattern, history_content, re.DOTALL)

# 逐个替换article
new_content = history_content
for i, card in enumerate(cards):
    if i >= len(articles):
        break
    
    # 提取图片路径
    img_match = re.search(r'<img src="([^"]+)"', card)
    if img_match:
        img_path = img_match.group(1)
        # 提取文件名（如 news_102.png）
        img_filename = img_path.split('/')[-1]
        # 直接使用原始文件名，不做任何修改
        img_path = f'../../../images/{year}/{month}/{today_file}/{img_filename}'
    
    # 提取标题
    title_match = re.search(r'<h3 class="news-title">(.*?)</h3>', card)
    title = title_match.group(1) if title_match else "无标题"
    
    # 提取摘要
    summary_match = re.search(r'<p class="news-summary">(.*?)</p>', card)
    summary = summary_match.group(1) if summary_match else "无内容"
    
    # 提取标签
    tags = re.findall(r'<span class="tag">(.*?)</span>', card)
    
    # 构建新的article
    old_article = f'<article class="news-card"[^>]*>{re.escape(articles[i])}</article>'
    new_article = f'''<article class="news-card" data-news-id="{i+1}">
        <div class="news-image">
            <img src="{img_path}" alt="{title}" loading="lazy">
        </div>
        <div class="news-content">
            <h3 class="news-title">{title}</h3>
            <p class="news-summary">{summary}</p>
            <div class="news-tags">'''
    
    for tag in tags:
        new_article += f'\n                <span class="tag">{tag}</span>'
    
    new_article += '''
            </div>
        </div>
    </article>'''
    
    new_content = re.sub(old_article, new_article, new_content, count=1, flags=re.DOTALL)

# 写回文件
with open(f"history/{year}/{month}/{today_file}.html", 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ 已将首页新闻内容替换到 history/{year}/{month}/{today_file}.html")

PYTHON_EOF

echo ""

# 步骤5：复制首页图片
echo "📝 步骤5：复制首页图片..."
mkdir -p "images/$YEAR/$MONTH/$TODAY_FILE"

python3 << PYTHON_EOF
import re
import shutil
import os

today_file = "$TODAY_FILE"  # 从bash获取
year = "$YEAR"
month = "$MONTH"

# 读取首页
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# 提取所有图片路径
img_pattern = r'<img src="images/(news_\d+\.png)"'
matches = re.findall(img_pattern, index_content)

if matches:
    print(f"✅ 从首页找到 {len(matches)} 张图片")
    
    # 直接拷贝图片，保持原始文件名
    for img_name in matches:
        src_path = f"images/{img_name}"
        dst_path = f"images/{year}/{month}/{today_file}/{img_name}"
        
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
            print(f"  ✅ {img_name} → {img_name}")
        else:
            print(f"  ⚠️  警告：找不到 {src_path}")
else:
    print("❌ 错误：无法从首页提取图片路径")

PYTHON_EOF

echo "✅ 已复制首页图片到 images/$YEAR/$MONTH/$TODAY_FILE/"
echo ""

# 步骤6：不再需要重命名图片，直接跳过
echo "📝 步骤6：跳过图片重命名（已使用原始文件名）"
echo ""

# 步骤7：更新历史索引页面
echo "📝 步骤7：更新历史索引页面..."

python3 << PYTHON_EOF
import re

# 从bash获取变量
today_file = "$TODAY_FILE"
today_date_str = "$TODAY_STR"
year = "$YEAR"
month = "$MONTH"

# 读取月份索引文件
index_path = f'history/{year}/{month}/index.html'

# 检查文件是否存在，如果不存在则创建
try:
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    # 创建新的月份索引文件
    content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{year}年{month}月 - 历史存档</title>
    <link rel="stylesheet" href="../../styles.css">
    <style>
        .month-header {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-bottom: 30px;
        }}

        .month-header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .month-header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .month-nav {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .month-nav a {{
            padding: 10px 20px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            text-decoration: none;
            color: #333;
            transition: all 0.3s;
        }}

        .month-nav a:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}

        .days-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .day-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            text-decoration: none;
            color: inherit;
        }}

        .day-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}

        .day-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.3em;
        }}

        .day-card p {{
            color: #666;
            font-size: 0.9em;
            margin: 0;
        }}

        .day-card .count {{
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="../../../index.html">首页</a>
            <a href="../index.html">{year}年</a>
            <a href="index.html" class="active">{month}月</a>
        </nav>
    </header>

    <div class="month-header">
        <h1>📅 {year}年{month}月</h1>
        <p>历史存档</p>
    </div>

    <div class="month-nav">
        <a href="../index.html">← 返回年份列表</a>
        <a href="../../../index.html">返回首页</a>
    </div>

    <div class="days-grid">
    </div>

    <footer>
        <p>&copy; {year} 环球新闻 | GitHub Pages</p>
    </footer>
</body>
</html>'''
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已创建新的月份索引文件：{index_path}")

# 提取今日新闻标题（用于索引描述）
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # 提取前3条新闻标题
    titles = []
    for match in re.finditer(r'<h3 class="news-title">(.*?)</h3>', index_html):
        title = match.group(1).strip()
        titles.append(title.split('·')[0])  # 取"·"前面的部分
        if len(titles) >= 3:
            break
    
    # 生成描述（取前3个标题的前几个字）
    description = '、'.join([t[:10] for t in titles[:3]])
    if len(description) > 30:
        description = description[:30] + '...'
    
except:
    # 如果无法提取，使用默认描述
    description = "每日新闻更新，涵盖科技、财经、国际等领域"

# 检查是否已包含今日的链接
if today_file not in content:
    # 生成新的历史项
    new_item = f'''
        <a href="{today_file}.html" class="day-card">
            <h3>{today_date_str} <span class="count">10条</span></h3>
            <p>{description}</p>
        </a>'''

    # 找到days-grid里面的最后一个 </a> 标签
    days_grid_start = content.find('<div class="days-grid">')
    if days_grid_start != -1:
        days_grid_end = content.find('</div>', days_grid_start + len('<div class="days-grid">'))
        if days_grid_end != -1:
            # 在days-grid里面找最后一个 </a> 标签
            days_grid_content = content[days_grid_start:days_grid_end]
            last_a_pos = days_grid_content.rfind('</a>')
            if last_a_pos != -1:
                # 在days-grid里面的最后一个 </a> 后面插入新项
                insert_pos = days_grid_start + last_a_pos + len('</a>')
                new_content = content[:insert_pos] + new_item + content[insert_pos:]
                
                # 写回
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ 月份索引已更新：添加 {today_date_str} 链接")
            else:
                # days-grid里面没有</a>标签，直接插入
                insert_pos = days_grid_start + len('<div class="days-grid">')
                new_content = content[:insert_pos] + new_item + content[insert_pos:]
                
                # 写回
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ 月份索引已更新：添加 {today_date_str} 链接")
        else:
            print(f"❌ 错误：无法找到days-grid的结束标签")
    else:
        print(f"❌ 错误：无法找到days-grid")
else:
    print(f"⏭️  月份索引已包含 {today_date_str}，跳过更新")

PYTHON_EOF

echo ""

# 步骤7.5：更新年份索引页面
echo "📝 步骤7.5：更新年份索引页面..."

python3 << PYTHON_EOF
import re

# 从bash获取变量
year = "$YEAR"
month = "$MONTH"

# 读取年份索引文件
year_index_path = f'history/{year}/index.html'
try:
    with open(year_index_path, 'r', encoding='utf-8') as f:
        content = f.read()
except:
    print(f"❌ 错误：无法读取 {year_index_path}")
    exit(1)

# 计算当前月份有多少天
month_index_path = f'history/{year}/{month}/index.html'
try:
    with open(month_index_path, 'r', encoding='utf-8') as f:
        month_content = f.read()
    
    # 统计 day-card 的数量
    day_count = month_content.count('class="day-card"')
    
    # 去掉月份的前导零（04 -> 4）
    month_display = month.lstrip('0')
    
    # 检查是否已存在该月份的链接卡片
    month_pattern = rf'<a href="{month}/index\.html" class="month-card">\s*<h3>{month_display}月 <span class="count">(\d+)天</span></h3>\s*<p>(.*?)</p>\s*</a>'
    match = re.search(month_pattern, content)
    
    if match:
        # 已存在链接卡片，更新天数和日期范围
        old_count = match.group(1)
        old_range = match.group(2)
        
        # 提取日期范围（如 "3月22日 - 3月28日"）
        if ' - ' in old_range:
            start_date = old_range.split(' - ')[0]
            # 更新结束日期为当前日期
            today_str = "$TODAY_STR"
            new_range = f"{start_date} - {today_str}"
        else:
            new_range = old_range
        
        # 替换
        new_month_card = f'''<a href="{month}/index.html" class="month-card">
            <h3>{month_display}月 <span class="count">{day_count}天</span></h3>
            <p>{new_range}</p>
        </a>'''
        
        content = re.sub(month_pattern, new_month_card, content)
        
        # 写回
        with open(year_index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 年份索引已更新：{month}月 {day_count}天 ({new_range})")
    else:
        # 不存在链接卡片，检查是否存在disabled卡片
        disabled_pattern = rf'<div class="month-card disabled">\s*<h3>{month_display}月</h3>\s*<p>暂无数据</p>\s*</div>'
        disabled_match = re.search(disabled_pattern, content)
        
        if disabled_match:
            # 将disabled卡片替换为链接卡片
            today_str = "$TODAY_STR"
            new_month_card = f'''<a href="{month}/index.html" class="month-card">
            <h3>{month_display}月 <span class="count">{day_count}天</span></h3>
            <p>{today_str}</p>
        </a>'''
            
            content = re.sub(disabled_pattern, new_month_card, content)
            
            # 写回
            with open(year_index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 年份索引已更新：{month}月 {day_count}天 ({today_str})")
        else:
            print(f"⚠️  警告：无法找到 {month}月的卡片")
        
except Exception as e:
    print(f"❌ 错误：无法更新年份索引 - {e}")

PYTHON_EOF

echo ""

# 步骤8：Git提交推送
echo "📝 步骤8：提交到Git..."
git add history/$YEAR/$MONTH/$TODAY_FILE.html images/$YEAR/$MONTH/$TODAY_FILE/ history/$YEAR/$MONTH/index.html history/$YEAR/index.html
git commit -m "晚上存档：添加$TODAY_STR历史页面

- 拷贝历史模板并替换日期
- 从首页提取新闻内容
- 复制并更新图片
- 重命名图片为 news_102.png 格式
- 更新月份索引页面
- 更新年份索引页面"

if git push; then
    echo "✅ 步骤8完成：Git推送成功"
    PUSH_SUCCESS=1
else
    echo "❌ 步骤8失败：Git推送失败"
    PUSH_SUCCESS=0
fi
echo ""

# 步骤9：发送飞书通知
echo "📝 步骤9：发送飞书通知..."
if [ $PUSH_SUCCESS -eq 1 ]; then
    /home/swg/.openclaw/workspace/news-blog/notify.sh "格式晚上7点存档任务完成。"
    echo "✅ 步骤9完成：飞书通知已发送"
else
    /home/swg/.openclaw/workspace/news-blog/notify.sh "⚠️ 格式晚上7点存档任务完成（Git推送失败）。"
    echo "⚠️ 步骤9完成：发送失败通知"
fi
echo ""

echo "========================================"
echo "✅ 晚上存档任务完成！"
echo "========================================"
echo "📅 存档日期：$TODAY_STR"
echo "📁 历史文件：history/$YEAR/$MONTH/$TODAY_FILE.html"
echo "📂 图片目录：images/$YEAR/$MONTH/$TODAY_FILE/"
echo "📤 Git推送：$([ $PUSH_SUCCESS -eq 1 ] && echo '成功 ✅' || echo '失败 ❌')"
echo "🕐 完成时间：$(date '+%Y-%m-%d %H:%M:%S UTC')"
echo "========================================"
