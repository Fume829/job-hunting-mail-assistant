import streamlit as st

from src.clients.gmail_client import get_unread_emails
from src.clients.openai_client import (
    analyze_email,
    answer_job_question,
    generate_daily_todo,
)
from src.data.database import get_companies, update_company_status

STATUS_OPTIONS = [
    "未対応",
    "応募検討",
    "応募済",
    "ES提出",
    "面接予定",
    "面接済",
    "最終面接",
    "内定",
    "辞退",
]

st.set_page_config(
    page_title="JobPilot AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 JobPilot AI")
st.caption("AIが就職活動をナビゲートするメールアシスタント")


def get_priority_label(priority):
    if priority >= 5:
        return "🔥 最優先"
    if priority == 4:
        return "⚠️ 重要"
    if priority == 3:
        return "📌 確認推奨"
    return "📨 参考"


if st.button("未読メールを解析する", type="primary"):
    with st.spinner("Gmailからメールを取得し、AIで解析しています..."):
        try:
            emails = get_unread_emails(max_results=5)

            if not emails:
                st.info("未読メールはありません。")
            else:
                results = []

                for email in emails:
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

                important_count = sum(
                    1
                    for result in results
                    if int(result["priority"]) >= 4
                )

                deadline_count = sum(
                    1
                    for result in results
                    if result["deadline"] != "未記載"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric("解析したメール", len(results))
                col2.metric("重要メール", important_count)
                col3.metric("締切あり", deadline_count)

                st.divider()

                categories = ["すべて"] + sorted(
                    set(result["category"] for result in results)
                )

                selected_category = st.selectbox(
                    "カテゴリで絞り込み",
                    categories,
                )

                if selected_category != "すべて":
                    results = [
                        result
                        for result in results
                        if result["category"] == selected_category
                    ]

                st.subheader("📬 解析結果")

                for result in results:
                    priority = int(result["priority"])
                    priority_label = get_priority_label(priority)

                    with st.container(border=True):
                        top_left, top_right = st.columns([4, 1])

                        with top_left:
                            st.subheader(result["company"])
                            st.caption(result["subject"])

                        with top_right:
                            st.markdown(
                                f"### {priority_label}"
                            )

                        st.write(f"**分類:** {result['category']}")
                        st.write(f"**要約:** {result['summary']}")
                        st.write(f"**やること:** {result['todo']}")
                        st.write(f"**締切:** {result['deadline']}")
                        st.write(
                            f"**優先度:** {'★' * priority}{'☆' * (5 - priority)}"
                        )

        except Exception as error:
            st.error(f"エラーが発生しました: {error}")


st.divider()
st.subheader("📊 応募状況管理")

companies = get_companies()

if not companies:
    st.info("保存されている就活情報がありません。")
else:
    for company in companies:
        with st.container(border=True):
            left, right = st.columns([3, 1])

            with left:
                st.subheader(company["company"])
                st.caption(company["subject"])
                st.write(f"**分類:** {company['category']}")
                st.write(f"**やること:** {company['todo']}")
                st.write(f"**締切:** {company['deadline']}")

            with right:
                current_status = company["status"]

                if current_status in STATUS_OPTIONS:
                    current_index = STATUS_OPTIONS.index(current_status)
                else:
                    current_index = 0

                selected_status = st.selectbox(
                    "応募状況",
                    STATUS_OPTIONS,
                    index=current_index,
                    key=f"status_{company['id']}",
                )

                if selected_status != current_status:
                    update_company_status(
                        company["id"],
                        selected_status,
                    )

                    st.success("応募状況を更新しました。")
                    st.rerun()


st.divider()
st.subheader("✅ 今日のAI ToDo")
st.caption("保存済みの就活情報から、今日やるべきことをAIが整理します。")

if st.button("今日やることを作成する"):
    companies = get_companies()

    with st.spinner("今日のTodoを作成しています..."):
        todo_text = generate_daily_todo(companies)

    st.session_state["daily_todo"] = todo_text

if "daily_todo" in st.session_state:
    with st.container(border=True):
        st.markdown(st.session_state["daily_todo"])


st.divider()
st.subheader("💬 就活AIチャット")
st.caption("SQLiteに保存された就活情報について質問できます。")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "就活情報について質問してください。"
                "例えば「優先度が高い情報を教えて」"
                "「今やるべきことは？」などに回答できます。"
            ),
        }
    ]

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "就活情報について質問してください"
)

if question:
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    companies = get_companies()

    with st.chat_message("assistant"):
        with st.spinner("就活情報を確認しています..."):
            answer = answer_job_question(
                question,
                companies,
            )

        st.markdown(answer)

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )