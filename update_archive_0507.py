#!/usr/bin/env python3
"""
更新5月7日归档页面，使用新的新闻配图
"""

# 读取当前 index.html
with open('index.html', 'r') as f:
    content = f.read()

# 1. 替换图片路径：history页面需要3层返回
content = content.replace('images/website-background-8k.png', '../../../images/website-background-8k.png')
content = content.replace('images/cover.png', '../../../images/cover.png')
content = content.replace('images/news-generated/', '../../../images/news-generated/')

# 2. 修改标题
content = content.replace(
    '<title>环球新闻 - 每日全球热点新闻精选</title>',
    '<title>全球20条热点新闻 - 2026年05月07日 | 环球新闻</title>'
)
content = content.replace(
    '<meta name="description" content="环球新闻首页，汇聚全球政治、经济、科技、军事等领域的热点新闻，为您呈现多维度的国际资讯视角">',
    '<meta name="description" content="2026年05月07日全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">'
)

# 3. 修顶部标题区域
content = content.replace(
    '<h1 class="cover-title">今日环球热点新闻</h1>',
    '<h1 class="cover-title">2026年05月07日 新闻归档</h1>'
)
content = content.replace(
    '<p class="cover-subtitle">欢迎访问环球新闻，获取每日最新全球资讯</p>',
    '<p class="cover-subtitle">共20条新闻 | 归档页面</p>'
)

# 4. 在页脚上方添加归档说明
archive_note = '''
        <div style="background: linear-gradient(145deg, #f6f8fa 0%, #ffffff 100%); padding: 20px; margin: 30px 0; border-radius: 12px; text-align: center; border: 1px solid rgba(0,0,0,0.1);">
            <p style="color: #333; opacity: 0.8; margin-bottom: 10px;">
                📁 此页面为 <strong>2026年05月07日</strong> 的新闻归档
            </p>
            <p style="margin: 0;">
                <a href="../index.html" style="color: #667eea; text-decoration: none; font-weight: 500;">
                    ← 返回首页查看最新新闻
                </a>
            </p>
        </div>
'''

# 在 footer 标签前插入
content = content.replace('<footer>', archive_note + '\n    <footer>')

# 写回
with open('history/2026/05/20260507.html', 'w') as f:
    f.write(content)

print("✅ 已更新 history/2026/05/20260507.html")
print("   - 使用新的新闻配图 (news-generated/)")
print("   - 更新标题和元信息")
print("   - 添加归档导航链接")