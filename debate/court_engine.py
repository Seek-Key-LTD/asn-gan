"""
debate/court_engine.py — ASN-GAN 庭辩对抗生成引擎
=================================================
通用的多智能体庭辩与对抗生成引擎（令牌环驱动），
默认基于《三更道场·第五期·陨》(S05) 案卷与核心公式展开对抗。
"""

import os
import json
import logging
from core.agent_card import VAULT_ZODIAC_CABINETS, FLOWER_PLEIADES_TABLE
from core.config import config
from core.db import load_dossier

log = logging.getLogger("asn_gan.court")


def _build_court_seat(base_key: str, fallback_title: str, default_team: str) -> dict:
    source_table = VAULT_ZODIAC_CABINETS if base_key in VAULT_ZODIAC_CABINETS else FLOWER_PLEIADES_TABLE
    cfg = source_table.get(base_key, {})
    return {
        "en_key": base_key,
        "base_stone": cfg.get("base_stone", base_key),
        "soul_name": cfg.get("soul_name", ""),
        "node": cfg.get("node", "fleet"),
        "k_agent_target": cfg.get("k_agent_target", f"k-agent-{base_key}@{cfg.get('node', 'fleet')}"),
        "matrix_id": cfg.get("matrix_id", ""),
        "avatars": cfg.get("avatars", {}),
        "default_title": cfg.get("avatars", {}).get("court", fallback_title),
        "team": default_team,
    }


SEATS_DICT = {
    "judge_chief": _build_court_seat("ruby", "🏛️ 审判长 (红宝石)", "judge"),
    "defendant": _build_court_seat("leopard", "👤 答辩席 (客卿/辩方)", "defendant"),
    "prosecutor_chief": _build_court_seat("topaz", "⚖️ 首席质询官 (黄玉)", "prosecutor"),
    "prosecutor_asst1": _build_court_seat("carbonado", "⚖️ 质询先锋 (黑金刚)", "prosecutor"),
    "defense_chief": _build_court_seat("diamond", "🛡️ 领衔立论律师 (金刚石)", "defense"),
    "defense_asst1": _build_court_seat("argentite", "🛡️ 事实分析员 (辉银矿)", "defense"),
    "defense_asst2": _build_court_seat("agate", "🛡️ 伦理与因果辩护员 (玛瑙)", "defense"),
    "judge_a": _build_court_seat("luna", "🏛️ 审判员 A (月华石)", "judge"),
    "judge_b": _build_court_seat("meigui", "🏛️ 审判员 B (玫瑰)", "judge"),
}

ROBERTS_STEPS = [
    ("judge_chief", "敲响法槌！宣布：‘ASN-GAN 庭辩朝堂正式开庭！本案审理议题：深空引力、极端气候与系统合法性解释权危机！’现场核对各方席位身份，告知质询与申辩权利，将令牌派发给立论席！"),
    ("defense_chief", "拿到了令牌！发表第一轮立论陈词：确立深空引力第一因，柯克伍德间隙引力摄动为纯客观物理输入，自然天灾不具备政治倾向！归还令牌！"),
    ("prosecutor_chief", "拿到了令牌！发表质询立论：自然物理输入必须经过社会网络感知转化为政治解释，新莽政权崩溃在于其垄断解释权的逻辑破产！归还令牌！"),
    ("prosecutor_asst1", "受首席质询官指派主动进攻：逼问辩方核心断点——①若天灾纯属自然偶然，为何昆阳天火偏偏瓦解了40万大军的战斗意志？②朝廷垄断谶纬解释权多年，为何在物理冲击面前瞬间发生反噬？归还令牌！"),
    ("defense_chief", "拿到了令牌！回应进攻质询：亮出地质年鉴与黄土序列书证，指出公元初年前后东亚季风骤变与海因里希冰期事件已使地表系统紧绷，火流星空爆是引爆脆弱系统的最后一根稻草！归还令牌！"),
    ("defense_asst1", "补充辩护：引入力学模型，论证深空引力熵转化为政治熵的传导链，证明系统脆弱性源于内部财政流动性枯竭！归还令牌！"),
    ("judge_a", "合议庭审判员A发难质询：追问质询方‘政治解释权丧失’的判定标准是什么？追问立论方‘客观物理输入’如何阻断人间责任？归还令牌！"),
    ("prosecutor_asst1", "【回应合议庭质询】正面回答审判员A：当一个庞大政权无法为全天下兑付最基础的安全与信用时，其解释权即在事实上归零！不得回避质询！归还令牌！"),
    ("defense_chief", "【回应合议庭质询】正面回答审判员A：物理输入不以人间意志为转移，但系统的弹性决定了是吸收冲击还是彻底崩解！归还令牌！"),
    ("defendant", "【最后陈述】总结各方立论：面对深空引力与宏观演进，唯有尊重铁客观律与制度弹性，方能跨越历史周期律！归还令牌！"),
    ("judge_chief", "收回令牌！综合合议庭评议，敲响法槌，发表判词！必须逐项检验核心公式六大节点：深空引力输入 ➔ 极端气候地质年鉴 ➔ 社会感知 ➔ 政治解释 ➔ 合法性危机 ➔ 秩序重置！给出终局判词并沉淀规则入库！"),
]


class CourtEngine:
    def __init__(self, article_text: str = ""):
        if not article_text:
            s05 = load_dossier("S05")
            self.article_text = s05["content_md"] if s05 else ""
            self.dossier_title = s05["title"] if s05 else "三更道场·第五期·陨"
        else:
            self.article_text = article_text
            self.dossier_title = "当前案卷"

    def run_debate(self):
        log.info(f"启动 ASN-GAN 庭辩引擎，案卷: {self.dossier_title} ({len(self.article_text)} 字符)")
        for seat_key, instruction in ROBERTS_STEPS:
            seat = SEATS_DICT.get(seat_key, {})
            log.info(f"[{seat.get('default_title', seat_key)}] 指令: {instruction[:60]}...")
