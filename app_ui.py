import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct
from datetime import datetime
from Login import login_page
# ================== SESSION STATE ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================== LOGIN ==================
if not st.session_state.logged_in:
    st.set_page_config(page_title="NEXUS", page_icon="🌌", layout="centered")
    st.title("NEXUS")
    st.markdown("**Intelligent Learning Assistant**")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username", value="student")
        password = st.text_input("Password", value="1234", type="password")
        if st.button("Sign In", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ================== CONFIG ==================
st.set_page_config(page_title="NEXUS - Intelligent Learning Assistant", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .stApp { background: #05050f; color: #e0e0e0; }
    .chat-user { 
        background: #1e2937; 
        padding: 14px 18px; 
        border-radius: 18px 18px 4px 18px; 
        margin: 10px 0;
        max-width: 80%;
    }
    .chat-bot { 
        background: #0f172a; 
        padding: 14px 18px; 
        border-radius: 4px 18px 18px 18px; 
        margin: 10px 0;
        max-width: 80%;
        border-left: 4px solid #00b4d8;
    }
    .stButton>button { background: #00b4d8; color: black; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Load Data
data = load_data()
vocab = build_vocab(data)

# Sidebar
st.sidebar.title("NEXUS")
st.sidebar.markdown("**Intelligent Academic Assistant**")
st.sidebar.divider()
st.sidebar.metric("Conversations", len(st.session_state.chat_history))

if st.sidebar.button("🗑️ New Conversation"):
    st.session_state.chat_history = []
    st.rerun()

# Main Interface
st.title("NEXUS")
st.caption("Your intelligent learning companion")

# Subject Selection
col1, col2 = st.columns([1, 1])
with col1:
    subject = st.selectbox("Subject", ["Science", "Commerce"], label_visibility="collapsed")
with col2:
    answer_type = st.selectbox("Response Style", ["Short", "Detailed"], label_visibility="collapsed")

selected_subject = "science" if subject == "Science" else "commerce"
selected_type = "short" if answer_type == "Short" else "long"

# Chat Display
if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f'<div class="chat-user"><strong>You</strong><br>{chat["question"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-bot"><strong>NEXUS</strong><br>{chat["answer"]}</div>', unsafe_allow_html=True)

# Input Area
question = st.chat_input("Ask any question...")

if question:
    corrected = auto_correct(question, vocab)
    
    with st.spinner("Thinking..."):
        answer, matched = get_best_answer(corrected, data, selected_type, selected_subject)
    
    st.session_state.chat_history.append({
        "question": question,
        "corrected": corrected,
        "answer": answer,
        "matched": matched,
        "type": selected_type,
        "time": datetime.now().strftime("%H:%M")
    })
    st.rerun()

# Footer
st.caption("NEXUS v3.8 • Knowledge Base Powered")
