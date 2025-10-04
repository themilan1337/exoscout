"""
ExoScout Backend - NASA Space Apps Challenge
A World Away – Hunting for Exoplanets with AI

FastAPI backend for exoplanet detection and analysis using NASA data sources.
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import resolve, features, lightcurve, predict

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataNotFoundError(Exception):
    """Raised when requested data is not found in NASA archives."""
    pass


class ExternalAPIError(Exception):
    """Raised when external API calls fail."""
    pass


class ModelError(Exception):
    """Raised when ML model operations fail."""
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting ExoScout Backend...")
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    yield
    
    logger.info("Shutting down ExoScout Backend...")


# Initialize FastAPI app
app = FastAPI(
    title="ExoScout Backend",
    description="NASA Space Apps Challenge - Exoplanet Detection with AI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(DataNotFoundError)
async def data_not_found_handler(request: Request, exc: DataNotFoundError):
    """Handle data not found errors."""
    logger.error(f"Data not found: {exc}")
    return JSONResponse(
        status_code=404,
        content={"error": "Data not found", "detail": str(exc)}
    )


@app.exception_handler(ExternalAPIError)
async def external_api_error_handler(request: Request, exc: ExternalAPIError):
    """Handle external API errors."""
    logger.error(f"External API error: {exc}")
    return JSONResponse(
        status_code=502,
        content={"error": "External API error", "detail": str(exc)}
    )


@app.exception_handler(ModelError)
async def model_error_handler(request: Request, exc: ModelError):
    """Handle ML model errors."""
    logger.error(f"Model error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Model error", "detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    )


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict[str, str]: Health status
    """
    return {"status": "ok"}


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint.
    
    Returns:
        Dict[str, str]: Welcome message
    """
    return {"message": "ExoScout Backend is running 🚀"}


# Include routers
app.include_router(resolve.router, prefix="/api/v1", tags=["resolve"])
app.include_router(features.router, prefix="/api/v1", tags=["features"])
app.include_router(lightcurve.router, prefix="/api/v1", tags=["lightcurve"])
app.include_router(predict.router, prefix="/api/v1", tags=["predict"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )