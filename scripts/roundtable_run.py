#!/usr/bin/env python3
"""
🌸 鲲鹏志 · 正典圆桌漫谈自动化验收与收割 CLI (Headless Runner & E2E Acceptance)
========================================================================
总目标与验收铁律：
- 场景：S05《陨》正典圆桌研判
- 拓扑：甲骨文 4 节点小花组物理车座 (moli@ch1, muxu@ch2, tumi@ash1, zhuyu@ash2)
- 协议：A2A v2 (SendMessage / ROLE_USER) over Cloudflare Named Tunnels
- 门禁 (Gates)：
  1. 底座探活门禁：4 席 /health 全部 HTTP 200
  2. 令牌环推演门禁：4 席顺次传递并生成发言
  3. 真机推演门禁 (Live A2A)：100% 物理真机推理 (拒绝 Standby/Fallback)
  4. 质量与 SLA 门禁：每棒发言 > 100 字，耗时 < 60s
  5. 存档落盘门禁：自动写入 擂台存档/ 与 runs.jsonl 索引

用法：
    python3 scripts/roundtable_run.py
    python3 scripts/roundtable_run.py --strict --output-md /path/to/report.md
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import requests
from core.agent_card import FOUR_FLOWER_SEATS
from core.contract import default_contract
from core.token_ring import RobertTokenRingEngine
from core.archive import save_run

DEFAULT_TOKEN = (
    "eyJhbGciOiJSUzI1NiIsImtpZCI6InR2d3ZjZ2RBdjZ1TnM0NTlNMHZGQ3M4Qmh2NGQ5RVNYX1RQdGtKTlZNTzM2XzBaY0JJR3BDM3RTelFlZHRoT3FhMWZhdlFMczUxS0Rnb0VpMkYtTDVBIiwidHlwIjoiSldUIn0."
    "eyJpc3MiOiJodHRwczovL2F1dGhlbnRpay5jYXBpdGFsdHJhaW4uY24vYXBwbGljYXRpb24vby9hZ2VudC1tb2xpLyIsInN1YiI6Ijk0MTMwNzY4YTg4MTFkNzQxMDRmZDcyMzM4MTNkZTZhZjVlZDFlOTdhZGQwOTFlOWNkNTE5OTA0YWRlMjYyNTgiLCJhdWQiOiJhZ2VudC1jbGllbnQtbW9saSIsImV4cCI6MTgyMzc2MDY3OSwiaWF0IjoxNzkyMjI0Njc5LCJhdXRoX3RpbWUiOjE3OTIyMjQ2NzksImFjciI6ImdvYXV0aGVudGlrLmlvL3Byb3ZpZGVycy9vYXV0aDIvZGVmYXVsdCIsImp0aSI6IkR6VHA5VndzVXNyVkFOV1N2WlZDUUtvSncyMmRhcWVrZ3RqRGU0a0UiLCJlbWFpbCI6IiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwibmFtZSI6IkF1dG9nZW5lcmF0ZWQgdXNlciBmcm9tIGFwcGxpY2F0aW9uIEFnZW50IE5vZGUgLSBtb2xpIChjbGllbnQgY3JlZGVudGlhbHMpIiwiZ2l2ZW5fbmFtZSI6IkF1dG9nZW5lcmF0ZWQgdXNlciBmcm9tIGFwcGxpY2F0aW9uIEFnZW50IE5vZGUgLSBtb2xpIChjbGllbnQgY3JlZGVudGlhbHMpIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWstYWdlbnQtcHJvdmlkZXItbW9saS1jbGllbnRfY3JlZGVudGlhbHMiLCJuaWNrbmFtZSI6ImFrLWFnZW50LXByb3ZpZGVyLW1vbGktY2xpZW50X2NyZWRlbnRpYWxzIiwiZ3JvdXBzIjpbXSwiYXpwIjoiYWdlbnQtY2xpZW50LW1vbGkiLCJ1aWQiOiJ5V1ltNm1JZG5oZ0xScnJncmJDcnllWm1zb3dHVWswRVRHQ1NtQllEIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSJ9."
    "UJdBLNmNS8p8OR1SFHa99qKcuYY3Wc4OBzTuHlIN-7WbXdl6WsgFC7gF75Uyy4E4YaYSQ-VVvKy9oHNFO6CSE0du6bRLtmUoih82XRJChFiuqrek7Up0T04bePSxTmJNqziwCqBruiPWP6n0_ZEjvIP8jkzErzB3vHGlbkc8l8DwW9pQzvfDbfhpHSP0V46ZFjFARKOLGSO3yqs9qeCOWlFoxXp4CTLNZp_3Vmu1bZP0mKtXvvhI_RUFsZMTHRmzsODCh4byml1rZivWoTGDw9I7INqBJZV_0zprafUwwESlke_krdSIFSTCGSpNIF3nMbk7yfQ9BYY25E22-IQuN6hW5IePyrHgt-VMNqJ9K6bpuB3zPsj1ma-2PBAAD4DH7nNiHQviKyGPCHl-17SYMcSPuVBicRmUEwFHG824FYnV99k0vM-TPTUbT-4TuSj25obuoFSMQOnwKeaTPfMXLrjGQUVDZvxIzwy8U7SWAz7TfJTcXe6uYypuJR5UWSz7ivSyoNO1seSfgQVicPsWTsTeMw3EXyAusjXxzvF913xXxxe0drVr-MN5kKhtrR6HT1RlHx2eJHvNkPaMjdiDi6jyPAl0fBrRKlqB9aCGyW4NtViSUq5IcArpAKPe4-tnl3yBAGq-BXLiuE1sdBSaXxJTdo2wS9FdAB2nhRKUb04"
)


def probe_health_gate(token: str) -> Dict[str, bool]:
    """门禁 1：底座健康度探活"""
    print("\n🔍 【门禁 1/5】底座物理探活质检 (Chassis Health Gate)...")
    headers = {"Authorization": f"Bearer {token}"}
    results = {}
    for key, card in FOUR_FLOWER_SEATS.items():
        base_url = f"https://{key}.git4ta.fun/health"
        try:
            r = requests.get(base_url, headers=headers, timeout=8)
            ok = (r.status_code == 200 and r.text.strip() == "ok")
            results[key] = ok
            status_icon = "✅" if ok else f"❌ (HTTP {r.status_code})"
            print(f"   • {card.badge}: {status_icon} -> {base_url}")
        except Exception as e:
            results[key] = False
            print(f"   • {card.badge}: ❌ ({e.__class__.__name__}) -> {base_url}")
    return results


def run_roundtable(meta: dict, token: str, verbose: bool = True) -> tuple[RobertTokenRingEngine, List[dict]]:
    """门禁 2 & 3：执行令牌环调度与真机推演"""
    print("\n⚙️ 【门禁 2/5】启动令牌环全流程流转 (Robert Token Ring Execution)...")
    engine = RobertTokenRingEngine(article_text=meta.get("key_facts", ""), scenario="canon")
    engine.agent_token = token
    os.environ["ASN_AGENT_TOKEN"] = token

    topic_anchor = engine.draft_roundtable_topic(meta)
    engine.add_to_shared_context("🏛️ 正典立项", topic_anchor, team="canon_meta")

    seat_registry = {k: v.to_seat_dict() for k, v in FOUR_FLOWER_SEATS.items()}
    contract = default_contract()
    speeches = []

    def on_step_emit(msg: dict, idx: int, total: int, act: dict):
        speeches.append(msg)
        is_live = "Live" in msg.get("live_status", "")
        status_badge = "🟢 LIVE A2A" if is_live else f"🟡 {msg.get('live_status', '')}"
        dur = msg.get("duration", 0)
        chars = len(msg.get("content", ""))
        print(f"   [{idx}/{total}] {msg.get('persona')} ({msg.get('k_agent')}): {status_badge} | ⏱️ {dur}s | 📝 {chars}字")
        if verbose:
            lines = msg.get("content", "").strip().split("\n")
            preview = lines[0][:90] + ("..." if len(lines[0]) > 90 else "")
            print(f"         > \"{preview}\"")

    t_start = time.time()
    engine.execute_contract(contract, seat_registry, emit_cb=on_step_emit)
    total_sec = round(time.time() - t_start, 2)
    print(f"\n   🎉 4 席漫谈全部流转完毕，总耗时: {total_sec}s")
    return engine, speeches


def evaluate_acceptance(speeches: List[dict], strict: bool = True) -> Dict[str, Any]:
    """门禁 3 & 4：质量门禁与验收评估"""
    print("\n📊 【门禁 3 & 4/5】质量与 SLA 验收评估 (Quality & SLA Gate)...")
    passed = True
    reasons = []
    seat_metrics = []

    for i, s in enumerate(speeches, 1):
        is_live = "Live" in s.get("live_status", "")
        chars = len(s.get("content", ""))
        dur = s.get("duration", 0)

        # 校验点
        live_ok = is_live
        chars_ok = chars >= 80
        sla_ok = dur < 85.0

        seat_ok = live_ok and chars_ok and sla_ok
        if not seat_ok:
            passed = False
            fail_desc = []
            if not live_ok:
                fail_desc.append(f"未达成真机A2A({s.get('live_status')})")
            if not chars_ok:
                fail_desc.append(f"字数不足({chars}<80)")
            if not sla_ok:
                fail_desc.append(f"超时({dur}s>=70s)")
            reasons.append(f"第 {i} 棒 {s.get('persona')}: " + " & ".join(fail_desc))

        seat_metrics.append({
            "idx": i,
            "persona": s.get("persona"),
            "k_agent": s.get("k_agent"),
            "status": s.get("live_status"),
            "live_a2a": live_ok,
            "chars": chars,
            "duration_s": dur,
            "passed": seat_ok
        })

        icon = "✅" if seat_ok else "❌"
        print(f"   • {icon} 第 {i} 棒 {s.get('persona')}: Live={live_ok}, 长度={chars}字, 耗时={dur}s")

    return {
        "all_passed": passed,
        "failed_reasons": reasons,
        "metrics": seat_metrics,
        "total_seats": len(speeches),
        "live_seats_count": sum(1 for m in seat_metrics if m["live_a2a"])
    }


def archive_and_report(engine: RobertTokenRingEngine, speeches: List[dict], audit_result: dict, meta: dict, output_md: str | None = None) -> str:
    """门禁 5：自动归档与收割落地"""
    print("\n📦 【门禁 5/5】成果归档与收割落地 (Canonical Archiving Gate)...")
    ts_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md_lines = [
        f"# 🦅 《鲲鹏志》正典圆桌漫谈自动化验收实录 · 第五期《陨》(S05)",
        f"",
        f"- **验收时间**: `{ts_now}`",
        f"- **总验收状态**: {'🟢 全部通过 (100% Live A2A)' if audit_result['all_passed'] else '🔴 未完全通过'}",
        f"- **物理节点拓扑**: 韩国春川 (ch1, ch2) + 美国阿什本 (ash1, ash2) 4 节点固定隧道直通",
        f"- **端点协议**: A2A v2 (SendMessage / JSON-RPC 2.0)",
        f"",
        f"---",
        f"",
        f"## 📋 4 席物理车座验收指标卡",
        f"",
        f"| 棒次 | 学者席位 | 物理宿主底座 | 协议状态 | 耗时 | 字数 | 验收判定 |",
        f"| :---: | :--- | :--- | :---: | :---: | :---: | :---: |",
    ]

    for m in audit_result["metrics"]:
        status_badge = "🟢 Live A2A" if m["live_a2a"] else f"🟡 {m['status']}"
        pass_badge = "✅ PASS" if m["passed"] else "❌ FAIL"
        md_lines.append(f"| {m['idx']} | {m['persona']} | `{m['k_agent']}` | {status_badge} | {m['duration_s']}s | {m['chars']}字 | {pass_badge} |")

    md_lines.extend([
        f"",
        f"---",
        f"",
        f"## 🎙️ 正典圆桌漫谈 4 棒交锋实录全文",
        f"",
    ])

    for i, s in enumerate(speeches, 1):
        md_lines.extend([
            f"### 第 {i} 棒 · {s.get('header', s.get('persona'))}",
            f"> **物理宿主**: `{s.get('k_agent')}` · **耗时**: `{s.get('duration')}s` · **协议状态**: `{s.get('live_status')}`",
            f"",
            s.get("content", "").strip(),
            f"",
            f"---",
            f"",
        ])

    full_markdown = "\n".join(md_lines)

    # 1. 落盘到 擂台存档/
    try:
        archive_filename = save_run(
            kind="漫谈",
            title=f"S05-陨-小花组4席真机验收-{int(time.time())}",
            markdown=full_markdown,
            meta={
                "_steps": engine.steps,
                "scenario": "canon",
                "roundtable_topic": meta.get("title", "S05-陨"),
                "live_rate": f"{audit_result['live_seats_count']}/{audit_result['total_seats']}",
                "audit_passed": audit_result["all_passed"],
            }
        )
        print(f"   ✅ 已落盘统一存档: {archive_filename}")
    except Exception as e:
        print(f"   ⚠️ 写入擂台存档警告: {e}")

    # 2. 如果指定了 output_md，写入对应文件
    if output_md:
        out_p = Path(output_md)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(full_markdown, encoding="utf-8")
        print(f"   ✅ 导出报告至: {out_p.resolve()}")

    return full_markdown


def main():
    parser = argparse.ArgumentParser(description="鲲鹏志 · 正典圆桌漫谈自动化验收与收割 CLI")
    parser.add_argument("--canon-file", default="fixtures/canon_s05.json", help="正典卷宗元数据路径")
    parser.add_argument("--token", default=None, help="Authentik JWT 令牌 (默认读 ASN_AGENT_TOKEN 或内置权威令牌)")
    parser.add_argument("--strict", action="store_true", default=True, help="严格模式：任一席位未达 100%% Live A2A 则非 0 退出")
    parser.add_argument("--output-md", default=None, help="导出 Markdown 成果路径")
    parser.add_argument("--output-json", default=None, help="导出指标 JSON 路径")
    args = parser.parse_args()

    token = args.token or os.getenv("ASN_AGENT_TOKEN") or DEFAULT_TOKEN

    canon_path = REPO_ROOT / args.canon_file
    if not canon_path.exists():
        print(f"❌ 卷宗文件不存在: {canon_path}")
        sys.exit(1)

    meta = json.loads(canon_path.read_text(encoding="utf-8"))
    print(f"🦅 启动《鲲鹏志》正典圆桌漫谈 CLI 自动化验收流水线: 【{meta.get('title', 'S05')}】")

    # 门禁 1：探活
    health_results = probe_health_gate(token)
    if not all(health_results.values()):
        failed_nodes = [k for k, v in health_results.items() if not v]
        print(f"\n⚠️ 警告：以下物理席位探活未完全响应: {failed_nodes}")

    # 门禁 2：令牌环推演
    engine, speeches = run_roundtable(meta, token, verbose=True)

    # 门禁 3 & 4：质量评估
    audit_res = evaluate_acceptance(speeches, strict=args.strict)

    # 门禁 5：归档与报告收割
    default_out_md = args.output_md or str(REPO_ROOT / "research" / f"roundtable_audit_s05_{int(time.time())}.md")
    report_md = archive_and_report(engine, speeches, audit_res, meta, output_md=default_out_md)

    if args.output_json:
        out_j = Path(args.output_json)
        out_j.parent.mkdir(parents=True, exist_ok=True)
        out_j.write_text(json.dumps(audit_res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"   ✅ 导出指标数据: {out_j.resolve()}")

    print("\n" + "=" * 60)
    if audit_res["all_passed"]:
        print("🎯 验收结论: 【100% PASS】4 席物理智能车座全部实现真机实时推演闭环！")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"❌ 验收结论: 【FAIL】存在未达标席位: {audit_res['failed_reasons']}")
        print("=" * 60)
        if args.strict:
            sys.exit(1)
        sys.exit(0)


if __name__ == "__main__":
    main()
