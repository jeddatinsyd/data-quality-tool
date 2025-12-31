from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import validation

app = FastAPI(title="Data Quality & Validation Tool")

# CORS configuration - must be before routes
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "https://dqtool.vercel.app",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(validation.router, prefix="/api", tags=["Validation"])

@app.get("/")
async def root():
    return {"message": "Data Quality Tool API is running"}
