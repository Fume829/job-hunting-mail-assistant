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