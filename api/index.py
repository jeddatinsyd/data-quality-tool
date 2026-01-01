from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Minimal Backend is working!", "path": "root"}

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return {"status": "Minimal Backend is working!", "path": full_path}

# Vercel entry point
handler = app
