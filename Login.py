import streamlit as st
import json
import os

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return []
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

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
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 Username", placeholder="Enter username", key="login_user")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password", key="login_pass")
            
            if st.button("🚀 Sign In", type="primary", use_container_width=True):
                if username and password:
                    users = load_users()
                    found = any(
                        user["username"] == username and user["password"] == password 
                        for user in users
                    )
                    if found or (username == "student" and password == "1234"):
                        st.session_state.logged_in = True
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("Please fill both fields")

    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            new_username = st.text_input("👤 Create Username", placeholder="Choose username", key="signup_user")
            new_password = st.text_input("🔑 Create Password", type="password", placeholder="Choose password", key="signup_pass")
            email = st.text_input("✉️ Email", placeholder="Enter your email")
            
            if st.button("📝 Create Account", type="primary", use_container_width=True):
                if new_username and new_password and email:
                    users = load_users()
                    # Check if username exists
                    if any(user["username"] == new_username for user in users):
                        st.error("❌ Username already exists")
                    else:
                        users.append({
                            "username": new_username,
                            "password": new_password,
                            "email": email
                        })
                        save_users(users)
                        st.success("✅ Account created successfully! Please sign in now.")
                else:
                    st.warning("Please fill all fields")

    st.caption("Accounts are saved locally in users.json")
