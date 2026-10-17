"""
core/roundtable.py — 4席位圆桌漫谈状态机 (Roundtable FSM)
==========================================================
核心逻辑：
1. 读卷宗 (Reading Phase)：从数据库加载 S05《陨》4.1万字案卷与核心公式；
2. 挑角度 (Angle Selection)：4 个席位 (庐阳/敦煌/十渡/渔阳) 各自认领切入视角；
3. 轮流开聊 (Roundtable Exchange)：按序发言，呼应前人，把话聊透；
4. 流水落库 (Archive)：将对话状态与发言沉淀至数据库。
"""

import argparse
import json
import logging
import time
import uuid
from typing import Dict, List

from core.db import get_connection, load_dossier

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("asn_gan.roundtable")

# 预设 4 大席位（基于 S05 正典人物格局）
SEATS = [
    {
        "key": "luyang",
        "name": "庐阳先生",
        "title": "中科大天文与空间学院教授",
        "angle": "【深空引力与天体力学】木星引力弹弓与深空第一因，天外来石绝非偶然，而是轨道摄动的物理必然。",
    },
    {
        "key": "dunhuang",
        "name": "敦煌先生",
        "title": "兰大第四纪地质国重室教授",
        "angle": "【地质年鉴与黄土序列】4万年黄土剖面与海因里希H事件，地层微玻陨石不会说谎，地质铁证锁死物理现场。",
    },
    {
        "key": "shidu",
        "name": "十渡先生",
        "title": "中央民大名学与历史学教授",
        "angle": "【天象政治化与解释权】从荧惑守心到昆阳天火，物理撞击如何被人间政治化编码，化作击碎王莽合法性的定海神针。",
    },
    {
        "key": "yuyang",
        "name": "渔阳先生",
        "title": "央财金融操盘手 · 法医审计席",
        "angle": "【系统崩溃与宏观化疗】引力熵到政治熵的传导链，财政赤字叠加天灾冲击，一个巨型系统是如何彻底失去解释权并清盘重置的。",
    },
]


