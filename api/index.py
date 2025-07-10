"""
Vercel API entry point for SkyNetAI backend
This file is required for Vercel deployment
"""

from backend import app

# Vercel expects the app to be named 'app' and be the default export
# The backend.py file contains the actual FastAPI application