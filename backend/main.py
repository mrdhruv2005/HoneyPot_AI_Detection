import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scam_intel_api")

from core.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to Redis/Mongo
    logger.info("Initializing Scam Intelligence Agent API...")
    db.connect()
    yield
    # Shutdown: Close connections
    logger.info("Shutting down API...")
    db.close()

app = FastAPI(
    title="Autonomous Scam Intelligence Agent",
    description="AI-powered Honeypot API for Scam Detection & Intelligence Extraction",
    version="2.0.0",
    lifespan=lifespan
)

from api.v1.router import router as v1_router
from routes.auth import router as auth_router

app.include_router(v1_router)
# Auth router removed
# app.include_router(auth_router, prefix="/api/v1")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Replace with Frontend URL in Production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request Failed: {e}")
        raise

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Scam Intelligence Agent",
        "version": "2.0.4",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    # TODO: Add Redis/Mongo Health Check
    return {"status": "healthy", "database": "connected", "redis": "connected"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
