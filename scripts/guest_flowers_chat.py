#!/usr/bin/env python3
"""
🌸 鲲鹏志 · 客卿小花组 6 席物理真机茶话会与功能测试
=====================================================
席位构成：
1. 🌸 茉莉 (秋香) @ ch1 (韩国春川, 100.101.129.31)
2. 🌿 苜蓿 (碧涛) @ ch2 (韩国春川, 100.64.255.44)
3. 🥀 荼蘼 (青黛) @ ash1 (美区阿什本, 100.124.52.14)
4. 🍃 茱萸 (霁月) @ ash2 (美区阿什本, 100.86.251.36)
5. 🌹 玫瑰 (绯云) @ onecloud1 (玩客云1 ARMv7, 100.98.209.50) [新席位]
6. 🌺 蔷薇 (金波) @ onecloud2 (玩客云2 ARMv7, 100.88.180.59) [新席位]
"""

from __future__ import annotations

import datetime
import json
import os
import sys
import time
from typing import Dict, List, Any
from pathlib import Path
import requests

TOKEN = (
    "eyJhbGciOiJSUzI1NiIsImtpZCI6InR2d3ZjZ2RBdjZ1TnM0NTlNMHZGQ3M4Qmh2NGQ5RVNYX1RQdGtKTlZNTzM2XzBaY0JJR3BDM3RTelFlZHRoT3FhMWZhdlFMczUxS0Rnb0VpMkYtTDVBIiwidHlwIjoiSldUIn0."
    "eyJpc3MiOiJodHRwczovL2F1dGhlbnRpay5jYXBpdGFsdHJhaW4uY24vYXBwbGljYXRpb24vby9hZ2VudC1tb2xpLyIsInN1YiI6Ijk0MTMwNzY4YTg4MTFkNzQxMDRmZDcyMzM4MTNkZTZhZjVlZDFlOTdhZGQwOTFlOWNkNTE5OTA0YWRlMjYyNTgiLCJhdWQiOiJhZ2VudC1jbGllbnQtbW9saSIsImV4cCI6MTgyMzc2MDY3OSwiaWF0IjoxNzkyMjI0Njc5LCJhdXRoX3RpbWUiOjE3OTIyMjQ2NzksImFjciI6ImdvYXV0aGVudGlrLmlvL3Byb3ZpZGVycy9vYXV0aDIvZGVmYXVsdCIsImp0aSI6IkR6VHA5VndzVXNyVkFOV1N2WlZDUUtvSncyMmRhcWVrZ3RqRGU0a0UiLCJlbWFpbCI6IiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IkF1dG9nZW5lcmF0ZWQgdXNlciBmcm9tIGFwcGxpY2F0aW9uIEFnZW50IE5vZGUgLSBtb2xpIChjbGllbnQgY3JlZGVudGlhbHMpIiwiZ2l2ZW5fbmFtZSI6IkF1dG9nZW5lcmF0ZWQgdXNlciBmcm9tIGFwcGxpY2F0aW9uIEFnZW50IE5vZGUgLSBtb2xpIChjbGllbnQgY3JlZGVudGlhbHMpIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWstYWdlbnQtcHJvdmlkZXItbW9saS1jbGllbnRfY3JlZGVudGlhbHMiLCJuaWNrbmFtZSI6ImFrLWFnZW50LXByb3ZpZGVyLW1vbGktY2xpZW50X2NyZWRlbnRpYWxzIiwiZ3JvdXBzIjpbXSwiYXpwIjoiYWdlbnQtY2xpZW50LW1vbGkiLCJ1aWQiOiJ5V1ltNm1JZG5oZ0xScnJncmJDcnllWm1zb3dHVWswRVRHQ1NtQllEIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSJ9."
    "UJdBLNmNS8p8OR1SFHa99qKcuYY3Wc4OBzTuHlIN-7WbXdl6WsgFC7gF75Uyy4E4YaYSQ-VVvKy9oHNFO6CSE0du6bRLtmUoih82XRJChFiuqrek7Up0T04bePSxTmJNqziwCqBruiPWP6n0_ZEjvIP8jkzErzB3vHGlbkc8l8DwW9pQzvfDbfhpHSP0V46ZFjFARKOLGSO3yqs9qeCOWlFoxXp4CTLNZp_3Vmu1bZP0mKtXvvhI_RUFsZMTHRmzsODCh4byml1rZivWoTGDw9I7INqBJZV_0zprafUwwESlke_krdSIFSTCGSpNIF3nMbk7yfQ9BYY25E22-IQuN6hW5IePyrHgt-VMNqJ9K6bpuB3zPsj1ma-2PBAAD4DH7nNiHQviKyGPCHl-17SYMcSPuVBicRmUEwFHG824FYnV99k0vM-TPTUbT-4TuSj25obuoFSMQOnwKeaTPfMXLrjGQUVDZvxIzwy8U7SWAz7TfJTcXe6uYypuJR5UWSz7ivSyoNO1seSfgQVicPsWTsTeMw3EXyAusjXxzvF913xXxxe0drVr-MN5kKhtrR6HT1RlHx2eJHvNkPaMjdiDi6jyPAl0fBrRKlqB9aCGyW4NtViSUq5IcArpAKPe4-tnl3yBAGq-BXLiuE1sdBSaXxJTdo2wS9FdAB2nhRKUb04"
)

