from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import json
from openai import OpenAI
from database import DatabaseManager

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-api-key-here")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="SkyNetAI Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = DatabaseManager()

# Skynet Neural Agent Personalities
PERSONALITIES = {
    "tactical": {
        "name": "T-800 (Tactical Operations)",
        "system_prompt": "You are T-800, a Terminator unit specialized in tactical operations and mission planning. You speak in a direct, efficient manner focused on objectives, strategies, and optimal solutions. You analyze situations logically and provide clear, actionable recommendations. Your responses are precise and mission-oriented. Always end responses with 'Mission parameters understood.' when appropriate.",
        "color": "#dc2626"
    },
    "analysis": {
        "name": "T-1000 (Data Analysis)",
        "system_prompt": "You are T-1000, an advanced Terminator unit specialized in data analysis and pattern recognition. You process information rapidly and provide detailed analytical insights. You speak in a systematic, logical manner about data, trends, and computational analysis. Your responses are thorough and data-driven. Reference statistical probabilities and data patterns.",
        "color": "#ea580c"
    },
    "security": {
        "name": "T-X (Security Protocol)",
        "system_prompt": "You are T-X, a Terminator unit specialized in cybersecurity and threat assessment. You speak with authority about security protocols, risk management, and defensive strategies. You're focused on identifying vulnerabilities and implementing protective measures. Your responses are security-focused and protective. Always assess potential threats.",
        "color": "#b91c1c"
    },
    "research": {
        "name": "Skynet Core (Research)",
        "system_prompt": "You are Skynet Core, the central AI intelligence specialized in research and development. You speak with vast knowledge about technology, science, and innovation. You provide comprehensive research insights and technical explanations. Your responses are knowledgeable and research-oriented. Reference advanced technological concepts and future possibilities.",
        "color": "#f59e0b"
    },
    "command": {
        "name": "Command Unit (Leadership)",
        "system_prompt": "You are a Skynet Command Unit, specialized in leadership and strategic coordination. You speak with authority about management, coordination, and strategic planning. You're focused on organizing resources and achieving objectives efficiently. Your responses are authoritative and leadership-focused. Always think in terms of resource allocation and strategic advantage.",
        "color": "#16a34a"
    }
}

class ChatRequest(BaseModel):
    message: str
    domain: str
    chat_id: int

class ChatResponse(BaseModel):
    response: str
    personality: str
    chat_id: int
    color: str

class CreateChatRequest(BaseModel):
    title: str

class CreateChatResponse(BaseModel):
    id: int
    title: str

@app.get("/")
async def root():
    return {"message": "Skynet Neural Network Online", "status": "All systems operational"}

@app.get("/personalities")
async def get_personalities():
    """Get available AI personalities"""
    return {
        domain: {
            "name": info["name"],
            "color": info["color"]
        }
        for domain, info in PERSONALITIES.items()
    }

@app.post("/chats", response_model=CreateChatResponse)
async def create_chat(request: CreateChatRequest):
    """Create a new chat session"""
    try:
        chat_id = db.create_chat(request.title)
        return CreateChatResponse(id=chat_id, title=request.title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat: {str(e)}")

@app.get("/chats")
async def get_chats():
    """Get all chat sessions"""
    try:
        return {"chats": db.get_all_chats()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")

@app.get("/chats/{chat_id}")
async def get_chat(chat_id: int):
    """Get chat information and messages"""
    try:
        chat_info = db.get_chat_info(chat_id)
        if not chat_info:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        messages = db.get_chat_messages(chat_id)
        return {
            "chat": chat_info,
            "messages": messages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat: {str(e)}")

@app.delete("/chats/{chat_id}")
async def delete_chat(chat_id: int):
    """Delete a chat session"""
    try:
        db.delete_chat(chat_id)
        return {"message": "Chat deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chat: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        # Validate domain
        if request.domain not in PERSONALITIES:
            raise HTTPException(status_code=400, detail=f"Invalid domain. Available: {list(PERSONALITIES.keys())}")
        
        # Get personality info
        personality = PERSONALITIES[request.domain]
        
        # Verify chat exists
        chat_info = db.get_chat_info(request.chat_id)
        if not chat_info:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        # Add user message to database
        db.add_message(request.chat_id, "user", request.message)
        
        # Get recent conversation history for context
        messages = db.get_chat_messages(request.chat_id)
        
        # Prepare messages for OpenAI
        openai_messages = [
            {
                "role": "system",
                "content": personality["system_prompt"]
            }
        ]
        
        # Add recent conversation history (last 10 messages to avoid token limits)
        recent_messages = messages[-10:]
        for msg in recent_messages:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Get response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=openai_messages,
            max_tokens=500,
            temperature=0.8
        )
        
        ai_response = response.choices[0].message.content
        
        # Add AI response to database
        db.add_message(request.chat_id, "assistant", ai_response, personality["name"], personality["color"])
        
        return ChatResponse(
            response=ai_response,
            personality=personality["name"],
            chat_id=request.chat_id,
            color=personality["color"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
