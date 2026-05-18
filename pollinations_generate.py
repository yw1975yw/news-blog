#!/usr/bin/env python3
"""
图片生成脚本：glm/CogView-3-Flash 主渠道，Pollinations 备用
Usage: python3 pollinations_generate.py "prompt" --output /path/to/output.png [--width 1344] [--height 768] [--seed N]

优先使用智谱 CogView-3-Flash，失败时自动切换 Pollinations（免费）
"""

import os
import sys
import argparse
import urllib.parse
import json
import time
import io
import subprocess
from pathlib import Path

try:
    import requests
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

try:
    from PIL import Image
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image


# ------------------------------------------------------------------
# 1. Pollinations（备用，免费，无需 key）
# ------------------------------------------------------------------
def generate_pollinations(prompt, output_path, width=1344, height=768, seed=None, model=None, nologo=False):
    """通过 Pollinations AI 生成图片（备用渠道）"""
    encoded_prompt = urllib.parse.quote(prompt)
    params = [f"width={width}", f"height={height}"]
    if seed:
        params.append(f"seed={seed}")
    if model:
        params.append(f"model={model}")
    if nologo:
        params.append("nologo=true")
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?{'&'.join(params)}"

    print(f"   [Pollinations] URL: {url[:80]}...")
    try:
        response = requests.get(url, timeout=120, headers={
            "User-Agent": "Mozilla/5.0 (compatible; Hermes/1.0)"
        })
        if response.status_code != 200:
            print(f"   [Pollinations] HTTP {response.status_code}")
            return False
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type and len(response.content) < 1000:
            print(f"   [Pollinations] 响应非图片: {content_type}")
            return False
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img = Image.open(io.BytesIO(response.content))
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_path, "PNG")
        size_kb = len(response.content) / 1024
        print(f"   [Pollinations] ✅ 成功 ({size_kb:.0f} KB)")
        return True
    except Exception as e:
        print(f"   [Pollinations] ❌ {e}")
        return False


# ------------------------------------------------------------------
# 2. glm/CogView-3-Flash（主渠道，需要 key）
# ------------------------------------------------------------------
def get_glm_api_keys():
    """从 config.yaml 读取智谱 API keys（支持 | 多行格式）"""
    import yaml
    config_path = Path.home() / ".hermes/config.yaml"
    if not config_path.exists():
        return []
    try:
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        # 找 image_gen.api_key
        keys = []
        ig = cfg.get("image_gen", {})
        ak = ig.get("api_key", "")
        if isinstance(ak, str):
            keys = [k.strip() for k in ak.splitlines() if k.strip()]
        elif isinstance(ak, list):
            keys = [k for k in ak if k]
        return keys
    except Exception as e:
        print(f"   [glm] 读取配置失败: {e}")
        return []


def generate_glm_cogview(prompt, output_path, width=1344, height=768, seed=None, nologo=False):
    """通过智谱 CogView-3-Flash 生成图片（主渠道）"""
    keys = get_glm_api_keys()
    if not keys:
        print("   [glm] 未找到 API key，跳过")
        return False

    base_url = "https://open.bigmodel.cn/api/paas/v4"
    # CogView-3-Flash 支持 width/height，aspect_ratio 参数
    payload = {
        "model": "cogview-3-flash",
        "prompt": prompt,
        "aspect_ratio": f"{width}:{height}",
        "extra_body": {"seed": seed} if seed else {}
    }

    for i, key in enumerate(keys):
        print(f"   [glm] 尝试 key {i+1}/{len(keys)}...")
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        try:
            resp = requests.post(
                f"{base_url}/images/generations",
                json=payload,
                headers=headers,
                timeout=120
            )
            if resp.status_code == 200:
                data = resp.json()
                image_url = None
                # 支持多种响应格式
                if "data" in data and len(data["data"]) > 0:
                    image_url = data["data"][0].get("url") or data["data"][0].get("b64_json")
                if not image_url:
                    print(f"   [glm] 响应格式异常: {str(data)[:100]}")
                    continue

                # 下载图片
                if image_url.startswith("data:"):
                    # base64 格式
                    import base64
                    b64 = image_url.split(",")[1]
                    img_data = base64.b64decode(b64)
                else:
                    img_resp = requests.get(image_url, timeout=60)
                    img_data = img_resp.content

                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                img = Image.open(io.BytesIO(img_data))
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(output_path, "PNG")
                size_kb = len(img_data) / 1024
                print(f"   [glm] ✅ 成功 ({size_kb:.0f} KB)")
                return True
            elif resp.status_code == 403 or resp.status_code == 401:
                print(f"   [glm] key {i+1} 认证失败，继续...")
                continue
            elif resp.status_code == 429:
                print(f"   [glm] key {i+1} 限流，继续...")
                continue
            else:
                print(f"   [glm] key {i+1} HTTP {resp.status_code}: {resp.text[:80]}")
                continue
        except Exception as e:
            print(f"   [glm] key {i+1} 异常: {e}")
            continue

    print("   [glm] 所有 key 均失败")
    return False


# ------------------------------------------------------------------
# 3. 主函数：优先 glm，失败则 Pollinations
# ------------------------------------------------------------------
def generate_image(prompt, output_path, width=1344, height=768, seed=None, model=None, nologo=False):
    """生成图片：glm 主渠道，Pollinations 备用"""
    output_path = Path(output_path)

    # 1. 优先尝试 glm/CogView-3-Flash
    print(f"🎨 Generating image: {prompt[:60]}... | {width}x{height}")
    print(f"   [glm] 优先使用智谱 CogView-3-Flash...")
    if generate_glm_cogview(prompt, output_path, width, height, seed, nologo):
        return True

    # 2. 备用 Pollinations
    print(f"   [Pollinations] 回退到 Pollinations...")
    if generate_pollinations(prompt, output_path, width, height, seed, model, nologo):
        return True

    print(f"❌ 所有渠道均失败")
    return False


def main():
    parser = argparse.ArgumentParser(description="图片生成（glm 主渠道，Pollinations 备用）")
    parser.add_argument("prompt", help="图片描述提示词")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    parser.add_argument("--width", type=int, default=1280, help="宽度 (默认 1280)")
    parser.add_argument("--height", type=int, default=720, help="高度 (默认 720)")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--model", default="flux", help="Pollinations 模型 (默认 flux)")
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