<<<<<<< HEAD
#!/usr/bin/env python3
"""
SkyNetAI - Cyberpunk AI Chatbot
Main entry point for the application

This script helps you start both the backend and frontend servers.
"""

import subprocess
import sys
import os
import threading
import time

def run_backend():
    """Run the backend server"""
    print("🚀 Starting Backend Server...")
    try:
        subprocess.run([sys.executable, "run_backend.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Run the frontend server"""
    print("🎨 Starting Frontend Server...")
    time.sleep(3)  # Wait for backend to start
    try:
        subprocess.run([sys.executable, "run_frontend.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def main():
    """Main entry point"""
    print("=" * 60)
    print("🤖 SkyNetAI - Cyberpunk AI Chatbot")
    print("=" * 60)
    print("Welcome to the Matrix of AI Consciousness!")
    print()
    print("This will start both the backend and frontend servers.")
    print("Backend (FastAPI): http://localhost:8000")
    print("Frontend (Streamlit): http://localhost:5000")
    print()
    print("⚠️  Make sure you have set your OPENAI_API_KEY environment variable!")
    print("   export OPENAI_API_KEY=your_api_key_here")
    print()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not found!")
        print("   Please set it and try again.")
        response = input("Do you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(1)
    
    print("🚀 Starting SkyNetAI servers...")
    print("Press Ctrl+C to stop both servers")
    print()
    
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Start frontend in main thread
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down SkyNetAI...")
        print("Goodbye from the Matrix!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
=======
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from chat_handler import get_openai_response
from memory import get_history, add_message, reset_session

load_dotenv()

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    domain: str
    session_id: str

class ChatResponse(BaseModel):
    reply: str
    history: list

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    if req.message.lower() == "__reset__":
        reset_session(req.session_id)
        return {"reply": "Session reset.", "history": []}
    history = get_history(req.session_id)
    add_message(req.session_id, "user", req.message)
    reply = get_openai_response(req.message, req.domain, req.session_id, history)
    add_message(req.session_id, "assistant", reply)
    updated_history = get_history(req.session_id)
    return {"reply": reply, "history": updated_history} 
>>>>>>> 40c0a3db4f3ad2d4297e7d1145c8ef533170b5c1
