import streamlit as st
import requests
import json
import uuid
import time
import base64
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

# Convert image to base64
def get_base64_image(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return ""

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
    skull_image = get_base64_image("static/terminator_skull.png")
    st.markdown(f"""
    <div class="header">
        <div class="header-content">
            <div class="header-left">
                <div class="logo">
                    <img src="data:image/png;base64,{skull_image}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; filter: brightness(0.9) contrast(1.1);">
                </div>
                <div class="title-section">
                    <h1 class="professional-title">SKYNET</h1>
                    <p class="subtitle">Neural Network Defense System</p>
                </div>
            </div>
            <div class="header-right">
                <div class="company-badge">System Online</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for chat management and personality selection
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Chat Management Section
        st.markdown("## 💬 Mission Archives")
        
        # New Chat Button
        if st.button("➕ New Mission", key="new_chat", use_container_width=True):
            # Generate a default title based on current time
            import datetime
            default_title = f"Mission {datetime.datetime.now().strftime('%m/%d %H:%M')}"
            new_chat = create_chat(default_title)
            if new_chat:
                st.session_state.current_chat_id = new_chat["id"]
                st.session_state.messages = []
                st.session_state.chats = get_chats()  # Refresh chats
                st.rerun()
        
        # Export Project Button
        if st.button("📦 Export Project", key="export_project", use_container_width=True):
            try:
                import subprocess
                import datetime
                
                # Run the export script
                result = subprocess.run(["python", "export_project.py"], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Get the zip filename from the output
                    output_lines = result.stdout.strip().split('\n')
                    zip_filename = None
                    for line in output_lines:
                        if line.startswith("📦 Export file:"):
                            zip_filename = line.split(": ")[1]
                            break
                    
                    if zip_filename:
                        # Read the zip file
                        with open(zip_filename, "rb") as f:
                            zip_data = f.read()
                        
                        # Create download button
                        st.download_button(
                            label="⬇️ Download Project",
                            data=zip_data,
                            file_name=zip_filename,
                            mime="application/zip",
                            key="download_zip"
                        )
                        st.success(f"✅ Project exported! Click above to download.")
                    else:
                        st.error("Could not find export file")
                else:
                    st.error(f"Export failed: {result.stderr}")
            except Exception as e:
                st.error(f"Export error: {str(e)}")
        
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
        st.markdown("## 🎯 Neural Agent Selection")
        
        if st.session_state.personalities:
            personality_options = {
                domain: f"{info['name']}" 
                for domain, info in st.session_state.personalities.items()
            }
            
            selected_personality = st.selectbox(
                "Select neural agent specialization:",
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
                <h2>Welcome to Skynet Neural Network</h2>
                <p>
                    Advanced neural network system with specialized tactical agents.
                </p>
                <p>
                    Initiate a new mission or access existing mission archives to begin operations.
                </p>
                <div style="margin-top: 2rem; padding: 1rem; background: rgba(220, 38, 38, 0.1); border-radius: 8px; border: 1px solid rgba(220, 38, 38, 0.2);">
                    <h4 style="color: #dc2626; margin-bottom: 0.5rem;">System Capabilities:</h4>
                    <ul style="color: #d4d4d4; line-height: 1.8; margin: 0;">
                        <li>Persistent mission archives</li>
                        <li>Multiple specialized neural agents</li>
                        <li>Advanced tactical interface</li>
                        <li>Real-time response processing</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <p style="margin: 0; font-weight: 600; color: var(--primary-red);">SKYNET NEURAL NETWORK</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted);">Powered by Advanced Learning Models | PostgreSQL Database</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted);">System Version 3.0</p>
                <p style="margin: 0; font-size: 0.8rem; color: var(--accent-orange); font-weight: 600;">Neural Network Defense System Initiated By Shaurya Singh</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
