from calendar_client import create_deadline_event


event = create_deadline_event(
    title="JobPilot AI テスト予定",
    deadline="2026-07-20T18:00:00",
    description="Google Calendar APIの接続テストです。",
)

print("カレンダーへの登録が完了しました。")
print(event.get("htmlLink"))