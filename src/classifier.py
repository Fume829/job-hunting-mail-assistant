def classify_email(subject, sender, snippet):
    """メール内容をキーワードで分類する。"""

    text = f"{subject} {sender} {snippet}".lower()

    # 学校・学習サービスなど、就活メールではないものを先に除外
    other_keywords = [
        "課題採点",
        "採点結果",
        "実習課題",
        "aiスクール",
        "share-wis.com",
    ]

    offer_keywords = [
        "オファー",
        "スカウト",
        "特別招待",
        "書類選考確約",
        "注目企業",
        "企業紹介",
        "tech offer",
        "techoffer",
    ]

    internship_keywords = [
        "インターン",
        "仕事体験",
        "説明会",
        "セミナー",
        "就業体験",
    ]

    interview_keywords = [
        "面接のご案内",
        "面接日程",
        "一次面接",
        "二次面接",
        "最終面接",
        "適性検査",
        "履歴書",
        "エントリーシート",
        "es提出",
        "マイページ",
        "予約依頼",
        "一次選考",
        "二次選考",
        "最終選考",
    ]

    if any(keyword in text for keyword in other_keywords):
        return "その他"

    if any(keyword in text for keyword in offer_keywords):
        return "企業からのオファー"

    if any(keyword in text for keyword in internship_keywords):
        return "インターン・説明会"

    if any(keyword in text for keyword in interview_keywords):
        return "選考・面接"

    return "その他"