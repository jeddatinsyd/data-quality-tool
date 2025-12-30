from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import validation

app = FastAPI(title="Data Quality & Validation Tool")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(validation.router, prefix="/api", tags=["Validation"])

@app.get("/")
async def root():
    return {"message": "Data Quality Tool API is running"}
