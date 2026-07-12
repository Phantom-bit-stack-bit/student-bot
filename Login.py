import streamlit as st

def login_page():
    st.title("🌌 NEXUS • Quantum Student AI")
    
    st.markdown("""
    <h3 style="text-align: center; color: #00ffcc;">
        Sign in to continue your learning journey
    </h3>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        
        if st.button("🚀 Sign In", type="primary", use_container_width=True):
            if username and password:
                if username.lower() == "student" and password == "1234":
                    st.session_state.logged_in = True
                    st.success("Welcome back! Redirecting to NEXUS...")
                    st.rerun()
                else:
                    st.error("❌ Incorrect username or password")
            else:
                st.warning("Please enter both username and password")
    
    st.caption("💡 Default credentials for demo: `student` / `1234`")
