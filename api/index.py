import sys
import traceback
from http.server import BaseHTTPRequestHandler
import json

# Try to load the fancy framework
try:
    from fastapi import FastAPI
    from mangum import Mangum
    
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"status": "FastAPI is WORKING!", "version": "Minimal"}

    @app.get("/{full_path:path}")
    def catch_all(full_path: str):
        return {"status": "FastAPI Caught path", "path": full_path}

    # If this line fails, we go to except
    handler = Mangum(app, lifespan="off")

except Exception:
    # If ANYTHING fails (ImportError, Mangum error, etc), catch it
    error_trace = traceback.format_exc()

    class handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "CRASHED during import/init",
                "error": error_trace
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
