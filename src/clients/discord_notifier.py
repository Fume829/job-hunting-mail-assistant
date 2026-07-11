import os

import requests
from dotenv import load_dotenv


load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_notification(results):
    """AI解析結果をDiscordへ通知する。"""

    if not WEBHOOK_URL:
        raise ValueError(
            "DISCORD_WEBHOOK_URLが.envに設定されていません。"
        )

    if not results:
        return

    lines = ["📬 **JobPilot AI 就活メール通知**", ""]

    for result in results:
        priority = int(result["priority"])
        stars = "★" * priority + "☆" * (5 - priority)

        lines.extend(
            [
                f"**{result['company']}**",
                f"分類: {result['category']}",
                f"要約: {result['summary']}",
                f"やること: {result['todo']}",
                f"締切: {result['deadline']}",
                f"優先度: {stars}",
                "",
            ]
        )

    message = "\n".join(lines)

    response = requests.post(
        WEBHOOK_URL,
        json={"content": message},
        timeout=10,
    )

    response.raise_for_status()