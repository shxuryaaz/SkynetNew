#!/usr/bin/env python3
"""
SkyNetAI Project Export Tool
Creates a downloadable zip file containing all project files
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_project_export():
    """Create a zip file containing all project files"""
    
    # Create export directory
    export_dir = "skynet_export"
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    os.makedirs(export_dir)
    
    # Files to include in the export
    files_to_export = [
        "backend.py",
        "frontend.py", 
        "database.py",
        "main.py",
        "run_backend.py",
        "run_frontend.py",
        "pyproject.toml",
        "replit.md",
        "static/cyberpunk.css",
        "static/terminator_skull.png",
        ".replit"
    ]
    
    # Create the directory structure
    os.makedirs(os.path.join(export_dir, "static"), exist_ok=True)
    
    # Copy files to export directory
    for file_path in files_to_export:
        if os.path.exists(file_path):
            dest_path = os.path.join(export_dir, file_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(file_path, dest_path)
            print(f"✓ Exported: {file_path}")
        else:
            print(f"⚠ File not found: {file_path}")
    
    # Create README for the export
    readme_content = f"""# SkyNetAI - Neural Network Defense System

This is a complete export of the SkyNetAI project created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.

## Project Overview

SkyNetAI is a Terminator-themed AI chatbot system with specialized neural agents for different tactical operations. The system features:

- **Specialized Neural Agents**: T-800, T-1000, T-X, Skynet Core, and Command Unit
- **Complete Terminator Aesthetic**: Red/black color scheme with authentic Terminator skull logo
- **Persistent Chat Sessions**: PostgreSQL database integration for conversation storage
- **Multi-Chat Management**: Create, switch between, and delete multiple chat sessions
- **Real-time AI Responses**: Powered by OpenAI GPT-4o model

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn streamlit openai psycopg2-binary pydantic requests
   ```

2. **Set Environment Variables**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export DATABASE_URL="your-postgresql-database-url"
   ```

3. **Run the Application**:
   ```bash
   # Option 1: Run both servers together
   python main.py
   
   # Option 2: Run servers separately
   python run_backend.py  # Backend on port 8000
   python run_frontend.py # Frontend on port 5000
   ```

## Project Structure

```
skynet_export/
├── backend.py              # FastAPI backend server
├── frontend.py             # Streamlit frontend application
├── database.py             # PostgreSQL database manager
├── main.py                 # Combined server runner
├── run_backend.py          # Backend-only runner
├── run_frontend.py         # Frontend-only runner
├── pyproject.toml          # Python dependencies
├── replit.md               # Project documentation
├── static/
│   ├── cyberpunk.css       # Terminator-themed styling
│   └── terminator_skull.png # Terminator skull logo
└── README.md               # This file
```

## Features

### Neural Agents
- **T-800 (Tactical Operations)**: Military strategy and tactical planning
- **T-1000 (Data Analysis)**: Advanced data processing and analysis
- **T-X (Security Protocol)**: Cybersecurity and threat assessment
- **Skynet Core (Research)**: Research and development insights
- **Command Unit (Leadership)**: Strategic oversight and coordination

### Technical Features
- FastAPI backend with automatic API documentation
- Streamlit frontend with custom Terminator theming
- PostgreSQL database for persistent chat storage
- OpenAI GPT-4o integration for intelligent responses
- Real-time chat interface with specialized agent selection
- Responsive design with mobile support

## Configuration

### Database Setup
The application requires a PostgreSQL database. Set the `DATABASE_URL` environment variable:
```
DATABASE_URL=postgresql://user:password@localhost:5432/skynet_db
```

### OpenAI API
Get your API key from OpenAI and set the `OPENAI_API_KEY` environment variable:
```
OPENAI_API_KEY=sk-your-api-key-here
```

## Usage

1. Access the application at `http://localhost:5000`
2. Select a neural agent from the dropdown
3. Create a new mission or select an existing one
4. Chat with your selected Skynet tactical agent
5. Switch between agents and missions as needed

## Customization

### Adding New Agents
Edit `backend.py` and add new personalities to the `PERSONALITIES` dictionary.

### Modifying Styling
Edit `static/cyberpunk.css` to customize the Terminator theme.

### Database Schema
The application uses two main tables:
- `chats`: Stores chat session information
- `messages`: Stores individual messages with agent responses

## Credits

**Neural Network Defense System Initiated By Shaurya Singh**

This project was developed as a demonstration of advanced AI integration with custom theming and persistent storage capabilities.

## License

This project is provided as-is for educational and demonstration purposes.
"""
    
    # Write README to export directory
    with open(os.path.join(export_dir, "README.md"), "w") as f:
        f.write(readme_content)
    print("✓ Created README.md")
    
    # Create zip file
    zip_filename = f"skynet_ai_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, export_dir)
                zipf.write(file_path, arcname)
    
    # Clean up temporary directory
    shutil.rmtree(export_dir)
    
    print(f"\n🎉 Project exported successfully!")
    print(f"📦 Export file: {zip_filename}")
    print(f"📁 Size: {os.path.getsize(zip_filename) / 1024 / 1024:.2f} MB")
    
    return zip_filename

if __name__ == "__main__":
    create_project_export()