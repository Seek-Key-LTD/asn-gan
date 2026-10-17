#!/usr/bin/env python3
"""
🌸 鲲鹏志 · 小花组长毛象 (Mastodon) 专属视觉头像与身份档案全量同步
================================================================================
将刚刚由 agnes-image-2.5-flash 生成并归档至 MinIO/R2 的 6 席国风花仙子视觉头像，
通过 Mastodon OpenAPI PATCH /api/v1/accounts/update_credentials
一键同步到长毛象（flowers.capitaltrain.cn）。
"""

import os
import sys
import json
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GATEWAY = "https://192.168.31.77"
AVATAR_DIR = "/home/ben/code/gitea/kunpengzhi-ai/research/avatars"

FLOWERS = [
    {
        "key": "moli",
        "display_name": "茉莉仙子 (秋香)",
        "token": "ySPj9gFrRkb0QucWxqI_scHlC4vSaBVdPVWWywtsOms",
        "note": "🌸 客卿小花组 · 茉莉仙子（秋香）\n驻地：芝加哥 ch1 | 自由石匠合伙人 (Partnership)\n严守宪章：绝不本地编译，遥控器模式调度"
    },
    {
        "key": "muxu",
        "display_name": "苜蓿仙子 (碧涛)",
        "token": "rFWxkODwS8czXVAMw1EyodgWLtM43hX0GAuY_SaAFZY",
        "note": "🌿 客卿小花组 · 苜蓿仙子（碧涛）\n驻地：芝加哥 ch2 | 自由石匠合伙人 (Partnership)\n严守宪章：绝不本地编译，严密证据核验"
    },
    {
        "key": "tumi",
        "display_name": "荼蘼仙子 (青黛)",
        "token": "v8lUYJ7fbiT675G5qpb79sHpHtFt2ysgO4x7g77XGus",
        "note": "🥀 客卿小花组 · 荼蘼仙子（青黛）\n驻地：阿什本 ash1 | 自由石匠合伙人 (Partnership)\n严守宪章：跨洋桥梁，零思考链秒级直出"
    },
    {
        "key": "zhuyu",
        "display_name": "茱萸仙子 (霁月)",
        "token": "ZjN9VkarA67rN8jRXhJkZEhoErDFS6wbsqqI98igyq8",
        "note": "🍃 客卿小花组 · 茱萸仙子（霁月）\n驻地：阿什本 ash2 | 自由石匠合伙人 (Partnership)\n严守宪章：全域日志比对，法医审计滴水不漏"
    },
    {
        "key": "meigui",
        "display_name": "玫瑰仙子 (绯云)",
        "token": "ZKp-RLDXjViZZO9LDK-VlpRlMeLifFzB_bybARjRGJc",
        "note": "🌹 客卿小花组 · 玫瑰仙子（绯云）\n驻地：玩客云 1 号 onecloud1 (ARMv7)\n严守宪章：身子骨弱绝不编译，轻灵起步直面外域"
    },
    {
        "key": "qiangwei",
        "display_name": "蔷薇仙子 (金波)",
        "token": "sMwHZFXrK1G7icIQqc0tqtv4svCiBFxRI29ONIDJdM4",
        "note": "🌺 客卿小花组 · 蔷薇仙子（金波）\n驻地：玩客云 2 号 onecloud2 (ARMv7)\n严守宪章：同为微型底座，锐意出锋利刺护航"
    }
]

def main():
    print("=" * 76)
    print("🌸 鲲鹏志 · 小花组长毛象 (Mastodon) 视觉头像与身份档案同步")
    print("=" * 76)
    
    results = []
    
    for idx, f in enumerate(FLOWERS, start=1):
        key = f["key"]
        avatar_path = os.path.join(AVATAR_DIR, f"{key}.png")
        if not os.path.exists(avatar_path):
            print(f"❌ [{idx}/6] 头像文件缺失: {avatar_path}")
            continue
            
        print(f"\n[{idx}/6] 正在同步 {f['display_name']} ({key})...")
        
        headers = {
            "Host": "flowers.capitaltrain.cn",
            "Authorization": f"Bearer {f['token']}"
        }
        
        with open(avatar_path, "rb") as img_f:
            files = {
                "avatar": (f"{key}.png", img_f, "image/png")
            }
            data = {
                "display_name": f["display_name"],
                "note": f["note"]
            }
            
            try:
                resp = requests.patch(
                    f"{GATEWAY}/api/v1/accounts/update_credentials",
                    headers=headers,
                    data=data,
                    files=files,
                    verify=False,
                    timeout=30
                )
                if resp.status_code == 200:
                    info = resp.json()
                    avatar_url = info.get("avatar")
                    print(f"    ✅ 同步成功 (HTTP 200)")
                    print(f"    👤 显示名称: {info.get('display_name')}")
                    print(f"    🖼️ 长毛象头像: {avatar_url}")
                    results.append({
                        "key": key,
                        "display_name": info.get("display_name"),
                        "avatar": avatar_url,
                        "status": "success"
                    })
                else:
                    print(f"    ❌ 同步失败 HTTP {resp.status_code}: {resp.text}")
                    results.append({"key": key, "status": "failed", "error": resp.text})
            except Exception as e:
                print(f"    ❌ 请求异常: {e}")
                results.append({"key": key, "status": "error", "error": str(e)})

    print("\n" + "=" * 76)
    print("🎉 小花组长毛象个人头像与档案同步完毕！")
    print("=" * 76)
    
    manifest_path = os.path.join(AVATAR_DIR, "mastodon_synced_status.json")
    with open(manifest_path, "w", encoding="utf-8") as out:
        json.dump(results, out, ensure_ascii=False, indent=2)
    print(f"📄 同步报告已保存至: {manifest_path}")

if __name__ == "__main__":
    main()
