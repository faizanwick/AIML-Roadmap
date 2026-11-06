from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Patient Management System",
    description="FastAPI app for managing patient records",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def home():
    return {"message" : "Patient Management System API is Running"}

@app.get("/health", tags=["health"])
def health_check():
    return {"status" : "healthy"}

app.include_router(api_router, prefix="/api/v1")