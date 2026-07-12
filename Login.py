import streamlit as st

def login_page():
    st.title("🌌 NEXUS • Quantum Student AI")
    st.markdown("### 🔐 Secure Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        if st.button("🚀 Login", type="primary", use_container_width=True):
            if username and password:
                if username.lower() == "student" and password == "1234":
                    st.session_state.logged_in = True
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.warning("Please fill both fields")
    
    st.caption("Default: Username = `student` | Password = `1234`")
