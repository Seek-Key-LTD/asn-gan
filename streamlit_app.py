"""
🦅 鲲鹏志 · 正典圆桌对抗研判系统 (Roundtable Discussion)
=========================================================
核心正典：第五期《陨》(S05) — 解构“天火、深空引力、黄土年鉴与一个巨型系统如何彻底失去解释权”
算力底座：甲骨文海外 4 节点智能车座（k-agent-moli@ch1, muxu@ch2, tumi@ash1, zhuyu@ash2）
门禁安全：Cloudflare 官方固定隧道 + X-ASN-Token 边缘认证
"""

import datetime
import os
import time
from pathlib import Path
import requests
import streamlit as st

from core.agent_card import FOUR_FLOWER_SEATS
from core.contract import default_contract
from core.token_ring import RobertTokenRingEngine

st.set_page_config(
    page_title="鲲鹏志 · 正典圆桌研判系统",
    page_icon="🦅",
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
        <div style="max-width: 480px; margin: 4rem auto; padding: 2.2rem; background: #ffffff; border: 2px solid #e2e8f0; border-radius: 14px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.06);">
            <div style="font-size: 2.8rem; margin-bottom: 0.5rem;">🦅</div>
            <h2 style="color: #0f172a; margin-bottom: 0.5rem; font-weight: 700;">鲲鹏志 · 正典圆桌研判系统</h2>
            <p style="color: #64748b; font-size: 0.92rem; margin-bottom: 1.5rem;">S05《陨》· 甲骨文海外 4 节点 K-Agent · 请输入访问 PIN 码</p>
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
                st.success("🔓 验证通过！正在进入正典研判总控台...")
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
    .persona-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }
    .persona-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }
    .badge-node {
        background: #f1f5f9;
        color: #475569;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #e2e8f0;
    }
    .badge-live {
        background: #e6fffa;
        color: #234e52;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #b2f5ea;
    }
    .speech-box {
        background: #ffffff;
        border-left: 5px solid #3b82f6;
        border-radius: 8px;
        padding: 1.3rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        border-top: 1px solid #f1f5f9;
        border-right: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
    }
    .speech-box-luyang { border-left-color: #3b82f6; }
    .speech-box-dunhuang { border-left-color: #10b981; }
    .speech-box-shidu { border-left-color: #f59e0b; }
    .speech-box-yuyang { border-left-color: #ef4444; }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 侧边栏：正典背景与系统架构
# ==============================================================================
with st.sidebar:
    st.markdown("### 🦅 鲲鹏志 · 正典大本营")
    st.caption("源自 `Seek-Key-LTD/kunpengzhi-podcast` 正典弹药库")
    
    st.divider()
    st.markdown("**📖 当前正典：第五期《陨》(S05)**")
    st.caption("“深空引力根本不在乎地上的皇帝姓王还是姓刘，它是纯粹客观的物理输入！”")

    st.divider()
    st.markdown("**🏛️ 物理智能车座底座 (4 节点)**")
    st.write("• **ch1** (春川): `moli.git4ta.fun` ➔ 庐阳先生")
    st.write("• **ch2** (春川): `muxu.git4ta.fun` ➔ 敦煌先生")
    st.write("• **ash1** (阿什本): `tumi.git4ta.fun` ➔ 十渡先生")
    st.write("• **ash2** (阿什本): `zhuyu.git4ta.fun` ➔ 渔阳先生")

    st.divider()
    st.markdown("**🛡️ 门禁与协议**")
    token_val = os.getenv("ASN_AGENT_TOKEN", "")
    token_display = f"`{token_val[:8]}...`" if token_val else "`未注入`"
    st.write(f"• **X-ASN-Token**: {token_display}")
    st.write("• **隧道回源**: `http://127.0.0.1:18790`")
    st.write("• **调度中枢**: 信号灯 (Semaphore)")

    st.divider()
    if st.button("🔄 刷新总控台", use_container_width=True):
        st.rerun()


# ==============================================================================
# 主屏 Header
# ==============================================================================
st.markdown("## 🦅 鲲鹏志 · 正典圆桌漫谈研判系统")
st.markdown("**第五期《陨》(S05)** · 解构“天火、深空引力、黄土年鉴与一个巨型系统如何彻底失去解释权”")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 核心理论公式 (LaTeX)
# ==============================================================================
with st.container():
    st.markdown("""
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.5rem; margin-bottom: 1.5rem;">
        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin-bottom: 0.3rem;">📊 S05 正典核心传导链与理论公式</div>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"F = G \frac{M m}{r^2} \implies \text{引力摄动} \implies \text{地质气候震荡} \implies \text{解释权反噬} \implies \text{政治熵增} \implies \text{系统重置}")

# ==============================================================================
# 4 席人物与物理车座看板
# ==============================================================================
st.markdown("##### 👥 圆桌 4 席人物格局与物理车座 (Hardware Chassis)")

cols = st.columns(4)
personas = [
    {
        "seat": "moli",
        "name": "庐阳先生",
        "title": "中科大天文与空间学院教授",
        "angle": "深空引力与天体力学",
        "node": "ch1",
        "region": "🇰🇷 韩国春川",
        "emoji": "🔭",
        "color": "#3b82f6",
        "duty": "柯伊伯带与木星引力弹弓，确立客观物理输入"
    },
    {
        "seat": "muxu",
        "name": "敦煌先生",
        "title": "兰大第四纪地质国重室教授",
        "angle": "地质年鉴与黄土序列",
        "node": "ch2",
        "region": "🇰🇷 韩国春川",
        "emoji": "📜",
        "color": "#10b981",
        "duty": "四十万年黄土剖面与海因里希H事件地质铁证"
    },
    {
        "seat": "tumi",
        "name": "十渡先生",
        "title": "中央民大名学与历史学教授",
        "angle": "天象政治化与解释权",
        "node": "ash1",
        "region": "🇺🇸 美区阿什本",
        "emoji": "🏛️",
        "color": "#f59e0b",
        "duty": "符命谶纬叙事瓦解，天火对政权合法性致命反噬"
    },
    {
        "seat": "zhuyu",
        "name": "渔阳先生",
        "title": "央财金融操盘手 · 法医审计席",
        "angle": "系统崩溃与宏观化疗",
        "node": "ash2",
        "region": "🇺🇸 美区阿什本",
        "emoji": "📊",
        "color": "#ef4444",
        "duty": "四次币制改革资产负债表归零，系统不可逆格式化"
    },
]

for i, p in enumerate(personas):
    with cols[i]:
        st.markdown(f"""
        <div class="persona-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.6rem;">{p['emoji']}</span>
                <span class="badge-node">{p['region']}</span>
            </div>
            <h4 style="margin: 0; color: #0f172a; font-weight: 700;">{p['name']}</h4>
            <div style="font-size: 0.8rem; color: #64748b; margin-bottom: 0.3rem;">{p['title']}</div>
            <div style="font-size: 0.85rem; color: {p['color']}; font-weight: 600; margin-bottom: 0.5rem;">【{p['angle']}】</div>
            <div style="font-size: 0.75rem; color: #475569; line-height: 1.4;">
                • 物理实体: <code>k-agent-{p['seat']}@{p['node']}</code><br>
                • 专属端点: <code>{p['seat']}.git4ta.fun</code><br>
                • 研判视角: {p['duty']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 正典背景与操作栏
# ==============================================================================
contract = st.session_state.get("contract") or default_contract()
meta = contract.get("meta", {})

with st.expander("📖 S05《陨》卷宗要件与核心脉络 (Canon Context)", expanded=False):
    st.write(meta.get("key_facts", ""))
    st.caption("提示：全体席位在漫谈开始前完成卷宗上下文对齐，各持切入角展开递进交锋。")

col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
with col_btn1:
    start_btn = st.button("🎙️ 启动正典圆桌漫谈 · 第五期《陨》(S05)", type="primary", use_container_width=True)
with col_btn2:
    ping_btn = st.button("📡 探测 4 节点端点心跳", use_container_width=True)
with col_btn3:
    clear_btn = st.button("🧹 清空漫谈记录", use_container_width=True)

if clear_btn:
    st.session_state.messages = []
    st.session_state.ping_results = {}
    st.rerun()

# 节点心跳快速拨测
if ping_btn:
    with st.spinner("正在向海外 4 节点固定隧道发起探活..."):
        p_res = {}
        token = os.getenv("ASN_AGENT_TOKEN", "")
        headers = {"X-ASN-Token": token, "Authorization": f"Bearer {token}"}
        for p in personas:
            sk = p["seat"]
            t0 = time.time()
            try:
                r = requests.get(f"https://{sk}.git4ta.fun/health", headers=headers, timeout=4)
                code = r.status_code
                dur = round((time.time() - t0) * 1000, 1)
                p_res[sk] = f"HTTP {code} ({dur}ms)"
            except Exception as e:
                p_res[sk] = f"待命/未开机 ({e.__class__.__name__})"
        st.session_state.ping_results = p_res

if st.session_state.get("ping_results"):
    st.info(" | ".join(f"**{sk}** ({FOUR_FLOWER_SEATS[sk].node}): `{v}`" for sk, v in st.session_state.ping_results.items()))

# ==============================================================================
# 圆桌漫谈执行调度
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if start_btn:
    st.session_state.messages = []
    progress_bar = st.progress(0, text="全体席位进入 S05《陨》漫谈场域，开始第一棒传递...")

    engine = RobertTokenRingEngine(article_text=meta.get("key_facts", ""), scenario="canon")
    topic_anchor = engine.draft_roundtable_topic(meta)
    engine.add_to_shared_context("🏛️ 正典立项", topic_anchor, team="canon_meta")

    seat_registry = {k: v.to_seat_dict() for k, v in FOUR_FLOWER_SEATS.items()}
    total_acts = len(contract.get("acts", []))

    def on_step_emit(msg, idx, total, act):
        st.session_state.messages.append(msg)
        progress_bar.progress(idx / total, text=f"【第 {idx}/{total} 棒】{msg['persona']} 正在开聊...")
        time.sleep(0.4)

    with st.spinner("4 席正典智能体正在推进跨国多维漫谈..."):
        engine.execute_contract(contract, seat_registry, emit_cb=on_step_emit)

    progress_bar.progress(1.0, text="🎉 S05《陨》4 席圆桌漫谈全流程圆满闭环！")
    st.balloons()
    st.rerun()


# ==============================================================================
# 漫谈实录流水呈现
# ==============================================================================
if st.session_state.get("messages"):
    st.markdown("### 🎙️ 正典圆桌漫谈发言实录 (Roundtable Stream)")

    box_classes = {
        "moli": "speech-box-luyang",
        "muxu": "speech-box-dunhuang",
        "tumi": "speech-box-shidu",
        "zhuyu": "speech-box-yuyang",
    }

    for idx, msg in enumerate(st.session_state.messages, 1):
        seat_k = ""
        for p in personas:
            if p["name"] in msg.get("header", ""):
                seat_k = p["seat"]
                break
        box_class = box_classes.get(seat_k, "speech-box")

        dur_text = f" · ⏱️ {msg.get('duration', 0)}s" if msg.get("duration") else ""
        status_text = f" · <span class='badge-live'>{msg.get('live_status', '')}</span>" if msg.get("live_status") else ""
        node_text = f"<code>{msg.get('k_agent', '')}</code>" if msg.get("k_agent") else ""

        st.markdown(f"""
        <div class="speech-box {box_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                <span style="font-weight: 700; font-size: 1.1rem; color: #0f172a;">
                    {msg.get('avatar', '🎙️')} 第 {idx} 棒 · {msg.get('header', '')}
                </span>
                <span style="font-size: 0.8rem; color: #64748b;">
                    {node_text}{dur_text}{status_text}
                </span>
            </div>
            <div style="font-size: 0.96rem; color: #1e293b; line-height: 1.7; white-space: pre-wrap;">
{msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        st.caption(f"S05 会话共收录 {len(st.session_state.messages)} 棒深刻交锋 | 时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col_s2:
        transcript_md = f"# 《{meta.get('title', '第五期 · 陨')}》正典圆桌漫谈实录\n\n"
        transcript_md += f"**核心公式**：{meta.get('core_formula', '')}\n\n---\n\n"
        for m in st.session_state.messages:
            transcript_md += f"### {m['avatar']} {m['header']} ({m.get('k_agent', '')})\n"
            transcript_md += f"{m['content']}\n\n"
        st.download_button(
            "💾 导出正典实录 (Markdown)",
            data=transcript_md,
            file_name=f"canon-roundtable-s05-{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True
        )

st.markdown("<br><hr><div style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>🦅 鲲鹏志 · 正典对抗生成网络 (ASN-GAN) · 2026</div>", unsafe_allow_html=True)
