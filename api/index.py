from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "FastAPI + Mangum is working!", "note": "No Pandas loaded yet."}

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return {"status": "FastAPI + Mangum reachable", "path": full_path}

# Wrap with Mangum
handler = Mangum(app)
