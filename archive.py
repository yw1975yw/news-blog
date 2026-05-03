#!/usr/bin/env python3
"""
环球新闻归档脚本
将当天的新闻归档到history目录
"""

import os
import re
from datetime import datetime
from pathlib import Path
import subprocess

# 配置
BLOG_PATH = "/home/swg/.openclaw/workspace/news-blog"
INDEX_FILE = Path(BLOG_PATH) / "index.html"
HISTORY_DIR = Path(BLOG_PATH) / "history"

def get_current_date():
    """获取当前日期"""
    return datetime.now().strftime("%Y%m%d")

def get_current_date_display():
    """获取当前日期显示格式"""
    return datetime.now().strftime("%Y年%m月%d日")

def get_year_month():
    """获取年月"""
    now = datetime.now()
    return now.strftime("%Y"), now.strftime("%m")

def archive_news():
    """归档新闻"""
    current_date = get_current_date()
    current_date_display = get_current_date_display()
    year, month = get_year_month()

    # 创建归档目录
    archive_dir = HISTORY_DIR / year / month
    archive_dir.mkdir(parents=True, exist_ok=True)

    # 归档文件路径
    archive_file = archive_dir / f"{current_date}.html"

    # 读取index.html
    if not INDEX_FILE.exists():
        print(f"❌ 错误：找不到 {INDEX_FILE}")
        return False

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 修改图片路径（从 images/ 改为 ../../../images/）
    content = content.replace('images/', '../../../images/')

    # 修改导航链接（从 index.html 改为 ../../../index.html）
    content = content.replace('href="index.html"', 'href="../../../index.html"')
    content = content.replace('href="about.html"', 'href="../../../about.html"')
    content = content.replace('href="contact.html"', 'href="../../../contact.html"')
    content = content.replace('href="history.html"', 'href="../../../history.html"')
    content = content.replace('href="rss.xml"', 'href="../../../rss.xml"')

    # 保存归档文件
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 归档文件已创建: {archive_file}")

    # 更新月份索引
    update_month_index(archive_dir, year, month)

    # 更新年份索引
    update_year_index(HISTORY_DIR / year, year)

    return True

def update_month_index(archive_dir, year, month):
    """更新月份索引"""
    index_file = archive_dir / "index.html"

    # 获取所有归档文件
    archive_files = sorted(archive_dir.glob("*.html"))
    archive_files = [f for f in archive_files if f.name != "index.html"]

    if not archive_files:
        print(f"❌ 错误：没有找到归档文件")
        return

    # 创建月份索引
    html_content = f"""<!DOCTYPE html>
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
        <h1>📅 {year}年{month}月国际要闻</h1>
        <p>全球政治、科技、经济热点汇总</p>
    </div>

    <div class="month-nav">
        <a href="../index.html">← 返回年份列表</a>
        <a href="../../../index.html">返回首页</a>
    </div>

    <div class="days-grid">
"""

    # 添加每一天的卡片
    for archive_file in archive_files:
        date_str = archive_file.stem
        # 格式化日期显示
        year_part = date_str[:4]
        month_part = date_str[4:6]
        day_part = date_str[6:8]
        display_date = f"{year_part}年{month_part}月{day_part}日"

        # 读取文件获取新闻数量
        with open(archive_file, 'r', encoding='utf-8') as f:
            content = f.read()
        news_count = content.count('<div class="news-card">')

        # 生成摘要
        summary = f"包含{news_count}条新闻，涵盖国际政治、经济、科技等领域的最新动态"

        html_content += f"""
        <a href="{date_str}.html" class="day-card">
            <h3>{display_date} <span class="count">{news_count}条</span></h3>
            <p>{summary}</p>
        </a>
"""

    html_content += """
    </div>

    <footer>
        <p>&copy; 2026 环球新闻 | GitHub Pages</p>
    </footer>
</body>
</html>
"""

    # 保存月份索引
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ 月份索引已更新: {index_file}")

