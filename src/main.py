from gmail_client import get_unread_emails
from openai_client import analyze_email


def main():
    try:
        emails = get_unread_emails(max_results=3)

        if not emails:
            print("未読メールはありません。")
            return

        for index, email in enumerate(emails, start=1):
            print(f"\n{index}件目をAIで解析しています...")

            email_body = email["body"]

            if not email_body:
                email_body = email["snippet"]

            result = analyze_email(
                email["subject"],
                email["sender"],
                email_body,
            )

            print("=" * 60)
            print(f"企業・サービス: {result['company']}")
            print(f"分類: {result['category']}")
            print(f"要約: {result['summary']}")
            print(f"やること: {result['todo']}")
            print(f"締切: {result['deadline']}")
            print(f"優先度: {'★' * result['priority']}")

    except FileNotFoundError:
        print("credentials/credentials.jsonが見つかりません。")

    except Exception as error:
        print(f"エラーが発生しました: {error}")


if __name__ == "__main__":
    main()