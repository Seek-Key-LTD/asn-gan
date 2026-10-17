"""
core/canon.py — 《鲲鹏志·正典》(Canon) 卷宗摄入与解析模块
=========================================================
专事从 kunpengzhi-podcast 弹药库拉取权威正稿，并灌入美区 river2 (OCI MySQL) 数据库。
"""

import base64
import json
import logging
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

log = logging.getLogger("asn_gan.canon")

# GitHub 弹药库仓库
PODCAST_REPO = "Seek-Key-LTD/kunpengzhi-podcast"
CANON_DIR = "content/canon"

# 期次文件名映射表
EPISODE_FILE_MAP = {
    0: "三更道场_第零期_缘起_正稿_普通话版.md",
    1: "三更道场_第一期_丹_正稿_普通话版.md",
    2: "三更道场_第二期_哗_正稿_普通话版.md",
    3: "三更道场_第三期_瑟_正稿_普通话版.md",
    4: "三更道场_第四期_玺_正稿_普通话版.md",
    5: "三更道场_第五期_陨_正稿_普通话版.md",
    6: "三更道场_第六期_翡_正稿_普通话版.md",
    7: "三更道场_第七期_血酬_正稿_普通话版.md",
    8: "三更道场_第八期_铁幕_正稿_普通话版.md",
    8.5: "三更道场_第八期半_天权_正稿_普通话版.md",
    9: "三更道场_第九期_回音_正稿_普通话版.md",
    10: "三更道场_第十期_割席_正稿_普通话版.md",
    11: "三更道场_第十一期_筑基_正稿_普通话版.md",
    12: "三更道场_第十二期_黄道_正稿_普通话版.md",
}


@dataclass
class CanonEpisode:
    episode_id: str
    episode_num: float
    name: str
    title: str
    core_formula: str
    cast: List[str]
    summary: str
    content_md: str
    word_count: int


def fetch_canon_from_github(episode_num: float = 5.0) -> CanonEpisode:
    """通过 GitHub API / gh CLI 从 kunpengzhi-podcast 仓库拉取指定期次的正典原文"""
    filename = EPISODE_FILE_MAP.get(episode_num)
    if not filename:
        raise ValueError(f"未收录期次 S{episode_num}，可选期次: {list(EPISODE_FILE_MAP.keys())}")

    path = f"{CANON_DIR}/{filename}"
    log.info(f"正在从 {PODCAST_REPO} 拉取正典卷宗: {path} ...")

    try:
        cmd = ["gh", "api", f"repos/{PODCAST_REPO}/contents/{path}?ref=hugo"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        content_b64 = data.get("content", "")
        raw_md = base64.b64decode(content_b64).decode("utf-8")
        return parse_canon_markdown(episode_num, raw_md)
    except Exception as e:
        log.error(f"GitHub API 拉取失败 ({e})，尝试检查本地 fixtures 缓存...")
        cache_path = f"./fixtures/canon_s{int(episode_num):02d}.json"
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                cdata = json.load(f)
                return CanonEpisode(**cdata)
        raise


def parse_canon_markdown(episode_num: float, raw_md: str) -> CanonEpisode:
    """解析正典 Markdown，提取人物、核心公式与纲要"""
    # 提取标题
    title_match = re.search(r"^#\s+(.+)$", raw_md, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else f"三更道场 第{episode_num}期"

    # 提取核心公式
    formula_match = re.search(r"核心公式：\s*\*\*(.+?)\*\*", raw_md)
    core_formula = formula_match.group(1).strip() if formula_match else ""

    # 提取纲要
    gang_match = re.search(r"纲：\s*\*\*(.+?)\*\*", raw_md)
    summary = gang_match.group(1).strip() if gang_match else ""

    # 提取出场人物声纹格局
    cast = []
    cast_block = re.search(r"人物声纹格局[^\n]*：\s*\n(.*?)(?=\n>|\n---|\n##)", raw_md, re.DOTALL)
    if cast_block:
        for line in cast_block.group(1).split("\n"):
            line = line.strip()
            if line.startswith("-") or line.startswith("•"):
                name_match = re.search(r"\*\*(.+?)\*\*", line)
                if name_match:
                    cast.append(name_match.group(1))

    return CanonEpisode(
        episode_id=f"S{int(episode_num):02d}" if episode_num.is_integer() else f"S{episode_num}",
        episode_num=episode_num,
        name="陨" if episode_num == 5 else f"EP_{episode_num}",
        title=title,
        core_formula=core_formula,
        cast=cast,
        summary=summary,
        content_md=raw_md,
        word_count=len(raw_md),
    )


def save_to_river2(episode: CanonEpisode, mysql_conn=None) -> bool:
    """将卷宗灌入美区 river2 (OCI MySQL :3306) 并同步本地 fixtures 缓存"""
    log.info(f"正在将卷宗 [{episode.episode_id} · {episode.name}] 灌入数据底座...")

    # 同步本地 fixtures 缓存备用
    os.makedirs("./fixtures", exist_ok=True)
    cache_path = f"./fixtures/canon_{episode.episode_id.lower()}.json"
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(asdict(episode), f, ensure_ascii=False, indent=2)

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS canon_dossiers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        episode_id VARCHAR(16) NOT NULL UNIQUE,
        episode_num FLOAT NOT NULL,
        name VARCHAR(64) NOT NULL,
        title VARCHAR(255) NOT NULL,
        core_formula VARCHAR(512),
        cast_json JSON,
        summary TEXT,
        content_md MEDIUMTEXT NOT NULL,
        word_count INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """

    upsert_sql = """
    INSERT INTO canon_dossiers (
        episode_id, episode_num, name, title, core_formula, cast_json, summary, content_md, word_count
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        title=VALUES(title),
        core_formula=VALUES(core_formula),
        cast_json=VALUES(cast_json),
        summary=VALUES(summary),
        content_md=VALUES(content_md),
        word_count=VALUES(word_count);
    """

    if mysql_conn:
        with mysql_conn.cursor() as cursor:
            cursor.execute(create_table_sql)
            cursor.execute(
                upsert_sql,
                (
                    episode.episode_id,
                    episode.episode_num,
                    episode.name,
                    episode.title,
                    episode.core_formula,
                    json.dumps(episode.cast, ensure_ascii=False),
                    episode.summary,
                    episode.content_md,
                    episode.word_count,
                ),
            )
        mysql_conn.commit()
        log.info(f"✅ 卷宗已持久化至 river2: {episode.episode_id}")
    else:
        log.info(f"ℹ️ (离线模式) 卷宗已就绪落盘于 fixtures 缓存: {cache_path} ({episode.word_count} 字符)")

    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    print("🚀 测试拉取第五期《陨》(Meteorite)...")
    ep5 = fetch_canon_from_github(5.0)
    print(f"✅ 成功摄入: {ep5.title}")
    print(f"📊 核心公式: {ep5.core_formula}")
    print(f"👥 出场席位: {ep5.cast[:6]}")
    print(f"📝 正文字数: {ep5.word_count} 字")
    save_to_river2(ep5)
