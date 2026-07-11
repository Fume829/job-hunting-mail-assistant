import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "jobpilot.db")


def get_connection():
    """SQLiteデータベースへ接続する。"""

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """企業管理用テーブルを作成する。"""

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                category TEXT NOT NULL,
                subject TEXT NOT NULL,
                summary TEXT NOT NULL,
                todo TEXT NOT NULL,
                deadline TEXT NOT NULL,
                priority INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT '未対応',
                sender TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_company(result):
    """AI解析結果を保存する。"""

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO companies (
                company,
                category,
                subject,
                summary,
                todo,
                deadline,
                priority,
                status,
                sender
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result["company"],
                result["category"],
                result["subject"],
                result["summary"],
                result["todo"],
                result["deadline"],
                int(result["priority"]),
                result.get("status", "未対応"),
                result.get("sender", ""),
            ),
        )


def get_companies():
    """保存済み企業データをすべて取得する。"""

    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT *
            FROM companies
            ORDER BY priority DESC, created_at DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def update_company_status(company_id, status):
    """応募状況を更新する。"""

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE companies
            SET status = ?
            WHERE id = ?
            """,
            (status, company_id),
        )