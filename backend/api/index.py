"""
Vercel serverless function wrapper for FastAPI
This file serves as the entry point for Vercel's serverless functions
"""
import sys
import os
from pathlib import Path

# # Add the backend directory to the Python path
# #backend_dir = Path(__file__).parent.parent
# #sys.path.insert(0, str(backend_dir))
# Add the backend directory to the Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.main import app

# Vercel's Python runtime will automatically wrap the exported 'app'
# Use handler as an alias just in case
handler = app

