import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct

# ================== CONFIG ==================
st.set_page_config(
    page_title="NEXUS • Quantum Student AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Sci-Fi CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0a1f 0%, #1a0033 100%);
        color: #00ffcc;
    }
    
    h1, h2, h3 {
        color: #00ffff !important;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
        font-family: 'Courier New', monospace;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #ff00ff);
        color: #000000;
        border: none;
        border-radius: 20px;
        padding: 12px 24px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 15px #00ffcc, 0 0 30px #ff00ff;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px #00ffcc, 0 0 50px #ff00ff;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a0033;
        color: #00ffcc;
        border: 2px solid #00ffff;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
    }
    
    .chat-container {
        border: 1px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        background: rgba(10, 10, 31, 0.8);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ================== LOAD DATA ==================
data = load_data()
vocab = build_vocab(data)

# ================== SESSION STATE ==================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================== SIDEBAR ==================
st.sidebar.title("⚡ NEURAL CONTROL PANEL")
st.sidebar.markdown("---")
st.sidebar.info("🌐 Accessing Quantum Knowledge Core v3.7")
st.sidebar.caption("Neural Interface Online")

if st.sidebar.button("🌀 PURGE MEMORY CACHE"):
    st.session_state.chat_history = []
    st.rerun()

st.sidebar.markdown("### 📡 SYSTEM STATUS")
st.sidebar.success("✅ Quantum Link Stable")
st.sidebar.progress(0.92)

# ================== MAIN HEADER ==================
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 🌌")
with col2:
    st.title("NEXUS • QUANTUM STUDENT AI")
    st.markdown("**_Neural Learning Interface v3.7_**")

st.markdown("---")

# ================== CONTROLS ==================
col1, col2, col3 = st.columns(3)

with col1:
    subject = st.selectbox(
        "📡 SELECT KNOWLEDGE DOMAIN",
        ["Science", "Commerce"],
        help="Choose your dimensional focus"
    )

with col2:
    answer_type = st.selectbox(
        "🔬 RESPONSE PROTOCOL",
        ["Short", "Detailed"],
        help="Neural output density"
    )

selected_subject = "science" if subject == "Science" else "commerce"
selected_type = "short" if answer_type == "Short" else "long"

# ================== QUANTUM SUGGESTIONS ==================
st.markdown("### 🔮 QUANTUM
