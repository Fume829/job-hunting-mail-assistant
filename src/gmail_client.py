import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_PATH = os.path.join(
    BASE_DIR,
    "credentials",
    "credentials.json",
)
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")


def authenticate_gmail():
    """Gmail APIの認証を行う。"""

    credentials = None

    if os.path.exists(TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(
            TOKEN_PATH,
            SCOPES,
        )

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES,
            )
            credentials = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w", encoding="utf-8") as token_file:
            token_file.write(credentials.to_json())

    return build("gmail", "v1", credentials=credentials)


def get_header(headers, name):
    """メールヘッダーから値を取得する。"""

    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]

    return ""


def get_unread_emails(max_results=10):
    """未読メールの件名、送信者、本文の一部を取得する。"""

    service = authenticate_gmail()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            q="is:unread",
            maxResults=max_results,
        )
        .execute()
    )

    messages = response.get("messages", [])
    emails = []

    for message in messages:
        message_data = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["Subject", "From"],
            )
            .execute()
        )

        headers = message_data["payload"].get("headers", [])

        emails.append(
            {
                "id": message["id"],
                "subject": get_header(headers, "Subject"),
                "sender": get_header(headers, "From"),
                "snippet": message_data.get("snippet", ""),
            }
        )

    return emails