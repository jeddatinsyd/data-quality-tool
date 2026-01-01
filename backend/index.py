import sys
import os
import traceback

try:
    # Add current directory to path so 'app' package is found
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    from app.main import app
    handler = app

except Exception as e:
    # Debugging: If startup fails, return the traceback as a response
    from fastapi import FastAPI, Response
    debug_app = FastAPI()
    
    @debug_app.get("/{path:path}")
    async def catch_all(path: str):
        error_trace = traceback.format_exc()
        return Response(
            content=f"Backend Startup Error:\n{error_trace}", 
            media_type="text/plain", 
            status_code=500
        )
    
    handler = debug_app
