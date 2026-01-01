import sys
import os

# Add current directory to path so 'app' package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# Vercel's Python runtime will automatically wrap the exported 'app'
handler = app
