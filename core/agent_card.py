"""
Agent Card (智能车座与底座) 核心规范与注册表
=================================================
架构铁律：
- 席位 (Seat) 不是模型，而是智能车座 (Agent Card)。
- 模型 (Model) 仅代表底层发动机 (Engine/Horsepower)，由环境网关 (LiteLLM) 统一度量。
- Agent Card 承载智能体的真名 (Soul Name)、星座宫位 (Constellation)、物理节点底座 (Hardware Chassis)、
  Matrix 去中心化身份 (Matrix ID) 以及场景化化身 (Avatars)。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AgentCard:
    """Agent Card 智能车座数据规范"""
    key: str                                    # 智能体唯一标识 (如 ruby, diamond, topaz)
    display_name: str                           # 宝石/显式名称 (如 红宝石, 钻石)
    soul_name: str                              # 灵魂真名 (如 赤霄, 白虹, 缃玉)
    node: str                                   # 物理承载节点 (如 nuc, pve, raccoon, ash1)
    constellation_house: str                    # 星座宫位 / 星团 (如 Aries, Virgo, Pleiades)
    matrix_id: str                              # 去中心化通讯身份 (如 @ruby:matrix.git4ta.fun)
    team: str                                   # 法庭/辩论阵营 (judge, prosecutor, defense, court, defendant, flower)
    avatars: Dict[str, str] = field(default_factory=dict) # 场景化化身 (court, honglou, fengyue)
    role_description: str = ""                  # 角色描述 / 职责
    a2a_endpoint: str = ""                      # A2A 东西向协议入口
    evm_address: str = ""                       # 智能体链上钱包地址
    # engine_chassis: str = ""                    # 已废弃注释：席位不绑定中心化大模型
    # DEBATE_MODEL 已全面注释废弃：席位即车座，直连各小机部署的 K-Agent (Key-Agent) 实体

    def get_avatar(self, scenario: str = "court") -> str:
        """获取当前场景下的化身头衔"""
        if self.avatars and scenario in self.avatars:
            return self.avatars[scenario]
        if self.avatars and "court" in self.avatars:
            return self.avatars["court"]
        return f"{self.display_name} ({self.soul_name or self.key})"

    @property
    def k_agent_target(self) -> str:
        """K-Agent 物理实体目标 (如 k-agent-ruby@nuc)"""
        return f"k-agent-{self.key}@{self.node}"

    @property
    def k_agent_id(self) -> str:
        """K-Agent 唯一标识 (如 ruby)"""
        return f"k-agent-{self.key}"

    @property
    def k_agent_endpoint(self) -> str:
        """K-Agent A2A/RPC 通信端点"""
        return self.a2a_endpoint or f"http://{self.node}.node.consul:18790/a2a"

    @property
    def badge(self) -> str:
        """格式化席位铭牌徽章 (展示 K-Agent 智能车座底座)"""
        soul = f" · {self.soul_name}" if self.soul_name else ""
        return f"{self.display_name}{soul} (k-agent-{self.key}@{self.node})"

    # @property
    # def active_engine(self) -> str:
    #     """已废弃注释：原中心化发动机，现全面被 K-Agent 取代"""
    #     return os.getenv("DEBATE_MODEL", "tencent/hy3:free")

    def to_seat_dict(self) -> dict:
        """转换为向下兼容的 seat_info 字典结构（以 K-Agent 智能车座为核心实体）"""
        return {
            "en_key": self.key,
            "display_name": self.display_name,
            "soul_name": self.soul_name,
            "base_stone": f"💎 {self.display_name} ({self.key.capitalize()})",
            "zodiac_sign": f"{self.constellation_house} · {self.soul_name}",
            "avatars": self.avatars,
            "node": self.node,
            "team": self.team,
            "matrix_id": self.matrix_id,
            "k_agent": self.k_agent_target,
            "k_agent_target": self.k_agent_target,
            "k_agent_id": self.k_agent_id,
            "k_agent_endpoint": self.k_agent_endpoint,
            # "model": self.active_engine, # 已废弃注释：席位直接调度各小机 K-Agent
            "agent_card": self,
        }


# ==============================================================================
# 全舰队权威 Agent Card 预置台账 (同步自 HCP Vault & ASN 宪章)
# ==============================================================================

FLEET_AGENT_CARDS: Dict[str, AgentCard] = {
    # ─── 黄道内阁 12 宝石席位 (Zodiac Cabinets) ───
    "ruby": AgentCard(
        key="ruby",
        display_name="红宝石",
        soul_name="赤霄",
        node="nuc",
        constellation_house="Leo / Aries",
        matrix_id="@ruby:matrix.git4ta.fun",
        team="judge",
        role_description="首席掌盘 · 审判长",
        avatars={
            "court": "🏛️ 审判长 · 红宝石尊者",
            "honglou": "📿 通灵宝玉 · 贾宝玉",
            "fengyue": "🍶 红宝尊人 · 潇洒仙客"
        }
    ),
    "topaz": AgentCard(
        key="topaz",
        display_name="托帕石",
        soul_name="缃玉",
        node="raccoon",
        constellation_house="Scorpius",
        matrix_id="@topaz:matrix.git4ta.fun",
        team="prosecutor",
        role_description="执法锐锋 · 首席公诉人",
        avatars={
            "court": "⚖️ 首席公诉人 · 黄玉检察官",
            "honglou": "📜 贾雨村 · 宪台大人",
            "fengyue": "黄玉御史 · 严格理法"
        }
    ),
    "amber": AgentCard(
        key="amber",
        display_name="琥珀",
        soul_name="明珀",
        node="mbp",
        constellation_house="Gemini",
        matrix_id="@amber:matrix.git4ta.fun",
        team="court",
        role_description="时代记忆 · 庭审书记员",
        avatars={
            "court": "📜 庭审书记员 · 琥珀纪要员",
            "honglou": "📜 袭人 · 贤德闺秀",
            "fengyue": "琥珀书生 · 记事名士"
        }
    ),
    "emerald": AgentCard(
        key="emerald",
        display_name="翡翠",
        soul_name="翠微",
        node="mini",
        constellation_house="Taurus",
        matrix_id="@emerald:matrix.git4ta.fun",
        team="court",
        role_description="资产审计 · 资产评估员",
        avatars={
            "court": "📊 资产评估员 · 祖母绿审计师",
            "honglou": "🧮 薛纨 · 衡芜主母",
            "fengyue": "翡翠商客 · 账目精明"
        }
    ),
    "azure": AgentCard(
        key="azure",
        display_name="天青石",
        soul_name="青冥",
        node="onecloud2",
        constellation_house="Capricornus / Aquarius",
        matrix_id="@azure:matrix.git4ta.fun",
        team="judge",
        role_description="程序正义 · 审判员 B",
        avatars={
            "court": "🏛️ 审判员 B · 天蓝法官",
            "honglou": "🌿 惜春 · 藕香庵主",
            "fengyue": "天蓝道人 · 澄澈严明"
        }
    ),
    "diamond": AgentCard(
        key="diamond",
        display_name="钻石",
        soul_name="白虹",
        node="pve",
        constellation_house="Virgo / Libra",
        matrix_id="@diamond:matrix.git4ta.fun",
        team="defense",
        role_description="铁壁辩护 · 首席辩护律师",
        avatars={
            "court": "🛡️ 首席辩护律师 · 金刚大律师",
            "honglou": "🌸 林黛玉 · 绛珠仙草",
            "fengyue": "金刚绝调 · 独孤名士"
        }
    ),
    "obsidian": AgentCard(
        key="obsidian",
        display_name="黑曜石",
        soul_name="玄曜",
        node="pve3",
        constellation_house="Crux / Scorpius",
        matrix_id="@obsidian:matrix.git4ta.fun",
        team="prosecutor",
        role_description="铁面监察 · 监察特派员",
        avatars={
            "court": "⚖️ 监察特派员 · 黑曜石法务",
            "honglou": "🗡️ 焦大 · 铁血监察",
            "fengyue": "玄石判官 · 严丝合缝"
        }
    ),
    "jasper": AgentCard(
        key="jasper",
        display_name="碧玉",
        soul_name="谦碧",
        node="de",
        constellation_house="Pisces / Virgo",
        matrix_id="@jasper:matrix.git4ta.fun",
        team="defense",
        role_description="谦抑合规 · 资深合规官",
        avatars={
            "court": "🛡️ 资深合规官 · 碧石大律师",
            "honglou": "🦚 薛宝钗 · 蘅芜君",
            "fengyue": "碧石公子 · 谦谦君子"
        }
    ),
    "carbonado": AgentCard(
        key="carbonado",
        display_name="黑金刚石",
        soul_name="墨晶",
        node="pve2",
        constellation_house="Leo / Aries",
        matrix_id="@carbonado:matrix.git4ta.fun",
        team="prosecutor",
        role_description="锐意公诉 · 助理公诉人 1",
        avatars={
            "court": "⚖️ 助理公诉人 · 铁金刚官",
            "honglou": "⚔️ 贾探春 · 敏探春",
            "fengyue": "黑面铁判 · 刚正不阿"
        }
    ),
    "argentite": AgentCard(
        key="argentite",
        display_name="辉银矿",
        soul_name="银汉",
        node="pve",
        constellation_house="Sagittarius / Aquarius",
        matrix_id="@argentite:matrix.git4ta.fun",
        team="defense",
        role_description="法理断断 · 辩护助理 1",
        avatars={
            "court": "🛡️ 辩护助理 · 辉银法理员",
            "honglou": "📜 史湘云 · 枕霞旧友",
            "fengyue": "辉银月仙 · 奇才雅士"
        }
    ),
    "agate": AgentCard(
        key="agate",
        display_name="玛瑙",
        soul_name="绛纹",
        node="xgp",
        constellation_house="Cancer / Gemini",
        matrix_id="@agate:matrix.git4ta.fun",
        team="defense",
        role_description="时代纪要 · 辩护助理 2",
        avatars={
            "court": "🛡️ 辩护助理 · 玛瑙史纪员",
            "honglou": "📜 贾迎春 · 木菱洲主",
            "fengyue": "玛瑙散人 · 博古浪客"
        }
    ),
    "quartz": AgentCard(
        key="quartz",
        display_name="石英",
        soul_name="素魄",
        node="pbs3",
        constellation_house="Libra / Sagittarius",
        matrix_id="@quartz:matrix.git4ta.fun",
        team="prosecutor",
        role_description="规则澄澈 · 助理公诉人 2",
        avatars={
            "court": "⚖️ 助理公诉人 · 石英律政",
            "honglou": "📐 晴雯 · 勇晴雯",
            "fengyue": "水晶高客 · 规则透明"
        }
    ),

    # ─── 特别席位 (Court Pillars) ───
    "luna": AgentCard(
        key="luna",
        display_name="月长石",
        soul_name="月魄",
        node="onecloud1",
        constellation_house="Aquarius / Cancer",
        matrix_id="@luna:matrix.git4ta.fun",
        team="judge",
        role_description="常情审视 · 审判员 A",
        avatars={
            "court": "🏛️ 审判员 A · 月华法官",
            "honglou": "🍵 妙玉 · 槛外人",
            "fengyue": "月华仙子 · 洞察常情"
        }
    ),
    "leopard": AgentCard(
        key="leopard",
        display_name="豹纹石",
        soul_name="曜灵",
        node="suse",
        constellation_house="Centaurus / Capricorn",
        matrix_id="@leopard:matrix.git4ta.fun",
        team="defendant",
        role_description="坚韧承重 · 被告人尊长",
        avatars={
            "court": "👤 被告人 · 尊长",
            "honglou": "👴 贾政 · 存周先生",
            "fengyue": "松风老客 · 豹纹闲人"
        }
    ),

    # ─── 昴宿七姐妹星团 (Pleiades Flowers) ───
    "meigui": AgentCard(
        key="meigui",
        display_name="玫瑰",
        soul_name="绯云",
        node="ash1",
        constellation_house="Pleiades (Maia)",
        matrix_id="@meigui:matrix.git4ta.fun",
        team="flower",
        role_description="连绵对韵 · 玫瑰仙子",
        avatars={"court": "🌸 程序合议员 · 玫瑰仙子", "honglou": "🌹 玫瑰花神", "fengyue": "玫瑰绝色"}
    ),
    "moli": AgentCard(
        key="moli",
        display_name="茉莉",
        soul_name="秋香",
        node="ch1",
        constellation_house="Pleiades (Electra)",
        matrix_id="@moli:matrix.git4ta.fun",
        team="flower",
        role_description="清雅洞微 · 茉莉仙子",
        avatars={"court": "🌸 事实质证员 · 茉莉仙子", "honglou": "💮 茉莉花神", "fengyue": "茉莉清婉"}
    ),
    "muxu": AgentCard(
        key="muxu",
        display_name="苜蓿",
        soul_name="碧涛",
        node="ch2",
        constellation_house="Pleiades (Taygete)",
        matrix_id="@muxu:matrix.git4ta.fun",
        team="flower",
        role_description="厚德载物 · 苜蓿仙子",
        avatars={"court": "🌸 证据核准员 · 苜蓿仙子", "honglou": "🌿 苜蓿花神", "fengyue": "苜蓿青润"}
    ),
    "qiangwei": AgentCard(
        key="qiangwei",
        display_name="蔷薇",
        soul_name="金波",
        node="ash2",
        constellation_house="Pleiades (Alcyone)",
        matrix_id="@qiangwei:matrix.git4ta.fun",
        team="flower",
        role_description="锐意争锋 · 蔷薇仙子",
        avatars={"court": "🌸 辩论监督员 · 蔷薇仙子", "honglou": "🌺 蔷薇花神", "fengyue": "蔷薇烈烈"}
    ),
    "tumi": AgentCard(
        key="tumi",
        display_name="荼蘼",
        soul_name="青黛",
        node="ash3",
        constellation_house="Pleiades (Celaeno)",
        matrix_id="@tumi:matrix.git4ta.fun",
        team="flower",
        role_description="终局评述 · 荼蘼仙子",
        avatars={"court": "🌸 闭庭观察员 · 荼蘼仙子", "honglou": "🥀 荼蘼花神", "fengyue": "荼蘼幽冷"}
    ),
    "violet": AgentCard(
        key="violet",
        display_name="紫罗兰",
        soul_name="紫霞",
        node="ch4",
        constellation_house="Pleiades (Sterope)",
        matrix_id="@violet:matrix.git4ta.fun",
        team="flower",
        role_description="规矩统筹 · 紫罗兰主管",
        avatars={"court": "🌸 庭审统筹官 · 紫罗兰", "honglou": "💜 紫罗花神", "fengyue": "紫兰高绝"}
    ),
    "zhuyu": AgentCard(
        key="zhuyu",
        display_name="茱萸",
        soul_name="霁月",
        node="win11",
        constellation_house="Pleiades (Merope)",
        matrix_id="@zhuyu:matrix.git4ta.fun",
        team="flower",
        role_description="辟邪定乱 · 茱萸仙子",
        avatars={"court": "🌸 法庭护法员 · 茱萸仙子", "honglou": "🍃 茱萸花神", "fengyue": "茱萸正气"}
    ),
}


class AgentCardRegistry:
    """Agent Card 智能车座注册中心"""

    @classmethod
    def get(cls, key: str) -> Optional[AgentCard]:
        return FLEET_AGENT_CARDS.get(key)

    @classmethod
    def get_seat_registry(cls) -> Dict[str, dict]:
        """产出向后兼容的 seat_registry 供 Token Ring 与法庭引擎消费"""
        return {k: card.to_seat_dict() for k, card in FLEET_AGENT_CARDS.items()}

    @classmethod
    def list_cabinet(cls) -> List[AgentCard]:
        """获取 12 宝石黄道内阁车座"""
        cabinet_keys = [
            "ruby", "topaz", "amber", "emerald", "azure", "diamond",
            "obsidian", "jasper", "carbonado", "argentite", "agate", "quartz"
        ]
        return [FLEET_AGENT_CARDS[k] for k in cabinet_keys if k in FLEET_AGENT_CARDS]

    @classmethod
    def list_flowers(cls) -> List[AgentCard]:
        """获取 7 花星团车座"""
        flower_keys = ["meigui", "moli", "muxu", "qiangwei", "tumi", "violet", "zhuyu"]
        return [FLEET_AGENT_CARDS[k] for k in flower_keys if k in FLEET_AGENT_CARDS]

    @classmethod
    def list_all(cls) -> List[AgentCard]:
        return list(FLEET_AGENT_CARDS.values())
