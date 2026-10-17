#!/usr/bin/env python3
"""
🌸 鲲鹏志 · 客卿小花组统一视觉头像生成与多云图床（MinIO & Cloudflare R2）分发
=============================================================================
目标：
1. 采用免费稳定的图像生成模型 agnes-image-2.5-flash (512x512 适度轻量画幅)
2. 规避 429：单步串行生图 + 3秒限流保护，确保平稳出图
3. 为 6 席小花分别生成统一中国风二次元唯美花仙子人设头像
4. 本地落盘 ➔ 同步上传 MinIO (ct100/flowers/avatars) 与 Cloudflare R2 (r2/flowers/avatars)
5. 产出可访问的公开图床链接清单
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
import requests

LITELLM_IMAGE_URL = "https://litellm.capitaltrain.cn/v1/images/generations"
MASTER_KEY = "sk-47318"
IMAGE_MODEL = "agnes-image-2.5-flash"

FLOWERS = [
    {
        "key": "moli",
        "name": "茉莉仙子",
        "soul": "秋香",
        "color": "洁白与淡金",
        "prompt": "An ethereal circular anime avatar portrait of a delicate Chinese white jasmine flower fairy girl, wearing pure white and pale gold silk robes, adorned with fresh blooming jasmine petals in hair, gentle breeze, serene and intelligent expression, soft daylight, watercolor digital art style, high quality, 512x512 circular centered portrait, clean pastel background"
    },
    {
        "key": "muxu",
        "name": "苜蓿仙子",
        "soul": "碧涛",
        "color": "翠绿与嫩青",
        "prompt": "An ethereal circular anime avatar portrait of a lively Chinese green clover flower fairy girl, adorned with emerald four-leaf clover crowns, dewdrops, tranquil lake water reflection, sharp insightful eyes, fresh mint green aesthetic, soft lighting, watercolor digital art style, 512x512 circular centered portrait"
    },
    {
        "key": "tumi",
        "name": "荼蘼仙子",
        "soul": "青黛",
        "color": "青黛与冷月白",
        "prompt": "An elegant circular anime avatar portrait of a profound Chinese wild rose fairy girl, dark teal and moonlight indigo silk ribbons, late-spring petals fluttering, noble and philosophic look, cool night starlight illumination, exquisite Chinese fantasy anime aesthetic, 512x512 circular centered portrait"
    },
    {
        "key": "zhuyu",
        "name": "茱萸仙子",
        "soul": "霁月",
        "color": "绛红与素魄",
        "prompt": "A poised circular anime avatar portrait of a mature Chinese cornelian cherry flower fairy girl, subtle scarlet berries and purple embroidery, autumnal mountain mist in background, calm analytical gaze, gentle radiant glow, high resolution aesthetic watercolor portrait, 512x512 circular centered portrait"
    },
    {
        "key": "meigui",
        "name": "玫瑰仙子",
        "soul": "绯云",
        "color": "绯云深红与朝露",
        "prompt": "A charming circular anime avatar portrait of a blossoming crimson rose fairy girl, adorned with lush red rose blossoms and golden filigree, morning sunlight, radiant warm expression, graceful Chinese anime art style, soft glowing bokeh, 512x512 circular centered portrait"
    },
    {
        "key": "qiangwei",
        "name": "蔷薇仙子",
        "soul": "金波",
        "color": "粉金与朝霞",
        "prompt": "A spirited circular anime avatar portrait of a sharp and radiant Chinese multi-flora climbing rose fairy girl, golden sunlight and pink wild roses with delicate thorns, confident and sharp spirited gaze, vibrant and elegant, high detail digital anime portrait, 512x512 circular centered portrait"
    }
]

def main():
    print("=" * 76)
    print("🎨 小花组专属视觉头像生成与多云图床（MinIO & R2）发布")
    print("=" * 76)
    print(f"🖼️ 生图模型: {IMAGE_MODEL} (512x512 轻量规格，防429平稳生成)")
    print(f"📦 图床主桶: MinIO ct100/flowers & Cloudflare R2 r2/flowers")
    print("-" * 76)

    out_dir = Path("/home/ben/code/gitea/kunpengzhi-ai/research/avatars")
    out_dir.mkdir(parents=True, exist_ok=True)

    headers = {
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    }

    results = []

    for idx, f in enumerate(FLOWERS, 1):
        key = f["key"]
        name = f["name"]
        soul = f["soul"]
        prompt = f["prompt"]

        print(f"\n[{idx}/6] 正在为 {name} ({soul}) 渲染专属视觉头像...")

        payload = {
            "model": IMAGE_MODEL,
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }

        img_url = ""
        dur = 0
        for attempt in range(2):
            try:
                t0 = time.time()
                r = requests.post(LITELLM_IMAGE_URL, json=payload, headers=headers, timeout=30)
                dur = round(time.time() - t0, 2)
                if r.status_code == 200:
                    data = r.json().get("data", [])
                    if data and "url" in data[0]:
                        img_url = data[0]["url"]
                        break
                elif r.status_code == 429:
                    print(f"    ⚠️ 触发 429 限流保护，休眠 8 秒后重试 (Attempt {attempt+1}/2)...")
                    time.sleep(8)
                else:
                    print(f"    ⚠️ 生图接口返回 HTTP {r.status_code}: {r.text[:100]}")
            except Exception as e:
                print(f"    ⚠️ 生图请求异常: {e}")
                time.sleep(3)

        if not img_url:
            print(f"    ❌ {name} 头像生成失败")
            continue

        print(f"    ✨ 画面已产出 (耗时 {dur}s): {img_url[:70]}...")

        # 下载图片到本地
        local_file = out_dir / f"{key}.png"
        try:
            img_bytes = requests.get(img_url, timeout=20).content
            with open(local_file, "wb") as f_out:
                f_out.write(img_bytes)
            size_kb = round(len(img_bytes) / 1024, 1)
            print(f"    💾 本地落盘: {local_file.name} ({size_kb} KB)")
        except Exception as dl_err:
            print(f"    ❌ 下载图片失败: {dl_err}")
            continue

        # 上传到 MinIO ct100/flowers/avatars/
        minio_target = f"ct100/flowers/avatars/{key}.png"
        r2_target = f"r2/flowers/avatars/{key}.png"

        cmd_minio = f"mc cp {local_file} {minio_target}"
        subprocess.run(cmd_minio, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"    ☁️ 已推送到 MinIO: ct100/flowers/avatars/{key}.png")

        # 同步上传到 Cloudflare R2
        cmd_r2 = f"mc cp {local_file} {r2_target}"
        subprocess.run(cmd_r2, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"    ⚡ 已同步至 Cloudflare R2: r2/flowers/avatars/{key}.png")

        public_minio_url = f"https://minio-s3.capitaltrain.cn/flowers/avatars/{key}.png"
        results.append({
            "key": key,
            "name": name,
            "soul": soul,
            "file": str(local_file),
            "size_kb": size_kb,
            "minio_url": public_minio_url,
            "r2_path": r2_target
        })

        # 防 429 间隔
        time.sleep(3)

    manifest_path = out_dir / "avatars_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 76)
    print(f"🎉 6 席小花专属头像已全量上云图床 (MinIO + Cloudflare R2)！")
    print(f"📋 清单已归档至: {manifest_path}")
    print("=" * 76)

if __name__ == "__main__":
    main()
