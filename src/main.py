from discord_notifier import send_discord_notification
from gmail_client import get_unread_emails
from openai_client import analyze_email


def main():
    try:
        emails = get_unread_emails(max_results=5)

        if not emails:
            print("未読メールはありません。")
            return

        results = []

        for index, email in enumerate(emails, start=1):
            print(f"{index}件目をAIで解析しています...")

            email_body = email["body"] or email["snippet"]

            analysis = analyze_email(
                email["subject"],
                email["sender"],
                email_body,
            )

            results.append(
                {
                    "subject": email["subject"],
                    "sender": email["sender"],
                    **analysis,
                }
            )

        results.sort(
            key=lambda item: int(item["priority"]),
            reverse=True,
        )
        results = [
            result
            for result in results
            if result["category"] != "その他"
        ]

        if not results:
            print("通知対象の就活メールはありませんでした。")
            return
        
        send_discord_notification(results)

        print("解析結果をDiscordへ送信しました。")

    except FileNotFoundError:
        print("credentials/credentials.jsonが見つかりません。")

    except Exception as error:
        print(f"エラーが発生しました: {error}")


if __name__ == "__main__":
    main()