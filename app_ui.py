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

# ================== SIMPLE LOGIN ==================
if not st.session_state.logged_in:
    st.set_page_config(page_title="NEXUS • Quantum Student AI", page_icon="🌌", layout="centered")
    st.title("🌌 NEXUS • Quantum Student AI")
    st.markdown("### Welcome back! Sign in to continue your learning journey ✨")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("👤 Username", value="student")
        password = st.text_input("🔑 Password", value="1234", type="password")
        if st.button("🚀 Sign In", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ================== CONFIG ==================
st.set_page_config(page_title="NEXUS • Quantum Student AI", page_icon="🌌", layout="wide")

# Beautiful Sci-Fi + Student Friendly CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0c0c2e 0%, #1a0033 100%);
    }
    h1, h2, h3 {
        color: #00f5ff !important;
        text-shadow: 0 0 20px #00f5ff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #ff00cc, #00ffcc);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px #00ffcc;
    }
    .stSuccess {
        background-color: rgba(0, 255, 204, 0.15) !important;
        border-left: 5px solid #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# ================== LOAD DATA ==================
data = load_data()
vocab = build_vocab(data)

# ================== SIDEBAR ==================
st.sidebar.title("⚡ NEURAL CONTROL PANEL")
st.sidebar.markdown(f"**👤 Student:** {st.session_state.get('current_user', 'Explorer')}")

if st.sidebar.button("🌀 Clear Learning History"):
    st.session_state.chat_history = []
    st.rerun()

st.sidebar.markdown("### 📊 Your Progress")
st.sidebar.metric("Questions Mastered", len(st.session_state.chat_history))
if len(st.session_state.chat_history) > 0:
    st.sidebar.progress(min(len(st.session_state.chat_history) / 20, 1.0))
    st.sidebar.success("You're doing amazing! Keep going! 🌟")

# ================== MAIN HEADER ==================
st.title("🌌 NEXUS • QUANTUM STUDENT AI")
st.markdown("**_Your Personal AI Learning Companion_**")

# ================== DOMAIN & TYPE ==================
col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("📚 Select Subject", ["Science", "Commerce"])
with col2:
    answer_type = st.selectbox("📝 Answer Type", ["Short", "Detailed"])

selected_subject = "science" if subject == "Science" else "commerce"
selected_type = "short" if answer_type == "Short" else "long"

# ================== SUGGESTIONS ==================
st.markdown("### 💡 Try These Questions")
suggestions = {
    "Science": ["What is gravity?", "Explain photosynthesis", "Difference between mass and weight"],
    "Commerce": ["What is business?", "Explain profit", "Difference between assets and liabilities"]
}

cols = st.columns(3)
for i, q in enumerate(suggestions[subject]):
    if cols[i].button(q, key=f"sug_{i}"):
        st.session_state.prefill = q
        st.rerun()

# ================== QUERY INPUT ==================
st.markdown("### ✴️ Ask Your Question")
question = st.text_input(
    "Type your question here:",
    value=st.session_state.get("prefill", ""),
    placeholder="e.g., What is photosynthesis?",
    key="main_input"
)

submit = st.button("🚀 Get Answer", type="primary", use_container_width=True)

# ================== LOGIC ==================
if submit and question.strip():
    corrected = auto_correct(question, vocab)
    
    if corrected != question.lower():
        st.info(f"🔄 I understood: **{corrected}**")
    
    if not any(c["corrected"] == corrected for c in st.session_state.chat_history):
        with st.spinner("🤖 Thinking..."):
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
        st.warning("You already asked this question!")

# ================== CHAT HISTORY ==================
if st.session_state.chat_history:
    st.markdown("### 📚 Your Learning History")
    for idx, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.container():
            st.markdown(f"**🧑 You:** {chat['question']}")
            st.success(chat["answer"])
            
            c1, c2 = st.columns([4, 1])
            with c1:
                st.caption(f"Matched: **{chat['matched']}** | Type: **{chat['type'].upper()}**")
            with c2:
                if st.button("📋 Copy Answer", key=f"copy_{idx}"):
                    st.code(chat["answer"])
                    st.toast("✅ Answer Copied!", icon="📋")
            
            st.markdown("---")

# ================== FOOTER ==================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #aaa; padding: 20px;">
    🌟 Made for Curious Students • Keep Learning, Keep Growing!
</div>
""", unsafe_allow_html=True)
