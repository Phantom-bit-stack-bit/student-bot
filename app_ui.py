import streamlit as st
from hh import get_best_answer, load_data

st.set_page_config(page_title="Student Helper", page_icon="🎓")

def get_data():
    return load_data()

data = get_data()

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

# Convert subject properly
if subject == "Science":
    selected_subject = "science"
else:
    selected_subject = "commerce"

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
answer_type = st.selectbox(
    "Choose answer type:",
    ["Short", "Detailed"]
)

if answer_type == "Short":
    selected_type = "short"
else:
    selected_type = "long"
# Input box
# Input box
# Session state
if "last_q" not in st.session_state:
    st.session_state.last_q = ""

with st.form("qa_form"):
    question = st.text_input("✍️ Enter your question here")
    submitted = st.form_submit_button("Get Answer 🚀")

if submitted:
    if len(question.strip()) < 3:
        st.warning("⚠️ Please enter a proper question")
    elif len(question.split()) < 2 and len(question) < 5:
        st.warning("⚠️ Try a more detailed question")
    elif (question.strip().lower(), selected_type, selected_subject) == st.session_state.last_q:
        st.info("You already asked this 😊")

    else:
        st.session_state.last_q = (question.strip().lower(), selected_type, selected_subject)

        with st.spinner("Thinking... 🤔"):
            answer, matched_q = get_best_answer(
                question, data, selected_type, selected_subject
            )

        st.markdown("### 🤖 Answer")
        st.success(answer)
        st.caption(f"Matched with: {matched_q}")

        print("User asked:", question)
        print("No match:", question)
col1, col2 = st.columns(2)

with col1:
    if st.button("👍 Helpful"):
        print("Helpful:", question)

with col2:
    if st.button("👎 Not helpful"):
        print("Not helpful:", question)
st.markdown("---")
st.caption("Built by Arpit 🚀")
