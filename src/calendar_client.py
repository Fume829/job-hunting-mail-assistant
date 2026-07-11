from datetime import datetime, timedelta

from googleapiclient.discovery import build

from gmail_client import get_credentials


def get_calendar_service():
    """Google Calendar APIのサービスを作成する。"""

    credentials = get_credentials()

    return build(
        "calendar",
        "v3",
        credentials=credentials,
    )


def create_deadline_event(
    title,
    deadline,
    description="JobPilot AIがメールから自動登録しました。",
):
    """締切予定をGoogleカレンダーに登録する。"""

    service = get_calendar_service()

    deadline_datetime = datetime.fromisoformat(deadline)

    start_time = deadline_datetime
    end_time = deadline_datetime + timedelta(minutes=30)

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Tokyo",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Tokyo",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {
                    "method": "popup",
                    "minutes": 1440,
                },
                {
                    "method": "popup",
                    "minutes": 60,
                },
            ],
        },
    }

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event,
        )
        .execute()
    )

    return created_event