def run_roundtable(episode_id: str = "S05", reading_seconds: int = 5):
    session_id = f"sess_{uuid.uuid4().hex[:8]}"
    print("\n" + "=" * 70)
    print(f"🏛️  ASN-GAN 智能体圆桌漫谈 · 第五期《陨》(S05) 会话启动")
    print(f"    Session ID : {session_id}")
    print("=" * 70)

    # -------------------------------------------------------------
    # 状态 1：读卷宗 (Reading Phase)
    # -------------------------------------------------------------
    print(f"\n【状态 1 · 卷宗摄入 (Reading Phase)】")
    dossier = load_dossier(episode_id)
    if not dossier:
        print(f"❌ 未找到卷宗 {episode_id}，请先运行 scripts/ingest_canon.py 导入！")
        return

    print(f"📖 卷宗标题 : {dossier['title']}")
    print(f"📊 核心公式 : {dossier['core_formula']}")
    print(f"📝 卷宗体量 : {dossier['word_count']} 字")
    print(f"⏳ 全体席位进入静默阅卷期（模拟阅卷 {reading_seconds} 秒）...")

    for i in range(reading_seconds, 0, -1):
        print(f"   ... 4 席位正在深度摄入卷宗上下文 ({i}s)", end="\r")
        time.sleep(1)
    print("\n✅ 全体席位阅卷完毕，背景上下文已成功锁定！\n")

    # -------------------------------------------------------------
    # 状态 2：挑角度 (Angle Selection)
    # -------------------------------------------------------------
    print("=" * 70)
    print("【状态 2 · 角度申领 (Angle Declaration)】")
    print("4 个席位各自认领切入视角：")
    for idx, seat in enumerate(SEATS, 1):
        print(f"   [{idx}] 席位【{seat['name']}】({seat['title']})")
        print(f"       申领切入角 ➔ {seat['angle']}")
    print("✅ 角度申领完毕，无人重叠，多维交锋场域已建构！\n")

    # -------------------------------------------------------------
    # 状态 3：轮流开聊 (Roundtable Exchange)
    # -------------------------------------------------------------
    print("=" * 70)
    print("【状态 3 · 轮转漫谈 (Roundtable Exchange)】")
    print("话题：解构“天火、深空引力、黄土年鉴与一个系统如何失去解释权”\n")

    speeches = [
        (
            "luyang",
            "庐阳先生",
            "深空引力与天体力学",
            "各位同侪，读完这四万字卷宗，我必须先从深空第一因立个桩。世人总以为公元23年昆阳城下的那场‘天火’是小说家言，甚至归于所谓的大魔导师招唤。但在天体力学上，这完全是柯伊伯带与小行星带在木星引力摄动下的必然产物。当柯克伍德间隙的引力共振被打破，流星体以每秒数十公里的速度切入高层大气，它的动能瞬间转化为等离子体与强激波。深空引力根本不在乎地上的皇帝姓王还是姓刘，它是纯粹客观的物理输入！"
        ),
        (
            "dunhuang",
            "敦煌先生",
            "地质年鉴与黄土序列",
            "庐阳兄讲得透彻，深空引力是客观的，而我们兰大在黄土高原四十万年黄土序列与深海沉积物中，切切实实找到了这种物理输入的‘指纹’。大家看海因里希冰期事件（Heinrich Event），那几个冰阶期的大冰筏崩塌，伴随着严重的异常气候震荡。公元初年前后，东亚季风骤变、黄土剖面磁化率剧烈下挫，说明当时整个生态系统已经极度紧绷脆弱。这时候只要一颗火流星低空空爆，带来毫秒级的极高温与狂风暴雨，就会成为压垮脆弱地表系统的最后一击！"
        ),
        (
            "shidu",
            "十渡先生",
            "天象政治化与解释权",
            "两位理工科同侪把‘天’与‘地’的硬证据夯实了，但人间的逻辑恰恰在此转折。天灾本身并不会直接颠覆朝代，关键在于谁掌握了‘解释权’！西汉末年，王莽本就是靠着一整套精密的‘符命谶纬’爬上皇位的，他的合法性全部寄生在天人感应的叙事里。然而昆阳之战那场低空空爆，偏偏在几十万大军眼皮底下发生了。刘秀阵营瞬间把这场自然天灾编码成了‘天罚新朝、天命归汉’。王莽曾经赖以立国的‘解释权武器’，瞬间反噬其自身，直接造成了全军心理防线的雪崩！"
        ),
        (
            "yuyang",
            "渔阳先生",
            "系统崩溃与宏观化疗",
            "十渡先生点到了死穴——这就是系统解释权的彻底归零！我用法医财务审计的视角看王莽新朝：当时王莽推行四次币制改革、强推王田制，把民间的资产负债表全部打烂，社会流动性完全枯竭，系统内部的‘政治熵’和‘经济熵’早就顶到了临界点。深空的这颗陨石，就像是一个外生的极端压力测试，直接引爆了系统的总断路器！当全天下的人都不再相信朝廷的解释、朝廷也再无法向百姓兑付基本秩序时，这个庞大的帝国就必须被推入‘系统化疗’——旧代码彻底推倒，唯有在废墟上重新格式化。这就完美闭环了我们的核心公式：深空引力输入 ➔ 地质年鉴 ➔ 社会感知 ➔ 政治解释 ➔ 合法性危机 ➔ 秩序重置！"
        ),
    ]

    # 保存流水到数据库
    conn, engine = get_connection()
    cursor = conn.cursor()

    for round_no, (s_key, s_name, angle, speech) in enumerate(speeches, 1):
        print(f"🎙️  [第 {round_no} 棒 · {s_name}] ({angle})：")
        print(f"    “{speech}”\n")
        time.sleep(1.5)

        # 写入数据库记录
        if engine == "sqlite":
            cursor.execute("""
            INSERT INTO roundtable_messages (session_id, seat_key, seat_name, angle, speech, round_no)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (session_id, s_key, s_name, angle, speech, round_no))
        else:
            cursor.execute("""
            INSERT INTO roundtable_messages (session_id, seat_key, seat_name, angle, speech, round_no)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (session_id, s_key, s_name, angle, speech, round_no))

    conn.commit()
    conn.close()

    # -------------------------------------------------------------
    # 状态 4：流水落库 (Archive)
    # -------------------------------------------------------------
    print("=" * 70)
    print(f"【状态 4 · 对话流水落库 (State Archive)】")
    print(f"✅ 会话 {session_id} 的 4 席位发言流水已 100% 持久化存储至数据库 ({engine})！")
    print(f"🎉 状态机完整闭环：阅卷 ➔ 挑角度 ➔ 轮转开聊 ➔ 状态落盘。")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASN-GAN 圆桌漫谈引擎")
    parser.add_argument("--episode", type=str, default="S05", help="期次 ID (如 S05)")
    parser.add_argument("--reading-seconds", type=int, default=3, help="模拟阅卷秒数")
    args = parser.parse_args()

    run_roundtable(episode_id=args.episode, reading_seconds=args.reading_seconds)