def update_year_index(year_dir, year):
    """更新年份索引"""
    index_file = year_dir / "index.html"

    # 获取所有月份目录
    month_dirs = sorted([d for d in year_dir.iterdir() if d.is_dir() and d.name.isdigit()])

    if not month_dirs:
        print(f"❌ 错误：没有找到月份目录")
        return

    # 创建年份索引
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{year}年 - 历史新闻</title>
    <link rel="stylesheet" href="../../styles.css">
    <style>
        .year-header {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-bottom: 30px;
        }}

        .year-header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .year-header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .year-nav {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }}

        .year-nav a {{
            padding: 10px 20px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            text-decoration: none;
            color: #333;
            transition: all 0.3s;
        }}

        .year-nav a:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}

        .months-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1000px;
            margin: 0 auto;
        }}

        .month-card {{
            background: white;
            border-radius: 10px;
            padding: 30px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            text-decoration: none;
            color: inherit;
            text-align: center;
        }}

        .month-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}

        .month-card h3 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.5em;
        }}

        .month-card p {{
            color: #666;
            font-size: 0.9em;
            margin: 0;
        }}

        .month-card .count {{
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            margin-left: 10px;
        }}

        .month-card.disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        .month-card.disabled:hover {{
            transform: none;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="../../index.html">首页</a>
            <a href="../../history.html">历史</a>
            <a href="index.html" class="active">{year}年</a>
        </nav>
    </header>

    <div class="year-header">
        <h1>📅 {year}年</h1>
        <p>历史新闻存档</p>
    </div>

    <div class="year-nav">
        <a href="../../history.html">← 返回历史列表</a>
        <a href="../../index.html">返回首页</a>
    </div>

    <div class="months-grid">
"""

    # 添加每个月的卡片
    for month_dir in month_dirs:
        month_num = month_dir.name
        month_name = f"{int(month_num)}月"

        # 获取该月的所有归档文件
        archive_files = sorted(month_dir.glob("*.html"))
        archive_files = [f for f in archive_files if f.name != "index.html"]

        if archive_files:
            # 计算天数
            days_count = len(archive_files)
            # 获取日期范围
            first_date = archive_files[0].stem
            last_date = archive_files[-1].stem

            # 格式化日期
            first_display = f"{first_date[:4]}年{first_date[4:6]}月{first_date[6:8]}日"
            last_display = f"{last_date[:4]}年{last_date[4:6]}月{last_date[6:8]}日"

            date_range = f"{first_display} - {last_display}"

            html_content += f"""
        <a href="{month_num}/index.html" class="month-card">
            <h3>{month_name} <span class="count">{days_count}天</span></h3>
            <p>{date_range}</p>
        </a>
"""
        else:
            html_content += f"""
        <div class="month-card disabled">
            <h3>{month_name}</h3>
            <p>暂无数据</p>
        </div>
"""

    # 添加其他月份（占位符）
    all_months = list(range(1, 13))
    existing_months = [int(d.name) for d in month_dirs if d.name.isdigit()]

    for month in all_months:
        if month not in existing_months:
            html_content += f"""
        <div class="month-card disabled">
            <h3>{month}月</h3>
            <p>暂无数据</p>
        </div>
"""

    html_content += """
    </div>

    <footer>
        <p>&copy; 2026 环球新闻 | 技术博客 | GitHub Pages</p>
    </footer>
</body>
</html>
"""

    # 保存年份索引
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ 年份索引已更新: {index_file}")

def commit_to_github():
    """提交到GitHub"""
    try:
        # 添加所有更改
        subprocess.run(
            ["git", "add", "."],
            cwd=BLOG_PATH,
            check=True,
            capture_output=True,
            text=True
        )

        # 提交
        current_date = get_current_date()
        commit_message = f"Archive: {current_date}"
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=BLOG_PATH,
            check=True,
            capture_output=True,
            text=True
        )

        # 推送
        subprocess.run(
            ["git", "push"],
            cwd=BLOG_PATH,
            check=True,
            capture_output=True,
            text=True
        )

        print(f"✅ 已提交到GitHub: {commit_message}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("📰 环球新闻归档")
    print("=" * 60)

    # 归档新闻
    if not archive_news():
        print("❌ 归档失败")
        return

    # 提交到GitHub
    if not commit_to_github():
        print("❌ Git提交失败")
        return

    print("=" * 60)
    print("✅ 归档完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
