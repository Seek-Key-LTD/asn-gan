"""
scripts/ingest_canon.py — 卷宗导入脚本
======================================
将《三更道场·第五期·陨》权威正稿拉取并灌入数据库底座。
"""

import argparse
import logging
import sys
from dataclasses import asdict

from core.canon import fetch_canon_from_github
from core.db import load_dossier, save_dossier

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ingest")


def main():
    parser = argparse.ArgumentParser(description="正典卷宗导入器")
    parser.add_argument("--episode", type=float, default=5.0, help="期次编号 (如 5.0 代表第五期·陨)")
    args = parser.parse_args()

    print(f"\n==========================================")
    print(f"📦 正在执行第 {args.episode} 期正典卷宗导入...")
    print(f"==========================================")

    # 1. 拉取与解析
    episode = fetch_canon_from_github(args.episode)
    print(f"✅ 拉取解析成功: {episode.title}")
    print(f"📊 核心公式: {episode.core_formula}")
    print(f"📝 正文字数: {episode.word_count} 字")

    # 2. 灌入数据库底座
    save_dossier(asdict(episode))

    # 3. 验证回读
    row = load_dossier(episode.episode_id)
    if row:
        print(f"\n🎉 导入验证成功！数据库记录如下:")
        print(f"   • episode_id : {row['episode_id']}")
        print(f"   • name       : {row['name']}")
        print(f"   • title      : {row['title']}")
        print(f"   • word_count : {row['word_count']}")
        print(f"   • formula    : {row['core_formula']}")
    else:
        print("❌ 回读验证失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
