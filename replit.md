# SkyNetAI - Cyberpunk AI Chatbot

## Overview

SkyNetAI is a cyberpunk-themed AI chatbot application that provides multiple AI personalities with distinct characteristics and visual themes. The application consists of a FastAPI backend that interfaces with OpenAI's GPT models and a Streamlit frontend with custom cyberpunk styling.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a client-server architecture with clear separation of concerns:

- **Backend**: FastAPI-based REST API server handling AI interactions and session management
- **Frontend**: Streamlit-based web interface with custom cyberpunk theming
- **AI Integration**: OpenAI GPT-4o model integration for chat functionality
- **Session Management**: In-memory session storage for conversation continuity

## Key Components

### Backend (backend.py)
- **FastAPI Application**: Main API server with CORS middleware for cross-origin requests
- **AI Personalities**: Pre-defined character personalities (hacker, corpo, netrunner, street_samurai, ai_construct) with unique system prompts and colors
- **Session Management**: In-memory dictionary storing conversation history per session
- **OpenAI Integration**: GPT-4o model integration for generating responses

### Frontend (frontend.py)
- **Streamlit Interface**: Web-based chat interface with cyberpunk styling
- **Session State Management**: Handles user sessions, messages, and personality selection
- **API Communication**: HTTP requests to backend for chat functionality and personality data

### Styling (static/cyberpunk.css)
- **Cyberpunk Theme**: Custom CSS with neon colors, futuristic fonts, and dark backgrounds
- **Responsive Design**: Styled components for chat interface, headers, and interactive elements
- **Typography**: Orbitron and Rajdhani fonts for authentic cyberpunk aesthetic

### Runner Scripts
- **main.py**: Orchestrates both backend and frontend server startup
- **run_backend.py**: Dedicated backend server runner with uvicorn
- **run_frontend.py**: Dedicated frontend server runner with Streamlit

## Data Flow

1. **User Interaction**: User selects personality and sends message through Streamlit frontend
2. **API Request**: Frontend makes HTTP request to FastAPI backend with message and personality
3. **AI Processing**: Backend sends message to OpenAI API with personality-specific system prompt
4. **Response Generation**: OpenAI returns AI-generated response in character
5. **Session Storage**: Backend stores conversation in in-memory session storage
6. **Frontend Update**: Response is displayed in chat interface with personality styling

## External Dependencies

### Core Dependencies
- **FastAPI**: Web framework for building the REST API
- **Streamlit**: Frontend framework for the web interface
- **OpenAI**: AI model integration for chat functionality
- **Uvicorn**: ASGI server for running FastAPI application
- **Pydantic**: Data validation and serialization
- **Requests**: HTTP client for frontend-backend communication

### Environment Variables
- **OPENAI_API_KEY**: Required for OpenAI API authentication

## Deployment Strategy

### Development Environment
- Backend runs on port 8000 with auto-reload enabled
- Frontend runs on port 5000 with Streamlit server
- Both servers can be started independently or together via main.py

### Server Configuration
- **Backend**: Uses uvicorn with hot reload for development
- **Frontend**: Streamlit server with custom port configuration
- **CORS**: Configured to allow all origins for development flexibility

### File Structure
```
/
├── backend.py          # FastAPI backend server
├── frontend.py         # Streamlit frontend application
├── main.py            # Combined server runner
├── run_backend.py     # Backend-only runner
├── run_frontend.py    # Frontend-only runner
└── static/
    └── cyberpunk.css  # Custom styling
```

### Architecture Benefits
- **Modularity**: Clear separation between backend API and frontend UI
- **Scalability**: FastAPI backend can handle multiple concurrent sessions
- **Flexibility**: Multiple AI personalities provide varied user experiences
- **Maintainability**: Separate runner scripts allow independent development and deployment

### Recent Enhancements (July 10, 2025)
- **Persistent Chat Sessions**: Added PostgreSQL database integration for permanent conversation storage
- **Multi-Chat Management**: Users can create, switch between, and delete multiple chat sessions
- **Enhanced Sidebar**: Added chat history sidebar with session management controls
- **Database Schema**: Implemented `chats` and `messages` tables with proper relationships
- **Session Persistence**: Conversations are now saved permanently across application restarts

### Current Limitations
- No user authentication or persistent user accounts
- Limited to OpenAI GPT models only
- No file upload capabilities
- No advanced visual effects or animations