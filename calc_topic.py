#!/usr/bin/env python3
from datetime import date

ref = date(2025, 1, 1)
today = date(2025, 5, 10)
days = (today - ref).days
idx = days % 10
topics = ['Python编程技巧', 'Docker容器化', 'Git版本控制', 'Linux系统管理', '数据库优化', 'Web安全防护', '微服务架构', '云原生', 'DevOps工具', 'AI/ML工程']

print(f'Days since ref: {days}')
print(f'Topic index: {idx}')
print(f'Topic: {topics[idx]}')
print(f'Image filename: images/tech_{today.strftime("%Y%m%d")}.png')
print(f'History link: history/{today.strftime("%Y/%m/%Y%m%d")}.html')