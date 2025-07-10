# SkyNetAI – Secure Conversational Intelligence

A cyberpunk-themed, session-based AI chatbot with FastAPI backend, Streamlit frontend, and OpenAI GPT integration. Inspired by the Terminator universe.

## Architecture
- **Backend:** FastAPI (REST API, session memory, OpenAI calls)
- **Frontend:** Streamlit (custom cyberpunk UI)
- **OpenAI:** GPT-3.5/4 via OpenAI API
- **Session Memory:** In-memory per session (memory.py)
- **Domain Context:** System prompt changes by domain (General, Finance, Education, Tech)

## Features
- Session-based chat memory (per session_id)
- Domain dropdown: General, Finance, Education, Tech
- System prompt changes per domain
- Reset button to clear chat
- Full chat history sent to OpenAI each time
- Cyberpunk UI: black/red, glowing, custom fonts, animated loading
- One `/chat` POST endpoint

## File Structure
- `main.py` – FastAPI backend
- `frontend.py` – Streamlit UI
- `chat_handler.py` – OpenAI logic
- `memory.py` – Session memory store
- `.env` – OpenAI API key
- `requirements.txt` – All dependencies

## Setup
1. **Clone the repo**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API key:**
   - Edit `.env` and add your key: `OPENAI_API_KEY=sk-...`
4. **Run the backend:**
   ```bash
   uvicorn main:app --reload
   ```
5. **Run the frontend:**
   ```bash
   streamlit run frontend.py
   ```
6. **Open Streamlit in your browser** (usually http://localhost:8501)

## Usage
- Select a domain from the dropdown
- Type your message and send
- See glowing chat bubbles and AI responses
- Click "Reset Chat" to clear session

## Customization
- **Prompts:** Edit `chat_handler.py` SYSTEM_PROMPTS
- **UI:** Tweak CSS/HTML in `frontend.py`
- **Model:** Change model in `chat_handler.py` (e.g., `gpt-4`)

## Security & Notes
- Memory is in-memory only (not persistent)
- For production, add authentication and persistent storage

---

**SkyNetAI** – The future is now. Welcome to the machine. 