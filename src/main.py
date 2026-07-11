from classifier import classify_email
from gmail_client import get_unread_emails


def main():
    try:
        emails = get_unread_emails(max_results=10)

        if not emails:
            print("未読メールはありません。")
            return

        for index, email in enumerate(emails, start=1):
            category = classify_email(
                email["subject"],
                email["sender"],
                email["snippet"],
            )

            print("=" * 60)
            print(f"{index}. [{category}]")
            print(f"件名: {email['subject']}")
            print(f"送信者: {email['sender']}")
            print(f"本文: {email['snippet']}")

    except FileNotFoundError:
        print("credentials/credentials.jsonが見つかりません。")

    except Exception as error:
        print(f"エラーが発生しました: {error}")


if __name__ == "__main__":
    main()