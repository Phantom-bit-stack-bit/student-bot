import streamlit as st

def login_page():
    st.title("🌌 NEXUS • Quantum Student AI")
    
    st.markdown("""
    <h3 style="text-align: center; color: #00ffcc;">
        Sign in to continue your learning journey
    </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Simple in-memory users (for demo)
    if "users" not in st.session_state:
        st.session_state.users = {"student": "1234"}

    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])

    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("👤 Username", placeholder="Enter username", key="login_username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password", key="login_password")
            
            if st.button("🚀 Sign In", type="primary", use_container_width=True):
                if username and password:
                    if username in st.session_state.users and st.session_state.users[username] == password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("Please enter both username and password")

    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            new_username = st.text_input("👤 Choose Username", placeholder="Choose username", key="signup_username")
            new_password = st.text_input("🔑 Choose Password", type="password", placeholder="Choose password", key="signup_password")
            email = st.text_input("✉️ Email", placeholder="Enter email")
            
            if st.button("📝 Create Account", type="primary", use_container_width=True):
                if new_username and new_password and email:
                    if new_username in st.session_state.users:
                        st.error("❌ Username already exists")
                    else:
                        st.session_state.users[new_username] = new_password
                        st.success("✅ Account created! Please go to Sign In tab.")
                else:
                    st.warning("Please fill all fields")

    st.caption("Signup works in this session. Data resets when you restart the app.")
