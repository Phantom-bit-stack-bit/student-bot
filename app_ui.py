import streamlit as st
from hh import get_best_answer, load_data, build_vocab, auto_correct

# ================== CONFIG ==================
st.set_page_config(
    page_title="NEXUS • Quantum Student AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Sci-Fi CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0a1f 0%, #1a0033 100%);
        color: #00ffcc;
    }
    
    h1, h2, h3 {
        color: #00ffff !important;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
        font-family: 'Courier New', monospace;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #ff00ff);
        color: #000000;
        border: none;
        border-radius: 20px;
        padding: 12px 24px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 15px #00ffcc, 0 0 30px #ff00ff;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px #00ffcc, 0 0 50px #ff00ff;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a0033;
        color: #00ffcc;
        border: 2px solid #00ffff;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
    }
    
    .chat-container {
        border: 1px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        background: rgba(10, 10, 31, 0.8);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ================== LOAD ==================
data = load_data()
vocab = build_vocab(data)

# ================== SESSION ==================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================== SIDEBAR ==================
st.sidebar.title("⚡ NEURAL CONTROL PANEL")
st.sidebar.markdown("---")
st.sidebar.info("🌐 Accessing Quantum Knowledge Core v3.7")
st.sidebar.caption("Neural Interface Online")

if st.sidebar.button("🌀 PURGE MEMORY CACHE"):
    st.session_state.chat_history = []
    st.rerun()

st.sidebar.markdown("### 📡 SYSTEM STATUS")
st.sidebar.success("✅ Quantum Link Stable")
st.sidebar.progress(0.92)

# ================== HEADER ==================
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("# 🌌")
with col2:
    st.title("NEXUS • QUANTUM STUDENT AI")
    st.markdown("**_Neural Learning Interface v3.7_**")

st.markdown("---")

# ================== CONTROLS ==================
col1, col2 = st.columns(2)

with col1:
    subject = st.selectbox(
        "📡 SELECT KNOWLEDGE DOMAIN",
        ["Science", "Commerce"]
    )

with col2:
    answer_type = st.selectbox(
        "🔬 RESPONSE PROTOCOL",
        ["Short", "Detailed"]
    )

selected_subject = "science" if subject == "Science" else "commerce"
selected_type = "short" if answer_type == "Short" else "long"

# ================== SUGGESTIONS ==================
st.markdown("### 🔮 QUANTUM SUGGESTIONS")
suggestions = {
    "Science": [
        "What is gravity?",
        "Explain photosynthesis",
        "Difference between mass and weight"
    ],
    "Commerce": [
        "What is business?",
        "Explain profit",
        "Difference between assets and liabilities"
    ]
}

cols = st.columns(3)
for i, q in enumerate(suggestions[subject]):
    with cols[i]:
        if st.button(q, key=f"sug_{i}"):
            st.session_state["prefill"] = q

# ================== QUERY INPUT ==================
st.markdown("### ✴️ TRANSMIT QUERY")
question = st.text_input(
    "Enter your query to the Neural Core:",
    value=st.session_state.get("prefill", ""),
    placeholder="e.g., Explain quantum entanglement..."
)

submit = st.button("🚀 TRANSMIT TO NEXUS", type="primary")

# ================== LOGIC ==================
if submit:
    if len(question.strip()) < 3:
        st.error("⚠️ QUERY TOO FRAGMENTED - Please provide more data")
    else:
        corrected_question = auto_correct(question, vocab)
        
        if corrected_question != question.lower():
            st.info(f"🔄 NEURAL INTERPRETATION: **{corrected_question}**")
        
        is_duplicate = any(chat["corrected"] == corrected_question 
                          for chat in st.session_state.chat_history)
        
        if not is_duplicate:
            # In the LOGIC section, change the spinner text and maybe force better answers
            with st.spinner("🔄 SYNCHRONIZING WITH QUANTUM ARCHIVES..."):
                answer, matched_q = get_best_answer(
                    corrected_question, data, selected_type, selected_subject
                )
            
            st.session_state.chat_history.append({
                "question": question,
                "corrected": corrected_question,
                "answer": answer,
                "matched": matched_q,
                "type": selected_type
            })
        else:
            st.warning("📡 DUPLICATE QUERY DETECTED IN TEMPORAL CACHE")

# ================== CHAT DISPLAY ==================
# ================== CHAT DISPLAY ==================
if st.session_state.chat_history:
    st.markdown("### 📜 TEMPORAL QUERY LOG")
    
    for chat in reversed(st.session_state.chat_history):
        interpreted = ""
        if chat["corrected"] != chat["question"].lower():
            interpreted = f'''
                <div style="color:#ffff00; font-size:0.85em; margin-top:8px;">
                    🔄 Interpreted as: <strong>{chat["corrected"]}</strong>
                </div>
            '''
        
        st.markdown(f"""
        <div class="chat-container">
            <div style="color:#ff00ff; font-weight:bold; margin-bottom:8px;">🧬 USER TRANSMISSION:</div>
            <div style="margin: 10px 0; padding: 12px; background: rgba(0,0,0,0.6); border-radius: 8px; color: #ffffff;">
                {chat["question"]}
            </div>
            
            <div style="color:#00ffcc; font-weight:bold; margin: 12px 0 8px 0;">🤖 NEXUS RESPONSE:</div>
            <div style="margin: 10px 0; padding: 15px; background: rgba(0, 255, 204, 0.1); 
                        border-radius: 8px; border: 1px solid #00ffcc; line-height: 1.5;">
                {chat["answer"]}
            </div>
            
            <div style="font-size: 0.85em; color: #888; margin-top: 12px;">
                📍 Matched: <strong>{chat['matched']}</strong> &nbsp;&nbsp;|&nbsp;&nbsp; 
                ⚙️ Protocol: <strong>{chat['type'].upper()}</strong>
            </div>
            {interpreted}
        </div>
        """, unsafe_allow_html=True)
# ================== FOOTER ==================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    ⚡️ <strong>NEXUS v3.7</strong> • Quantum Education Division • 
    <span style="color:#00ffcc">Built by Arpit</span> • 
    <span style="color:#ff00ff">NEURAL CORE ONLINE</span>
</div>
""", unsafe_allow_html=True)
