from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Backend is reachable!", "message": "Configuration is correct."}

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return {"status": "Backend reachable", "path": full_path, "note": "Caught by wildcard"}

# Vercel entry point
handler = app
