import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct

# ================== SESSION STATE ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {"student": "1234"}

def login_page():
    st.title("🌌 NEXUS • Quantum Student AI")
    st.markdown("""
    <h3 style="text-align: center; color: #00ffcc;">
        Sign in to continue your learning journey
    </h3>
    """, unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])

    with tab1:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            username = st.text_input("👤 Username", placeholder="Enter username", key="login_user")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password", key="login_pass")
            
            if st.button("🚀 Sign In", type="primary", use_container_width=True):
                if username and password:
                    if username in st.session_state.users and st.session_state.users[username] == password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.warning("Please fill both fields")

    with tab2:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            new_user = st.text_input("👤 Choose Username", placeholder="New username", key="new_user")
            new_pass = st.text_input("🔑 Choose Password", type="password", placeholder="New password", key="new_pass")
            email = st.text_input("✉️ Email", placeholder="Your email")
            
            if st.button("📝 Create Account", type="primary", use_container_width=True):
                if new_user and new_pass and email:
                    if new_user in st.session_state.users:
                        st.error("Username already exists")
                    else:
                        st.session_state.users[new_user] = new_pass
                        st.success("Account created! Please Sign In.")
                else:
                    st.warning("Please fill all fields")

    st.caption("Data is saved during this session only.")

# ================== LOGIN GATE ==================
if not st.session_state.logged_in:
    login_page()
    st.stop()

# ================== MAIN APP ==================
st.set_page_config(
    page_title="NEXUS • Quantum Student AI",
    page_icon="🌌",
    layout="wide"
)

# Custom CSS (your previous styling)
st.markdown("""<style> ... your css here ... </style>""", unsafe_allow_html=True)

# Rest of your main app code goes here...
# (Paste the rest of your original app code from header to footer)

st.sidebar.title("⚡ NEURAL CONTROL PANEL")
# ... (add the rest of your code)
