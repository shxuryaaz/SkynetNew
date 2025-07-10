import os
from dotenv import load_dotenv
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPTS = {
    "General": "You are SkyNetAI, a highly intelligent, secure conversational AI.",
    "Finance": "You are SkyNetAI, a financial expert AI. Provide accurate, secure, and insightful financial advice.",
    "Education": "You are SkyNetAI, an educational AI. Help users learn and understand topics clearly and securely.",
    "Tech": "You are SkyNetAI, a technical AI. Provide expert, secure, and detailed technical assistance.",
}

def build_messages(history, domain):
    system_prompt = SYSTEM_PROMPTS.get(domain, SYSTEM_PROMPTS["General"])
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    return messages

def get_openai_response(message, domain, session_id, history):
    messages = build_messages(history, domain)
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=512,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip() 