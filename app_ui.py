import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct

st.set_page_config(page_title="Student Helper", page_icon="🎓")

# Load data
data = load_data()
vocab = build_vocab(data)

# Session state
if "last_q" not in st.session_state:
    st.session_state.last_q = ""

if "last_interaction" not in st.session_state:
    st.session_state.last_interaction = None

# UI
st.title("⚡ Quick Exam Helper")

subject = st.selectbox("Select Subject:", ["Science", "Commerce"])
selected_subject = "science" if subject == "Science" else "commerce"

answer_type = st.selectbox("Choose answer type:", ["Short", "Detailed"])
selected_type = "short" if answer_type == "Short" else "long"

# FORM
with st.form("qa_form"):
    question = st.text_input("✍️ Enter your question here")
    submitted = st.form_submit_button("Get Answer 🚀")

# LOGIC
if submitted:
    if len(question.strip()) < 3:
        st.warning("⚠️ Please enter a proper question")

    elif (question.strip().lower(), selected_type, selected_subject) == st.session_state.last_q:
        st.info("You already asked this 😊")

    else:
        st.session_state.last_q = (
            question.strip().lower(),
            selected_type,
            selected_subject
        )

        corrected_question = auto_correct(question, vocab)

        answer, matched_q = get_best_answer(
            corrected_question,
            data,
            selected_type,
            selected_subject
        )

        # 🔥 STORE RESULT (MOST IMPORTANT FIX)
        st.session_state.last_interaction = {
            "question": question,
            "corrected": corrected_question,
            "answer": answer,
            "matched": matched_q
        }

# ✅ ALWAYS SHOW LAST ANSWER (outside submit)
if st.session_state.last_interaction:
    data = st.session_state.last_interaction

    st.markdown("### 🤖 Answer")
    st.success(data["answer"])
    st.caption(f"Matched with: {data['matched']}")

    # Feedback buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Helpful"):
            st.success("Thanks for feedback!")

    with col2:
        if st.button("👎 Not helpful"):
            st.warning("Got it! Will improve.")

st.markdown("---")
st.caption("🚀 Built by Arpit")
