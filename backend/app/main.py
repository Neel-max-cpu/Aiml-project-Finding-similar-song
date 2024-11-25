from fastapi import FastAPI
from app.api import endpoints
from app.api.endpoints import router

app = FastAPI()

# Include API routes
# app.include_router(endpoints.router)
app.include_router(router, prefix="/api")
