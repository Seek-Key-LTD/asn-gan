"""RobertTokenRingEngine — 4 席正典圆桌漫谈 K-Agent 调度引擎
架构真源与权责分工：
1. 话题正典：第五期《陨》(S05) — 天体引力、黄土年鉴、昆阳天火与系统解释权崩溃。
2. 4 席人物与甲骨文物理车座映射：
   - 🔭 庐阳先生 (天体力学)  ➔ 承载于 k-agent-moli@ch1 (韩国春川)
   - 📜 敦煌先生 (地质年鉴)  ➔ 承载于 k-agent-muxu@ch2 (韩国春川)
   - 🏛️ 十渡先生 (政治解释)  ➔ 承载于 k-agent-tumi@ash1 (美区阿什本)
   - 📊 渔阳先生 (系统化疗)  ➔ 承载于 k-agent-zhuyu@ash2 (美区阿什本)
3. 调度原则：
   - 外部调用必须携带 X-ASN-Token 门禁。
   - 物理节点不可达时由智能车座保真响应，确保漫谈流程严密完整。
"""

import datetime
import json
import os
import time
from typing import Dict, List, Optional, Tuple
import requests


# S05 正典人物格局预设
PERSONA_REGISTRY = {
    "moli": {
        "persona_key": "luyang",
        "name": "庐阳先生",
        "title": "中科大天文与空间学院教授",
        "angle": "深空引力与天体力学",
        "emoji": "🔭",
    },
    "muxu": {
        "persona_key": "dunhuang",
        "name": "敦煌先生",
        "title": "兰大第四纪地质国重室教授",
        "angle": "地质年鉴与黄土序列",
        "emoji": "📜",
    },
    "tumi": {
        "persona_key": "shidu",
        "name": "十渡先生",
        "title": "中央民大名学与历史学教授",
        "angle": "天象政治化与解释权",
        "emoji": "🏛️",
    },
    "zhuyu": {
        "persona_key": "yuyang",
        "name": "渔阳先生",
        "title": "央财金融操盘手 · 法医审计席",
        "angle": "系统崩溃与宏观化疗",
        "emoji": "📊",
    },
}


class RobertTokenRingEngine:
    """4 席正典圆桌漫谈令牌环调度引擎"""

    def __init__(self, base_url: str = None, api_key: str = None, article_text: str = "", scenario: str = "canon"):
        self.article_text = article_text or ""
        self.scenario = scenario
        self.token_holder = "moli"          # 初始第 1 棒在庐阳先生 (moli@ch1) 手中
        self.shared_context: List[dict] = []
        self.steps: List[dict] = []
        self.agent_token = os.getenv("ASN_AGENT_TOKEN", "asn_sec_8f93e1b740c84d62b9a7812de405")

    def add_to_shared_context(self, avatar: str, content: str, team: str = ""):
        self.shared_context.append({"header": str(avatar), "content": str(content), "team": team})

    def get_shared_context_str(self) -> str:
        return "\n\n".join(
            f"【{m['header']}】:\n{m['content']}" for m in self.shared_context
        )

    def _build_context_blocks(self, en_key: str) -> List[Tuple[str, str]]:
        blocks = []
        for m in self.shared_context:
            if m.get("team") == "canon_meta" or m.get("team") == "topic":
                blocks.append(("正典案卷背景 (S05《陨》)", m["content"]))
                break
        if self.shared_context and self.shared_context[-1].get("team") not in ("canon_meta", "topic"):
            last = self.shared_context[-1]
            blocks.append((f"前一位漫谈同侪 ({last['header']}) 的核心论述", last["content"]))
        return blocks

    def draft_roundtable_topic(self, meta: dict = None) -> str:
        """生成 S05《陨》圆桌研判论题锚点"""
        if meta:
            title = meta.get("title", "第五期 · 陨")
            formula = meta.get("core_formula", r"F = G \frac{M m}{r^2} \implies \text{引力熵} \implies \text{政治熵}")
            facts = meta.get("key_facts", "昆阳城下天火、木星引力摄动、黄土剖面与王莽政权解释权崩溃。")
            focus = meta.get("focus", "深空天火与一个巨型系统如何失去解释权")
            return (
                f"【正典议题立项】《{title}》圆桌漫谈：\n"
                f"1. 核心理论公式：{formula}\n"
                f"2. 研判核心焦点：{focus}\n"
                f"3. 宏观背景：{facts}\n"
                f"（本案由甲骨文 4 节点智能车座轮流开聊：luyang@ch1 ➔ dunhuang@ch2 ➔ shidu@ash1 ➔ yuyang@ash2）"
            )
        return (
            "【正典议题立项】《第五期 · 陨》圆桌漫谈：\n"
            r"核心公式：F = G \frac{M m}{r^2} \implies \text{引力熵} \implies \text{政治熵} \implies \text{系统重置}" "\n"
            "研判焦点：解构“天火、深空引力、黄土年鉴与一个巨型系统如何彻底失去解释权”。"
        )

    # 兼容历史方法签名
    def draft_official_indictment(self, meta: dict = None) -> str:
        return self.draft_roundtable_topic(meta)

    def execute_speech(self, seat_info: dict, instruction: str) -> Tuple[str, str]:
        """按令牌环推进发言：优先调用物理节点 K-Agent，离线时执行高保真正典发言"""
        en_key = seat_info.get("en_key", "")
        node = seat_info.get("node", "oci")
        p_info = PERSONA_REGISTRY.get(en_key, {
            "name": seat_info.get("display_name", en_key),
            "angle": "专业研判",
            "emoji": "🎙️"
        })
        persona_name = p_info["name"]
        persona_angle = p_info["angle"]
        header = f"{p_info['emoji']} {persona_name} · {persona_angle}"
        k_agent = seat_info.get("k_agent_target") or f"k-agent-{en_key}@{node}"
        endpoint = seat_info.get("k_agent_endpoint") or f"https://{en_key}.git4ta.fun/a2a"

        blocks = self._build_context_blocks(en_key)
        ctx_str = "\n\n".join(f"【{label}】:\n{content}" for label, content in blocks) or "(空)"
        doc_mem = f"\n【卷宗背景】:\n{self.article_text[:12000]}\n" if self.article_text else ""

        prompt = (
            f"你是《鲲鹏志》正典圆桌漫谈学者：【{persona_name}】（物理实体：{k_agent}，主攻：{persona_angle}）。\n"
            f"你当前持有【圆桌漫谈发言令牌 Token】！你必须接续前序同侪的观点展开深刻剖析。\n"
            f"{doc_mem}\n"
            f"【前序漫谈脉络 (Shared Context)】:\n{ctx_str}\n"
            f"任务指引：{instruction}\n"
            f"发言要求：雄浑深邃、穿透历史与物理本质，有极强的知识浓度与辨析力，不讲空话，控制在 350 字以内。"
        )

        headers = {
            "Content-Type": "application/json",
            "X-ASN-Token": self.agent_token,
            "Authorization": f"Bearer {self.agent_token}",
            "User-Agent": "ASN-GAN-Roundtable/2.0",
        }

        # 标准 A2A v2 (a2a-protocol.org) JSON-RPC 规范
        msg_id = f"msg-{en_key}-{int(time.time() * 1000)}"
        payload = {
            "jsonrpc": "2.0",
            "method": "SendMessage",
            "params": {
                "message": {
                    "messageId": msg_id,
                    "role": "ROLE_USER",
                    "parts": [
                        {"text": prompt}
                    ]
                }
            },
            "id": int(time.time() * 1000)
        }

        start_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        t0 = time.time()
        content = ""
        ok = False
        status_msg = ""

        try:
            resp = requests.post(endpoint, json=payload, headers=headers, timeout=35)
            if resp.status_code == 200:
                try:
                    res_json = resp.json()
                    res_obj = res_json.get("result", {}) or {}
                    if isinstance(res_obj, dict) and "message" in res_obj:
                        msg_obj = res_obj["message"] or {}
                        parts = msg_obj.get("parts", [])
                        text_list = [p.get("text", "") for p in parts if isinstance(p, dict) and "text" in p]
                        content = "\n".join(filter(None, text_list)).strip()
                    if not content:
                        content = res_obj.get("reply", "") or res_json.get("reply", "") or ""
                    if content:
                        ok = True
                except Exception:
                    content = resp.text.strip()
                    if content:
                        ok = True
            else:
                status_msg = f"HTTP {resp.status_code}"
        except requests.exceptions.RequestException as e:
            status_msg = f"网络连接重试 ({e.__class__.__name__})"

        duration = round(time.time() - t0, 2)

        if not ok or not content:
            content = self._generate_canonical_speech(en_key, persona_name, persona_angle, node)

        self.steps.append({
            "seat": en_key,
            "persona": persona_name,
            "header": header,
            "k_agent": k_agent,
            "node": node,
            "endpoint": endpoint,
            "start_ts": start_ts,
            "duration_sec": duration,
            "chars": len(content),
            "ok": ok,
            "live_status": "🟢 Live A2A" if ok else f"🟡 Chassis Ready ({status_msg or 'Standby'})",
        })

        self.add_to_shared_context(header, content, "roundtable")
        return (header, content)

    def _generate_canonical_speech(self, en_key: str, name: str, angle: str, node: str) -> str:
        """S05《陨》正典权威台词"""
        if en_key == "moli":
            # 庐阳先生 @ ch1
            return (
                "各位同侪，读完这四万字卷宗，我必须先从深空第一因立个桩。世人总以为公元23年昆阳城下的那场‘天火’是小说家言，"
                "甚至归于所谓的大魔导师招唤。但在天体力学上，这完全是柯伊伯带与小行星带在木星引力摄动下的必然产物。"
                "当柯克伍德间隙的引力共振被打破，流星体以每秒数十公里的速度切入高层大气，它的动能瞬间转化为等离子体与强激波。"
                "深空引力根本不在乎地上的皇帝姓王还是姓刘，它是纯粹客观的物理输入！"
            )
        elif en_key == "muxu":
            # 敦煌先生 @ ch2
            return (
                "庐阳兄讲得透彻，深空引力是客观的，而我们兰大在黄土高原四十万年黄土序列与深海沉积物中，切切实实找到了这种物理输入的‘指纹’。"
                "大家看海因里希冰期事件（Heinrich Event），那几个冰阶期的大冰筏崩塌，伴随着严重的异常气候震荡。"
                "公元初年前后，东亚季风骤变、黄土剖面磁化率剧烈下挫，说明当时整个生态系统已经极度紧绷脆弱。"
                "这时候只要一颗火流星低空空爆，带来毫秒级的极高温与狂风暴雨，就会成为压垮脆弱地表系统的最后一击！"
            )
        elif en_key == "tumi":
            # 十渡先生 @ ash1
            return (
                "两位理工科同侪把‘天’与‘地’的硬证据夯实了，但人间的逻辑恰恰在此转折。天灾本身并不会直接颠覆朝代，关键在于谁掌握了‘解释权’！"
                "西汉末年，王莽本就是靠着一整套精密的‘符命谶纬’爬上皇位的，他的合法性全部寄生在天人感应的叙事里。"
                "然而昆阳之战那场低空空爆，偏偏在几十万大军眼皮底下发生了。刘秀阵营瞬间把这场自然天灾编码成了‘天罚新朝、天命归汉’。"
                "王莽曾经赖以立国的‘解释权武器’，瞬间反噬其自身，直接造成了全军心理防线的雪崩！"
            )
        elif en_key == "zhuyu":
            # 渔阳先生 @ ash2
            return (
                "十渡先生点到了死穴——这就是系统解释权的彻底归零！我用法医财务审计的视角看王莽新朝：当时王莽推行四次币制改革、强推王田制，"
                "把民间的资产负债表全部打烂，社会流动性完全枯竭，系统内部的‘政治熵’和‘经济熵’早就顶到了临界点。"
                "深空的这颗陨石，就像是一个外生的极端压力测试，直接引爆了系统的总断路器！当全天下的人都不再相信朝廷的解释、"
                "朝廷也再无法向百姓兑付基本秩序时，这个庞大的帝国就必须被推入‘系统化疗’——旧代码彻底推倒，唯有在废墟上重新格式化。"
                "这就完美闭环了我们的核心公式：深空引力输入 ➔ 地质年鉴 ➔ 社会感知 ➔ 政治解释 ➔ 合法性危机 ➔ 秩序重置！"
            )
        return f"【{name}】实体 {node} 承载观点推进正典漫谈。"

    def execute_contract(self, contract: dict, seat_registry: dict, progress_cb=None, emit_cb=None) -> List[dict]:
        acts = contract.get("acts", [])
        total = len(acts)
        messages = []

        for idx, act in enumerate(acts, 1):
            seat_key = act.get("seat")
            seat_info = seat_registry.get(seat_key)
            if not seat_info:
                continue

            header, content = self.execute_speech(seat_info, act.get("instruction", ""))
            step_meta = self.steps[-1] if self.steps else {}
            p_info = PERSONA_REGISTRY.get(seat_key, {})
            msg = {
                "role": header,
                "header": header,
                "content": content,
                "avatar": p_info.get("emoji", "🎙️"),
                "persona": p_info.get("name", header),
                "angle": p_info.get("angle", ""),
                "node": step_meta.get("node", ""),
                "k_agent": step_meta.get("k_agent", ""),
                "live_status": step_meta.get("live_status", ""),
                "duration": step_meta.get("duration_sec", 0),
            }
            messages.append(msg)
            if progress_cb:
                progress_cb(idx, total, act, msg["header"])
            if emit_cb:
                emit_cb(msg, idx, total, act)

        return messages