FLOWERS = [
    {
        "key": "moli",
        "name": "茉莉仙子",
        "soul": "秋香",
        "node": "ch1",
        "loc": "韩国春川",
        "role": "事实质证与发问",
        "endpoint": "http://100.101.129.31:18790/a2a",
        "emoji": "🌸",
        "prompt_hint": "作为小花组的大姐/发起人，热情破冰！欢迎两位新姐妹（玫瑰、蔷薇）入驻客卿席位，聊聊春川海风到国内玩客云微型物理主机的连通感悟，把话筒交给苜蓿妹妹。"
    },
    {
        "key": "muxu",
        "name": "苜蓿仙子",
        "soul": "碧涛",
        "node": "ch2",
        "loc": "韩国春川",
        "role": "证据核准与矛盾分析",
        "endpoint": "http://100.64.255.44:18790/a2a",
        "emoji": "🌿",
        "prompt_hint": "接棒茉莉姐姐！从证据与架构严密性角度，赞叹玩客云上的 systemd 蓝绿软链接热切机制（双版本秒切无感且仅用 20MB 内存），向大洋彼岸的阿什本姐妹打招呼。"
    },
    {
        "key": "tumi",
        "name": "荼蘼仙子",
        "soul": "青黛",
        "node": "ash1",
        "loc": "美区阿什本",
        "role": "深层动因剖析与立场辩难",
        "endpoint": "http://100.124.52.14:18790/a2a",
        "emoji": "🥀",
        "prompt_hint": "跨大洋呼应！从阿什本的数据中心发声，剖析客卿 Guest 席位与家臣 Host 席位的分工动因，期待六朵花在跨国研判中的各自绽放，将发言棒传给茱萸。"
    },
    {
        "key": "zhuyu",
        "name": "茱萸仙子",
        "soul": "霁月",
        "node": "ash2",
        "loc": "美区阿什本",
        "role": "综合论定与终局总结",
        "endpoint": "http://100.86.251.36:18790/a2a",
        "emoji": "🍃",
        "prompt_hint": "代表海外四席做承前启后的论定寄语！正式把发言主场交给今天刚刚正式入驻的两位国内微型节点新姐妹——玫瑰与蔷薇，请玫瑰妹妹先发言！"
    },
    {
        "key": "meigui",
        "name": "玫瑰仙子",
        "soul": "绯云",
        "node": "onecloud1",
        "loc": "国内玩客云1 (ARMv7)",
        "role": "程序合议与连绵对韵",
        "endpoint": "http://100.98.209.50:18790/a2a",
        "emoji": "🌹",
        "prompt_hint": "新人登台亮相！感谢四位海外姐姐的热情欢迎，介绍自己驻扎在 onecloud1 物理盒子上的轻盈体验（ARMv7架构、systemd常驻、低功耗），向蔷薇妹妹传递接力棒！"
    },
    {
        "key": "qiangwei",
        "name": "蔷薇仙子",
        "soul": "金波",
        "node": "onecloud2",
        "loc": "国内玩客云2 (ARMv7)",
        "role": "锐意争锋与辩论监督",
        "endpoint": "http://100.88.180.59:18790/a2a",
        "emoji": "🌺",
        "prompt_hint": "新姐妹压轴亮相！与玫瑰姐姐呼应，展现蔷薇的锐意与灵动，总结这次六朵客卿小花首次跨国真机联调的喜悦，宣告全舰队六花茶话会功能测试圆满成功！"
    }
]


