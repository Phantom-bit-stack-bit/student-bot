import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct
from datetime import datetime

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Login
if not st.session_state.logged_in:
    st.set_page_config(page_title="NEXUS", page_icon="🌌", layout="centered")
    st.title("🌌 NEXUS")
    st.markdown("### Your Intelligent Learning Companion")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Sign In as Student", type="primary"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# Config + Styling
st.set_page_config(page_title="NEXUS", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a1f 0%, #1a0033 100%);
    }
    h1 {
        color: #00f0ff;
        text-shadow: 0 0 20px #00f0ff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .chat-user {
        background: linear-gradient(90deg, #1e3a5f, #2a4a7a);
        padding: 16px 20px;
        border-radius: 20px 20px 4px 20px;
        margin: 12px 0;
        color: white;
    }
    .chat-bot {
        background: linear-gradient(90deg, #0f172a, #1e2937);
        padding: 16px 20px;
        border-radius: 4px 20px 20px 20px;
        margin: 12px 0;
        border-left: 5px solid #00f0ff;
        color: #e0f0ff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00f0ff, #ff00cc);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 12px;
    }
    .stTextInput > div > div > input {
        background: #1a1a2e;
        color: white;
        border: 2px solid #00f0ff;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
data = load_data()
vocab = build_vocab(data)

# Sidebar
st.sidebar.title("🌌 NEXUS")
st.sidebar.markdown("**Intelligent Learning Assistant**")
st.sidebar.divider()
st.sidebar.metric("Questions Asked", len(st.session_state.chat_history))

if st.sidebar.button("New Chat"):
    st.session_state.chat_history = []
    st.rerun()

# Main UI
st.title("NEXUS")
st.markdown("*Your personal academic companion*")

# Controls
col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("Subject", ["Science", "Commerce"])
with col2:
    answer_type = st.selectbox("Response Style", ["Short", "Detailed"])

selected_subject = "science" if subject == "Science" else "commerce"
selected_type = "short" if answer_type == "Short" else "long"

# Chat Display
if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"""
        <div class="chat-user">
            <strong>You</strong><br>{chat['question']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="chat-bot">
            <strong>NEXUS</strong><br>{chat['answer']}
        </div>
        """, unsafe_allow_html=True)

# Input
question = st.chat_input("Ask any academic question...")

if question:
    corrected = auto_correct(question, vocab)
    with st.spinner("Finding best answer..."):
        answer, matched = get_best_answer(corrected, data, selected_type, selected_subject)
    
    st.session_state.chat_history.append({
        "question": question,
        "answer": answer,
        "matched": matched,
        "type": selected_type
    })
    st.rerun()

st.caption("NEXUS v3.9 • Helping Students Learn Better")
