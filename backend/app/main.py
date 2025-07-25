"""
Pickup Football API - Modular FastAPI Application

This is the main application file that brings together all the modular components:
- Core configuration and database management
- Pydantic models for data validation
- Service layer for business logic
- Route handlers for API endpoints
- Utility functions for common operations

The modular structure improves maintainability, testability, and scalability.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import core configuration
from .core import settings

# Import route modules
from .routes import user_router, game_router, health_router

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    # Initialize FastAPI app with configuration
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="A modern API for organizing pickup football games with smart team balancing"
    )
    
    # Add CORS middleware to allow React frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include route modules
    app.include_router(health_router)  # Health and utility endpoints
    app.include_router(user_router)    # User management endpoints
    app.include_router(game_router)    # Game management endpoints
    
    return app

# Create the application instance
app = create_app()

# Run the application (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
