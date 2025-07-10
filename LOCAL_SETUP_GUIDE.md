# SkyNetAI - Complete Local Setup Guide

## Overview

SkyNetAI is a Terminator-themed neural network defense system featuring specialized AI tactical agents. This guide will walk you through setting up the complete project locally from scratch, including database configuration, dependencies, and deployment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Step-by-Step Installation](#step-by-step-installation)
4. [Database Setup](#database-setup)
5. [Environment Configuration](#environment-configuration)
6. [Running the Application](#running-the-application)
7. [Vercel Deployment](#vercel-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Project Structure](#project-structure)
10. [Customization](#customization)

---

## Prerequisites

Before starting, ensure you have the following installed on your system:

### Required Software
- **Python 3.8+** (Python 3.10 or 3.11 recommended)
- **PostgreSQL 12+** (for database)
- **Git** (for version control)
- **pip** (Python package manager)

### Optional but Recommended
- **Python Virtual Environment** (venv or conda)
- **pgAdmin** (PostgreSQL management tool)
- **VS Code** or your preferred code editor

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space
- **Network**: Internet connection for API calls

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **RAM**: 8GB or more
- **Storage**: 5GB free space
- **CPU**: Multi-core processor for better performance

---

## Step-by-Step Installation

### 1. Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and **check "Add Python to PATH"**
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### macOS
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
# Verify installation
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

### 2. Install PostgreSQL

#### Windows
1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer and remember the password you set for the `postgres` user
3. Default port: 5432
4. Verify installation:
   ```cmd
   psql --version
   ```

#### macOS
```bash
# Using Homebrew
brew install postgresql
brew services start postgresql

# Verify installation
psql --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

### 3. Clone/Create Project Directory

```bash
# Create project directory
mkdir skynet-ai
cd skynet-ai

# If you have the project files, copy them here
# If downloading from a source, extract the files here
```

### 4. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv skynet-env

# Activate virtual environment
# Windows:
skynet-env\Scripts\activate

# macOS/Linux:
source skynet-env/bin/activate

# Your terminal should now show (skynet-env)
```

### 5. Install Python Dependencies

Create a `requirements.txt` file with the following content:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
streamlit==1.28.1
openai==1.3.0
psycopg2-binary==2.9.9
pydantic==2.5.0
requests==2.31.0
python-multipart==0.0.6
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install fastapi uvicorn streamlit openai psycopg2-binary pydantic requests python-multipart
```

---

## Database Setup

### 1. Create PostgreSQL Database

#### Method 1: Using psql Command Line
```bash
# Connect to PostgreSQL as postgres user
# Windows:
psql -U postgres

# macOS/Linux:
sudo -u postgres psql

# In psql, create database and user:
CREATE DATABASE skynet_db;
CREATE USER skynet_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE skynet_db TO skynet_user;
\q
```

#### Method 2: Using pgAdmin (GUI)
1. Open pgAdmin
2. Connect to your PostgreSQL server
3. Right-click "Databases" → "Create" → "Database"
4. Name: `skynet_db`
5. Owner: Create a new user `skynet_user` with password

### 2. Test Database Connection

```bash
# Test connection
psql -U skynet_user -d skynet_db -h localhost

# If successful, you should see:
# skynet_db=>
# Type \q to exit
```

### 3. Database Schema

The application will automatically create the required tables when you first run it. The schema includes:

- **chats**: Stores chat session information
- **messages**: Stores individual messages and AI responses

---

## Environment Configuration

### 1. Create Environment Variables

Create a `.env` file in your project root:

```env
# Database Configuration
DATABASE_URL=postgresql://skynet_user:your_secure_password@localhost:5432/skynet_db
PGHOST=localhost
PGPORT=5432
PGUSER=skynet_user
PGPASSWORD=your_secure_password
PGDATABASE=skynet_db

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
BACKEND_PORT=8000
FRONTEND_PORT=5000
```

### 2. Get OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create an account if you don't have one
3. Generate a new API key
4. Copy the key and add it to your `.env` file

**Important**: Keep your API key secure and never commit it to version control!

### 3. Load Environment Variables (Optional)

For automatic environment loading, install python-dotenv:
```bash
pip install python-dotenv
```

Then add to your Python files:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Running the Application

### Option 1: Run Both Servers Together

```bash
# Make sure you're in the project directory with virtual environment activated
python main.py
```

This will start:
- Backend API server on `http://localhost:8000`
- Frontend web interface on `http://localhost:5000`

### Option 2: Run Servers Separately

**Terminal 1 - Backend:**
```bash
# Activate virtual environment
source skynet-env/bin/activate  # Linux/macOS
# or
skynet-env\Scripts\activate     # Windows

# Run backend
python run_backend.py
```

**Terminal 2 - Frontend:**
```bash
# Activate virtual environment
source skynet-env/bin/activate  # Linux/macOS
# or
skynet-env\Scripts\activate     # Windows

# Run frontend
python run_frontend.py
```

### Option 3: Manual Server Start

**Backend:**
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
streamlit run frontend.py --server.port 5000
```

### 4. Access the Application

- **Frontend (Main Interface)**: http://localhost:5000
- **Backend API Documentation**: http://localhost:8000/docs
- **Backend API**: http://localhost:8000

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Error
```
Error: could not connect to server: Connection refused
```

**Solutions:**
- Ensure PostgreSQL service is running
- Check database credentials in `.env` file
- Verify database exists and user has permissions
- Try connecting manually with psql

#### 2. OpenAI API Error
```
Error: Incorrect API key provided
```

**Solutions:**
- Verify your OpenAI API key is correct
- Check you have credits in your OpenAI account
- Ensure the key is properly set in environment variables

#### 3. Port Already in Use
```
Error: [Errno 48] Address already in use
```

**Solutions:**
- Kill processes using the ports:
  ```bash
  # Find process using port
  lsof -i :8000  # or :5000
  
  # Kill process
  kill -9 <PID>
  ```
- Use different ports by modifying the run scripts

#### 4. Module Not Found Error
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**
- Ensure virtual environment is activated
- Install missing dependencies:
  ```bash
  pip install -r requirements.txt
  ```

#### 5. Permission Denied (Linux/macOS)
```
Permission denied when accessing files
```

**Solutions:**
- Check file permissions:
  ```bash
  chmod +x run_backend.py run_frontend.py main.py
  ```

### Database Troubleshooting

#### Reset Database
If you need to reset the database:
```sql
-- Connect to PostgreSQL
psql -U postgres

-- Drop and recreate database
DROP DATABASE skynet_db;
CREATE DATABASE skynet_db;
GRANT ALL PRIVILEGES ON DATABASE skynet_db TO skynet_user;
```

#### Check Database Status
```bash
# Check if PostgreSQL is running
# Windows:
sc query postgresql-x64-14

# macOS:
brew services list | grep postgresql

# Linux:
sudo systemctl status postgresql
```

---

## Project Structure

```
skynet-ai/
├── backend.py              # FastAPI backend server
├── frontend.py             # Streamlit frontend application
├── database.py             # PostgreSQL database manager
├── main.py                 # Combined server runner
├── run_backend.py          # Backend-only runner
├── run_frontend.py         # Frontend-only runner
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── LOCAL_SETUP_GUIDE.md    # This guide
├── replit.md               # Project documentation
└── static/
    ├── cyberpunk.css       # Terminator-themed styling
    └── terminator_skull.png # Terminator skull logo
```

### Key Files Description

- **backend.py**: FastAPI server handling AI interactions and API endpoints
- **frontend.py**: Streamlit web interface with Terminator theming
- **database.py**: PostgreSQL database operations and schema management
- **main.py**: Convenience script to run both servers together
- **static/**: Contains CSS styling and images

---

## Customization

### Adding New AI Agents

1. Edit `backend.py`
2. Add new personality to the `PERSONALITIES` dictionary:

```python
PERSONALITIES = {
    "new_agent": {
        "name": "New Agent (Specialization)",
        "prompt": "You are a specialized AI agent...",
        "color": "#FF5733"
    }
}
```

### Modifying the Theme

1. Edit `static/cyberpunk.css`
2. Change CSS variables for colors:

```css
:root {
    --primary-red: #your-color;
    --bg-primary: #your-bg-color;
}
```

### Database Schema Changes

1. Edit `database.py`
2. Add new table creation in `init_database()` method
3. Add corresponding methods for new operations

### Environment Variables

Add new environment variables in `.env`:
```env
CUSTOM_SETTING=your_value
```

Access in Python:
```python
import os
custom_value = os.environ.get("CUSTOM_SETTING")
```

---

## Security Considerations

1. **Never commit `.env` file** to version control
2. **Use strong passwords** for database
3. **Keep OpenAI API key secure**
4. **Run on localhost only** for development
5. **Use HTTPS** in production

---

## Performance Tips

1. **Use SSD storage** for better database performance
2. **Allocate sufficient RAM** for Python processes
3. **Monitor API usage** to avoid OpenAI rate limits
4. **Use database indexing** for better query performance
5. **Enable caching** for repeated requests

---

## Vercel Deployment

### Overview

Vercel is a popular platform for deploying web applications. This section covers deploying both the FastAPI backend and Streamlit frontend to Vercel.

### Prerequisites for Vercel Deployment

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **Vercel CLI** (optional): `npm install -g vercel`
4. **PostgreSQL Database**: Use a cloud database service (see Database Options below)

### Database Options for Production

Since Vercel doesn't provide database hosting, you'll need a cloud database:

#### Option 1: Supabase (Recommended)
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your database URL from Settings → Database
4. Format: `postgresql://[user]:[password]@[host]:[port]/[database]`

#### Option 2: Railway
1. Go to [railway.app](https://railway.app)
2. Create a new PostgreSQL service
3. Get connection details from the Variables tab

#### Option 3: Neon
1. Go to [neon.tech](https://neon.tech)
2. Create a new database
3. Get connection string from the dashboard

### Backend Deployment (FastAPI)

#### Step 1: Prepare Backend for Vercel

Create `vercel.json` in your project root:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}
```

#### Step 2: Create API Directory Structure

Vercel requires specific structure for Python APIs:

```
project-root/
├── api/
│   └── index.py      # Your FastAPI app
├── backend.py        # Keep original
├── vercel.json       # Vercel configuration
└── requirements.txt  # Dependencies
```

Create `api/index.py`:
```python
from backend import app

# Vercel expects the app to be named 'app' and be the default export
```

#### Step 3: Update requirements.txt

Create `requirements.txt` with exact versions:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
openai==1.3.0
psycopg2-binary==2.9.9
pydantic==2.5.0
requests==2.31.0
python-multipart==0.0.6
python-dotenv==1.0.0
```

#### Step 4: Deploy Backend to Vercel

**Method 1: Using Vercel Dashboard**
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Select the repository containing your backend
5. Configure environment variables:
   - `DATABASE_URL`: Your cloud database URL
   - `OPENAI_API_KEY`: Your OpenAI API key
6. Deploy

**Method 2: Using Vercel CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
vercel

# Follow prompts and add environment variables
vercel env add DATABASE_URL
vercel env add OPENAI_API_KEY

# Deploy
vercel --prod
```

#### Step 5: Configure Environment Variables

In Vercel dashboard:
1. Go to your project
2. Click "Settings" → "Environment Variables"
3. Add:
   - `DATABASE_URL`: `postgresql://user:pass@host:port/db`
   - `OPENAI_API_KEY`: `sk-your-api-key`
   - `PGHOST`: Database host
   - `PGPORT`: Database port (usually 5432)
   - `PGUSER`: Database username
   - `PGPASSWORD`: Database password
   - `PGDATABASE`: Database name

### Frontend Deployment (Streamlit)

#### Important Note
Streamlit applications require a different approach on Vercel since they're not typical web apps.

#### Option 1: Convert to FastAPI + HTML/JS Frontend

**Create a new FastAPI frontend:**

`frontend_api.py`:
```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SkyNet AI</title>
        <link rel="stylesheet" href="/static/cyberpunk.css">
    </head>
    <body>
        <div class="header">
            <div class="header-content-centered">
                <div class="logo">
                    <img src="/static/terminator_skull.png" alt="Skynet Logo">
                </div>
                <div class="title-section-centered">
                    <h1 class="professional-title">SKYNET</h1>
                    <p class="subtitle">Neural Network Defense System</p>
                    <div class="company-badge-centered">System Online</div>
                </div>
            </div>
        </div>
        <!-- Add your chat interface here -->
    </body>
    </html>
    """

@app.get("/chat")
async def chat_interface():
    # Your chat logic here
    pass
```

#### Option 2: Deploy Streamlit on Streamlit Cloud

**Streamlit Cloud (Recommended for Streamlit apps):**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file path: `frontend.py`
5. Add secrets in the Streamlit Cloud dashboard:
   ```toml
   # .streamlit/secrets.toml (for Streamlit Cloud)
   [database]
   DATABASE_URL = "postgresql://user:pass@host:port/db"
   
   [openai]
   OPENAI_API_KEY = "sk-your-api-key"
   ```

#### Option 3: Use Vercel with Custom Build

Create `package.json`:
```json
{
  "name": "skynet-frontend",
  "version": "1.0.0",
  "scripts": {
    "build": "python -m streamlit run frontend.py --server.port $PORT",
    "start": "python -m streamlit run frontend.py --server.port 8501"
  },
  "dependencies": {}
}
```

Update `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "."
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend.py"
    }
  ]
}
```

### Complete Deployment Workflow

#### Step 1: Prepare Your Repository

```bash
# Create deployment branch
git checkout -b deployment

# Create necessary files
touch vercel.json
touch requirements.txt
mkdir -p api
```

#### Step 2: Update Code for Production

**Update backend.py for CORS:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Update frontend.py for production API:**
```python
# Replace localhost with your Vercel backend URL
BACKEND_URL = os.environ.get("BACKEND_URL", "https://your-backend.vercel.app")
```

#### Step 3: Deploy Both Services

**Backend:**
```bash
# Create separate repo for backend
git subtree push --prefix=backend origin backend-deploy

# Deploy to Vercel
vercel --prod
```

**Frontend:**
```bash
# Deploy to Streamlit Cloud or create HTML/JS version for Vercel
```

### Environment Variables for Production

Create `.env.production`:
```env
# Database (use cloud database)
DATABASE_URL=postgresql://user:pass@host:port/db

# OpenAI
OPENAI_API_KEY=sk-your-production-key

# Backend URL (for frontend)
BACKEND_URL=https://your-backend.vercel.app

# Security
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-streamlit.app
```

### Custom Domain Setup

#### For Vercel:
1. Go to project settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

#### For Streamlit Cloud:
1. Go to app settings
2. Add custom domain
3. Configure DNS with CNAME record

### Monitoring and Logs

#### Vercel:
- View logs in Vercel dashboard
- Monitor usage and performance
- Set up alerts for errors

#### Streamlit Cloud:
- View logs in Streamlit Cloud dashboard
- Monitor app health
- Check resource usage

### Production Considerations

1. **Security:**
   - Use environment variables for all secrets
   - Enable HTTPS (automatic on Vercel)
   - Configure proper CORS settings

2. **Performance:**
   - Use connection pooling for database
   - Implement caching for API responses
   - Optimize images and static assets

3. **Monitoring:**
   - Set up error tracking (Sentry)
   - Monitor API usage and costs
   - Track user analytics

4. **Scaling:**
   - Configure auto-scaling settings
   - Monitor resource usage
   - Set up load balancing if needed

### Troubleshooting Vercel Deployment

#### Common Issues:

**Build Fails:**
```bash
# Check build logs in Vercel dashboard
# Ensure requirements.txt has correct versions
# Verify Python version compatibility
```

**API Errors:**
```bash
# Check environment variables are set
# Verify database connection
# Check API endpoint URLs
```

**CORS Issues:**
```python
# Add proper CORS configuration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Support and Updates

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Check environment variables are set correctly
4. Ensure database is running and accessible

---

## License

This project is provided for educational and demonstration purposes. Please ensure you comply with OpenAI's terms of service when using their API.

---

**Neural Network Defense System Initiated By Shaurya Singh**