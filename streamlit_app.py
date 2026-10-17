from core.db import load_dossier
"""
⚡ ASN-GAN · 代理化社交网络对抗生成引擎 (12 黄道内阁与小花组) (加锁保护与 LXC 落宫规划)
=================================================================================
1. 🔐 Staging 云端防泄露访问控制：
   - PIN 码锁：简单 4 位密码 (默认 `3131`)。
2. 🏛️ 物理节点落宫与同构 LXC 规划：
   - 💎 Jasper (碧石 · 12内阁)：规划落宫至 `vault` 宿主 LXC 容器，确保密钥零延迟注入！
   - 🌸 Violet (紫罗兰 · 小花组 Manager)：规划落宫至 `warden` 宿主 LXC 容器，担当小花评审团掌门！
"""

import streamlit as st
import openai
import os
import time
import html
import json
import subprocess
from pathlib import Path
from core.token_ring import RobertTokenRingEngine
from core.contract import default_contract, summarize_contract
from core.script_compiler import compile_contract

# ⚙️ FIELD 场配置：field = 场景化节目容器（法庭只是其中一种场）
# trading panel 只显示「此刻」一个画面；content_source 决定素材通道
FIELD_REGISTRY = {
    "court": {
        "name": "⚖️ 法庭场（看盘式庭审）",
        "layout": "left=ticker / right=order flow / mid-top=trading panel(庭辩) / mid-bottom=news feed(笔录)",
        "content_source": "case",          # 案件卷宗（dossiers/ 本地）
        "gameplay": "庭辩对抗：12 黄道内阁 vs 公诉 · 剧本编译驱动",
    },
    "interrogation": {
        "name": "🕵️ 讯问场（调查阶段）",
        "layout": "left=讯问流 / right=证据笔录 / mid-top=被讯问人状态 / mid-bottom=攻心节奏",
        "content_source": "case",          # 似有暗香来调查阶段
        "gameplay": "讯问攻防：证据牌系统 + 心理防线模型（规划中）",
    },
    "studio": {
        "name": "📡 演播场（发布会/播报）",
        "layout": "left=ticker / right=order flow / mid-top=播报画面 / mid-bottom=news feed",
        "content_source": "essay",         # 鲲鹏志论述（gbrain RAG）
        "gameplay": "RAG 播报：gbrain 检索章节 → 编译剧本 → 播报（规划中）",
    },
}

DEFAULT_FIELD = "court"


def load_research_file(filepath):
    if not filepath or not os.path.exists(filepath):
        return ""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"加载文献失败: {e}"


def load_material(mtype: str, query: str = "") -> str:
    """统一调用层（大一统）：
    type=case  → dossiers/ 本地案卷文件（内容资产）
    type=essay → gbrain RAG 检索鲲鹏志论述（content 在 gbrain，不搬文件）
    """
    if mtype == "case":
        return load_research_file(query)
    if mtype == "essay":
        return gbrain_query(query)
    return ""


def gbrain_query(question: str, limit: int = 3) -> str:
    """gbrain RAG 检索（nuc 本地调用，VOYAGE_API_KEY 已纳管 /etc/environment）
    1) 先直接 get（question 为注册表 slug 时精确拉全文）
    2) 失败再 query 定位 slug → get 拉全文（--detail low 只给片段）
    """
    if not question:
        return ""
    env = dict(os.environ)
    try:
        # ① 直接 get：slug 精确拉取（如 第13章-黄河之水天上来）
        r0 = subprocess.run(
            [os.path.expanduser("~/.bun/bin/bun"), os.path.expanduser("~/.bun/bin/gbrain"),
             "get", question],
            capture_output=True, text=True, timeout=60, env=env,
        )
        full0 = (r0.stdout or "").strip()
        low0 = (full0 + (r0.stderr or "")).lower()
        if full0 and "not found" not in low0 and "error" not in low0 and "usage:" not in low0:
            return full0[:12000]

        # ② query 定位（自由文本）
        r = subprocess.run(
            [os.path.expanduser("~/.bun/bin/bun"), os.path.expanduser("~/.bun/bin/gbrain"),
             "query", question, "--detail", "low"],
            capture_output=True, text=True, timeout=90, env=env,
        )
        out = (r.stdout or "").strip()
        if not out or "No results" in out:
            r2 = subprocess.run(
                [os.path.expanduser("~/.bun/bin/bun"), os.path.expanduser("~/.bun/bin/gbrain"),
                 "search", question],
                capture_output=True, text=True, timeout=60, env=env,
            )
            out = (r2.stdout or "").strip()
        # 提取首个命中 slug（行首 [score] slug -- 标题）→ 拉全文
        import re
        m = re.search(r"^\[[0-9.]+\]\s+(\S+)\s+--", out, re.M)
        if m:
            slug = m.group(1)
            r3 = subprocess.run(
                [os.path.expanduser("~/.bun/bin/bun"), os.path.expanduser("~/.bun/bin/gbrain"),
                 "get", slug],
                capture_output=True, text=True, timeout=60, env=env,
            )
            full = (r3.stdout or "").strip()
            if full and len(full) > len(out):
                return full[:12000]
        return out[:12000]
    except Exception as e:
        return f"gbrain 检索失败: {e}"

