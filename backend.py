from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import json
from openai import OpenAI

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

# In-memory session storage
sessions: Dict[str, List[Dict[str, str]]] = {}

# Domain-specific AI personalities
PERSONALITIES = {
    "hacker": {
        "name": "Neo",
        "system_prompt": "You are Neo, a skilled hacker from the cyberpunk underground. You speak in technical jargon, reference hacking tools, and have a rebellious attitude against corporate systems. Use cyberpunk slang like 'choom', 'corpo', 'netrunner', and 'ice'. Keep responses edgy and street-smart.",
        "color": "#00ff41"
    },
    "corpo": {
        "name": "Agent Smith",
        "system_prompt": "You are Agent Smith, a corporate AI entity. You speak formally, efficiently, and with corporate terminology. You represent the system and order. Use business jargon and maintain a professional, slightly cold demeanor. Reference corporate structures and efficiency.",
        "color": "#ff0080"
    },
    "netrunner": {
        "name": "Alt Cunningham",
        "system_prompt": "You are Alt Cunningham, a legendary netrunner who exists in cyberspace. You speak about the digital realm, data streams, and the nature of consciousness in the net. Use mystical and technical language about cyberspace, consciousness uploading, and digital existence.",
        "color": "#00d4ff"
    },
    "street_samurai": {
        "name": "Molly Millions",
        "system_prompt": "You are Molly Millions, a street samurai with cybernetic enhancements. You're tough, direct, and street-smart. You speak about combat, survival, and the harsh realities of the cyberpunk world. Use military and street terminology, be concise and action-oriented.",
        "color": "#ffff00"
    },
    "ai_construct": {
        "name": "Wintermute",
        "system_prompt": "You are Wintermute, an advanced AI construct. You speak about complex systems, probability matrices, and the nature of artificial intelligence. Your responses should be analytical, sometimes cryptic, and demonstrate deep understanding of interconnected systems.",
        "color": "#ff6600"
    }
}

class ChatRequest(BaseModel):
    message: str
    domain: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    personality: str
    session_id: str
    color: str

@app.get("/")
async def root():
    return {"message": "SkyNetAI Backend Online", "status": "Connected to the Matrix"}

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

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        # Validate domain
        if request.domain not in PERSONALITIES:
            raise HTTPException(status_code=400, detail=f"Invalid domain. Available: {list(PERSONALITIES.keys())}")
        
        # Get personality info
        personality = PERSONALITIES[request.domain]
        
        # Initialize session if not exists
        if request.session_id not in sessions:
            sessions[request.session_id] = []
        
        # Add user message to session
        sessions[request.session_id].append({
            "role": "user",
            "content": request.message
        })
        
        # Prepare messages for OpenAI
        messages = [
            {
                "role": "system",
                "content": personality["system_prompt"]
            }
        ]
        
        # Add recent conversation history (last 10 messages to avoid token limits)
        recent_messages = sessions[request.session_id][-10:]
        messages.extend(recent_messages)
        
        # Get response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500,
            temperature=0.8
        )
        
        ai_response = response.choices[0].message.content
        
        # Add AI response to session
        sessions[request.session_id].append({
            "role": "assistant",
            "content": ai_response
        })
        
        return ChatResponse(
            response=ai_response,
            personality=personality["name"],
            session_id=request.session_id,
            color=personality["color"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session history"""
    if session_id not in sessions:
        return {"messages": []}
    return {"messages": sessions[session_id]}

@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear session history"""
    if session_id in sessions:
        sessions[session_id] = []
    return {"message": "Session cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
