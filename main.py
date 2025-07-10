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