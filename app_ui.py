import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct

st.set_page_config(page_title="Student Helper V3", page_icon="🎓")

# ================== LOAD ==================
data = load_data()
vocab = build_vocab(data)

# ================== SESSION ==================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================== SIDEBAR ==================
st.sidebar.title("📌 About")
st.sidebar.info("Exam helper with AI-like chat experience.")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# ================== UI ==================
st.title("🎓 Student Helper V3")

subject = st.selectbox("📚 Subject", ["Science", "Commerce"])
selected_subject = "science" if subject == "Science" else "commerce"

answer_type = st.selectbox("🧠 Answer Type", ["Short", "Detailed"])
selected_type = "short" if answer_type == "Short" else "long"

# Suggestions
suggestions = {
    "Science": [
        "What is gravity?",
        "Explain photosynthesis",
        "Difference between mass and weight"
    ],
    "Commerce": [
        "What is business?",
        "Explain profit",
        "Difference between assets and liabilities"
    ]
}

st.markdown("### 💡 Try asking:")
for q in suggestions[subject]:
    if st.button(q):
        st.session_state["prefill"] = q

# ================== INPUT ==================
question = st.text_input(
    "✍️ Ask your question",
    value=st.session_state.get("prefill", "")
)

submit = st.button("🚀 Get Answer")

# ================== LOGIC ==================
if submit:
    if len(question.strip()) < 3:
        st.warning("⚠️ Please enter a proper question")
    else:
        corrected_question = auto_correct(question, vocab)

        # 🔥 Did you mean
        if corrected_question != question.lower():
            st.info(f"Did you mean: {corrected_question}?")

        # 🔍 Duplicate check
        is_duplicate = False
        for chat in st.session_state.chat_history:
            if chat["corrected"] == corrected_question:
                is_duplicate = True
                break

        if not is_duplicate:
            with st.spinner("Thinking... 🤔"):
                answer, matched_q = get_best_answer(
                    corrected_question,
                    data,
                    selected_type,
                    selected_subject
                )

            st.session_state.chat_history.append({
                "question": question,
                "corrected": corrected_question,
                "answer": answer,
                "matched": matched_q,
                "type": selected_type
            })
        else:
            st.info("Already asked (same meaning) 😊")

# ================== CHAT DISPLAY ==================
if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history):

        with st.container():
            st.markdown("#### 🧑 You")
            st.write(chat["question"])

            st.markdown("#### 🤖 Bot")
            st.success(chat["answer"])

            # Extra info
            st.caption(f"Matched with: {chat['matched']} | Type: {chat['type']}")

            if chat["corrected"] != chat["question"].lower():
                st.caption(f"Interpreted as: {chat['corrected']}")

            st.markdown("---")

# ================== FOOTER ==================
st.markdown("---")
st.caption("🚀 Built by Arpit | V3")
