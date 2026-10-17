"""
Session Contract — 4 席小花组（甲骨文 4 节点）K-Agent 对抗讨论契约规范
====================================================================
极简架构：
- 4 席物理 Agent（Single Source of Truth）：
    1. moli  (🌸 茉莉 @ ch1 韩国春川)  — 事实质证与发问
    2. muxu  (🌿 苜蓿 @ ch2 韩国春川)  — 证据核准与矛盾分析
    3. tumi  (🥀 荼蘼 @ ash1 美国阿什本) — 深层动因剖析与立场辩难
    4. zhuyu (🍃 茱萸 @ ash2 美国阿什本) — 综合论定与终局总结
- 4 阶段对抗流程（4 Acts）：
    Stage 1: 事实首发质证 (moli)
    Stage 2: 证据链核准 (muxu)
    Stage 3: 动机与边界辩难 (tumi)
    Stage 4: 终局合议论定 (zhuyu)
"""
from __future__ import annotations

# 4 席小花组法定白名单
SEAT_WHITELIST = {"moli", "muxu", "tumi", "zhuyu"}
STAGE_COUNT = 4


def default_stage_flow() -> list[dict]:
    """小花组 4 席对抗讨论标准阶段流"""
    return [
        {"id": 1, "name": "1. 事实质证与首发立论", "emoji": "🌸", "desc": "茉莉仙子 (moli@ch1) 调取案件首发事实，质证核心焦点与资金往来前提"},
        {"id": 2, "name": "2. 证据核准与矛盾分析", "emoji": "🌿", "desc": "苜蓿仙子 (muxu@ch2) 逐笔比对时间序与客观书证，排查指控中的逻辑断层"},
        {"id": 3, "name": "3. 动因剖析与立场辩难", "emoji": "🥀", "desc": "荼蘼仙子 (tumi@ash1) 深入探究公职背景与民间亲友互助的法理与伦理冲突"},
        {"id": 4, "name": "4. 综合论定与终局总结", "emoji": "🍃", "desc": "茱萸仙子 (zhuyu@ash2) 统筹四席合议观点，依照罪刑法定原则给出终局裁断"},
    ]


def default_cast() -> list[dict]:
    """小花组 4 席位映射"""
    return [
        {"seat": "moli",  "archetype": "investigator", "role": "事实质证席", "team": "flower", "node": "ch1"},
        {"seat": "muxu",  "archetype": "verifier",     "role": "证据核准席", "team": "flower", "node": "ch2"},
        {"seat": "tumi",  "archetype": "debater",      "role": "辩难分析席", "team": "flower", "node": "ash1"},
        {"seat": "zhuyu", "archetype": "arbiter",      "role": "综合论定席", "team": "flower", "node": "ash2"},
    ]


def default_contract() -> dict:
    """内置《极昼》4 席小花组极简讨论契约"""
    return {
        "protocol": "flower_quad_debate",
        "meta": {
            "title": "极昼",
            "source_type": "留置案讨论",
            "defendant": "尊长",
            "charge": "民间借贷过桥、职务影响与失职犯罪边界争议",
            "court_name": "安徽省阜阳市中级人民法院",
            "case_number": "极昼留置专案研判",
            "key_facts": "2016年尊长筹措1000万资金过桥划转亲友企业救急，后分10次平价全额还本，中煤资产无实际亏空；2026年被留置审查。",
            "prosecution_claim": "是否构成利用特定职务影响力隐形背书或规避合规监管？",
            "defense_claim": "资金链闭环全额归还、零利差无自肥、客观零亏空，符合法无明文规定不为罪。",
            "focus": "区分公职行为与民间正常救急；职务隐性影响的认定红线与刑法谦抑性。",
        },
        "stage_flow": default_stage_flow(),
        "cast": default_cast(),
        "acts": [
            {
                "stage": 1,
                "seat": "moli",
                "instruction": "【第一轮 · 事实质证】作为 ch1 事实质证席，调取全案资金流水首发证据。针对所谓利用职务借道过桥的指控，直接质证资金借入与归还的完整商业借据凭据，明确区分正常救急过桥与权钱交易对价！"
            },
            {
                "stage": 2,
                "seat": "muxu",
                "instruction": "【第二轮 · 证据核准】作为 ch2 证据核准席，正面接续茉莉仙子提出的质证疑点。重点比对还款时间序与行政审批节点，指出行政审批发生时借贷早已平价归还的时间错位，核准是否存在客观财产损失！"
            },
            {
                "stage": 3,
                "seat": "tumi",
                "instruction": "【第三轮 · 动因辩难】作为 ash1 辩难立论席，切入最深层法理与伦理冲突。正面回答前两席关于流水完备性的论述，同时剖析公职人员身份对亲友企业获得的隐性信誉背书，论证民间借贷司法保护界限！"
            },
            {
                "stage": 4,
                "seat": "zhuyu",
                "instruction": "【第四轮 · 终局论定】作为 ash2 综合论定席，收束前三席关于事实、证据链与动因辩难的合议结论。逐项检验定罪构成要件，坚持疑罪从无与刑法谦抑原则，给出终局合议意见！"
            },
        ],
        "constraints": {"max_speech_chars": 350, "tone": "严谨、深刻、直击要害"},
        "token_policy": "fixed_order",
    }


def validate_contract(contract: dict) -> tuple[bool, list[str]]:
    """确定性契约校验"""
    problems = []
    if not isinstance(contract, dict):
        return False, ["契约不是合法字典对象"]
    acts = contract.get("acts") or []
    stages = contract.get("stage_flow") or []

    if len(stages) != STAGE_COUNT:
        problems.append(f"阶段数应为 {STAGE_COUNT}，实为 {len(stages)}")

    if not acts:
        problems.append("acts 为空——缺少发言序列")

    for idx, a in enumerate(acts):
        seat = a.get("seat")
        if seat not in SEAT_WHITELIST:
            problems.append(f"acts[{idx}] seat={seat} 不在小花组白名单")
        if not (a.get("instruction") or "").strip():
            problems.append(f"acts[{idx}] 指令为空")

    return (len(problems) == 0), problems


def summarize_contract(contract: dict) -> str:
    """契约摘要说明"""
    meta = contract.get("meta", {})
    stages = contract.get("stage_flow", [])
    acts = contract.get("acts", [])
    return (
        f"🌸 协议：4 席小花组对抗讨论 ({contract.get('protocol')})\n"
        f"📖 议题：{meta.get('title', '极昼')}\n"
        f"🎯 争点：{meta.get('focus', '事实与法律边界')}\n"
        f"⚡ 席位序列：{' ➔ '.join(a['seat'] for a in acts)} (共 {len(stages)} 阶段)"
    )
