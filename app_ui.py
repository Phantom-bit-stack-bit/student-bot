import streamlit as st
from hh import get_best_answer, load_data

# Page config
st.set_page_config(page_title="Student Helper", page_icon="🎓")

# Load data
@st.cache_data
def get_data():
    return load_data()

data = get_data()

# Sidebar
st.sidebar.title("📌 About")
st.sidebar.info("This tool helps students get quick exam-ready answers.")

# Custom style
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

# Title
st.title("🎓 Student Exam Helper")

@st.cache_data
def get_data():
    return load_data()

data = get_data()

# Input box (FIXED)
question = st.text_input("✍️ Enter your question here")

# Button
if st.button("Get Answer 🚀"):
    if question.strip():   # safer check
        with st.spinner("Thinking... 🤔"):
            answer = get_best_answer(question, data)

        st.markdown("### 🤖 Answer")
        st.markdown(f"```\n{answer}\n```")
    else:
        st.warning("⚠️ Please enter a question")

st.markdown("---")
st.caption("Built by Arpit 🚀")
