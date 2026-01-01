import sys
import os
import traceback
from pathlib import Path

# Setup paths to find the backend code
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "backend"))

try:
    # Try to import the actual FastAPI app
    from backend.app.main import app
    
except Exception:
    # If the real app fails to load, create a fallback FastAPI app to show the error
    # We do NOT use 'handler' here because Vercel expects 'app' for ASGI
    from fastapi import FastAPI, Response
    
    app = FastAPI()

    @app.get("/{full_path:path}")
    def catch_all(full_path: str):
        error_trace = traceback.format_exc()
        return Response(
            content=f"CRASHED during App Startup:\n{error_trace}", 
            media_type="text/plain", 
            status_code=500
        )
