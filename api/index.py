import sys
import os
import traceback
from pathlib import Path
from http.server import BaseHTTPRequestHandler
import json

# Setup paths to find the backend code
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "backend"))

try:
    # Try to import the actual FastAPI app
    from mangum import Mangum
    from backend.app.main import app as fast_api_app
    
    # Wrap it for Vercel
    handler = Mangum(fast_api_app)

except Exception:
    # If the app fails to start (e.g. error in main.py or dependencies), catch it!
    error_trace = traceback.format_exc()

    class handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "CRASHED during App Startup",
                "error": error_trace
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
