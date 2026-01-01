from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Backend is reachable!", "message": "Configuration is correct."}

@app.get("/api/{path:path}")
def catch_api(path: str):
    return {"status": "API route reachable", "path": path}

# Vercel entry point
handler = app
