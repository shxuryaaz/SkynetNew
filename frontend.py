import streamlit as st
import requests
import json
import uuid
import time
from typing import Dict, List

# Configure Streamlit page
st.set_page_config(
    page_title="SkyNetAI - Cyberpunk Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open("static/cyberpunk.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_personality" not in st.session_state:
        st.session_state.current_personality = "hacker"
    if "personalities" not in st.session_state:
        st.session_state.personalities = {}

# API endpoints
BACKEND_URL = "http://localhost:8000"

def get_personalities():
    """Fetch available personalities from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/personalities")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch personalities")
            return {}
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return {}

def send_message(message: str, domain: str, session_id: str):
    """Send message to backend"""
    try:
        payload = {
            "message": message,
            "domain": domain,
            "session_id": session_id
        }
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error sending message: {e}")
        return None

def clear_session():
    """Clear current session"""
    try:
        requests.delete(f"{BACKEND_URL}/session/{st.session_state.session_id}")
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.success("Session cleared")
    except Exception as e:
        st.error(f"Error clearing session: {e}")

def main():
    # Load CSS and initialize
    load_css()
    init_session_state()
    
    # Get personalities from backend
    if not st.session_state.personalities:
        st.session_state.personalities = get_personalities()
    
    # Header
    st.markdown("""
    <div class="header">
        <h1 class="neon-title">🤖 SkyNetAI</h1>
        <p class="subtitle">Enter the Matrix of AI Consciousness</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for personality selection
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("## 🎭 Select AI Personality")
        
        if st.session_state.personalities:
            personality_options = {
                domain: f"{info['name']}" 
                for domain, info in st.session_state.personalities.items()
            }
            
            selected_personality = st.selectbox(
                "Choose your cyberpunk companion:",
                options=list(personality_options.keys()),
                format_func=lambda x: personality_options[x],
                index=list(personality_options.keys()).index(st.session_state.current_personality) if st.session_state.current_personality in personality_options else 0
            )
            
            st.session_state.current_personality = selected_personality
            
            # Display personality info
            if selected_personality in st.session_state.personalities:
                personality_info = st.session_state.personalities[selected_personality]
                st.markdown(f"""
                <div class="personality-info">
                    <h3 style="color: {personality_info['color']}">
                        {personality_info['name']}
                    </h3>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Session controls
        st.markdown("## 🔧 Session Controls")
        if st.button("🗑️ Clear Session", key="clear_session"):
            clear_session()
        
        st.markdown(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="message-header">
                    <span class="user-icon">👤</span>
                    <span class="user-name">User</span>
                </div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            color = message.get("color", "#00ff41")
            personality = message.get("personality", "AI")
            st.markdown(f"""
            <div class="ai-message">
                <div class="message-header">
                    <span class="ai-icon">🤖</span>
                    <span class="ai-name" style="color: {color}">{personality}</span>
                </div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Enter your message:",
                placeholder="Type your message to the AI...",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("Send 🚀")
        
        if submit_button and user_input:
            # Add user message to session
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Show loading indicator
            with st.spinner("AI is thinking..."):
                # Send message to backend
                response = send_message(
                    user_input,
                    st.session_state.current_personality,
                    st.session_state.session_id
                )
                
                if response:
                    # Add AI response to session
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["response"],
                        "personality": response["personality"],
                        "color": response["color"]
                    })
                    
                    # Rerun to update the chat display
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>⚡ Powered by SkyNetAI | 🌐 Connected to the Matrix</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
