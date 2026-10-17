"""
core/contract.py — 会话规约 (Session Spec / Contract)
======================================================
定义对抗生成会话的数据结构与阶段流。
默认会话锚定正典第五期《陨》(S05 · 陨石/天火/深空引力/解释权卷)。
"""

from __future__ import annotations
from typing import Dict, List, Any

# 席位白名单
SEAT_WHITELIST = {
    # 4 大主理人席位 (S05 核心发言席)
    "luyang", "dunhuang", "shidu", "yuyang",
    # 12 黄道内阁
    "ruby", "topaz", "amber", "emerald", "azure", "diamond",
    "obsidian", "jasper", "carbonado", "argentite", "agate", "quartz",
    # 附席
    "luna", "leopard",
    # 昴宿七姐妹
    "meigui", "qiangwei", "tumi", "zhuyu", "moli", "muxu", "violet",
}

STAGE_COUNT = 5


def default_stage_flow() -> list[dict]:
    """标准 5 阶段状态机流程"""
    return [
        {"id": 1, "name": "1. 卷宗摄入与身份检录", "emoji": "⚖️", "desc": "审判长/主持席核对各方席位身份，载入当期正典卷宗核心事实"},
        {"id": 2, "name": "2. 多维角度申领与立论", "emoji": "📜", "desc": "各席位基于专业底座认领切入视角，确立底层逻辑公理"},
        {"id": 3, "name": "3. 魁魅对抗与事实质询", "emoji": "🛡️", "desc": "判别器冷酷撕扯逻辑漏洞，辩手弃子争先、迫近真理"},
        {"id": 4, "name": "4. 同侪评议与量化打分", "emoji": "⚔️", "desc": "专家陪审团合议，根据反驳有效率与立论深度展开 Peer Pressure 打分"},
        {"id": 5, "name": "5. 终局裁判与规则沉淀", "emoji": "🏛️", "desc": "宣读终审裁定文书，将对抗生成的硬核规则沉淀至 Memory Bank"},
    ]


def default_cast() -> list[dict]:
    return [
        {"seat": "luyang", "archetype": "天文学家", "role": "深空引力与天体力学席", "team": "立论组"},
        {"seat": "dunhuang", "archetype": "地质学家", "role": "地质年鉴与古气候席", "team": "立论组"},
        {"seat": "shidu", "archetype": "政治学者", "role": "名学与合法性解释权席", "team": "质询组"},
        {"seat": "yuyang", "archetype": "法医审计", "role": "系统崩溃与宏观化疗席", "team": "审计组"},
        {"seat": "ruby", "archetype": "审判长", "role": "红宝石首席大法官", "team": "合议庭"},
        {"seat": "topaz", "archetype": "主审判官", "role": "黄玉第二法官", "team": "合议庭"},
        {"seat": "diamond", "archetype": "领衔答辩", "role": "金刚石大律师", "team": "辩护组"},
        {"seat": "carbonado", "archetype": "进攻公诉", "role": "黑金刚公诉先锋", "team": "控方组"},
        {"seat": "violet", "archetype": "小花掌门", "role": "紫罗兰专家评议席", "team": "评委组"},
    ]


def default_contract() -> dict:
    """默认正典《S05 · 陨》会话契约"""
    return {
        "protocol": "court_debate",
        "meta": {
            "episode_id": "S05",
            "title": "三更道场 第五期 · 陨",
            "topic": "天火、深空引力、黄土年鉴与一个系统如何失去解释权",
            "core_formula": "深空引力输入 ➔ 极端气候与地质年鉴 ➔ 人类社会感知 ➔ 政治化解释 ➔ 合法性危机 ➔ 秩序重置",
            "court_name": "ASN-GAN 庭辩朝堂",
            "prosecutor_org": "事实法医审计公诉席",
            "case_number": "ASN-S05-METEORITE",
            "key_facts": "公元23年西汉末年，昆阳城下火流星低空空爆引发极端热对流强降雨；王莽新朝建立在天人感应谶纬之上，天火成为颠覆其政治合法性的催化剂。",
            "prosecution_claim": "自然天灾不具备政治意志，新莽政权崩溃本质是币制改革与土地政策导致的社会流动性枯竭与制度过载。",
            "defense_claim": "深空引力输入通过黄土年鉴与物候传导为人间感知，政治合法性解释权丧失是系统不可逆的熵增必然。",
            "focus": "引力熵到政治熵的传导链；当系统遭遇外部极端压力测试时，解释权如何归零。",
        },
        "stage_flow": default_stage_flow(),
        "cast": default_cast(),
        "acts": [
            {"stage": 1, "seat": "ruby", "instruction": "敲响法槌！宣布：‘ASN-GAN 庭辩朝堂第一季第五期《陨》正式开庭！载入4.1万字卷宗，全体席位检录就绪！’"},
            {"stage": 2, "seat": "luyang", "instruction": "【深空第一因】阐述天体力学：木星引力弹弓与轨道摄动，火流星切入大气层为纯物理输入！"},
            {"stage": 2, "seat": "dunhuang", "instruction": "【地质证据】出示黄土剖面与海因里希冰阶期生态脆弱性证据，论证地表系统承压极限！"},
            {"stage": 3, "seat": "shidu", "instruction": "【解释权交锋】质询新莽政权：为何一场物理空爆会成为压垮40万大军合法性防线的致命毒药？"},
            {"stage": 3, "seat": "carbonado", "instruction": "【进攻质证】直击痛点：王莽为何无法自圆其说？符命谶纬的造神逻辑是如何发生反噬的？"},
            {"stage": 3, "seat": "yuyang", "instruction": "【法医审计】亮出财政资产负债表：四次币制改革抽干流动性，引力熵转化为政治熵的临界点！"},
            {"stage": 4, "seat": "violet", "instruction": "【专家评审团合议】汇总各席位立论严密性，评估深空物理与人间制度交锋的有效反驳率！"},
            {"stage": 5, "seat": "ruby", "instruction": "发表终审判词：深空引力无情，制度弹性唯真；将《陨》篇规则沉淀入 Memory Bank，闭庭！"},
        ],
        "constraints": {"max_speech_chars": 500, "tone": "深邃、严密、极具对抗性与法理厚度"},
        "token_policy": "fixed_order",
    }


def validate_contract(contract: dict) -> tuple[bool, list[str]]:
    """确定性校验"""
    problems = []
    if not isinstance(contract, dict):
        return False, ["契约必须为 dict"]
    if "meta" not in contract:
        problems.append("缺失 meta")
    if "acts" not in contract or not isinstance(contract.get("acts"), list):
        problems.append("缺失 acts 列表")
    return len(problems) == 0, problems


def summarize_contract(contract: dict) -> str:
    meta = contract.get("meta", {})
    return f"【{meta.get('title', '未命名')}】(议题: {meta.get('topic', '无')}, 阶段数: {len(contract.get('stage_flow', []))}, 幕数: {len(contract.get('acts', []))})"
