"""
core/db.py — ASN-GAN 统一数据底座适配器
========================================
单一数据面原则：默认对接美区 river2 (OCI MySQL :3306)。
若未配置 MySQL 凭据或处于本地离线模式，优雅降级为本地 SQLite (data/asn_gan.db)，
确保状态机在任何环境下均可 100% 闭环运转。
"""

import json
import logging
import os
import sqlite3
from typing import Any, Dict, List, Optional

log = logging.getLogger("asn_gan.db")

SQLITE_PATH = os.getenv("ASN_GAN_SQLITE_PATH", "data/asn_gan.db")
RIVER2_HOST = os.getenv("RIVER2_MYSQL_HOST", "")
RIVER2_PORT = int(os.getenv("RIVER2_MYSQL_PORT", "33062"))
RIVER2_USER = os.getenv("RIVER2_MYSQL_USER", "")
RIVER2_PASS = os.getenv("RIVER2_MYSQL_PASS", "")
RIVER2_DB = os.getenv("RIVER2_MYSQL_DB", "asn_gan")


def get_connection():
    """获取数据库连接（优先 MySQL，降级 SQLite）"""
    if RIVER2_HOST and RIVER2_USER:
        try:
            import pymysql
            conn = pymysql.connect(
                host=RIVER2_HOST,
                port=RIVER2_PORT,
                user=RIVER2_USER,
                password=RIVER2_PASS,
                database=RIVER2_DB,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
            )
            return conn, "mysql"
        except Exception as e:
            log.warning(f"直连 river2 MySQL 失败 ({e})，降级为本地 SQLite 数据底座")

    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn, "sqlite"


def init_schema():
    """初始化数据库表结构 (幂等)"""
    conn, engine = get_connection()
    cursor = conn.cursor()

    if engine == "sqlite":
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS canon_dossiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            episode_id TEXT UNIQUE NOT NULL,
            episode_num REAL NOT NULL,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            core_formula TEXT,
            summary TEXT,
            content_md TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS roundtable_sessions (
            session_id TEXT PRIMARY KEY,
            episode_id TEXT NOT NULL,
            topic TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS roundtable_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            seat_key TEXT NOT NULL,
            seat_name TEXT NOT NULL,
            angle TEXT NOT NULL,
            speech TEXT NOT NULL,
            round_no INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS canon_dossiers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            episode_id VARCHAR(16) NOT NULL UNIQUE,
            episode_num FLOAT NOT NULL,
            name VARCHAR(64) NOT NULL,
            title VARCHAR(255) NOT NULL,
            core_formula VARCHAR(512),
            summary TEXT,
            content_md MEDIUMTEXT NOT NULL,
            word_count INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS roundtable_sessions (
            session_id VARCHAR(64) PRIMARY KEY,
            episode_id VARCHAR(16) NOT NULL,
            topic VARCHAR(255) NOT NULL,
            status VARCHAR(32) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS roundtable_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(64) NOT NULL,
            seat_key VARCHAR(64) NOT NULL,
            seat_name VARCHAR(64) NOT NULL,
            angle VARCHAR(255) NOT NULL,
            speech TEXT NOT NULL,
            round_no INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

    conn.commit()
    conn.close()
    log.info(f"数据表初始化完成 (底座引擎: {engine})")


def save_dossier(dossier: Dict[str, Any]):
    """存入正典卷宗"""
    init_schema()
    conn, engine = get_connection()
    cursor = conn.cursor()

    if engine == "sqlite":
        cursor.execute("""
        INSERT INTO canon_dossiers (
            episode_id, episode_num, name, title, core_formula, summary, content_md, word_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(episode_id) DO UPDATE SET
            title=excluded.title,
            core_formula=excluded.core_formula,
            summary=excluded.summary,
            content_md=excluded.content_md,
            word_count=excluded.word_count;
        """, (
            dossier["episode_id"],
            dossier["episode_num"],
            dossier["name"],
            dossier["title"],
            dossier["core_formula"],
            dossier["summary"],
            dossier["content_md"],
            dossier["word_count"],
        ))
    else:
        cursor.execute("""
        INSERT INTO canon_dossiers (
            episode_id, episode_num, name, title, core_formula, summary, content_md, word_count
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title=VALUES(title),
            core_formula=VALUES(core_formula),
            summary=VALUES(summary),
            content_md=VALUES(content_md),
            word_count=VALUES(word_count);
        """, (
            dossier["episode_id"],
            dossier["episode_num"],
            dossier["name"],
            dossier["title"],
            dossier["core_formula"],
            dossier["summary"],
            dossier["content_md"],
            dossier["word_count"],
        ))

    conn.commit()
    conn.close()
    log.info(f"✅ 卷宗已持久化: {dossier['episode_id']} · {dossier['title']}")


def load_dossier(episode_id: str) -> Optional[Dict[str, Any]]:
    """读取指定卷宗"""
    init_schema()
    conn, engine = get_connection()
    cursor = conn.cursor()

    if engine == "sqlite":
        cursor.execute("SELECT * FROM canon_dossiers WHERE episode_id = ?", (episode_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    else:
        cursor.execute("SELECT * FROM canon_dossiers WHERE episode_id = %s", (episode_id,))
        row = cursor.fetchone()
        conn.close()
        return row
