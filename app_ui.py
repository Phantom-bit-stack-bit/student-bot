import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct
from Login import login_page
# ================== SESSION STATE ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prefill" not in st.session_state:
    st.session_state.prefill = ""

# ================== LOGIN ==================
if not st.session_state.logged_in:
    st.title("🌌 NEXUS • Quantum Student AI")
    st.markdown("### Sign in to continue your learning journey ✨")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username", "student")
        password = st.text_input("Password", "1234", type="password")
        if st.button("🚀 Sign In", type="primary"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ================== CONFIG ==================
st.set_page_config(page_title="NEXUS", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);}
    h1,h2,h3 {color: #00f5ff !important; text-shadow: 0 0 15px #00f5ff;}
    .stButton>button {background: linear-gradient(45deg,#ff00cc,#00ffcc); color:white; font-weight:bold;}
    .stSuccess {border-left: 6px solid #00ffcc;}
</style>
""", unsafe_allow_html=True)

# Load Data
data = load_data()
vocab = build_vocab(data)

# Sidebar
st.sidebar.title("⚡ NEXUS CONTROL")
st.sidebar.markdown(f"**👤 Student:** Explorer")
if st.sidebar.button("🌀 Clear History"):
    st.session_state.chat_history = []
    st.rerun()

st.sidebar.metric("Questions Asked", len(st.session_state.chat_history))

# Main UI
st.title("🌌 NEXUS • Quantum Student AI")
st.markdown("**Your Smart Learning Companion** 🌟")

# Controls
col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("Subject", ["Science", "Commerce"])
with col2:
    answer_type = st.selectbox("Answer Type", ["Short", "Detailed"])

selected_subject = "science" if subject == "Science" else "commerce"
selected_type = "short" if answer_type == "Short" else "long"

# Suggestions (Fixed)
st.markdown("### 💡 Quick Questions")
suggestions = {
    "Science": ["What is gravity?", "Explain photosynthesis", "Difference between mass and weight"],
    "Commerce": ["What is business?", "Explain profit", "Difference between assets and liabilities"]
}

cols = st.columns(3)
for i, q in enumerate(suggestions[subject]):
    if cols[i].button(q, key=f"sug_{i}"):
        st.session_state.prefill = q
        st.rerun()

# Query Input
st.markdown("### ✴️ Ask Anything")
question = st.text_input(
    "Type your question",
    value=st.session_state.get("prefill", ""),
    placeholder="What is gravity?",
    key="main_input"
)

if st.button("🚀 Get Answer", type="primary", use_container_width=True):
    if question.strip():
        corrected = auto_correct(question, vocab)
        if corrected != question.lower():
            st.info(f"🔄 Interpreted as: **{corrected}**")
        
        if not any(c["corrected"] == corrected for c in st.session_state.chat_history):
            with st.spinner("Thinking..."):
                answer, matched = get_best_answer(corrected, data, selected_type, selected_subject)
            
            st.session_state.chat_history.append({
                "question": question,
                "corrected": corrected,
                "answer": answer,
                "matched": matched,
                "type": selected_type
            })
            st.session_state.prefill = ""
        else:
            st.warning("Already asked!")

# Chat History with Copy
if st.session_state.chat_history:
    st.markdown("### 📚 Learning History")
    for idx, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.container():
            st.markdown(f"**🧑 You:** {chat['question']}")
            st.success(chat["answer"])
            
            c1, c2 = st.columns([4,1])
            with c1:
                st.caption(f"Matched: **{chat['matched']}** | {chat['type'].upper()}")
            with c2:
                if st.button("📋 Copy", key=f"copy_{idx}"):
                    st.code(chat["answer"])
                    st.toast("✅ Copied to clipboard!", icon="📋")
            st.markdown("---")

st.caption("🚀 Built for curious students • Keep Learning!")