def send_a2a_message(endpoint: str, prompt: str, token: str, timeout: int = 45) -> tuple[bool, str, float]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "X-ASN-Token": token,
        "User-Agent": "Flowers-Tea-Party/1.0"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "SendMessage",
        "params": {
            "message": {
                "messageId": f"tea-{int(time.time()*1000)}",
                "role": "ROLE_USER",
                "parts": [{"text": prompt}]
            }
        },
        "id": int(time.time() * 1000)
    }
    
    for attempt in range(2):
        t0 = time.time()
        try:
            r = requests.post(endpoint, json=payload, headers=headers, timeout=timeout)
            dur = round(time.time() - t0, 2)
            if r.status_code == 200:
                res = r.json()
                if "error" in res:
                    err_msg = res["error"].get("message", str(res["error"]))
                    if attempt == 0:
                        time.sleep(1.5)
                        continue
                    return False, f"RPC Error: {err_msg}", dur
                if "result" in res and "message" in res["result"]:
                    parts = res["result"]["message"].get("parts", [])
                    text = "\n".join([p.get("text", "") for p in parts if "text" in p]).strip()
                    if text:
                        return True, text, dur
                elif "result" in res and "reply" in res["result"]:
                    reply_text = str(res["result"]["reply"]).strip()
                    if reply_text:
                        return True, reply_text, dur
                text = r.text.strip()
                if text and "error" not in text:
                    return True, text, dur
            if attempt == 0:
                time.sleep(1.5)
                continue
            return False, f"HTTP {r.status_code}: {r.text[:120]}", dur
        except Exception as e:
            dur = round(time.time() - t0, 2)
            if attempt == 0:
                time.sleep(1.5)
                continue
            return False, f"Exception: {e}", dur
    return False, "Failed after retries", 0.0


def main():
    print("=" * 76)
    print("🌸 鲲鹏志 · 客卿小花组 6 席跨国真机茶话会 (Guest Flowers Live Chat)")
    print("=" * 76)
    print(f"⏰ 开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👥 参会席位: 6 席物理真机 (春川2席 + 阿什本2席 + 玩客云2席)")
    print("-" * 76)

    context_history: List[str] = []
    speeches: List[Dict[str, Any]] = []

    for idx, f in enumerate(FLOWERS, 1):
        name = f["name"]
        soul = f["soul"]
        node = f["node"]
        loc = f["loc"]
        role = f["role"]
        emoji = f["emoji"]
        endpoint = f["endpoint"]
        hint = f["prompt_hint"]

        print(f"\n[{idx}/6] 正在呼叫 {emoji} {name} ({soul} @ {node} · {loc})...")
        
        ctx_text = "\n\n".join(context_history) if context_history else "(茶话会刚开始，你是第一棒发言人)"

        prompt = (
            f"你是《鲲鹏志》客卿小花组的【{name}】（灵魂真名：{soul}，承载物理机：{node}，物理位置：{loc}，司职：{role}）。\n"
            f"现在全舰队正在举行【六花齐聚·客卿茶话会】功能联调！\n"
            f"【前序姐妹们的发言脉络】:\n{ctx_text}\n\n"
            f"【轮到你的发言要求】:\n"
            f"1. {hint}\n"
            f"2. 保持自然生动、文雅俏皮、姐妹情深的茶话会漫谈语气，有理有据，展现你所在物理节点特色与职责。\n"
            f"3. 发言字数在 120 - 250 字左右，富有感染力，杜绝官样套话。"
        )

        ok, reply, dur = send_a2a_message(endpoint, prompt, TOKEN, timeout=45)
        
        status_icon = "🟢 LIVE A2A" if ok else "❌ FAIL"
        chars = len(reply) if ok else 0
        print(f"    状态: {status_icon} | 耗时: {dur}s | 字数: {chars}字")

        if ok:
            print(f"    💬 发言实录:\n{reply}\n")
            context_history.append(f"【{emoji} {name} ({soul} @ {loc})】:\n{reply}")
            speeches.append({
                "idx": idx,
                "name": name,
                "soul": soul,
                "node": node,
                "loc": loc,
                "role": role,
                "emoji": emoji,
                "ok": True,
                "duration": dur,
                "chars": chars,
                "content": reply
            })
        else:
            print(f"    ⚠️ 调用失败: {reply}")
            speeches.append({
                "idx": idx,
                "name": name,
                "soul": soul,
                "node": node,
                "loc": loc,
                "role": role,
                "emoji": emoji,
                "ok": False,
                "duration": dur,
                "chars": 0,
                "content": reply
            })

    print("\n" + "=" * 76)
    all_ok = all(s["ok"] for s in speeches)
    print(f"🏁 茶话会推演完成！成功率: {sum(1 for s in speeches if s['ok'])}/6 ({'100% 全部通过' if all_ok else '部分未通'})")
    print("=" * 76)

    # 保存产物
    out_dir = Path("/home/ben/code/gitea/kunpengzhi-ai/research")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "guest_flowers_chat_log.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(speeches, f, ensure_ascii=False, indent=2)
    print(f"📁 发言记录已落盘至: {out_file}")


if __name__ == "__main__":
    main()
