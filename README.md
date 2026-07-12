# JobPilot AI

就職活動に関するメールをAIで自動整理し、応募状況やTodoを管理できる就活支援アプリです。

Gmailに届いた就活関連メールを取得し、OpenAI APIを使って企業名、分類、要約、Todo、締切、優先度を解析します。  
解析結果はSQLiteに保存し、Streamlit上で確認・管理できます。

## 開発背景

就職活動では、企業から届くメールの確認、締切管理、応募状況の整理など、多くの情報を個別に管理する必要があります。

特に、メールの件数が増えると、重要な連絡や締切を見落とす可能性があります。

そこで、就活関連メールの整理から応募状況の管理までを一つの画面で行える、AI就活アシスタントを開発しました。

## 主な機能

### Gmailメール取得

Gmail APIを利用して、就活に関係する未読メールの件名、送信者、本文全文を取得します。

### AIによるメール解析

OpenAI APIを使用して、取得したメールから次の情報を抽出します。

- 企業名・サービス名
- メールの分類
- 内容の要約
- 対応すべきTodo
- 締切
- 優先度

### Streamlitダッシュボード

解析したメールを、優先度やカテゴリとともに一覧表示します。

### 応募状況管理

企業ごとに、次の応募状況を管理できます。

- 未対応
- 応募検討
- 応募済
- ES提出
- 面接予定
- 面接済
- 最終面接
- 内定
- 辞退

変更した応募状況はSQLiteに保存されます。

### AIチャット

SQLiteに保存された就活情報を参照し、自然言語による質問に回答します。

質問例：

- 優先度が高い企業を教えて
- 応募検討中の企業を教えて
- 今やるべきことを教えて
- 面接予定の企業を一覧にして

### AI ToDo生成

保存された企業情報、優先度、締切、応募状況をもとに、今日取り組むべきTodoをAIが生成します。

### Discord通知

重要な就活メールの解析結果をDiscordへ通知します。

### Googleカレンダー連携

就活イベントや締切をGoogleカレンダーへ登録できます。

## 使用技術

- Python
- Streamlit
- OpenAI API
- Gmail API
- Google Calendar API
- Discord Webhook
- SQLite
- Git
- GitHub

## ディレクトリ構成

```text
src/
├─ clients/
│  ├─ gmail_client.py
│  ├─ openai_client.py
│  ├─ calendar_client.py
│  └─ discord_notifier.py
├─ data/
│  └─ database.py
├─ ui/
│  └─ dashboard.py
├─ main.py
├─ test_calendar.py
└─ test_discord.py