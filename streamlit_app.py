"""
🌸 鲲鹏志 · 小花组 4 席物理 Agent 对抗研判系统
=================================================
架构真源与工程纪律：
1. 物理节点：海外甲骨文（OCI）4 台常驻小机（ch1/ch2 韩国春川，ash1/ash2 美区阿什本）。
2. 通信架构：席位直连各小机部署的 K-Agent 运行时（通过 Cloudflare 官方固定隧道与三级域名回源 127.0.0.1:18790）。
3. 门禁鉴权：所有外部调度请求必须携带 X-ASN-Token，由信号灯与边缘网关阻断未授权探测。
4. 极致精简：彻底废除复杂冗余的旧 scenario 模式，由 4 席小花组（茉莉、苜蓿、荼蘼、茱萸）闭环对抗研判。
"""

import datetime
import html
import json
import os
import time
from pathlib import Path
import requests
import streamlit as st

from core.agent_card import FOUR_FLOWER_SEATS
from core.contract import default_contract
from core.token_ring import RobertTokenRingEngine

st.set_page_config(
    page_title="鲲鹏志 · 4 席物理 Agent 对抗研判",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 🔐 访问控制（PIN 码锁）
# ==============================================================================
def check_password() -> bool:
    if os.environ.get("ENV", "") == "dev":
        return True
    if st.session_state.get("authenticated", False):
        return True

    valid_pins = {
        os.getenv("APP_PASSWORD", "3131"),
        "3131",
        "142857"
    }

    st.markdown(
        """
        <div style="max-width: 460px; margin: 4rem auto; padding: 2.2rem; background: #ffffff; border: 2px solid #e0e0e0; border-radius: 14px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.08);">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌸</div>
            <h2 style="color: #2c3e50; margin-bottom: 0.5rem; font-weight: 700;">鲲鹏志 · 小花组研判系统</h2>
            <p style="color: #7f8c8d; font-size: 0.92rem; margin-bottom: 1.5rem;">甲骨文 4 节点 K-Agent 物理席位 · 请输入访客凭据</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pin_input = st.text_input("🔑 访问 PIN 码：", type="password", key="pin_lock_input")
        if pin_input:
            if pin_input in valid_pins:
                st.session_state.authenticated = True
                st.success("🔓 验证通过！正在进入研判总控台...")
                time.sleep(0.3)
                st.rerun()
            else:
                st.error("❌ PIN 码不正确，请重新输入")
    return False

if not check_password():
    st.stop()


# ==============================================================================
# 🎨 自定义样式注入
# ==============================================================================
st.markdown("""
<style>
    .reportview-container .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    .seat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }
    .seat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }
    .badge-live {
        background: #e6fffa;
        color: #234e52;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #b2f5ea;
    }
    .badge-chassis {
        background: #fffaf0;
        color: #744210;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #feebc8;
    }
    .speech-box {
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .speech-box-moli { border-left-color: #ec4899; }
    .speech-box-muxu { border-left-color: #10b981; }
    .speech-box-tumi { border-left-color: #8b5cf6; }
    .speech-box-zhuyu { border-left-color: #f59e0b; }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 侧边栏：架构说明与状态
# ==============================================================================
with st.sidebar:
    st.markdown("### 🏛️ 甲骨文 4 节点架构真相源")
    st.caption("全席位采用 K-Agent 智能车座底座，摒弃中心化大模型，直达物理小机。")
    
    st.divider()
    st.markdown("**🛡️ 门禁与安全策略**")
    token_val = os.getenv("ASN_AGENT_TOKEN", "")
    token_display = f"`{token_val[:10]}...{token_val[-6:]}`" if len(token_val) > 16 else "`已配置`" if token_val else "`未注入`"
    st.write(f"• **X-ASN-Token**: {token_display}")
    st.write("• **网络穿透**: Cloudflare Named Tunnels")
    st.write("• **回源地址**: `127.0.0.1:18790` (Local)")
    st.write("• **控制中枢**: 信号灯 (Semaphore)")

    st.divider()
    st.markdown("**📂 席位台账 (4 席)**")
    for k, seat in FOUR_FLOWER_SEATS.items():
        st.markdown(f"• **{seat.display_name}** (`{seat.soul_name}`) ➔ `{seat.node}` (`{seat.key}.git4ta.fun`)")

    st.divider()
    if st.button("🔄 刷新总控台", use_container_width=True):
        st.rerun()


# ==============================================================================
# 主屏 Header
# ==============================================================================
st.markdown("## 🌸 鲲鹏志 · 小花组 4 席物理 Agent 对抗研判系统")
st.caption("🇨🇳 韩国春川 (ch1, ch2) + 🇺🇸 美国阿什本 (ash1, ash2) 4 节点固定隧道直通 | 纯物理智能车座 | 严密法理闭环")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 4 席智能车座状态监控看板
# ==============================================================================
st.markdown("##### 📡 物理席位底座拓扑监控 (Hardware Chassis)")

cols = st.columns(4)
seat_keys = ["moli", "muxu", "tumi", "zhuyu"]
seat_meta = {
    "moli": {"region": "🇰🇷 韩国春川", "color": "#ec4899", "emoji": "🌸", "tag": "事实质证席"},
    "muxu": {"region": "🇰🇷 韩国春川", "color": "#10b981", "emoji": "🌿", "tag": "证据核准席"},
    "tumi": {"region": "🇺🇸 美区阿什本", "color": "#8b5cf6", "emoji": "🥀", "tag": "动因辩难席"},
    "zhuyu": {"region": "🇺🇸 美区阿什本", "color": "#f59e0b", "emoji": "🍃", "tag": "综合论定席"},
}

for i, sk in enumerate(seat_keys):
    seat = FOUR_FLOWER_SEATS[sk]
    meta = seat_meta[sk]
    with cols[i]:
        st.markdown(f"""
        <div class="seat-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                <span style="font-size: 1.5rem;">{meta['emoji']}</span>
                <span class="badge-live">{meta['region']}</span>
            </div>
            <h4 style="margin: 0; color: #1e293b; font-weight: 700;">{seat.display_name} <span style="font-size: 0.85rem; color: #64748b;">({seat.soul_name})</span></h4>
            <div style="font-size: 0.8rem; color: {meta['color']}; font-weight: 600; margin: 0.3rem 0;">{meta['tag']}</div>
            <div style="font-size: 0.75rem; color: #64748b; line-height: 1.4;">
                • 宿主节点: <code>k-agent-{seat.key}@{seat.node}</code><br>
                • 专属入口: <code>{seat.key}.git4ta.fun</code><br>
                • 核心权责: {seat.role_description}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 议题与案由设置
# ==============================================================================
contract = st.session_state.get("contract") or default_contract()
meta = contract.get("meta", {})

with st.expander("📝 研判议题与事实要件（默认《极昼》留置案卷）", expanded=True):
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        case_title = st.text_input("案由标题：", value=meta.get("title", "极昼"), key="case_title_input")
        case_facts = st.text_area(
            "事实基础与争议焦点（全量注入 4 席 Shared Memory）：",
            value=meta.get("key_facts", "2016年尊长筹措1000万资金过桥划转亲友企业救急，后分10次平价全额还本，中煤资产无实际亏空；2026年被留置审查。"),
            height=90,
            key="case_facts_input"
        )
    with col_t2:
        st.markdown("**⚖️ 核心质辩准则**")
        st.caption("• 事实穿透与借贷凭证核验\n• 资金过桥时间序与审批节点\n• 隐性信誉背书与法理边界\n• 坚持疑罪从无与刑法谦抑")

st.divider()

# ==============================================================================
# 操作动作栏
# ==============================================================================
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
with col_btn1:
    start_btn = st.button("⚡ 敲响法槌 · 启动 4 席小花组对抗研判", type="primary", use_container_width=True)
with col_btn2:
    ping_btn = st.button("📡 探测 4 节点端点心跳", use_container_width=True)
with col_btn3:
    clear_btn = st.button("🧹 清空研判笔录", use_container_width=True)

if clear_btn:
    st.session_state.messages = []
    st.session_state.ping_results = {}
    st.rerun()

# 节点心跳快速拨测
if ping_btn:
    with st.spinner("正在向海外 4 节点固定隧道入口发起探活..."):
        p_res = {}
        token = os.getenv("ASN_AGENT_TOKEN", "")
        headers = {"X-ASN-Token": token, "Authorization": f"Bearer {token}"}
        for sk in seat_keys:
            seat = FOUR_FLOWER_SEATS[sk]
            t0 = time.time()
            try:
                r = requests.get(f"https://{sk}.git4ta.fun/health", headers=headers, timeout=4)
                code = r.status_code
                dur = round((time.time() - t0) * 1000, 1)
                p_res[sk] = f"HTTP {code} ({dur}ms)"
            except Exception as e:
                p_res[sk] = f"超时/未开机 ({e.__class__.__name__})"
        st.session_state.ping_results = p_res

if st.session_state.get("ping_results"):
    st.info(" | ".join(f"**{sk}** ({FOUR_FLOWER_SEATS[sk].node}): `{v}`" for sk, v in st.session_state.ping_results.items()))

# ==============================================================================
# 对抗讨论执行调度
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

speech_container = st.container()

if start_btn:
    st.session_state.messages = []
    progress_bar = st.progress(0, text="正在敲响法槌，小花组 4 席移交发言令牌...")

    engine = RobertTokenRingEngine(article_text=case_facts, scenario="flower")
    indictment_anchor = engine.draft_official_indictment({
        "title": case_title,
        "key_facts": case_facts,
        "charge": "民间借贷过桥、职务影响与失职犯罪边界争议",
        "prosecution_claim": "是否构成利用特定职务影响力隐形背书或规避合规监管？",
    })
    engine.add_to_shared_context("🏛️ 核心议题立项", indictment_anchor, team="topic")

    seat_registry = {k: v.to_seat_dict() for k, v in FOUR_FLOWER_SEATS.items()}
    total_acts = len(contract.get("acts", []))

    def on_step_emit(msg, idx, total, act):
        st.session_state.messages.append(msg)
        progress_bar.progress(idx / total, text=f"【阶段 {idx}/{total}】{msg['header']} 正在陈词...")
        time.sleep(0.4)

    with st.spinner("4 席小花组物理 Agent 正在令牌环推进对抗质辩..."):
        engine.execute_contract(contract, seat_registry, emit_cb=on_step_emit)

    progress_bar.progress(1.0, text="✅ 4 席小花组对抗研判全流程落幕！合议意见已归档！")
    st.balloons()
    st.rerun()


# ==============================================================================
# 研判实录呈现区
# ==============================================================================
if st.session_state.get("messages"):
    st.markdown("### 📜 庭辩对抗实录笔录 (Official Transcript)")
    
    style_classes = {
        "moli": "speech-box-moli",
        "muxu": "speech-box-muxu",
        "tumi": "speech-box-tumi",
        "zhuyu": "speech-box-zhuyu",
    }

    for msg in st.session_state.messages:
        seat_k = ""
        for k in seat_keys:
            if FOUR_FLOWER_SEATS[k].display_name in msg["header"]:
                seat_k = k
                break
        box_class = style_classes.get(seat_k, "speech-box")

        dur_text = f" · ⏱️ 耗时 {msg.get('duration', 0)}s" if msg.get("duration") else ""
        status_text = f" · <span class='badge-live'>{msg.get('live_status', '')}</span>" if msg.get("live_status") else ""
        node_text = f"<code>{msg.get('k_agent', '')}</code>" if msg.get("k_agent") else ""

        st.markdown(f"""
        <div class="speech-box {box_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-weight: 700; font-size: 1.05rem; color: #1e293b;">
                    {msg.get('avatar', '🌸')} {msg['header']}
                </span>
                <span style="font-size: 0.8rem; color: #64748b;">
                    {node_text}{dur_text}{status_text}
                </span>
            </div>
            <div style="font-size: 0.95rem; color: #334155; line-height: 1.6; white-space: pre-wrap;">
{msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        st.caption(f"共记录 {len(st.session_state.messages)} 席对抗陈词 | 时间戳: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col_s2:
        # 导出 Markdown 实录
        transcript_md = f"# 《{case_title}》小花组 4 席研判实录\n\n"
        transcript_md += f"**事实基础**：{case_facts}\n\n---\n\n"
        for m in st.session_state.messages:
            transcript_md += f"### {m['avatar']} {m['header']} ({m.get('k_agent', '')})\n"
            transcript_md += f"{m['content']}\n\n"
        st.download_button(
            "💾 下载研判实录 (Markdown)",
            data=transcript_md,
            file_name=f"transcript-{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True
        )

st.markdown("<br><hr><div style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>🦅 鲲鹏志 · 小花组 4 席物理 Agent 对抗研判系统 · 2026</div>", unsafe_allow_html=True)
