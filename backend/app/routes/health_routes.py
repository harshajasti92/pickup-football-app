"""
Health check and utility endpoints
"""
from fastapi import APIRouter
from ..core import get_db_connection

router = APIRouter(tags=["health"])

@router.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Pickup Football API is running!", "version": "1.0.0"}

@router.get("/api/health/db")
async def check_database():
    """Check database connection health"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        user_count = result['count']
        cursor.close()
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_users": user_count
        }
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Database health check failed: {str(e)}")

@router.get("/api/users/{user_id}/games")
async def get_user_games(user_id: int, status: str = None):
    """Get games for a specific user"""
    from ..services import GameService
    return GameService.get_user_games(user_id, status)
