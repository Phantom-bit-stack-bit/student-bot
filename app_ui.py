import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct
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
    st.markdown("### Intelligent Learning Assistant")
    st.markdown("Sign in to access your personal academic helper")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username", "student")
        password = st.text_input("Password", "1234", type="password")
        if st.button("Sign In", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ================== MAIN CONFIG ==================
st.set_page_config(page_title="NEXUS - Intelligent Learning Assistant", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0a0a0f; color: #e0e0e0; }
    .main { background: #0a0a0f; }
    h1 { color: #00ccff; }
    .stButton>button { background: #00ccff; color: black; font-weight: 600; }
    .stSuccess { background-color: #1a2a3a; border-left: 4px solid #00ccff; }
    .chat-user { background: #1e3a5f; padding: 15px; border-radius: 15px; margin: 10px 0; }
    .chat-bot { background: #16213e; padding: 15px; border-radius: 15px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# Load Data
data = load_data()
vocab = build_vocab(data)

# Sidebar
st.sidebar.title("NEXUS")
st.sidebar.markdown(f"**Student:** {st.session_state.get('current_user', 'Active User')}")
if st.sidebar.button("New Chat"):
    st.session_state.chat_history = []
    st.rerun()

st.sidebar.metric("Sessions", len(st.session_state.chat_history))

# Main Title
st.title("NEXUS")
st.markdown("**Intelligent Academic Assistant**")

# Subject & Type
col1, col2 = st.columns([1, 1])
with col1:
    subject = st.selectbox("Subject", ["Science", "Commerce"], label_visibility="collapsed")
with col2:
    answer_type = st.selectbox("Response Style", ["Short", "Detailed"], label_visibility="collapsed")

selected_subject = "science" if subject == "Science" else "commerce"
selected_type = "short" if answer_type == "Short" else "long"

# Chat Interface
if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"""
        <div class="chat-user">
            <strong>You:</strong> {chat['question']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="chat-bot">
            <strong>NEXUS:</strong><br>{chat['answer']}
        </div>
        """, unsafe_allow_html=True)

# Input Area
question = st.text_input("Ask your question...", placeholder="What is Newton's Second Law?", key="user_input")

col1, col2 = st.columns([4, 1])
with col1:
    if st.button("Send", type="primary", use_container_width=True):
        if question.strip():
            corrected = auto_correct(question, vocab)
            with st.spinner("Searching knowledge base..."):
                answer, matched = get_best_answer(corrected, data, selected_type, selected_subject)
            
            st.session_state.chat_history.append({
                "question": question,
                "corrected": corrected,
                "answer": answer,
                "matched": matched,
                "type": selected_type
            })
            st.rerun()

with col2:
    st.button("Clear", on_click=lambda: st.session_state.chat_history.clear())

st.caption("NEXUS v3.8 • Powered by Knowledge Base")