st.set_page_config(
    page_title="鲲鹏志 · 12黄道内阁与紫罗兰掌门法庭",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔑 极简 Staging 密码锁 (PIN: 142857)
def check_password():
    # dev 环境（本地）跳过 PIN；staging(Heroku) 需要
    import os
    if os.environ.get("ENV", "") == "dev":
        return True
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        
    if not st.session_state.authenticated:
        st.markdown(
            """
            <div style="max-width: 420px; margin: 5rem auto; padding: 2rem; background: #fff7e6; border: 2px solid #FF9800; border-radius: 12px; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.5);">
                <h2 style="color: #FF9800; margin-bottom: 0.5rem;">🔐 鲲鹏志 · 预发环境访问锁</h2>
                <p style="color: #666; font-size: 0.9rem;">本环境受 Group Policy 保护，请输入访问 PIN 码</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            pin_input = st.text_input("🔑 访客 PIN 码：", type="password", key="pin_lock_input")
            if pin_input == "142857":
                st.session_state.authenticated = True
                st.success("🔓 验证通过！正在进入 ASN-GAN 对抗生成界面...")
                time.sleep(0.4)
                st.rerun()
            elif pin_input:
                st.error("❌ PIN 码不正确，请重新输入")
        return False
    return True

if not check_password():
    st.stop()

# 多环境：经环境变量注入（dev=本地 litellm / staging-Heroku=seekkey.eu.org），代码不硬编码
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://litellm.seekkey.eu.org/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-47318")

# 场景模式选择
SCENARIOS = {
    "court": "⚖️ ASN-GAN 庭辩朝堂模式",
    "honglou": "📿 《红楼梦》贾府大观园模式",
    "fengyue": "🍶 潇洒风月风流雅集模式"
}

# ==============================================================================
# ☀️ Vault Space 12 黄道内阁 & 🌸 昴宿七姐妹星团 (Agent Card 智能车座底座)
# ==============================================================================
# 架构铁律：
# 席位 (Seat) 是智能车座 (Agent Card)，模型代表底层发动机。
# 席位直接绑定全舰队 Agent 身份契约，不再硬编码单一模型。
from core.agent_card import AgentCardRegistry

# ☀️ 12 宝石黄道内阁车座
VAULT_ZODIAC_CABINETS = {
    card.key: card.to_seat_dict()
    for card in AgentCardRegistry.list_cabinet()
}

# 审判员 Luna & 被告人 Leopard (特别车座)
LUNA_JUDGE = AgentCardRegistry.get("luna").to_seat_dict()
DEFENDANT_SEAT = AgentCardRegistry.get("leopard").to_seat_dict()

# 🌸 昴宿七姐妹星团车座
FLOWER_PLEIADES_TABLE = {
    card.key: card.to_seat_dict()
    for card in AgentCardRegistry.list_flowers()
}

# 补充合议指令 (场景化指令)
_FLOWER_INSTRUCTIONS = {
    "meigui": "你是昴宿一【玫瑰】。针对庭审发表程序合议评议：复核深空物理与人间解释权传导程序，重点评议《刑法》第12条从旧兼从轻对2016年4月新规的阻断效力！",
    "qiangwei": "你是昴宿二【蔷薇】。针对庭审发表实体证据合议评议：复核1000万10次平价还本水单，确认中煤账目零亏空，认定四大罪名完全不成立！",
    "tumi": "你是昴宿三【荼蘼】。针对庭审发表社会常情合议评议：还原2015-2016山河四省最冷冬天的真实背景，认定尊长救助亲家属于无罪义举！",
    "zhuyu": "你是昴宿四【茱萸】。针对庭审发表刑法谦抑性评议：强调无财物收受与权钱交易对价时，不得以道德或拟制罪名构陷无辜！",
    "moli": "你是昴宿五【茉莉】。针对庭审发表证据闭环评议：强调书证效力优先于监委口供，1000万平进平出证明主观非法占有目的为零！",
    "muxu": "你是昴宿六【苜蓿】。针对庭审发表合议裁决评议：复核全体连绵小花组成员意见，确认控方起诉证据链断裂！",
    "violet": "你是昴宿七兼小花组掌门【紫罗兰】。作为 Flower Team Manager，代表全连绵小花组向审判长红宝石提交《无罪合议意见书》，建议依法宣告尊长无罪！",
}
for k, inst in _FLOWER_INSTRUCTIONS.items():
    if k in FLOWER_PLEIADES_TABLE:
        FLOWER_PLEIADES_TABLE[k]["instruction"] = inst


def render_custom_css():
    st.markdown("""
    <style>
      /* 纯白模式（暗黑切换后续加） */
      .stApp { background: #ffffff; color: #1a1a1a; }
      .block-container { padding-top: 2.5rem; padding-left: 1rem; padding-right: 1rem; }
      .stMarkdown, .stText, .stMarkdown p { color: #1a1a1a !important; }
      .circle-progress-widget {
        position: fixed; bottom: 28px; right: 28px; z-index: 999999;
        display: flex; align-items: center; justify-content: center;
        width: 72px; height: 72px; border-radius: 50%;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45); cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      }
      .circle-progress-widget:hover { transform: scale(1.08); }
      .circle-inner {
        width: 58px; height: 58px; border-radius: 50%;
        background: #121214; display: flex; flex-direction: column;
        align-items: center; justify-content: center; color: #FFFFFF;
        font-weight: bold; font-size: 0.78rem; text-align: center; line-height: 1.1;
      }
      .circle-percent { font-size: 0.95rem; color: #FF9800; font-weight: 800; }
      /* 左 sidebar = 25%（用户目标 25/50/25）。展开态才生效，不破坏折叠功能；
         max-width 覆盖 Streamlit 折叠态 emotion clamp（max-width:0），25vw 封顶 480px 防超宽屏 */
      [data-testid="stSidebar"][aria-expanded="true"] {
        width: min(25vw, 480px) !important;
        max-width: min(25vw, 480px) !important;
        min-width: 300px;
      }
      /* order flow（右）：可滚动信息流（像 ticker 一样独立滚动） */
      .stMain [data-testid="stColumn"]:last-child > div {
        max-height: calc(100vh - 140px);
        overflow-y: auto;
        padding-right: 6px;
      }
      /* ===== 看盘式 fixed 布局（用户术语：ticker | trading panel + news feed | order flow） ===== */
      /* trading panel（中区上半）：固定视口，只渲染当前阶段/当前发言，不堆叠历史。高度 = 黄金分割 0.618 */
      .trading-panel {
        height: calc((100vh - 300px) * 0.618);
        min-height: 300px;
        border: 2px solid #FF9800;
        border-radius: 10px;
        padding: 12px 16px;
        background: #fafafa;
        overflow-y: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
      }
      .trading-panel .focus-stage { font-size: 0.82rem; color: #FF9800; font-weight: 700; border-bottom: 1px solid #FFE0B2; padding-bottom: 6px; margin-bottom: 8px; }
      .trading-panel .focus-speaker { font-size: 1.05rem; font-weight: 800; margin-bottom: 6px; }
      .trading-panel .focus-content { font-size: 0.92rem; line-height: 1.65; color: #222; white-space: pre-wrap; }
      /* news feed（中区下半）：固定高度内部可滚（黄金分割 0.382） */
      .news-feed {
        height: calc((100vh - 300px) * 0.382);
        min-height: 140px;
        border: 1px solid #ddd; border-radius: 8px;
        padding: 10px 14px; background: #f8f9fa; overflow-y: auto;
        font-size: 0.84rem;
      }
      /* order flow（右栏）：全量历史可滚 */
      .order-flow {
        max-height: calc(100vh - 420px); min-height: 180px;
        overflow-y: auto; border: 1px solid #eee; border-radius: 8px;
        padding: 10px; background: #fff; font-size: 0.83rem;
      }
      /* 中区起诉书：限高内部滚，不撑破 fixed 视口 */
      .indictment-box {
        max-height: 200px; overflow-y: auto;
        background: #fff8f0; border-left: 4px solid #B71C1C;
        padding: 10px; border-radius: 6px; font-size: 0.88rem;
      }
    </style>
    """, unsafe_allow_html=True)

render_custom_css()

# 场景选择
selected_scenario_key = "court"  # 模式由 Coding Agent 剧本决定（暂固定 court）

# Session Contract：Coding Agent（编剧室）编译产物，驱动阶段流与发言序列
if "contract" not in st.session_state:
    st.session_state.contract = default_contract()
if "material_text" not in st.session_state:
    st.session_state.material_text = ""


def get_stages():
    """阶段流从当前契约读取（无契约时回退内置S05·陨）"""
    c = st.session_state.get("contract")
    if c and c.get("stage_flow"):
        return c["stage_flow"]
    return default_contract()["stage_flow"]

def render_progress_components(current_stage):
    if "current_stage_id" not in st.session_state:
        st.session_state.current_stage_id = 0
        current_stage = 0
    current_stage = int(current_stage or 0)
    pct = min(int((current_stage / 5.0) * 100), 100)

    # 1. 顶部 Sticky Banner：分段式进度条
    segments_html = ""
    for stage in get_stages():
        if stage["id"] < current_stage:
            color = "#4CAF50"
        elif stage["id"] == current_stage:
            color = "#FF9800"
        else:
            color = "#444444"
        segments_html += f'<div style="flex: 1; height: 8px; border-radius: 4px; background-color: {color}; transition: all 0.3s;"></div>'
    titles_html = ""
    for stage in get_stages():
        style = "color: #FF9800; font-weight: bold;" if stage["id"] == current_stage else ("color: #81C784;" if stage["id"] < current_stage else "color: #777;")
        titles_html += f'<span style="{style}">{stage["emoji"]} {stage["name"]}</span>'

    top_banner = f"""
    <div style="position: sticky; top: 0rem; z-index: 99999; background: #121214; border-bottom: 2px solid #FF9800; padding: 10px 16px; margin-bottom: 1rem; border-radius: 0 0 8px 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
      <div style="display: flex; gap: 8px; margin-bottom: 8px;">
        {segments_html}
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.82rem; overflow-x: auto;">
        {titles_html}
      </div>
    </div>
    """
    st.markdown(top_banner, unsafe_allow_html=True)

    # 2. 右下角悬浮圆形进度徽章 (conic-gradient 环形充盈)
    deg = int((pct / 100) * 360)
    circle_bg = f"conic-gradient(#FF9800 0deg {deg}deg, #333333 {deg}deg 360deg)"
    circle_widget = f"""
    <div class="circle-progress-widget" style="background: {circle_bg};" title="当前庭审进度：{pct}% ({current_stage}/5 阶段)">
      <div class="circle-inner">
        <span class="circle-percent">{pct}%</span>
        <span style="font-size: 0.65rem; color: #AAA;">{current_stage}/5 阶段</span>
      </div>
    </div>
    """
    st.markdown(circle_widget, unsafe_allow_html=True)

render_progress_components(st.session_state.get("current_stage_id", 0))

def render_speaker_ticker(current_speaker=None):
    """左区（sidebar）：发言者 ticker——谁在发言→高亮"""
    spk = current_speaker or st.session_state.get("current_speaker", "")
    for k, v in VAULT_ZODIAC_CABINETS.items():
        avatar = v["avatars"].get(selected_scenario_key, v["avatars"].get("court", k))
        if k == spk:
            st.markdown(f"<div style='background:#FF980033;border-left:3px solid #FF9800;padding:4px 8px;border-radius:4px;margin:2px 0;'><b>💬 {avatar}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:#777;padding:4px 8px;border-left:3px solid transparent;'>💎 {avatar}</div>", unsafe_allow_html=True)
    for k, v in FLOWER_PLEIADES_TABLE.items():
        avatar = v.get("avatars", {}).get("court", k)
        st.markdown(f"<div style='color:#9c27b0;padding:4px 8px;'>🌸 {avatar}</div>", unsafe_allow_html=True)

def render_stage_progress():
    """右区（25%）：刑事诉讼法流程进度——当前步高亮（给 layperson）"""
    st.markdown("### ⚖️ 刑事诉讼法·庭审进度")
    cur = st.session_state.get("current_stage_id", 0)
    for stage in get_stages():
        sid = stage["id"]
        if sid < cur:
            mark, style = "✅", "color:#4CAF50;"
        elif sid == cur:
            mark, style = "▶️", "color:#FF9800;font-weight:bold;background:#FF980022;"
        else:
            mark, style = "⏳", "color:#888;"
        st.markdown(f"<div style='{style}padding:6px 8px;border-radius:4px;margin:2px 0;'>{mark} {stage['emoji']} {stage['name']}</div>", unsafe_allow_html=True)

def render_trading_panel():
    """trading panel（fixed 视口）：只显示「此刻」——当前阶段 + 当前发言（不堆叠历史）"""
    cur = st.session_state.get("current_stage_id", 0)
    stage = next((s for s in get_stages() if s["id"] == cur), None)
    if stage:
        stage_html = f'<div class="focus-stage">{stage["emoji"]} 阶段 {stage["id"]}/5：{stage["name"]} — {stage["desc"]}</div>'
    else:
        stage_html = '<div class="focus-stage">⚖️ 庭审尚未开始 —— 敲响法槌后，「此刻」画面将在此固定呈现（看盘式 fixed 核心）</div>'

    msgs = st.session_state.get("messages", [])
    if msgs:
        msg = msgs[-1]
        speaker = html.escape(str(msg.get("role", "")))
        avatar = html.escape(str(msg.get("avatar", "🗣️")))
        # role 常已带头像 emoji（如 "🏛️ 审判长 · 红宝石尊者"），避免与 avatar 重复
        if speaker.startswith(avatar) and len(speaker) > len(avatar):
            speaker = speaker[len(avatar):].strip()
        content = html.escape(str(msg.get("content", "")))
        html_out = f"""
        <div class="trading-panel">
          {stage_html}
          <div class="focus-speaker">{avatar} {speaker}</div>
          <div class="focus-content">{content}</div>
        </div>
        """
    else:
        contract = st.session_state.get("contract") or default_contract()
        meta = contract.get("meta", {})
        note = meta.get("compile_note", "")
        summary = summarize_contract(contract)
        html_out = f"""
        <div class="trading-panel">
          {stage_html}
          <div class="focus-speaker" style="color:#999;">🎬 剧本已就绪 —— 敲响法槌开演</div>
          <div class="focus-content" style="font-size:0.85rem;color:#555;">{html.escape(summary)}</div>
          <div class="focus-content" style="font-size:0.8rem;color:#c62828;">{html.escape(note)}</div>
        </div>
        """
    st.markdown(html_out, unsafe_allow_html=True)


def render_news_feed():
    """news feed（中区下半，固定高度）：实时总结流 + 小花组媒体评论"""
    parts = ['<div class="news-feed">']
    parts.append("<b>📰 场外媒体评论团（小花组 · 异步）</b>")
    media_views = {
        "🌸 玫瑰（BBC 视角）": "程序正义与证据链：'利用影响力'与'私人信用'的边界是本案法理核心。",
        "🌸 茉莉（CCTV 视角）": "国企合规与党纪要求：未报备的救急行为存在程序瑕疵。",
        "🌸 紫罗兰（Flower Manager）": "汇总：事实层面资金闭环无亏空，程序层面存在'未报备'瑕疵——法理与情理对峙。",
    }
    for k, v in media_views.items():
        parts.append(f"<div style='margin:3px 0;'><b>{html.escape(k)}</b>：{html.escape(v)}</div>")
    parts.append("<hr style='border-color:#ddd;margin:8px 0;'/>")
    parts.append("<b>📜 庭审实时总结流</b>")
    msgs = st.session_state.get("messages", [])
    if msgs:
        for msg in msgs[-6:]:
            head = html.escape((msg.get("header") or "")[:40])
            snippet = html.escape(((msg.get("content") or "").replace("\n", " "))[:70])
            parts.append(f"<div style='margin:3px 0;'>• <b>{head}</b>：{snippet}…</div>")
    else:
        parts.append("<div style='color:#999;'>庭审尚未开始——每步发言将实时滚动总结。</div>")
    parts.append("</div>")
    st.markdown("\n".join(parts), unsafe_allow_html=True)


def render_order_flow():
    """order flow（右）：全量历史笔录（可滚）——历史移去滚动区，trading panel 只留「此刻」"""
    msgs = st.session_state.get("messages", [])
    if not msgs:
        st.caption("庭审尚未开始——全量笔录将在此滚动呈现。")
        return
    parts = []
    for msg in msgs:
        head = html.escape(str(msg.get("header") or msg.get("role") or ""))
        avatar = html.escape(str(msg.get("avatar", "🗣️")))
        content = html.escape(((msg.get("content") or "").replace("\n", " "))[:400])
        parts.append(
            f"<div style='margin:6px 0;padding:6px 8px;border-left:3px solid #FF9800;background:#fdfdfd;border-radius:4px;'>"
            f"<b>{avatar} {head}</b><br/><span style='color:#555;'>{content}…</span></div>"
        )
    st.markdown(f'<div class="order-flow">{"".join(parts)}</div>', unsafe_allow_html=True)


def build_court_markdown() -> str:
    contract = st.session_state.get("contract") or default_contract()
    meta = contract.get("meta", {})
    lines = ["# 🦅 鲲鹏志 · 法庭实录", ""]
    lines.append(f"剧本: {meta.get('title', '?')} · 协议: {contract.get('protocol')}")
    lines.append(f"阶段进度: {st.session_state.get('current_stage_id', 0)}/5")
    lines.append("")
    if st.session_state.get("indictment_text"):
        lines += ["## 📜 起诉书 (阜检刑诉〔2026〕88号)", st.session_state.indictment_text, ""]
    for msg in st.session_state.get("messages", []):
        lines += [f"### {msg['header']}", msg.get("content", ""), ""]
    return "\n".join(lines)


def save_court_transcript() -> str:
    from core.archive import save_run
    return save_run(
        "法庭", "S05-ASN庭辩朝堂", build_court_markdown(),
        {"steps": len(st.session_state.get("messages", [])), "scenario": selected_scenario_key},
    )


mid_col, right_col = st.columns([2, 1], gap="small")
with right_col:
    render_stage_progress()
    st.markdown("### 📜 庭审笔录（全量 · 可滚）")
    order_flow_ph = st.empty()
    with order_flow_ph.container():
        render_order_flow()





with mid_col:
    cur_c = st.session_state.get("contract") or default_contract()
    st.markdown(f'<div class="main-title">⚡ ASN-GAN · 《{cur_c["meta"].get("title", "第五期 · 陨")}》 代理化社交网络对抗生成朝堂</div>', unsafe_allow_html=True)
    cur_c = st.session_state.get("contract") or default_contract()
    st.markdown(f'<div class="sub-title">☀️ 12 黄道内阁 + 🌸 昴宿七姐妹 · 剧本：<b>{cur_c["meta"].get("title", "?")}</b> · 协议：<b>{cur_c.get("protocol")}</b> · {len(cur_c.get("acts", []))} 幕</div>', unsafe_allow_html=True)

    # 🎛️ FIELD 选择器（场 = 场景化节目容器）
    field_key = st.session_state.get("field", DEFAULT_FIELD)
    field_opts = list(FIELD_REGISTRY.keys())
    field_names = [FIELD_REGISTRY[k]["name"] for k in field_opts]
    sel_field = st.sidebar.radio("🎛️ 场 (Field)", field_names, index=field_opts.index(field_key) if field_key in field_opts else 0, key="field_selector")
    selected_field = field_opts[field_names.index(sel_field)]
    if selected_field != field_key:
        st.session_state.field = selected_field
        st.rerun()
    field_cfg = FIELD_REGISTRY[selected_field]
    st.sidebar.caption(f"⚙️ {field_cfg['gameplay']}")

    with st.sidebar:
        # 🎬 Coding Agent 编剧室：任意文本 → 剧本编译（Session Contract）
        with st.expander("🎬 Coding Agent 编剧室 · 剧本编译", expanded=False):
            new_material = st.text_area("📝 新素材（粘贴案件/纪实/章节文本）", height=120, key="new_material_input")
            col_a, col_b = st.columns(2)
            with col_a:
                compile_btn = st.button("🧪 编译剧本", use_container_width=True)
            with col_b:
                load_s05_btn = st.button("📥 载入《S05·陨》", use_container_width=True)
            if compile_btn:
                if new_material.strip():
                    with st.spinner("🎬 编剧室编译中（解析→绑定→挂载→校验）..."):
                        c = compile_contract(new_material, OPENAI_BASE_URL, OPENAI_API_KEY)
                    st.session_state.contract = c
                    st.session_state.material_text = new_material
                    st.session_state.messages = []
                    st.session_state.indictment_text = ""
                    st.session_state.current_stage_id = 0
                    note = c["meta"].get("compile_note", "")
                    st.success(f"✅ 编译完成：{c['meta'].get('title')} · {c.get('protocol')} · {len(c.get('acts', []))} 幕")
                    if note:
                        st.warning(f"回退说明：{note}")
                    st.rerun()
                else:
                    st.warning("请先粘贴素材文本")
            if load_jizhou_btn:
                st.session_state.contract = default_contract()
                st.session_state.material_text = ""
                st.session_state.messages = []
                st.session_state.indictment_text = ""
                st.session_state.current_stage_id = 0
                st.rerun()
            cur_c = st.session_state.get("contract") or default_contract()
            st.caption(f"当前剧本：{cur_c['meta'].get('title', '?')} · 协议 {cur_c.get('protocol')} · {len(cur_c.get('acts', []))} 幕")

        # 📚 卷宗素材库（RAG 统一调用层）：case=本地案卷 / essay=gbrain 论述
        with st.expander("📚 卷宗素材库 · RAG（case 本地 / essay gbrain）", expanded=False):
            essay_books = []
            essay_dir = Path(__file__).parent / "dossiers" / "论述"
            if essay_dir.exists():
                essay_books = [f.stem for f in sorted(essay_dir.glob("*.json"))]
            mtype = st.radio("素材类型", ["essay（gbrain 论述）", "case（本地案卷）"], horizontal=True, key="rag_mtype")
            if mtype.startswith("essay"):
                if essay_books:
                    book = st.selectbox("📖 书目", essay_books, key="rag_book")
                    meta = json.load(open(essay_dir / f"{book}.json", encoding="utf-8"))
                    chap_titles = [f"{c['title']}（{c['slug']}）" for c in meta["chapters"]]
                    chap = st.selectbox("章节", chap_titles, key="rag_chap")
                    if st.button("🔍 拉取 gbrain 章节", use_container_width=True, key="rag_fetch"):
                        slug = chap.split("（")[-1].rstrip("）")
                        with st.spinner("gbrain 检索中..."):
                            text = load_material("essay", slug)
                        if text and not text.startswith("gbrain 检索失败"):
                            st.session_state.material_text = text
                            st.session_state.rag_source = f"gbrain/{book}/{slug}"
                            st.session_state.messages = []
                            st.session_state.indictment_text = ""
                            st.session_state.current_stage_id = 0
                            st.success(f"✅ 已拉取 {book}/{slug}（{len(text)} 字符）→ 可编译剧本")
                            st.rerun()
                        else:
                            st.warning(text or "gbrain 未命中")
                else:
                    st.caption("无 dossiers/论述 注册表（可先在仓库添加）")
            else:
                case_opts = ["S05 · 第五期《陨》(陨石与解释权)", "S01 · 第一期《丹》", "S02 · 第二期《哗》", "S04 · 第四期《玺》", "S08.5 · 天权《银道》", "S12 · 第十二期《黄道》"]
                sel_case = st.selectbox("📁 案卷", case_opts, key="rag_case")
                if st.button("📥 载入正典卷宗", use_container_width=True, key="rag_case_btn"):
                    ep_key = sel_case.split(" · ")[0].strip()
                    d = load_dossier(ep_key)
                    if d:
                        st.session_state.material_text = d["content_md"]
                        st.session_state.rag_source = d["title"]
                        st.session_state.messages = []
                        st.session_state.indictment_text = ""
                        st.session_state.current_stage_id = 0
                        st.success(f"✅ 已载入 {d['title']}（{d['word_count']} 字符）")
                        st.rerun()
                    else:
                        st.warning(f"数据库中未找到 {ep_key} 卷宗，请先运行 ingest 导入！")
            if st.session_state.get("rag_source"):
                st.caption(f"当前素材源：{st.session_state.rag_source}")

        st.markdown("### 📊 席位实时状态（ticker）")
        render_speaker_ticker()
        st.divider()
        st.markdown("### ☀️ Vault 12 黄道内阁 · Agent Card 智能车座")
        for k, v in VAULT_ZODIAC_CABINETS.items():
            avatar = v["avatars"].get(selected_scenario_key, v["avatars"]["court"])
            soul = f" ({v['soul_name']})" if v.get("soul_name") else ""
            matrix = f" | `{v['matrix_id']}`" if v.get("matrix_id") else ""
            st.caption(f"• **{v['base_stone']}**{soul}: **{avatar}** (`k-agent-{k}@{v['node']}`{matrix})")
        
        st.divider()
        st.markdown("### 🌸 昴宿七姐妹星团 · K-Agent 车座")
        for k, v in FLOWER_PLEIADES_TABLE.items():
            avatar = v["avatars"].get(selected_scenario_key, v["avatars"]["court"])
            soul = f" ({v['soul_name']})" if v.get("soul_name") else ""
            matrix = f" | `{v['matrix_id']}`" if v.get("matrix_id") else ""
            st.caption(f"• **{v['base_stone']}**{soul}: **{avatar}** (`k-agent-{k}@{v['node']}`{matrix})")


        st.divider()
        if st.button("💾 保存庭审实录 (本地 + MinIO + lake1)", use_container_width=True):
            if st.session_state.get("messages"):
                try:
                    fname = save_court_transcript()
                    st.success(f"✅ 已落盘存档: {fname}")
                except Exception as e:
                    st.warning(f"落盘失败（不影响笔录展示）: {e}")
            else:
                st.warning("暂无庭审笔录可保存")

    # 默认从数据库底座读取 S05 陨石正典
    if "material_text" not in st.session_state:
        s05_dossier = load_dossier("S05")
        if s05_dossier:
            st.session_state.material_text = s05_dossier["content_md"]
            st.session_state.rag_source = s05_dossier["title"]
    article_text = st.session_state.get("material_text", "")
    cur_c = st.session_state.get("contract") or default_contract()
    cur_title = cur_c["meta"].get("title", "第五期 · 陨")

    with st.expander(f"📌 当期正典卷宗全文与核心公式（{cur_title}）", expanded=False):
        st.markdown(f"### **议题：{cur_c['meta'].get('topic', '天火、深空引力与系统解释权')}**")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**核心公式**：{cur_c['meta'].get('core_formula', '深空引力输入 ➔ 极端气候地质年鉴 ➔ 社会感知 ➔ 政治解释 ➔ 合法性危机 ➔ 秩序重置')}")
        with col2:
            st.success(f"**争议焦点**：{cur_c['meta'].get('focus', '引力熵到政治熵的传导链；系统如何失去解释权')}")
        st.caption(f"**案卷事实**：{cur_c['meta'].get('key_facts', '')}")
        
        if article_text:
            st.markdown(f'<div style="background:#f8f9fa;padding:10px;border-left:4px solid #B71C1C;font-size:0.88rem;max-height:180px;overflow-y:auto;">{article_text[:2500]}...\n\n*(共 {len(article_text)} 字符全量案卷)*</div>', unsafe_allow_html=True)

    st.divider()

    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        start_btn = st.button("⚖️ 敲响法槌 · 启动 12 黄道与紫罗兰掌门法庭演练", type="primary", use_container_width=True)
    with col_btn2:
        clear_btn = st.button("🧹 清空庭审笔录", use_container_width=True)

    if clear_btn:
        st.session_state.messages = []
        st.session_state.indictment_text = ""
        st.session_state.current_stage_id = 0
        st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "indictment_text" in st.session_state and st.session_state.indictment_text:
        st.markdown("### 📜 公诉机关独立撰写之正式起诉书")
        st.markdown(f'<div class="indictment-box">{st.session_state.indictment_text}</div>', unsafe_allow_html=True)

    # ===== trading panel + news feed（用户术语）：只渲染「此刻」一个画面 =====
    # 历史不在此堆叠——已移去 order flow（右）滚动区（render_order_flow）
    trading_panel_ph = st.empty()
    news_feed_ph = st.empty()
    with trading_panel_ph.container():
        render_trading_panel()
    with news_feed_ph.container():
        render_news_feed()

    if start_btn:
        contract = st.session_state.get("contract") or default_contract()
        meta = contract.get("meta", {})
        st.session_state.messages = []
        st.session_state.current_stage_id = 1
        engine = RobertTokenRingEngine(OPENAI_BASE_URL, OPENAI_API_KEY, article_text, selected_scenario_key)
    
        st.session_state.current_stage_id = 2
        topaz_avatar = VAULT_ZODIAC_CABINETS["topaz"]["avatars"].get(selected_scenario_key, VAULT_ZODIAC_CABINETS["topaz"]["avatars"]["court"])
        case_no = meta.get("case_number") or ""
        with st.spinner(f"⚖️ 公诉团队 ({topaz_avatar}) 正在独立撰写《起诉书》..."):
            indictment_text = engine.draft_official_indictment(meta)
            st.session_state.indictment_text = indictment_text
            # 流式会话文件：边跑边写，中断不丢已发言
            from core.archive import open_stream, append_stream
            title = meta.get("title") or "S05·陨"
            court = meta.get("court_name") or "ASN庭辩朝堂"
            path, filename, ts = open_stream("法庭", f"{title}-{court}")
            st.session_state.stream_path, st.session_state.stream_file, st.session_state.stream_ts = path, filename, ts
            append_stream(path, f"📜 起诉书 ({case_no or '未编号'})", indictment_text)
            st.rerun()

    if "indictment_text" in st.session_state and st.session_state.indictment_text and len(st.session_state.messages) == 0:
        contract = st.session_state.get("contract") or default_contract()
        meta = contract.get("meta", {})
        engine = RobertTokenRingEngine(OPENAI_BASE_URL, OPENAI_API_KEY, article_text, selected_scenario_key)
        topaz_avatar = VAULT_ZODIAC_CABINETS["topaz"]["avatars"].get(selected_scenario_key, VAULT_ZODIAC_CABINETS["topaz"]["avatars"]["court"])
        engine.add_to_shared_context(topaz_avatar, f"【起诉书全景】:\n{st.session_state.indictment_text}", team="indictment")
        intel_path = Path(__file__).resolve().parent / "research" / "反方弹药-恶意揣测.md"
        if intel_path.exists():
            engine.add_to_shared_context(
                topaz_avatar, f"【反方内部研判·恶意揣测全景】:\n{intel_path.read_text(encoding='utf-8')}",
                team="prosecution_intel",
            )
    
        progress_bar = st.progress(0, text="正在敲响法槌，传唤当事人到庭...")

        # 座位注册表：12 石 + 附席 + 7 花（契约 seat 引用 → 座位信息）
        seat_registry = {}
        seat_registry.update(VAULT_ZODIAC_CABINETS)
        seat_registry.update(FLOWER_PLEIADES_TABLE)
        seat_registry["luna"] = LUNA_JUDGE
        seat_registry["leopard"] = DEFENDANT_SEAT

        stage_count = len(contract.get("stage_flow", []))

        def _on_emit(msg, idx, total_steps, act):
            """每步发言落地：入库 + 进度 + 看盘三区刷新 + 流式落盘"""
            st.session_state.messages.append(msg)
            st.session_state.current_stage_id = act.get("stage", 0)
            progress_bar.progress(idx / total_steps, text=f"【阶段 {act.get('stage')}/{stage_count} 推进 -> {msg['header']}】 ...")
            # 流式落盘：每席发言实时追加，不等待整轮结束
            if st.session_state.get("stream_path"):
                from core.archive import append_stream
                append_stream(st.session_state["stream_path"], msg["header"], msg["content"])
            # 看盘式：trading panel 只替换「此刻」画面，不堆叠历史；历史进 order flow（右）
            with trading_panel_ph.container():
                render_trading_panel()
            with news_feed_ph.container():
                render_news_feed()
            with order_flow_ph.container():
                render_order_flow()
            time.sleep(0.5)

        # 契约驱动：Coding Agent 编译的 Session Contract 决定发言序列（不再写死 COURT_FLOW）
        engine.execute_contract(contract, seat_registry, emit_cb=_on_emit)

        st.session_state.current_stage_id = stage_count
        progress_bar.progress(1.0, text="⚖️ 全流程落幕！全案笔录已永久驻留！")
        try:
            from core.archive import close_stream
            title = meta.get("title") or "S05·陨"
            court = meta.get("court_name") or "ASN庭辩朝堂"
            fname = close_stream(
                st.session_state["stream_path"], st.session_state["stream_file"],
                st.session_state["stream_ts"], "法庭", f"{title}-{court}",
                {"steps": len(st.session_state.get("messages", [])), "protocol": contract.get("protocol"), "scenario": selected_scenario_key},
            )
            st.success(f"💾 庭审实录已流式落盘 (本地 + MinIO + lake1): {fname}")
        except Exception as e:
            st.warning(f"自动落盘失败（不影响笔录展示）: {e}")
        st.balloons()
        st.rerun()

    # ============ 底部 newsfeed：实时总结流 + 小花组媒体评论（异步） ============
    st.divider()
    # ============ news feed 已并入中区固定区域（render_news_feed） ============

    st.divider()
    st.markdown(
        "<div style='text-align:center;color:#888;font-size:0.85rem;padding:1.5rem 0;'>"
    "🦅 鲲鹏志 AI · 12 黄道内阁 + 昴宿七姐妹 (紫罗兰 Manager) · 2026"
    "</div>",
    unsafe_allow_html=True
)
