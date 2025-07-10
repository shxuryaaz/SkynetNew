import streamlit as st
import requests
import uuid
import time

st.set_page_config(page_title="SkyNetAI – Secure Conversational Intelligence", page_icon="🤖", layout="wide")

# Custom CSS and fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Share+Tech+Mono&display=swap');
    html, body, [class*="css"]  {
        background-color: #0a0a0a !important;
        color: #fff !important;
        font-family: 'Share Tech Mono', 'Orbitron', monospace !important;
    }
    .skynet-title {
        font-family: 'Orbitron', monospace;
        color: #ff003c;
        font-size: 2.5rem;
        letter-spacing: 2px;
        text-shadow: 0 0 10px #ff003c, 0 0 20px #ff003c;
        border-bottom: 2px solid #ff003c;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .skynet-dropdown label, .skynet-dropdown select {
        color: #ff003c !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 1.1rem;
    }
    .skynet-chatbox {
        background: #18181a;
        border: 2px solid #ff003c;
        border-radius: 10px;
        padding: 1rem;
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        box-shadow: 0 0 20px #ff003c44;
    }
    .skynet-bubble-user {
        background: #ff003c22;
        color: #ff003c;
        border-left: 4px solid #ff003c;
        margin: 0.5rem 0;
        padding: 0.5rem 1rem;
        border-radius: 8px 8px 8px 2px;
        font-family: 'Share Tech Mono', monospace;
        text-shadow: 0 0 5px #ff003c88;
    }
    .skynet-bubble-ai {
        background: #222226;
        color: #fff;
        border-left: 4px solid #ff003c;
        margin: 0.5rem 0;
        padding: 0.5rem 1rem;
        border-radius: 8px 8px 2px 8px;
        font-family: 'Share Tech Mono', monospace;
        text-shadow: 0 0 5px #fff8;
    }
    .skynet-reset {
        border: 2px solid #ff003c !important;
        color: #ff003c !important;
        background: #0a0a0a !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 1.1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 0 10px #ff003c44;
        transition: box-shadow 0.2s;
    }
    .skynet-reset:hover {
        box-shadow: 0 0 20px #ff003c;
        background: #18181a !important;
    }
    .skynet-input input {
        background: #18181a !important;
        color: #ff003c !important;
        border: 2px solid #ff003c !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1.1rem !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state["history"] = []
if "domain" not in st.session_state:
    st.session_state["domain"] = "General"

API_URL = "http://localhost:8000/chat"

def render_chat():
    st.markdown('<div class="skynet-chatbox">', unsafe_allow_html=True)
    for msg in st.session_state["history"]:
        if msg["role"] == "user":
            st.markdown(f'<div class="skynet-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f'<div class="skynet-bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def send_message(message):
    data = {
        "message": message,
        "domain": st.session_state["domain"],
        "session_id": st.session_state["session_id"]
    }
    try:
        resp = requests.post(API_URL, json=data)
        if resp.status_code == 200:
            result = resp.json()
            st.session_state["history"] = result["history"]
            return result["reply"]
        else:
            return "[Error: Backend unavailable]"
    except Exception as e:
        return f"[Error: {e}]"

# Title
st.markdown('<div class="skynet-title">SkyNetAI – Secure Conversational Intelligence</div>', unsafe_allow_html=True)

# Domain dropdown
with st.container():
    st.markdown('<div class="skynet-dropdown">', unsafe_allow_html=True)
    domain = st.selectbox("Select Domain", ["General", "Finance", "Education", "Tech"], key="domain")
    st.markdown('</div>', unsafe_allow_html=True)

# Chat history
render_chat()

# User input
with st.form(key="skynet-chat-form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", key="user_input", placeholder="Enter your message here", label_visibility="collapsed")
    submitted = st.form_submit_button("Send", use_container_width=True)

if submitted and user_input.strip():
    with st.spinner("AI is thinking ..."):
        # Animated loading dots
        for i in range(3):
            st.markdown(f'<span style="color:#ff003c;font-family:Orbitron;font-size:1.2rem;">AI is thinking{'.' * (i+1)}</span>', unsafe_allow_html=True)
            time.sleep(0.3)
        send_message(user_input)
        st.rerun()

# Reset button
if st.button("Reset Chat", key="reset", help="Clear chat session", use_container_width=True):
    send_message("__reset__")
    st.session_state["history"] = []
    st.session_state["session_id"] = str(uuid.uuid4())
    st.rerun() 