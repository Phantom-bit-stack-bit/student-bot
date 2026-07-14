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

# ================== LOGIN (Simple) ==================
if not st.session_state.logged_in:
    st.title("🌌 NEXUS • Quantum Student AI")
    st.markdown("### Sign in to continue your learning journey")
    username = st.text_input("Username", "student")
    password = st.text_input("Password", type="password", value="1234")
    if st.button("🚀 Sign In"):
        if username and password:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ================== CONFIG ==================
st.set_page_config(page_title="NEXUS • Quantum Student AI", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #0f1b3d, #2a0052); }
    h1, h2, h3 { color: #00ffff !important; text-shadow: 0 0 15px #00ffff; }
    .stButton>button { background: linear-gradient(45deg, #ff00ff, #00ffcc); color: white; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ================== LOAD DATA ==================
data = load_data()
vocab = build_vocab(data)

# ================== SIDEBAR ==================
st.sidebar.title("⚡ NEURAL CONTROL PANEL")
st.sidebar.info(f"👤 Logged in as: **{st.session_state.get('current_user', 'Student')}**")

if st.sidebar.button("🌀 Clear All History"):
    st.session_state.chat_history = []
    st.rerun()

st.sidebar.markdown("### 📊 Progress")
st.sidebar.metric("Questions Asked", len(st.session_state.chat_history))
if len(st.session_state.chat_history) > 0:
    st.sidebar.progress(min(len(st.session_state.chat_history) / 15, 1.0))

# ================== HEADER ==================
st.title("🌌 NEXUS • QUANTUM STUDENT AI")
st.markdown("**_Neural Learning Interface v3.7_** 🌟")

# ================== CONTROLS ==================
col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("📡 Knowledge Domain", ["Science", "Commerce"])
with col2:
    answer_type = st.selectbox("🔬 Answer Type", ["Short", "Detailed"])

selected_subject = "science" if subject == "Science" else "commerce"
selected_type = "short" if answer_type == "Short" else "long"

# ================== SUGGESTIONS ==================
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

# ================== QUERY INPUT ==================
st.markdown("### ✴️ TRANSMIT QUERY")
question = st.text_input(
    "Enter your question:",
    value=st.session_state.get("prefill", ""),
    placeholder="Ask anything...",
    key="question_input"
)

submit = st.button("🚀 TRANSMIT TO NEXUS", type="primary")

# ================== LOGIC ==================
if submit and question.strip():
    corrected_question = auto_correct(question, vocab)
    
    if corrected_question != question.lower():
        st.info(f"🔄 Interpreted as: **{corrected_question}**")
    
    if not any(chat["corrected"] == corrected_question for chat in st.session_state.chat_history):
        with st.spinner("🔄 Thinking..."):
            answer, matched_q = get_best_answer(corrected_question, data, selected_type, selected_subject)
        
        st.session_state.chat_history.append({
            "question": question,
            "corrected": corrected_question,
            "answer": answer,
            "matched": matched_q,
            "type": selected_type
        })
        st.session_state.prefill = ""  # Clear prefill after submit
    else:
        st.warning("You already asked this!")

# ================== CHAT DISPLAY ==================
if st.session_state.chat_history:
    st.markdown("### 📚 Your Learning History")
    for idx, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.container():
            st.markdown(f"**🧑 You:** {chat['question']}")
            st.success(chat["answer"])
            
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.caption(f"📍 Matched: **{chat['matched']}** | Type: **{chat['type'].upper()}**")
            with col_b:
                if st.button("📋 Copy", key=f"copy_{idx}"):
                    st.code(chat["answer"])
                    st.toast("✅ Copied!", icon="📋")
            
            if chat["corrected"] != chat["question"].lower():
                st.caption(f"🔄 Interpreted as: **{chat['corrected']}**")
            
            st.markdown("---")

# ================== FOOTER ==================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888;">
    🌟 Keep Learning • Made with ❤️ for curious minds
</div>
""", unsafe_allow_html=True)
