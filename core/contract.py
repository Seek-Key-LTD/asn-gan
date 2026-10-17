"""
Session Contract — 鲲鹏志正典圆桌对抗研判契约规范 (Canonical Roundtable)
========================================================================
架构真源：
1. 话题正典：第五期《陨》(S05) — 天体引力、黄土年鉴、昆阳天火与系统解释权崩溃。
2. 4 席人物与甲骨文物理车座映射：
   - luyang   (庐阳先生 · 中科大天体物理)  ➔ 承载于 k-agent-moli@ch1 (韩国春川)
   - dunhuang (敦煌先生 · 兰大地质年鉴)    ➔ 承载于 k-agent-muxu@ch2 (韩国春川)
   - shidu    (十渡先生 · 民大名学历史)    ➔ 承载于 k-agent-tumi@ash1 (美区阿什本)
   - yuyang   (渔阳先生 · 央财法医审计)    ➔ 承载于 k-agent-zhuyu@ash2 (美区阿什本)
3. 状态机闭环：
   Stage 1: 深空引力与天体力学 (庐阳先生)
   Stage 2: 地质年鉴与黄土序列 (敦煌先生)
   Stage 3: 天象政治化与解释权 (十渡先生)
   Stage 4: 系统崩溃与宏观化疗 (渔阳先生)
"""
from __future__ import annotations

SEAT_WHITELIST = {"moli", "muxu", "tumi", "zhuyu", "luyang", "dunhuang", "shidu", "yuyang"}
STAGE_COUNT = 4


def default_stage_flow() -> list[dict]:
    """S05《陨》圆桌漫谈四阶段演进流"""
    return [
        {
            "id": 1,
            "name": "1. 深空引力与天体力学",
            "emoji": "🔭",
            "desc": "庐阳先生 (moli@ch1) 解析柯伊伯带与木星引力摄动，确立深空第一因的纯粹物理输入"
        },
        {
            "id": 2,
            "name": "2. 地质年鉴与黄土序列",
            "emoji": "📜",
            "desc": "敦煌先生 (muxu@ch2) 调取四十万年黄土序列与海因里希H事件，锁死微玻陨石地质铁证"
        },
        {
            "id": 3,
            "name": "3. 天象政治化与解释权",
            "emoji": "🏛️",
            "desc": "十渡先生 (tumi@ash1) 剖析西汉末年符命谶纬叙事，解构昆阳天火对政权合法性的致命反噬"
        },
        {
            "id": 4,
            "name": "4. 系统崩溃与宏观化疗",
            "emoji": "📊",
            "desc": "渔阳先生 (zhuyu@ash2) 审计资产负债表与社会流动性枯竭，闭环引力熵到政治熵的系统重置"
        },
    ]


def default_cast() -> list[dict]:
    """4 席位人物格局映射"""
    return [
        {
            "seat": "moli",
            "persona_key": "luyang",
            "persona_name": "庐阳先生",
            "title": "中科大天文与空间学院教授",
            "angle": "深空引力与天体力学",
            "node": "ch1",
        },
        {
            "seat": "muxu",
            "persona_key": "dunhuang",
            "persona_name": "敦煌先生",
            "title": "兰大第四纪地质国重室教授",
            "angle": "地质年鉴与黄土序列",
            "node": "ch2",
        },
        {
            "seat": "tumi",
            "persona_key": "shidu",
            "persona_name": "十渡先生",
            "title": "中央民大名学与历史学教授",
            "angle": "天象政治化与解释权",
            "node": "ash1",
        },
        {
            "seat": "zhuyu",
            "persona_key": "yuyang",
            "persona_name": "渔阳先生",
            "title": "央财金融操盘手 · 法医审计席",
            "angle": "系统崩溃与宏观化疗",
            "node": "ash2",
        },
    ]


