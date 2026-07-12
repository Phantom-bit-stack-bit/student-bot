import streamlit as st

def login_page():
    st.title("🌌 NEXUS • Quantum Student AI")
    st.markdown("### 🔐 Secure Access")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("🚀 Login", type="primary", use_container_width=True):
            if username and password:
                # Simple authentication (you can improve this later)
                if username.lower() == "student" and password == "1234":
                    st.session_state.logged_in = True
                    st.success("Login Successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
    
    st.caption("Default Login → Username: `student` | Password: `1234`")
