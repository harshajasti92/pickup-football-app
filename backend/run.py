#!/usr/bin/env python3
"""
Startup script for Pickup Football API
"""
import uvicorn
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
