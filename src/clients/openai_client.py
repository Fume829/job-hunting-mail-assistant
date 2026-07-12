import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEYが.envに設定されていません。")

client = OpenAI(api_key=api_key)


def analyze_email(subject, sender, snippet):
    """就活メールをAIで解析し、辞書形式で返す。"""

    prompt = f"""
以下のメールを、就職活動の観点から解析してください。

【件名】
{subject}

【送信者】
{sender}

【本文】
{snippet}

次のJSON形式だけを返してください。

{{
  "company": "企業名またはサービス名",
  "category": "選考・面接、インターン・説明会、企業からのオファー、その他のいずれか",
  "summary": "メールの内容を1文で要約",
  "todo": "受信者が行うべきこと。なければ「なし」",
  "deadline": "締切。記載がなければ「未記載」",
  "priority": 1から5の整数
}}

優先度の目安：
5 = 締切が近い、または早急な対応が必要
4 = 対応が必要
3 = 確認した方がよい
2 = 参考情報
1 = 就活と関係が薄い
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    result_text = response.output_text.strip()

    # ```json ... ``` が返された場合にも対応
    if result_text.startswith("```"):
        result_text = result_text.removeprefix("```json")
        result_text = result_text.removeprefix("```")
        result_text = result_text.removesuffix("```")
        result_text = result_text.strip()

    return json.loads(result_text)

def answer_job_question(question, companies):
    """SQLiteに保存された就活情報を参照して質問に回答する。"""

    if not companies:
        return "保存されている就活情報がありません。先にメールを取得・解析してください。"

    company_data = json.dumps(
        companies,
        ensure_ascii=False,
        indent=2,
        default=str,
    )

    prompt = f"""
あなたは就職活動を支援するAIアシスタント「JobPilot AI」です。

以下はSQLiteデータベースに保存されている就活情報です。
この情報だけを根拠として、ユーザーの質問に日本語で回答してください。

【就活情報】
{company_data}

【ユーザーの質問】
{question}

【回答ルール】
- 保存されている情報を分かりやすく整理して回答する
- 締切、Todo、優先度、応募状況を重視する
- 複数の情報がある場合は、箇条書きを使用する
- データに存在しない内容は推測しない
- 情報が見つからない場合は、その旨を明確に伝える
- 締切が「未記載」の場合は、締切不明と伝える
"""

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt,
        )

        return response.output_text.strip()

    except Exception as error:
        return f"AIによる回答の生成中にエラーが発生しました: {error}"