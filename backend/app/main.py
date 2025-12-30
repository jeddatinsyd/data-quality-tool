from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import validation

app = FastAPI(title="Data Quality & Validation Tool")

# CORS configuration - must be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(validation.router, prefix="/api", tags=["Validation"])

@app.get("/")
async def root():
    return {"message": "Data Quality Tool API is running"}

# Explicit OPTIONS handler for debugging
@app.options("/api/{path:path}")
async def options_handler(path: str):
    return {}
