#!/usr/bin/env python3
"""
SkyNetAI Backend Runner
Starts the FastAPI backend server on port 8000
"""

import uvicorn
import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run the FastAPI backend server"""
    print("🚀 Starting SkyNetAI Backend Server...")
    print("📡 Backend will be available at: http://localhost:8000")
    print("🤖 API Documentation: http://localhost:8000/docs")
    print("⚡ Make sure your OPENAI_API_KEY environment variable is set!")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING: OPENAI_API_KEY environment variable not found!")
        print("   Please set it with: export OPENAI_API_KEY=your_api_key_here")
    
    try:
        uvicorn.run(
            "backend:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 SkyNetAI Backend Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
