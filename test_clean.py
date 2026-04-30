import sys, os
# 禁用logger输出
os.environ['HERMES_QUIET'] = '1'
sys.path.insert(0, '.')

# 直接测试clean_title在step_1里的实际效果
from auto_update import step_1_search_news, clean_title

news = step_1_search_news(2)
print(f"step_1返回{len(news)}条")
for n in news:
    t = n['title']
    c = clean_title(t)
    print(f"原始[{len(t)}]: {t}")
    print(f"清洗[{len(c)}]: {c}")
    print(f"相同: {t==c}")
    print()