def default_contract() -> dict:
    """内置 S05《陨》正典契约"""
    return {
        "protocol": "roundtable_s05_meteorite",
        "meta": {
            "title": "第五期 · 陨",
            "episode_id": "S05",
            "source_type": "正典圆桌",
            "core_formula": r"F = G \frac{M m}{r^2} \implies \text{引力熵} \implies \text{政治熵} \implies \text{系统重置}",
            "focus": "天火、深空引力、黄土年鉴与一个巨型系统如何彻底失去解释权",
            "key_facts": "公元23年昆阳之战城下出现低空大火球空爆；柯克伍德间隙引力摄动；四十万年洛川黄土剖面磁化率震荡；王莽改制失败与解释权全面归零。",
        },
        "stage_flow": default_stage_flow(),
        "cast": default_cast(),
        "acts": [
            {
                "stage": 1,
                "seat": "moli",
                "persona": "庐阳先生",
                "instruction": "【第一棒 · 深空第一因】从柯伊伯带与木星引力弹弓切入。阐明昆阳城下的天火绝非小说家言，而是天体力学小行星轨道共振摄动的物理必然，深空引力作为不以人的意志为转移的客观物理输入！"
            },
            {
                "stage": 2,
                "seat": "muxu",
                "persona": "敦煌先生",
                "instruction": "【第二棒 · 地表铁证】接续深空引力输入，调取黄土高原四十万年黄土序列与深海沉积物指纹。结合海因里希H事件东亚季风骤变，证明当时气候与生态的极度紧绷脆弱，火流星如何成为压垮骆驼的最后一根稻草！"
            },
            {
                "stage": 3,
                "seat": "tumi",
                "persona": "十渡先生",
                "instruction": "【第三棒 · 政治解释权】承接天地客观物理证据，转入人间社会心理机制。剖析王莽如何以符命谶纬夺权，又如何因昆阳天火被刘秀阵营反向编码为天罚，赖以立国的解释权武器瞬间反噬其自身！"
            },
            {
                "stage": 4,
                "seat": "zhuyu",
                "persona": "渔阳先生",
                "instruction": "【第四棒 · 系统总清盘】从法医财务审计视角收官。结合王莽四次币制改革导致的资产负债表与流动性彻底枯竭，论证引力熵引爆系统总断路器，帝国陷入不可逆化疗与格式化重置！"
            },
        ],
        "constraints": {"max_speech_chars": 400, "tone": "深邃、雄浑、穿透历史"},
        "token_policy": "fixed_order",
    }


def validate_contract(contract: dict) -> tuple[bool, list[str]]:
    problems = []
    if not isinstance(contract, dict):
        return False, ["契约不是合法字典对象"]
    acts = contract.get("acts") or []
    stages = contract.get("stage_flow") or []

    if len(stages) != STAGE_COUNT:
        problems.append(f"阶段数应为 {STAGE_COUNT}，实为 {len(stages)}")

    if not acts:
        problems.append("acts 为空")

    for idx, a in enumerate(acts):
        seat = a.get("seat")
        if seat not in SEAT_WHITELIST:
            problems.append(f"acts[{idx}] seat={seat} 不在白名单")
        if not (a.get("instruction") or "").strip():
            problems.append(f"acts[{idx}] 指令为空")

    return (len(problems) == 0), problems


def summarize_contract(contract: dict) -> str:
    meta = contract.get("meta", {})
    stages = contract.get("stage_flow", [])
    acts = contract.get("acts", [])
    return (
        f"🦅 协议：正典圆桌漫谈 ({contract.get('protocol')})\n"
        f"📖 期次：{meta.get('title', '第五期 · 陨')}\n"
        f"📊 公式：{meta.get('core_formula', '')}\n"
        f"🎯 焦点：{meta.get('focus', '')}\n"
        f"🎙️ 轮转：{' ➔ '.join(a.get('persona', a['seat']) for a in acts)} (共 {len(stages)} 棒)"
    )
