"""
Routes module initialization
"""
from .user_routes import router as user_router
from .game_routes import router as game_router
from .health_routes import router as health_router

__all__ = ["user_router", "game_router", "health_router"]
