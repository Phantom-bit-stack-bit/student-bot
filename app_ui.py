import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct
import csv

st.set_page_config(page_title="Student Helper", page_icon="🎓")

def get_data():
    return load_data()

data = get_data()
vocab = build_vocab(data)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_q" not in st.session_state:
    st.session_state.last_q = ""

st.sidebar.title("📌 About")
st.sidebar.info("This tool helps students get quick exam-ready answers.")

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.stTextInput>div>div>input {
    background-color: #262730;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Quick Exam Helper")

# Subject selector
subject = st.selectbox(
    "Select Subject:",
    ["Science", "Commerce"]
)

selected_subject = "science" if subject == "Science" else "commerce"

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
    st.write(f"- {q}")

# Answer type
answer_type = st.selectbox(
    "Choose answer type:",
    ["Short", "Detailed"]
)

selected_type = "short" if answer_type == "Short" else "long"

# FORM
with st.form("qa_form"):
    question = st.text_input(
        "✍️ Enter your question here",
        placeholder="e.g. What is gravity?"
    )
    submitted = st.form_submit_button("Get Answer 🚀")

# LOGIC
if submitted:
    if len(question.strip()) < 3:
        st.warning("⚠️ Please enter a proper question")

    else:
        corrected_question = auto_correct(question, vocab)

        # 🔍 duplicate check
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
                "matched": matched_q
            })

            print("User asked:", question)  # ✅ moved inside

        else:
            st.info("Already asked (same meaning) 😊")

# ✅ SHOW ANSWER ALWAYS (OUTSIDE submit)
if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history):

        st.markdown("### 🧑 Question")
        st.write(chat["question"])

        st.markdown("### 🤖 Answer")
        st.success(chat["answer"])
        st.caption(f"Matched with: {chat['matched']}")

        st.markdown("---")

    # Feedback buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Helpful"):
            st.success("Thanks for feedback!")

    with col2:
        if st.button("👎 Not helpful"):
            st.warning("Got it! Will improve.")

st.markdown("---")
st.caption("🚀Build by Arpit.")
