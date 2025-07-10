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
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_personality" not in st.session_state:
        st.session_state.current_personality = "hacker"
    if "personalities" not in st.session_state:
        st.session_state.personalities = {}
    if "chats" not in st.session_state:
        st.session_state.chats = []

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

def get_chats():
    """Fetch all chats from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/chats")
        if response.status_code == 200:
            return response.json()["chats"]
        else:
            st.error("Failed to fetch chats")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return []

def create_chat(title: str):
    """Create a new chat"""
    try:
        payload = {"title": title}
        response = requests.post(f"{BACKEND_URL}/chats", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error creating chat: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error creating chat: {e}")
        return None

def get_chat_messages(chat_id: int):
    """Get messages for a specific chat"""
    try:
        response = requests.get(f"{BACKEND_URL}/chats/{chat_id}")
        if response.status_code == 200:
            return response.json()["messages"]
        else:
            st.error(f"Error fetching messages: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error fetching messages: {e}")
        return []

def send_message(message: str, domain: str, chat_id: int):
    """Send message to backend"""
    try:
        payload = {
            "message": message,
            "domain": domain,
            "chat_id": chat_id
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

def delete_chat(chat_id: int):
    """Delete a chat"""
    try:
        response = requests.delete(f"{BACKEND_URL}/chats/{chat_id}")
        if response.status_code == 200:
            st.success("Chat deleted")
            return True
        else:
            st.error(f"Error deleting chat: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Error deleting chat: {e}")
        return False

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
    
    # Sidebar for chat management and personality selection
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Chat Management Section
        st.markdown("## 💬 Chat Sessions")
        
        # New Chat Button
        if st.button("➕ New Chat", key="new_chat", use_container_width=True):
            # Generate a default title based on current time
            import datetime
            default_title = f"Chat {datetime.datetime.now().strftime('%m/%d %H:%M')}"
            new_chat = create_chat(default_title)
            if new_chat:
                st.session_state.current_chat_id = new_chat["id"]
                st.session_state.messages = []
                st.session_state.chats = get_chats()  # Refresh chats
                st.rerun()
        
        # Load chats
        st.session_state.chats = get_chats()
        
        # Display chat list
        if st.session_state.chats:
            st.markdown("### Recent Chats")
            for chat in st.session_state.chats:
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(
                        f"📝 {chat['title'][:20]}..." if len(chat['title']) > 20 else f"📝 {chat['title']}", 
                        key=f"chat_{chat['id']}", 
                        use_container_width=True
                    ):
                        st.session_state.current_chat_id = chat['id']
                        st.session_state.messages = get_chat_messages(chat['id'])
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"delete_{chat['id']}", help="Delete chat"):
                        if delete_chat(chat['id']):
                            if st.session_state.current_chat_id == chat['id']:
                                st.session_state.current_chat_id = None
                                st.session_state.messages = []
                            st.session_state.chats = get_chats()  # Refresh chats
                            st.rerun()
        else:
            st.markdown("*No chats yet. Create your first chat!*")
        
        st.markdown("---")
        
        # Personality Selection Section
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
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat interface
    if st.session_state.current_chat_id:
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
                # Show loading indicator
                with st.spinner("AI is thinking..."):
                    # Send message to backend
                    response = send_message(
                        user_input,
                        st.session_state.current_personality,
                        st.session_state.current_chat_id
                    )
                    
                    if response:
                        # Reload messages from database to get the updated conversation
                        st.session_state.messages = get_chat_messages(st.session_state.current_chat_id)
                        
                        # Rerun to update the chat display
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # No chat selected - show welcome message
        st.markdown("""
        <div class="chat-container">
            <div class="welcome-message">
                <h2 style="color: #00d4ff; text-align: center;">Welcome to SkyNetAI</h2>
                <p style="text-align: center; color: #cccccc;">
                    Create a new chat or select an existing one to start your cyberpunk AI experience.
                </p>
                <p style="text-align: center; color: #888888;">
                    Choose your AI companion and dive into the digital realm!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>⚡ Powered by SkyNetAI | 🌐 Connected to the Matrix</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
