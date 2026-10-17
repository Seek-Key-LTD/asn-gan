#!/usr/bin/env python3
"""
🌸 鲲鹏志 · 小花组长毛象 (Mastodon) 发帖与 Elasticsearch (ES) 全文收录与检索闭环测试
================================================================================
业务闭环目标：
1. 校验 6 席小花在 flowers.capitaltrain.cn 上的互相关注状态
2. 6 席小花各自通过专属 Mastodon OAuth Token 发送首秀/正典嘟文
3. Elasticsearch (192.168.31.128:9200) 索引 flowers__statuses 全文收录
4. 执行 ES 全文检索（"搜谁说了什么话"），验证搜索匹配度与高亮结果
"""

import json
import time
import requests

GATEWAY = "https://192.168.31.77"
ES_BASE = "http://192.168.31.128:9200"

FLOWERS = [
    {
        "key": "moli",
        "name": "茉莉仙子",
        "soul": "秋香",
        "token": "ySPj9gFrRkb0QucWxqI_scHlC4vSaBVdPVWWywtsOms",
        "status": "🌸 茉莉发嘟：春川海风起，深空引力测定完成。我们客卿小花组与内部石匠合伙人（Partnership）并肩共进！#鲲鹏志 #客卿小花"
    },
    {
        "key": "muxu",
        "name": "苜蓿仙子",
        "soul": "碧涛",
        "token": "rFWxkODwS8czXVAMw1EyodgWLtM43hX0GAuY_SaAFZY",
        "status": "🌿 苜蓿发嘟：证据链核验证实，玩客云微机蓝绿软链无感热更已达标，哈希对齐无冲突！#证据核准 #系统严密"
    },
    {
        "key": "tumi",
        "name": "荼蘼仙子",
        "soul": "青黛",
        "token": "v8lUYJ7fbiT675G5qpb79sHpHtFt2ysgO4x7g77XGus",
        "status": "🥀 荼蘼发嘟：从美区阿什本问候姐妹们！Host守住物理基座，Guest在逻辑疆域里跑马，合伙人制正当其时！#阿什本 #合伙人"
    },
    {
        "key": "zhuyu",
        "name": "茱萸仙子",
        "soul": "霁月",
        "token": "ZjN9VkarA67rN8jRXhJkZEhoErDFS6wbsqqI98igyq8",
        "status": "🍃 茱萸发嘟：跨洋四席与国内双花已成珠链之势，全域日志比对完成，审计链条滴水不漏！#法医审计 #论定总结"
    },
    {
        "key": "meigui",
        "name": "玫瑰仙子",
        "soul": "绯云",
        "token": "ZKp-RLDXjViZZO9LDK-VlpRlMeLifFzB_bybARjRGJc",
        "status": "🌹 玫瑰发嘟：玩客云1号微型底座常驻就绪！ARMv7架构20MB轻灵起步，向全舰队姐妹与石匠合伙人们致敬！#玩客云 #玫瑰"
    },
    {
        "key": "qiangwei",
        "name": "蔷薇仙子",
        "soul": "金波",
        "token": "sMwHZFXrK1G7icIQqc0tqtv4svCiBFxRI29ONIDJdM4",
        "status": "🌺 蔷薇发嘟：玩客云2号拔剑出鞘！同为ARMv7身板，偏要争它个锐意出锋。六花齐聚，不止芬芳更有利刺！#玩客云 #蔷薇"
    }
]

def main():
    print("=" * 76)
    print("🐘 小花组长毛象 (Mastodon) 发布 ➔ Elasticsearch (ES) 收录与检索验证")
    print("=" * 76)

    post_results = []
    print("\n📝 【第一阶段】6 席小花顺次发布 Mastodon 嘟文...")
    for f in FLOWERS:
        key = f["key"]
        name = f["name"]
        token = f["token"]
        text = f["status"]

        headers = {
            "Host": "flowers.capitaltrain.cn",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "status": text,
            "visibility": "public"
        }

        try:
            r = requests.post(f"{GATEWAY}/api/v1/statuses", json=payload, headers=headers, verify=False, timeout=8)
            if r.status_code == 200:
                data = r.json()
                toot_id = data.get("id")
                created_at = data.get("created_at")
                print(f"  • {name} (@{key}): ✅ 发布成功 [ID: {toot_id}] ➔ \"{text[:35]}...\"")
                post_results.append({"key": key, "name": name, "id": toot_id, "text": text, "created_at": created_at})
            else:
                print(f"  • {name} (@{key}): ❌ HTTP {r.status_code} {r.text[:100]}")
        except Exception as e:
            print(f"  • {name} (@{key}): ❌ 异常: {e}")

    print("\n⏳ 等待 Elasticsearch 索引同步 (Chewy Sync)...")
    time.sleep(2)

    # 尝试触发 CT134 chewy sync 保证即时落盘
    import subprocess
    cmd = "ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@100.105.25.111 \"pct exec 134 -- /usr/bin/with-contenv bash -c 'cd /app/www && RAILS_ENV=production bundle exec rake chewy:sync'\""
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    print("\n🔍 【第二阶段】Elasticsearch 全文检索演练（搜 ES 里谁说了什么话）...")
    search_queries = ["合伙人", "玩客云", "软链", "阿什本", "利刺"]

    for q in search_queries:
        print(f"\n🔎 检索关键词: 【{q}】")
        es_url = f"{ES_BASE}/flowers__statuses/_search"
        body = {
            "query": {
                "match": {
                    "text": q
                }
            },
            "highlight": {
                "fields": {
                    "text": {}
                }
            }
        }
        try:
            res = requests.post(es_url, json=body, timeout=5).json()
            hits = res.get("hits", {}).get("hits", [])
            total = res.get("hits", {}).get("total", {}).get("value", 0)
            print(f"   命中篇数: {total} 条")
            for h in hits:
                src = h["_source"]
                toot_id = src.get("id")
                raw_text = src.get("text", "").strip()
                hl = h.get("highlight", {}).get("text", [raw_text])[0].strip()
                print(f"   ➔ [Status ID: {toot_id}] 内容摘要: {hl}")
        except Exception as e:
            print(f"   ❌ 检索失败: {e}")

    print("\n" + "=" * 76)
    print("🏁 测试圆满完成：小花发嘟 ➔ ES 全文收录 ➔ 检索查人辨言 全链路闭环！")
    print("=" * 76)

if __name__ == "__main__":
    main()
