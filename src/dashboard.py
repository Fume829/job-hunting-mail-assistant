import streamlit as st

from gmail_client import get_unread_emails
from openai_client import analyze_email
from database import get_companies


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