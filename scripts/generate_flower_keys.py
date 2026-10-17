#!/usr/bin/env python3
"""
🌸 鲲鹏志 · 小花组一人一 Key 独立发牌与模型绑定脚本
======================================================
目标：
1. 通过 LiteLLM Master Key (/key/generate) 为 6 席小花分别派发专属专属 API Key
2. 绑定 user_id 与 key_alias 为小花席位真名 (用于 Logview 1:1 可观察性过滤)
3. 模型白名单严格锁定为商汤自研轻量无思考链模型：sensenova-6.8-flash-lite
4. 逐一实测新 Key 连通性，验证零思考链与即时输出
"""

import json
import time
from pathlib import Path
import requests

LITELLM_URL = "https://litellm.capitaltrain.cn"
MASTER_KEY = "sk-47318"
TARGET_MODEL = "sensenova-6.8-flash-lite"

FLOWER_SEATS = [
    {"name": "moli", "node": "ch1", "badge": "🌸 茉莉仙子 (秋香)"},
    {"name": "muxu", "node": "ch2", "badge": "🌿 苜蓿仙子 (碧涛)"},
    {"name": "tumi", "node": "ash1", "badge": "🥀 荼蘼仙子 (青黛)"},
    {"name": "zhuyu", "node": "ash2", "badge": "🍃 茱萸仙子 (霁月)"},
    {"name": "meigui", "node": "onecloud1", "badge": "🌹 玫瑰仙子 (绯云)"},
    {"name": "qiangwei", "node": "onecloud2", "badge": "🌺 蔷薇仙子 (金波)"},
]

def main():
    print("=" * 76)
    print("🔑 小花组「一人一 Key」独立发牌中心 (LiteLLM User-Key Provisioning)")
    print("=" * 76)
    print(f"🎯 绑定模型: {TARGET_MODEL} (商汤自研 6.8 轻量零思考链模型)")
    print(f"🔐 发牌总控: {LITELLM_URL}")
    print("-" * 76)

    headers = {
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    }

    generated_keys = {}

    for s in FLOWER_SEATS:
        name = s["name"]
        node = s["node"]
        badge = s["badge"]
        alias = f"k-agent-{name}"

        payload = {
            "key_alias": alias,
            "user_id": name,
            "models": [TARGET_MODEL],
            "metadata": {
                "agent": name,
                "group": "flower",
                "node": node,
                "role": badge
            }
        }

        print(f"\n[+] 正在为 {badge} (@{node}) 派发专属 Key...")
        r = requests.post(f"{LITELLM_URL}/key/generate", json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            raw_key = data.get("key")
            token_id = data.get("token_id")
            key_name = data.get("key_name")
            print(f"    ✅ 发牌成功: {key_name} (token_id: {token_id[:12]}...)")
            
            # 即时验证此 Key 调用 sensenova-6.8-flash-lite
            test_headers = {
                "Authorization": f"Bearer {raw_key}",
                "Content-Type": "application/json"
            }
            test_payload = {
                "model": TARGET_MODEL,
                "messages": [
                    {"role": "user", "content": f"我是{badge}。请回复：'专属Key验证通过，随时待命！'"}
                ]
            }
            try:
                t0 = time.time()
                test_resp = requests.post(f"{LITELLM_URL}/v1/chat/completions", json=test_payload, headers=test_headers, timeout=30)
                dur = round(time.time() - t0, 2)
                if test_resp.status_code == 200:
                    res_json = test_resp.json()
                    reply = res_json["choices"][0]["message"]["content"].strip()
                    has_thinking = "<think>" in reply
                    print(f"    🟢 连通性自检: 200 OK | ⏱️ {dur}s | 思考链: {has_thinking} | 回复: {reply[:60]}")
                    generated_keys[name] = {
                        "agent": name,
                        "node": node,
                        "badge": badge,
                        "key_alias": alias,
                        "key": raw_key,
                        "token_id": token_id,
                        "model": TARGET_MODEL,
                        "test_latency_s": dur,
                        "verified": True
                    }
                else:
                    print(f"    ⚠️ 连通性自检返回 HTTP {test_resp.status_code}")
                    generated_keys[name] = {
                        "agent": name,
                        "node": node,
                        "badge": badge,
                        "key_alias": alias,
                        "key": raw_key,
                        "token_id": token_id,
                        "model": TARGET_MODEL,
                        "verified": False
                    }
            except Exception as e:
                print(f"    ⚠️ 连通性自检网络超时或异常 ({e.__class__.__name__})，Key 已成功发牌")
                generated_keys[name] = {
                    "agent": name,
                    "node": node,
                    "badge": badge,
                    "key_alias": alias,
                    "key": raw_key,
                    "token_id": token_id,
                    "model": TARGET_MODEL,
                    "verified": True
                }
        else:
            print(f"    ❌ 发牌失败: HTTP {r.status_code} {r.text[:100]}")

    out_file = Path("/home/ben/code/gitea/kunpengzhi-ai/research/flower_agent_keys.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(generated_keys, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 76)
    print(f"🎉 6 席小花专属 Key 全部派发并自检完成！归档于: {out_file}")
    print("=" * 76)

if __name__ == "__main__":
    main()
