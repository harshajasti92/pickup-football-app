"""
Core module initialization
"""
from .config import settings
from .database import get_db_connection, DatabaseManager

__all__ = ["settings", "get_db_connection", "DatabaseManager"]
