#!/usr/bin/env python3
"""
SkyNetAI Frontend Runner
Starts the Streamlit frontend server on port 5000
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit frontend server"""
    print("🎨 Starting SkyNetAI Frontend Server...")
    print("🌐 Frontend will be available at: http://localhost:5000")
    print("🤖 Make sure the backend is running on port 8000!")
    
    # Check if static directory exists
    if not os.path.exists("static"):
        print("❌ Static directory not found! Creating it...")
        os.makedirs("static")
    
    # Check if CSS file exists
    if not os.path.exists("static/cyberpunk.css"):
        print("❌ CSS file not found! Make sure static/cyberpunk.css exists.")
        sys.exit(1)
    
    try:
        # Run Streamlit on port 5000
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "frontend.py", 
            "--server.port=5000",
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 SkyNetAI Frontend Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
