from http.server import BaseHTTPRequestHandler
import json
import traceback

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        status = "Raw Python working!"
        details = "Dependencies not tested."
        
        try:
            import fastapi
            import mangum
            import uvicorn
            import pandas as pd
            import numpy as np
            details = f"Imports Successful! FastAPI: {fastapi.__version__}, Pandas: {pd.__version__}"
        except Exception:
            status = "Import Failed"
            details = traceback.format_exc()

        response = {
            "status": status,
            "details": details
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
