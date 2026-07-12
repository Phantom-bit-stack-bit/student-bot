import streamlit as st
import json
from pathlib import Path

# File to store users
USERS_FILE = Path("users.json")

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {"student": "1234"}  # default user

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def login_page():
    st.title("🌌 NEXUS • Quantum Student AI")
    st.markdown("""
    <h3 style="text-align: center; color: #00ffcc;">
        Sign in to continue your learning journey
    </h3>
    """, unsafe_allow_html=True)
    st.markdown("---")

    users = load_users()

    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])

    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 Username", placeholder="Enter username", key="login_user")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password", key="login_pass")
            
            if st.button("🚀 Sign In", type="primary", use_container_width=True):
                if username and password:
                    if username in users and users[username] == password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("Please fill both fields")

    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            new_username = st.text_input("👤 Choose Username", placeholder="Enter new username", key="signup_user")
            new_password = st.text_input("🔑 Choose Password", type="password", placeholder="Enter password", key="signup_pass")
            email = st.text_input("✉️ Email", placeholder="Enter your email")
            
            if st.button("📝 Create Account", type="primary", use_container_width=True):
                if new_username and new_password and email:
                    if new_username in users:
                        st.error("Username already exists")
                    else:
                        users[new_username] = new_password
                        save_users(users)
                        st.success("✅ Account created successfully! You can now Sign In.")
                else:
                    st.warning("Please fill all fields")

    st.caption("New users can sign up. Your data is saved locally.")
