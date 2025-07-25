"""
Database connection and management utilities
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from .config import settings

def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        print(f"Attempting to connect with config: {settings.DATABASE_CONFIG}")
        conn = psycopg2.connect(**settings.DATABASE_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection failed: {str(e)}"
        )

class DatabaseManager:
    """Context manager for database operations"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        return self.cursor, self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
