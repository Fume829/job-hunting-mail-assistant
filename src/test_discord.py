from discord_notifier import send_discord_notification


sample_results = [
    {
        "company": "ベルシステム24",
        "category": "選考・面接",
        "summary": "イベント予約が必要です。",
        "todo": "マイページからイベントを予約する",
        "deadline": "未記載",
        "priority": 4,
    }
]


send_discord_notification(sample_results)

print("Discordへの送信が完了しました。")