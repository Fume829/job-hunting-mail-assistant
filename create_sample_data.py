import sqlite3


DATABASE_PATH = "jobpilot.db"


sample_companies = [
    (
        "株式会社テックフューチャー",
        "選考・面接",
        "一次面接の日程について",
        "一次面接の日程候補を確認する連絡です。",
        "面接可能な日時を返信する",
        "2026-07-14",
        5,
        "面接予定",
        "採用担当者",
    ),
    (
        "ネクストAI株式会社",
        "インターン・説明会",
        "AIエンジニア向けインターンのご案内",
        "AI開発を体験できるインターンの案内です。",
        "応募フォームを確認してエントリーする",
        "2026-07-18",
        4,
        "応募検討",
        "インターン事務局",
    ),
    (
        "株式会社クラウドワークスラボ",
        "企業からのオファー",
        "開発職オファーのお知らせ",
        "Web開発職の特別オファーが届いています。",
        "募集内容を確認してオファーへ回答する",
        "未記載",
        4,
        "未対応",
        "採用チーム",
    ),
    (
        "デジタルソリューション株式会社",
        "選考・面接",
        "エントリーシート受領のお知らせ",
        "提出したエントリーシートが受領されました。",
        "選考結果の連絡を待つ",
        "未記載",
        2,
        "ES提出",
        "新卒採用担当",
    ),
]


def main():
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("DELETE FROM companies")

        connection.executemany(
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
            sample_companies,
        )

    print("サンプルデータを4件登録しました。")


if __name__ == "__main__":
    main()