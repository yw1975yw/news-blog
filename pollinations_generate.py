#!/usr/bin/env python3
"""
Pollinations 图片生成脚本
免费，无需 API key，直接调用 https://image.pollinations.ai/
Usage: python3 pollinations_generate.py "prompt" --output /path/to/output.png [--width 1344] [--height 768]
"""

import os
import sys
import argparse
import urllib.parse
import requests
from pathlib import Path


def generate_image(prompt, output_path, width=1344, height=768, seed=None, model=None, nologo=False):
    """通过 Pollinations AI 生成图片"""
    
    # URL 编码提示词
    encoded_prompt = urllib.parse.quote(prompt)
    
    # 构建 URL - 使用 prompt/ 前缀，用 & 分隔参数
    # 第一个参数用 ? 分隔，其他用 & 分隔
    params = [f"width={width}", f"height={height}"]
    if seed:
        params.append(f"seed={seed}")
    if model:
        params.append(f"model={model}")
    if nologo:
        params.append("nologo=true")
    
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?{'&'.join(params)}"
    
    print(f"🎨 Generating image...")
    print(f"   Prompt: {prompt[:60]}...")
    print(f"   Size: {width}x{height}")
    if seed:
        print(f"   Seed: {seed}")
    
    try:
        response = requests.get(url, timeout=120, headers={
            "User-Agent": "Mozilla/5.0 (compatible; Hermes/1.0)"
        })
        
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
            return False
        
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type and len(response.content) < 1000:
            print(f"❌ 响应不是图片: {content_type}, size={len(response.content)}")
            print(f"   Body: {response.text[:200]}")
            return False
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        size_kb = len(response.content) / 1024
        print(f"✅ 图片已保存: {output_path} ({size_kb:.0f} KB)")
        return True
        
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Pollinations 图片生成")
    parser.add_argument("prompt", help="图片描述提示词")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    parser.add_argument("--width", type=int, default=1344, help="宽度 (默认 1344)")
    parser.add_argument("--height", type=int, default=768, help="高度 (默认 768)")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--model", default="turbo", help="模型名称 (flux, turbo 等，默认 turbo)")
    parser.add_argument("--nologo", action="store_true", help="不添加水印")
    
    args = parser.parse_args()
    
    success = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        width=args.width,
        height=args.height,
        seed=args.seed,
        model=args.model,
        nologo=args.nologo
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
